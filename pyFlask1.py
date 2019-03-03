from flask import Flask, render_template, request
import plotly as py
import pandas as pd

import plotly.plotly as py
import plotly.tools as plotly_tools
from plotly.graph_objs import *

import os
py.sign_in("ACodeMZ", "FC5PBOKLqkR0GSFE94e9")
app = Flask(__name__)

#  Read the csv into a pandas DataFrame
data = pd.read_csv('FluNetInteractiveReport.csv')

#  Provide users with the raw data from their selected time frames
#       Option 1: Start date to end date
#           ex: Jan 1 2012 - Mar - 2013
#       Option 2: Start date to end date with annual frequency
#           ex: Jan 1 - Mar 1 for the past 5 years

# If user selects "Inclusive" - will deliver continuous filtered data from start week, start year, to end week of end year
def time_filter_inclusive(start_year, start_week, end_year, end_week):
    #find start row
    temp_df = data.loc[data['Year']==start_year]
    start_row = temp_df.loc[temp_df['Week']==start_week]
    #find end row
    temp_df = data.loc[data['Year']==end_year]
    end_row = temp_df.loc[temp_df['Week']==end_week+1]
        
    filtered_data = data.iloc[start_row.index[0]:end_row.index[0],:]
    filtered_data.drop('Country', axis=1, inplace=True)
    filtered_data.drop('WHOREGION', axis=1, inplace=True)
    filtered_data.drop('FLUREGION', axis=1, inplace=True)
    return filtered_data

# If user selects "Weekly" - will deliver filtered data from start week to end week over all over all the years
def time_filter_weekly(start_year, start_week, end_year, end_week):
    #create empty df to append each uyear's filtered data at ecah ioteration
    filtered_data = pd.DataFrame()
        
    for year in range(start_year, end_year+1):
        #find start row
        temp_df = data.loc[data['Year']==year]
        start_row = temp_df.loc[temp_df['Week']==start_week]
        #find end row
        temp_df = data.loc[data['Year']==year]
        end_row = temp_df.loc[temp_df['Week']==end_week]
        #append to df
        filtered_data = filtered_data.append(data.iloc[start_row.index[0]:end_row.index[0],:])

    filtered_data.drop('Country', axis=1, inplace=True)
    filtered_data.drop('WHOREGION', axis=1, inplace=True)
    filtered_data.drop('FLUREGION', axis=1, inplace=True)                                        
    return filtered_data        

@app.route("/send")                             #sets up default page
def my_form():
    return render_template('my-form.html')

@app.route("/send", methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        #retrieve input boundaries from user
        yearF = request.form['ctl_list_YearFrom']
        yearFi = int(yearF)
        weekF = request.form['ctl_list_WeekFrom']
        weekFi = int(weekF)
        yearT = request.form['ctl_list_YearTo']
        yearTi = int(yearT)
        weekT = request.form['ctl_list_WeekTo']
        weekTi = int(weekT)
        typeSelect = request.form['selectType']

        if typeSelect == "Start End":
            df = time_filter_inclusive(yearFi, weekFi, yearTi, weekTi)
            dfWS = df

            #Week Fixer
            if yearFi != yearTi:
                i = 0
                for index, row in df.iterrows():
                    if row['Year'] != yearFi:
                        count = row['Year'] - yearFi
                        dfWS.iat[i, 1] = row['Week'] + (count * 52)
                    i += 1
            
            #create graph
            A_H1 = Scatter(x = dfWS['Week'], y = dfWS['AH1'], mode = 'markers', name = 'A (H1)')
            A_H1N1 = Scatter(x = dfWS['Week'], y = dfWS['AH1N12009'], mode = 'markers', name = 'A (H1N1)')
            A_H3 = Scatter(x = dfWS['Week'], y = dfWS['AH3'], mode = 'markers', name = 'A (H3)')
            A_H5 = Scatter(x = dfWS['Week'], y = dfWS['AH5'], mode = 'markers', name = 'A (H5)')
            A_NoSub = Scatter(x = dfWS['Week'], y = dfWS['ANOTSUBTYPED'], mode = 'markers', name = 'A (No subtype)')
            A_Total = Scatter(x = dfWS['Week'], y = dfWS['INF_A'], mode = 'markers', name = 'A Total')
            B_Yamagata = Scatter(x = dfWS['Week'], y = dfWS['BYAMAGATA'], mode = 'markers', name = 'B (Yamagata)')
            B_Victoria = Scatter(x = dfWS['Week'], y = dfWS['BVICTORIA'], mode = 'markers', name = 'B (Victoria)')
            B_NoLineage = Scatter(x = dfWS['Week'], y = dfWS['BNOTDETERMINED'], mode = 'markers', name = 'B (No lineage)')
            B_Total = Scatter(x = dfWS['Week'], y = dfWS['INF_B'], mode = 'markers', name = 'B Total')
            data = [A_H1, A_H1N1, A_H3, A_H5, A_NoSub, A_Total, B_Yamagata, B_Victoria, B_NoLineage, B_Total]
            first_plot_url = py.plot(data, filename='Inclusive Graph', auto_open=False,)
            firsttPlotHTML = plotly_tools.get_embed(first_plot_url)
        else:
            df = time_filter_weekly(yearFi, weekFi, yearTi, weekTi)
            dfWS = df

            #Week Fixer
            if yearFi != yearTi:
                i = 0
                for index, row in df.iterrows():
                    if row['Year'] != yearFi:
                        count = row['Year'] - yearFi
                        dfWS.iat[i, 1] = row['Week'] + (count * 52)
                    i += 1
            
            #create graph
            A_H1 = Scatter(x = dfWS['Week'], y = dfWS['AH1'], mode = 'markers', name = 'A (H1)')
            A_H1N1 = Scatter(x = dfWS['Week'], y = dfWS['AH1N12009'], mode = 'markers', name = 'A (H1N1)')
            A_H3 = Scatter(x = dfWS['Week'], y = dfWS['AH3'], mode = 'markers', name = 'A (H3)')
            A_H5 = Scatter(x = dfWS['Week'], y = dfWS['AH5'], mode = 'markers', name = 'A (H5)')
            A_NoSub = Scatter(x = dfWS['Week'], y = dfWS['ANOTSUBTYPED'], mode = 'markers', name = 'A (No subtype)')
            A_Total = Scatter(x = dfWS['Week'], y = dfWS['INF_A'], mode = 'markers', name = 'A Total')
            B_Yamagata = Scatter(x = dfWS['Week'], y = dfWS['BYAMAGATA'], mode = 'markers', name = 'B (Yamagata)')
            B_Victoria = Scatter(x = dfWS['Week'], y = dfWS['BVICTORIA'], mode = 'markers', name = 'B (Victoria)')
            B_NoLineage = Scatter(x = dfWS['Week'], y = dfWS['BNOTDETERMINED'], mode = 'markers', name = 'B (No lineage)')
            B_Total = Scatter(x = dfWS['Week'], y = dfWS['INF_B'], mode = 'markers', name = 'B Total')
            data = [A_H1, A_H1N1, A_H3, A_H5, A_NoSub, A_Total, B_Yamagata, B_Victoria, B_NoLineage, B_Total]
            first_plot_url = py.plot(data, filename='Inclusive Graph', auto_open=False,)
            firsttPlotHTML = plotly_tools.get_embed(first_plot_url)

        #create html raw data table
        dfRaw = df.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">') #Table of raw data
        dfRaw = dfRaw.replace("<thead>",'<thead class="thead-dark">')

        #Run data analysis
        df.drop('Year', axis=1, inplace=True)
        df.drop('Week', axis=1, inplace=True)
        dfSum = df.describe()

        #create html summary table
        dfSum = dfSum.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">')  #Table of analyzed data
        dfSum = dfSum.replace("<thead>",'<thead class="thead-dark">')
        os.remove("/Users/Andres/Documents/Python/templates/result.html")   #clear old results

        #HTML code for the results
        html_string = '''
        <html>
        <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"></script>

        <title>Results</title>

        <style>
        body {
            position: relative;
        }
        </style>

        </head>

            <body data-spy="scroll" data-target=".navbar" data-offset="50">

    <!--NarBar-->
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="#section1">Data Selection Graph</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#section2">Full Data Selection Results</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#section3">Summary table</a>
        </li>
      </ul>
    </nav>

    <div id="section1" class="container-fluid" style="padding-top:70px;padding-bottom:70px">
      <div class="container">
        <div class="pb2 mt-4 mb-2 border-bottom">
          <h2>Data Selection Graph</h2>
        </div>
      </div>
      ''' + firsttPlotHTML + '''
    </div>

    <div id="section2" class="container-fluid" style="padding-top:70px;padding-bottom:70px">
      <div class="container">
        <div class="pb2 mt-4 mb-2 border-bottom">
          <h3>Full Data Selection Results</h3>
        </div>
      </div>
                ''' + dfRaw + '''
    </div>

    <div id="section3" class="container-fluid" style="padding-top:70px;padding-bottom:70px">
        <div class="container">
            <div class="pb2 mt-4 mb-2 border-bottom">
                <h3>Summary table: Data Selection Results</h3>
            </div>
        </div>
                ''' + dfSum + '''
        </div>
            </body>
        </html>'''

        #create the HTML file 
        f = open('/Users/Andres/Documents/Python/templates/result.html','w')
        f.write(html_string)
        f.close()
        
        #Return results to user
        return render_template('result.html')

    return render_template('my-form.html')




if __name__ == "__main__":
    app.run(debug=True)

#import all libraries
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

# instantiate flask app object
app = Flask(__name__)


# Read file in a pandas dataframe
path = r'absolute path to csv file'
dataframe = pd.read_csv(path)

# Separate the data yearly - we need them records for each year in a separate dataframe for better data analysis
dataframe_2015 = dataframe[dataframe["year"]==2015]
dataframe_2016 = dataframe[dataframe["year"]==2016]
dataframe_2017 = dataframe[dataframe["year"]==2017]

# Compute mean and median for each year
mean_2015 = dataframe_2015['net_revenue'].mean()
median_2015 = dataframe_2015['net_revenue'].mean()

mean_2016 = dataframe_2016['net_revenue'].mean()
median_2016 = dataframe_2015['net_revenue'].median()

mean_2017 = dataframe_2017['net_revenue'].mean()
median_2017 = dataframe_2015['net_revenue'].median()


'''
get_total_revenue() 
@:param year - the year for which the revenue is to be computed 
@:return total revenue for that year
'''
def get_total_revenue(year):
    filtered_data = dataframe[dataframe["year"] == year]
    return int(filtered_data['net_revenue'].sum())

# combining the two consecutive year dataframe
# (2015 + 2016) and (2016 + 2017)
dataframe_2015_16 = dataframe_2015.append(dataframe_2016)
dataframe_2016_17 = dataframe_2016.append(dataframe_2017)


# Compute Revenues from new customers in 2016
# From the combined 2015-16, remove duplicate values and drop rows with year = "2015
# Repeat the same from 2016 to 2017
new_customers_2015_16 = dataframe_2015_16.drop_duplicates(subset=['customer_email'])
new_customers_2016_17 = dataframe_2016_17.drop_duplicates(subset=['customer_email'])


# save new and lost customers in global variables to access later
# from the combined 2015 and 2016 with out duplicates, do minus the customers from previous year to get new customers
new_customers_count_2016 = (len(dataframe_2016.index) - len(dataframe_2015))
# from the same combined dataset, do minus customers from current year to get lost customers
lost_customers_count_2016 = (len(dataframe_2015.index) - len(dataframe_2016))

#do the same from 2016 to 2017
new_customers_count_2017 = (len(dataframe_2017.index) - len(dataframe_2016))
lost_customers_count_2017 = (len(dataframe_2016.index) - len(dataframe_2017))

new_customers_2015_16.drop(new_customers_2015_16.loc[new_customers_2015_16['year']==2015].index, inplace=True)
new_customers_2016_17.drop(new_customers_2016_17.loc[new_customers_2016_17['year']==2016].index, inplace=True)


current_revenue_2016 = new_customers_2015_16['net_revenue'].sum()
current_revenue_2017 = new_customers_2016_17['net_revenue'].sum()

# Route the home page of the web app
@app.route('/')
def index():
    return render_template('index.html')

# Route for the page of 2015
@app.route('/output15',methods=['GET'])
def year2015():

    total_revenue_2015 = get_total_revenue(2015)  # total revenue pf 2016
    new_customers_revenue_2015 = "N/A"  # revenue of new customers in 2016
    existing_customer_growth_2015 = "N/A"
    lost_revenue_attrition = "N/A"
    customer_revenue_current = "N/A"
    customer_revenue_prior = "N/A"
    total_customer_current_year = len(dataframe_2015.index)
    total_customer_previous_year = "N/A"
    total_new_customers = "N/A"
    total_lost_customers = "N/A"

    out = "\nTotal Revenue : " + str(total_revenue_2015) + "\nRevenue from new Customers : " + str(
        new_customers_revenue_2015) + "\nExisting customer growth : " + str(
        existing_customer_growth_2015) + "\nRevenue Lost from Attrition : " + str(
        lost_revenue_attrition) + "\nExisting Customer Revenue Current Year : " + str(
        customer_revenue_current) + "\nExisting Customer Revenue Prior Year :" + str(
        customer_revenue_prior) + "\nTotal Customers Current Year : " + str(
        total_customer_current_year) + "\nTotal Customers Previous Year : " + str(total_customer_previous_year) + "\nNew Customers : " + total_new_customers + " \nLost Customers : " + total_lost_customers

    return "<xmp>"  "\n" + "FY 2015 :\n" + out + "\n" + " </xmp> "

# Route for the page of 2016
@app.route('/output16',methods=['GET'])
def year2016():

    total_revenue_2016 = get_total_revenue(2016) # total revenue pf 2016
    new_customers_revenue_2016 = new_customers_2015_16['net_revenue'].sum() # revenue of new customers in 2016
    existing_customer_growth_2017 = total_revenue_2016 - get_total_revenue(2015)
    lost_revenue_attrition = total_revenue_2016-current_revenue_2016
    customer_revenue_current = current_revenue_2016
    customer_revenue_prior = get_total_revenue(2015)
    total_customer_current_year = len(dataframe_2016.index)
    total_customer_previous_year = len(dataframe_2015.index)
    # total new customers and lost customers called from the global variables


    out = "\nTotal Revenue : " + str(total_revenue_2016) + "\nRevenue from new Customers : " + str(new_customers_revenue_2016) + "\nExisting customer growth : " + str(existing_customer_growth_2017) + "\nRevenue Lost from Attrition : " + str(lost_revenue_attrition) + "\nExisting Customer Revenue Current Year : " + str(customer_revenue_current) + "\nExisting Customer Revenue Prior Year :" + str(customer_revenue_prior)+ "\nTotal Customers Current Year : " + str(total_customer_current_year) + "\nTotal Customers Previous Year : " + str(total_customer_previous_year) + "\nNew Customers : " + str(new_customers_count_2016) + "\nLost Customers : " + str(lost_customers_count_2016)

    return "<xmp>"  "\n" + "FY 2016 : \n" + out + "\n" + " </xmp> "

# Route for the page of 2017
@app.route('/output17.html',methods=['GET'])
def year2017():

    total_revenue_2017 = get_total_revenue(2017)  # total revenue pf 2016
    new_customers_revenue_2017 = new_customers_2016_17['net_revenue'].sum()  # revenue of new customers in 2016
    existing_customer_growth_2017 = total_revenue_2017 - get_total_revenue(2016)
    lost_revenue_attrition = total_revenue_2017-current_revenue_2017
    customer_revenue_current = current_revenue_2017
    customer_revenue_prior = get_total_revenue(2016)
    total_customer_current_year = len(dataframe_2017.index)
    total_customer_previous_year = len(dataframe_2016.index)


    out = "\nTotal Revenue : " + str(total_revenue_2017) + "\nRevenue from new Customers : " + str(
        new_customers_revenue_2017) + "\nExisting customer growth : " + str(
        existing_customer_growth_2017) + "\nRevenue Lost from Attrition : " + str(
        lost_revenue_attrition) + "\nExisting Customer Revenue Current Year : " + str(
        customer_revenue_current) + "\nExisting Customer Revenue Prior Year :" + str(
        customer_revenue_prior) + "\nTotal Customers Current Year : " + str(
        total_customer_current_year) + "\nTotal Customers Previous Year : " + str(
        total_customer_previous_year) + "\n New Customers : " + str(
        new_customers_count_2017) + "\nLost Customers : " + str(lost_customers_count_2017)

    return "<xmp>"  "\n" + "FY 2017 : \n" + out + "\n" + " </xmp> "


# Route for the page of visualizations
@app.route('/visualizations')
def visualizations():
    return render_template('visualizations.html')

# store the total revenue in a global variable which can be used for further processing
total = get_total_revenue(2015) + get_total_revenue(2016) + get_total_revenue(2017)

# Route for the Pie Chart - Matplotlib visualization
# We will route the pie chart inside HTML frame in the visualizations.html page
@app.route('/piechart')
def piechart():
    img = io.BytesIO()
    #y = [1, 2, 3, 4, 5]
    #x = [0, 2, 1, 3, 4]
    labels = 'FY-2015', 'FY-2016', 'FY-2017'
    sizes = [get_total_revenue(2015)/total, get_total_revenue(2016)/total,get_total_revenue(2017)/total]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    plt.title("Pie Chart : Yearly Revenue Composition")
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    #return render_template('piechart.html',data=data)
    return '<img src="data:image/png;base64,{}">'.format(plot_url)

# Route for the Bar Graph - Matplotlib visualization
# We will also route the Bar Graph inside HTML frame in the visualizations.html page
@app.route('/bargraph')
def bargraph():
    img = io.BytesIO()

    data = {'FY-2015': len(dataframe_2015.index), 'FY-2016': len(dataframe_2016.index), 'FY-2017': len(dataframe_2017.index)}
    year = list(data.keys())
    customers = list(data.values())

    fig= plt.figure(figsize=(5, 4))

    # creating the bar plot
    plt.barh(year, customers, color='maroon',align='center', height=0.3)
    plt.xlabel("total_customers")
    #plt.ylabel("total_customers")
    plt.title("Bar Plot : Changes in Total No. of Customers")
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url2 = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url2)

# Route for the Observations of the Matplotlib visualizations
# We will route the observations text data inside HTML frame in the visualizations.html page along with pie chart and bar graph
@app.route('/observations')
def observations():

    return render_template('observations.html')

# Driver Function
if __name__ == '__main__':
    app.run(debug=True)


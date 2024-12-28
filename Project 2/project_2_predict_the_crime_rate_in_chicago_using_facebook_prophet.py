# -*- coding: utf-8 -*-
"""Project 2: Predict the Crime Rate in Chicago using Facebook Prophet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fOdZkcPEEsrZ4ESZ5g6n3GEYjtOXIly3

# Problem Statement

The Chicago Crime dataset contains a summary of the reported crimes occurred in the City of Chicago from 2001 to 2017.

- Dataset contains the following columns:
    - ID: Unique identifier for the record.
    - Case Number: The Chicago Police Department RD Number (Records Division Number), which is unique to the incident.
    - Date: Date when the incident occurred.
    - Block: address where the incident occurred
    - IUCR: The Illinois Unifrom Crime Reporting code.
    - Primary Type: The primary description of the IUCR code.
    - Description: The secondary description of the IUCR code, a subcategory of the primary description.
    - Location Description: Description of the location where the incident occurred.
    - Arrest: Indicates whether an arrest was made.
    - Domestic: Indicates whether the incident was domestic-related as defined by the Illinois Domestic Violence Act.
    - Beat: Indicates the beat where the incident occurred. A beat is the smallest police geographic area – each beat has a dedicated police beat car.
    - District: Indicates the police district where the incident occurred.
    - Ward: The ward (City Council district) where the incident occurred.
    - Community Area: Indicates the community area where the incident occurred. Chicago has 77 community areas.
    - FBI Code: Indicates the crime classification as outlined in the FBI's National Incident-Based Reporting System (NIBRS).
    - X Coordinate: The x coordinate of the location where the incident occurred in State Plane Illinois East NAD 1983 projection.
    - Y Coordinate: The y coordinate of the location where the incident occurred in State Plane Illinois East NAD 1983 projection.
    - Year: Year the incident occurred.
    - Updated On: Date and time the record was last updated.
    - Latitude: The latitude of the location where the incident occurred. This location is shifted from the actual location for partial redaction but falls on the same block.
    - Longitude: The longitude of the location where the incident occurred. This location is shifted from the actual location for partial redaction but falls on the same block.
    - Location: The location where the incident occurred in a format that allows for creation of maps and other geographic operations on this data portal. This location is shifted from the actual location for partial redaction but falls on the same block.

--> Predict the crime rate using Facebook prophet tool.
"""

!pip install prophet

"""# Import the dataset"""

import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt
from prophet import Prophet

data_1 = pd.read_csv("/content/Chicago_Crimes_2001_to_2004.csv")
data_2 = pd.read_csv("/content/Chicago_Crimes_2005_to_2007.csv")
data_3 = pd.read_csv("/content/Chicago_Crimes_2005_to_2007.csv")
data_4 = pd.read_csv("/content/Chicago_Crimes_2012_to_2017.csv")

data_1.info()

data_2.info()

data_3.info()

data_4.info()

chicago_data=pd.concat([data_1,data_2,data_3,data_4])
chicago_data

chicago_data.info()

chicago_data.shape

chicago_data.describe()

chicago_data.head()

chicago_data.isnull().sum()

chicago_data.columns

chicago_data=chicago_data.drop(['Unnamed: 0','ID', 'Case Number','IUCR',
                   'X Coordinate', 'Y Coordinate','Updated On',
                   'Year','FBI Code','Beat','Ward',
                   'Community Area','Location','Latitude',
                    'Longitude','District'],axis=1)

chicago_data.head()

chicago_data.info()

chicago_data.Date = pd.to_datetime(chicago_data.Date, format='%m/%d/%Y %I:%M:%S %p', errors='coerce')

chicago_data.head()

chicago_data.index=pd.DatetimeIndex(chicago_data.Date)

chicago_data['Primary Type'].value_counts()

chicago_data['Primary Type'].value_counts().iloc[:15]

order_data=chicago_data['Primary Type'].value_counts().iloc[:15].index
order_data.is_unique

chicago_data['Location Description'].value_counts()

chicago_data['Location Description'].value_counts().iloc[:15]

chicago_data.resample("Y").size()

plt.plot(chicago_data.resample("Y").size())
plt.title("Crime Count Per Year")
plt.xlabel("Years")
plt.ylabel("Numer of Crimes")

"""#Prepare the Data"""

chicago_data_prophet= chicago_data.resample("M").size().reset_index()
chicago_data_prophet

chicago_data_prophet.columns=['Date','Crime Count']
chicago_data_prophet

chicago_data_prophet_final=chicago_data_prophet.rename(columns={'Date':'ds',"Crime Count":"y"})
chicago_data_prophet_final

"""# Make Predictions"""

m = Prophet()
m.fit(chicago_data_prophet_final)

future = m.make_future_dataframe(periods=365)
forecast=m.predict(future)
forecast

figure=m.plot(forecast,xlabel="Date",ylabel="Crime Rate")

figure=m.plot_components(forecast)

future = m.make_future_dataframe(periods=720)
forecast=m.predict(future)
forecast

figure=m.plot(forecast,xlabel="Date",ylabel="Crime Rate")

figure=m.plot_components(forecast)
#!/usr/bin/env python

import pandas as pd 
pd.set_option('display.max_rows', 15500)
pd.set_option('display.max_columns', 55500)
pd.set_option('display.width', 551000)
data = pd.read_csv("crimemar14.csv")
data.head()

newdata = data["Datetime"].str.split("@", n = 1, expand = True)

data["date"] = newdata[0]

data["time"] = newdata[1]
data.head()

data["time"]= pd.to_datetime(data["time"],format=' %I:%M %p' ).dt.time

data["date"]= pd.to_datetime(data["date"],errors='coerce' )
data["day"]= data["date"].dt.day
data["dayname"]= data["date"].dt.day_name()
data["dayofweek"] = data["date"].dt.dayofweek
data["monthname"] = data["date"].dt.month_name()
data['Datetime'] = pd.to_datetime(data["Datetime"],format='%m/%d/%Y @ %I:%M %p',errors='coerce')
data.head()

daycrime = data.groupby('Crime_Type')['day'].value_counts()

daycrime = data.groupby('Crime_Type')['monthname'].value_counts()

crimetypes = [ "Arson", "Assault", "Burglary", "Disturbing the Peace", "Drugs / Alcohol Violations", "DUI", "Fraud", "Homicide", "Motor Vehicle Theft", "Robbery", "Sex Crimes", "Theft / Larceny", "Vandalism", "Vehicle Break-In / Theft", "Weapons"]

df = pd.DataFrame()

#for crime in crimetypes:

d1 = daycrime["Assault"]
df["Type"] = d1
#print(df)
crimes = daycrime.index
for x in daycrime["Assault"]:
   print(x)

  #df.append(d1)

data
daystreetcrime = data["Street_Address"].str.split(" ", n = 2, expand = True)
data['StreetName'] = daystreetcrime[2]
streetofcrime = data.groupby('dayname')['StreetName'].value_counts()

print(streetofcrime)

import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
import csv

def prepareSet(testWeather, day):
    import pandas as pd
    #Load weather dataset
    #Sets the index to date

    modifiedSet = testWeather[["PRCP", "SNWD", "TMAX","TMIN"]].copy()

    #Fill in empty values
    modifiedSet["PRCP"] = modifiedSet["PRCP"].fillna(0)
    modifiedSet["SNWD"] = modifiedSet["SNWD"].fillna(0)
    modifiedSet = modifiedSet.fillna(method="ffill")

    #Remove the first value, as it can't be filled in
    modifiedSet = modifiedSet.iloc[1:,:].copy()

    #Convert date string to date type
    modifiedSet.index = pd.to_datetime(modifiedSet.index)

    #Convert F to C
    modifiedSet["TMAX"] = (modifiedSet["TMAX"]-32)* (5/9)

    modifiedSet["TMIN"] = (modifiedSet["TMIN"]-32)* (5/9)

    #Monthly average
    modifiedSet["MONTHLY_AVG"] = modifiedSet["TMAX"].groupby(modifiedSet.index.month).apply(lambda x: x.expanding(1).mean())

    #Daily average
    modifiedSet["DAY_OF_YEAR_AVG"] = modifiedSet["TMAX"].groupby(modifiedSet.index.day_of_year).apply(lambda x: x.expanding(1).mean())

    #Set target to TMAX, shifted by the number of days
    modifiedSet["TARGET_MAX"] = modifiedSet.shift(-day)["TMAX"]
    modifiedSet["TARGET_MIN"] = modifiedSet.shift(-day)["TMIN"]
    modifiedSet["TARGET_PRCP"] = modifiedSet.shift(-day)["PRCP"]

    #Removes the last row as it does not have a target (depending on the number of days shifted)
    modifiedSet = modifiedSet.iloc[:-day,:].copy()


   

    return modifiedSet


def makePrediction(predictors, modifiedSet, currentData, reg, target):
    #Split dataset into training set and test set
    train = modifiedSet
    test = currentData

    #Fit training model to dataset
    reg.fit(train[predictors], train[target])
    predictions = reg.predict(test[predictors])

    return predictions

testWeather = pd.read_csv("set1.csv", index_col="DATE")


def run():
    import pandas as pd
    from sklearn.linear_model import Ridge
    from sklearn.metrics import mean_absolute_error
    import csv

    #API Data

    import requests
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Cirencester&appid=8f4b263a6f4f6e42c57cf48937167bed")
    precipitation = requests.get("http://api.weatherapi.com/v1/current.json?key=915eec29b4cf4596810115908230209&q=Cirencester&aqi=no")

    api_data=response.json()
    api_precipitation=precipitation.json()


    #Convert to csv


    #Opens/creates file
    currentWeather = open('currentData.csv', 'w')
    currentWeather.truncate()

    csv_writer = csv.writer(currentWeather)

    mintempk = api_data["main"]["temp_min"]
    mintempc = mintempk - 273.15
    maxtempk = api_data["main"]["temp_max"]
    maxtempc = maxtempk - 273.15

    
    
    rainfall = api_precipitation["current"]["precip_mm"]
    
    from datetime import date
    today = date.today()



    csv_writer.writerow(["DATE","TMIN", "TMAX", "PRCP"])
    csv_writer.writerow([today, mintempc, maxtempc, rainfall, ] )
        
    currentWeather.close()

    overall_results = []

    for each in range(0,14):
        testWeather = pd.read_csv("set1.csv", index_col="DATE")
        modifiedSet = prepareSet(testWeather, each+1)

        currentData=pd.read_csv("currentData.csv", index_col="DATE")

        #Prediction
        reg=Ridge(alpha=.1)

        #Variables used to make predictions
        predictors = ["PRCP","TMAX","TMIN"]

        max_result = makePrediction(predictors, modifiedSet, currentData, reg, "TARGET_MAX")

        

        min_result = makePrediction(predictors, modifiedSet, currentData, reg, "TARGET_MIN")

        

        prcp_result = makePrediction(predictors, modifiedSet, currentData, reg, "TARGET_PRCP")

        

        overall_results.append({"day":each+1, "TMIN":min_result[0], "TMAX":max_result[0],"PRCP":prcp_result[0]})
   
    print(overall_results)
    return overall_results
overall_results=run()



from src import createDatabase
from src import trimbleData
from src import treatments
from src import seasons 
from src import sampleDates
from src import soilMoisture
from src import plantData
from src import rootScan

DB = "Schantz_Forage_DB.sqlite"
Datasheet = r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\Pasture Study Data, Weights, and Labels.xlsx"


"""
From module createDatabase instantiates the class createDatabase.
The __init__ constructor will create and connect to a new Databse with
the file name defined above by variable DB. The tables will populate
with the defined columns and supply the datatype.
Need only run once.
"""
# createDB = createDatabase.createDatabase(DB)


"""
From module trimbleData instantiates the class location supplied with
variable DB.
The __init__ constructor will make the connection to the Database. 
The method addLocation will perform a check of the coordinates and
supply the id and name of location of the studies (Temple and Riesel)
to the Table Location.
"""
# loc = trimbleData.location(DB)
# loc.addLocation()



"""
From module trimbleData instantiates the class plotCorners supplied 
with the variable DB.
The __init__ constructor will make the connection to the Database.
The addPlotsAndCorners will read a .CSV file and add the plot numbers
to the Table Plots and the geographic data of the plot corners to the
Table Plot_Corners.
"""
# pc = trimbleData.plotCorners(DB)
# pc.addPlotsAndCorners("Schantz_Temple_Pasture_Plots.csv")
# pc.addPlotsAndCorners("Schantz Forage Pasture Study (Riesel).csv")


"""
From module seasons instantiates the class seasons supplied
with the variable DB
The __init__constructor will make the connection to the Database.
The add seasons function will read from the excel file tied to
the variable Datasheet and adds Unique entries of the Year and season
to the Table Season.
"""
# seas = seasons.seasons(DB)
# seas.addSeasons(Datasheet)


"""
From module treatments instantiates the class treatments supplied
with the variable DB.
The __init__ constructor will make the connection to the Databse.
The addTreatments function will read from a csv the treatments
for the corresponding plots and adds the records to the Table
Treatments
"""
# treat = treatments.treatments(DB)
# treat.addTreatments(Datasheet)


"""
From module sampleDates instantiates the class dates supplied with
the variable DB.
The __init__ constructor will make the connection to the Database.
The addDates function will read from the excel file tied to the
variable Datasheet and adds the Sample Dates to the Table Sample_Dates.
"""
# date = sampleDates.dates(DB)
# date.addDates(Datasheet)


"""
From module soilMoisture instantiates the class soilMoisture supplied with
the variable DB.
The __init__ constructor will make the connection to the Database.
The addSoilMoisture function will read from the excel file tied to the
variable Datasheet and adds the soil moisture values of each sampling 
to the table Soil_Moisture.
"""
# sm = soilMoisture.soilMoisture(DB)
# sm.addSoilMoisture(Datasheet)


"""
From module plantData instantiates the class plantData supplied with
the variable DB.
The __init__ constructor will make the connection to the Database.
The addData function will read from the excel file tied to the
variable Datasheet and adds the gravimetric values of each sampling 
to the table Plant_Data.
"""
# plant = plantData.plantData(DB)
# plant.addData(Datasheet)


"""
From module trimbleData instantiates the class samplingPoints supplied
witht the variable DB.
the __init__ constructor will make the connection to the Database.
The addSamplingPoints function will read from the .CSV file supplied as a 
paramater and adds the geographic coordinates to the Table 
Sampling_Points
"""
# TSu24S1 = trimbleData.samplingPoints(DB)
# TSu24S1.addSamplingPoints(r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\GIS - Pasture Study Sampling Points\Temple Sampling Points\TSu24_CSVfiles\TSu24_S1 Sampling Points.csv")
# TSu24S2 = trimbleData.samplingPoints(DB)
# TSu24S2.addSamplingPoints(r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\GIS - Pasture Study Sampling Points\Temple Sampling Points\TSu24_CSVfiles\TSu24_S2 Sampling Points.csv")
# TSu24S3 = trimbleData.samplingPoints(DB)
# TSu24S3.addSamplingPoints(r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\GIS - Pasture Study Sampling Points\Temple Sampling Points\TSu24_CSVfiles\TSu24_S3 Sampling Points.csv")
# TSu24S4 = trimbleData.samplingPoints(DB)
# TSu24S4.addSamplingPoints(r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\GIS - Pasture Study Sampling Points\Temple Sampling Points\TSu24_CSVfiles\TSu24_S4 Sampling Points.csv")
# TWi24S1 = trimbleData.samplingPoints(DB)
# TWi24S1.addSamplingPoints(r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\GIS - Pasture Study Sampling Points\Temple Sampling Points\TWi24_CSVFiles\TWi24_S1 Sampling Points.csv")
# TWi24S2 = trimbleData.samplingPoints(DB)
# TWi24S2.addSamplingPoints(r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\GIS - Pasture Study Sampling Points\Temple Sampling Points\TWi24_CSVFiles\TWi24_S2 Sampling Points.csv")

# RWi24S1 = trimbleData.samplingPoints(DB)
# RWi24S1.addSamplingPoints(r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\GIS - Pasture Study Sampling Points\Riesel Sampling Points\RWi24_CSVFiles\RWi24_S1 Sampling Points.csv")

"""
From module rootScan instantiates the class rootScanData supplied
with the variable DB.
THe __init__ constructor will make the connection to the Database and
read the output excel file from the rootscanner and passes the DataFrame
through the class.
The addSamples function will take this DataFrame and add the Sample
Names to the Table Root_Scan_Samples.
The addResults function will take the DataFrame and add the measured
values to the Table Root_Scan_Data.
"""
# TSu24S3Root = rootScan.rootScanData(DB, r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\Root Scans\Temple\TSu24_S3_rootscan\TSu24_S3_rootscan_processed.xlsx")
# TSu24S3Root.addSamples()
# TSu24S3Root.addResults()
# TSu24S4Root = rootScan.rootScanData(DB, r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\Root Scans\Temple\TSu24_S4_rootscan\TSu24_S4_rootscan_processed.xlsx")
# TSu24S4Root.addSamples()
# TSu24S4Root.addResults()
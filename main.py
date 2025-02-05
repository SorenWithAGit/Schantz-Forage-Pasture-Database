from src import createDatabase
from src import trimbleData
from src import treatments
from src import seasons 
from src import sampleDates
from src import soilMoisture
from src import plantData

DB = "Schantz_Temple_Pasture_DB.sqlite"
Datasheet = r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\Pasture Study Data, Weights, and Labels.xlsx"

# Create Database
# createDB = createDatabase.createDatabase(DB)

# Add Locations
# loc = trimbleData.location(DB)
# loc.addLocation()

# Add Plot Corners
# pc = trimbleData.plotCorners(DB)
# pc.addPlotsAndCorners("Schantz_Temple_Pasture_Plots.csv")
# pc.addPlotsAndCorners("Schantz Forage Pasture Study (Riesel).csv")

# Add Treatments
# treat = treatments.treatments(DB)
# treat.addTreatments("Schantz Pasture Study Treatments.csv")

# Add Seasons
# seas = seasons.seasons(DB)
# seas.addSeasons(Datasheet)

# Add Sample Dates
# date = sampleDates.dates(DB)
# date.addDates(Datasheet)

# Add Soil Moisture
sm = soilMoisture.soilMoisture(DB)
sm.addSoilMoisture(Datasheet)

# Add Plant Data
# plant = plantData.plantData(DB)
# plant.addData(Datasheet)




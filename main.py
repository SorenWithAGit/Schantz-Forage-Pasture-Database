from src import createDatabase as cd
from src import trimbleData as atd
from src import treatments as at
from src import seasons 
from src import sampleDates

DB = "Schantz_Temple_Pasture_DB.sqlite"
Datasheet = r"C:\Users\john.sorensen\Box\Schantz Group Shared Data\Pasture Study\Pasture Study Data, Weights, and Labels.xlsx"

# Create Database
#DB = cd.createDatabase(DB)

# Add Plot Corners
# pc = atd.plotCorners(DB)
# pc.addPlotAndCorners("Schantz_Temple_Pasture_Plots.csv")

# Add Treatments
# treat = at.treatments(DB)
# treat.addTreatments("Schantz Pasture Study Treatments.csv")

# Add Seasons
# seas = addSeasons.seasons(DB)
# seas.addSeasons(Datasheet)

# Add Sample Dates
date = sampleDates.dates(DB)
date.addDates(Datasheet)


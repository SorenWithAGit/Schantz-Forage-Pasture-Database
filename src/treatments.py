import sqlite3
import pandas as pd

class treatments:

    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

    def addTreatments(self, filename):
        treatment_df = pd.read_excel(filename, sheet_name = "Data Sheet")
        plots_query = '''SELECT * FROM Plots'''
        location_query = '''SELECT * FROM Location'''
        seasons_query = '''SELECT * FROM Season'''
        Plots_ids = []
        location_ids = []
        Seasons_ids = []

        location_results = self.cur.execute(location_query).fetchall()
        location_df = pd.DataFrame(location_results, columns = [description[0] for description in self.cur.description])
        for ind in treatment_df.index:
            for i in range(len(location_df)):
                if treatment_df.iloc[ind]["Location"] == location_df.iloc[i]["Location"]:
                    location_id = location_df.iloc[i]['id']
                    location_ids.append(location_id)
        treatment_df["Location_id"] = location_ids

        plots_results = self.cur.execute(plots_query).fetchall()
        plots_df = pd.DataFrame(plots_results, columns=[description[0] for description in self.cur.description])
        for record in treatment_df.index:
            for ind in range(len(plots_df)):
                if treatment_df.iloc[record]["Location_id"] == plots_df.iloc[ind]["Location_id"] and treatment_df.iloc[record]['Block #'] == plots_df.iloc[ind]['Block'] and treatment_df.iloc[record]['Plot #'] == plots_df.iloc[ind]['Plot']:
                    #print('Success! Block: ' + str(soil_m_df.iloc[record]['Block #']) + ' and Plot: ' + str(soil_m_df.iloc[record]['Plot #']) + ' Found!' + 
                            #'Plot_id = ' + str(plots_df.iloc[ind]['id']))
                    plot_id = plots_df.iloc[ind]['id'] 
                    Plots_ids.append(plot_id)
        treatment_df['Plots_id'] = Plots_ids

        seasons_results = self.cur.execute(seasons_query).fetchall()
        seasons_df = pd.DataFrame(seasons_results, columns = [description[0] for description in self.cur.description])
        for i in treatment_df.index:
            for s in range(len(seasons_df)):
                if treatment_df.iloc[i]['Year/Season Mix'] == seasons_df.iloc[s]["Year/Season Mix"]:
                    season_id = seasons_df.iloc[s]['id']
                    Seasons_ids.append(season_id)
        treatment_df['Season_id'] = Seasons_ids
        treatment_df = treatment_df.iloc[:,[20, 19, 21, 0, 1, 2, 5, 6, 7, 8]]

        for record in treatment_df.index:
            if treatment_df.iloc[record]["Sampling #"] == 1:
                plot_id = int(treatment_df.iloc[record]['Plots_id'])
                loc_id = int(treatment_df.iloc[record]['Location_id'])
                seas_id = int(treatment_df.iloc[record]["Season_id"])
                seeding = treatment_df.iloc[record]['Seeding']
                fert = treatment_df.iloc[record]['Fert. Treatment']
                till = treatment_df.iloc[record]['Till. Treatment']
                self.cur.execute('''INSERT INTO Treatments (
                            Plots_id,
                            Location_id,
                            Season_id,
                            Seeding,
                            Fertilizer_Treatment,
                            Tillage_Treatment)
                            VALUES (?, ?, ?, ?, ?, ?)''', (
                            plot_id,
                            loc_id,
                            seas_id,
                            seeding,
                            fert,
                            till,)
                            )
        self.conn.commit()

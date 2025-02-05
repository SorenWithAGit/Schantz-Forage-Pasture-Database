import sqlite3
import pandas as pd

class dates:

    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

    def addDates(self, filename):
        date_df = pd.read_excel(filename, sheet_name = "Data Sheet")
        date_df.drop(['BP', 
                     'Seeding',
                     'Fert. Treatment',
                     'Till. Treatment',
                     'Soil Tin Number',
                     'Soil Wet Weight (g)',
                     'Soil Dry Weight (g)',
                     'Grass Dry Weight (g)',
                     'Non-Grass Dry Weight (g)',
                     'Other Dry Weight (g)',
                     'Litter Dry Weight (g)',
                     'Root Dry Weight (g)'], axis = 1, inplace = True)
        plots_query = '''SELECT * FROM Plots'''
        location_query = """SELECT * FROM Location"""
        treatments_query = '''SELECT * FROM Treatments'''
        seasons_query = '''SELECT * FROM Season'''
        plots_results = self.cur.execute(plots_query).fetchall()
        plots_df = pd.DataFrame(plots_results, columns=[description[0] for description in self.cur.description])
        location_results = self.cur.execute(location_query).fetchall()
        loc_df = pd.DataFrame(location_results, columns = [description[0] for description in self.cur.description])
        Plots_ids = []
        Treatments_ids = []
        Seasons_ids = []
        loc_ids = []
        for ind in date_df.index:
            for l in range(len(loc_df)):
                if date_df.iloc[ind]['Location'] == loc_df.iloc[l]['Location']:
                    loc_id = loc_df.iloc[l]['id']
                    loc_ids.append(loc_id)
        date_df['Location_id'] = loc_ids
        seasons_results = self.cur.execute(seasons_query).fetchall()
        seasons_df = pd.DataFrame(seasons_results, columns = [description[0] for description in self.cur.description])
        for i in date_df.index:
            for s in range(len(seasons_df)):
                if str(date_df.iloc[i]['Year/Season Mix']) == str(seasons_df.iloc[s]['Year/Season Mix']):
                    season_id = seasons_df.iloc[s]['id']
                    Seasons_ids.append(season_id)
        date_df['Season_id'] = Seasons_ids
        for record in date_df.index:
                for ind in range(len(plots_df)):
                    for i in range(len(seasons_df)):
                        if date_df.iloc[record]['Year/Season Mix'] == seasons_df.iloc[i]['Year/Season Mix'] and date_df.iloc[record]["Location_id"] == plots_df.iloc[ind]["Location_id"]:
                            if  date_df.iloc[record]['Block #'] == plots_df.iloc[ind]['Block'] and date_df.iloc[record]['Plot #'] == plots_df.iloc[ind]['Plot']:
                                #print('Success! Block: ' + str(date_df.iloc[record]['Block #']) + ' and Plot: ' + str(date_df.iloc[record]['Plot #']) + ' Found!' + 
                                #'Plot_id = ' + str(plots_df.iloc[ind]['id']))
                                plot_id = plots_df.iloc[ind]['id'] 
                                Plots_ids.append(plot_id)
        date_df['Plots_id'] = Plots_ids
        print(date_df)
        treatments_results = self.cur.execute(treatments_query).fetchall()
        treatments_df = pd.DataFrame(treatments_results, columns=[description[0] for description in self.cur.description])
        for x in date_df.index:
            for y in range(len(treatments_df)):
                if date_df.iloc[x]['Plots_id'] == treatments_df.iloc[y]['Plots_id']:
                    treatment_id = treatments_df.iloc[y]['id']
                    Treatments_ids.append(treatment_id)
        #            print('index = ' + str(date_df.index.get_loc(x)) + ', Plots_id = ' + str(date_df.iloc[x]['Plots_id']) + ' treatment_id = ' + str(treatment_id))
        date_df['Treatments_id'] = Treatments_ids
        for entry in date_df.index:
            plt_id = int(date_df.iloc[entry]['Plots_id'])
            treat_id = int(date_df.iloc[entry]['Treatments_id'])
            ssn_id = int(date_df.iloc[entry]['Season_id'])
            spl_date = str(date_df.iloc[entry]['Sample Date'])
            locat_id = int(date_df.iloc[entry]['Location_id'])
            self.cur.execute('''INSERT INTO Sampling_Dates (
                        Plots_id,
                        Location_id,
                        Treatments_id,
                        Season_id,
                        Sample_Date)
                        VALUES (?, ?, ?, ?, ?)''', (
                        plt_id,
                        locat_id,
                        treat_id,
                        ssn_id,
                        spl_date,)
                       )
            self.conn.commit()
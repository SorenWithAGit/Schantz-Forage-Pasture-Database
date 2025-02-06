import sqlite3
import pandas as pd

class rootScanData:

    def __init__(self, database, file):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
        self.rootScanData = file
        self.rootScanDF = pd.read_excel(self.rootScanData, sheet_name = "Cleaned Data")
        self.rootScanDF['Plot'] = self.rootScanDF['Sample Id'].str.replace('_', '').str[0:3]
        self.rootScanDF["Location_identity"] = self.rootScanDF["Sample Id"].str.replace("_", "").str[3]
        locat = []
        for item in self.rootScanDF.index:
            if str(self.rootScanDF.iloc[item]["Location_identity"]) == "T":
                locat.append("Temple")
            elif str(self.rootScanDF.iloc[item]["Location_identity"]) == "R":
                locat.append("Riesel")
        self.rootScanDF["Location"] = locat
        try:
            self.rootScanDF['Season'] = self.rootScanDF['Sample Id'].str.replace('_', '').str[4:6].replace('Su', 'Summer')
        except:
            self.rootScanDF['Season'] = self.rootScanDF['Sample Id'].str.replace('_', '').str[4:6].replace('Wi', 'Winter')
        self.rootScanDF['Year'] = self.rootScanDF['Date'].dt.year
        plots_query = '''SELECT * FROM Plots'''
        location_query = """SELECT * FROM Location"""
        treatments_query = '''SELECT * FROM Treatments'''
        sample_date_query = '''SELECT * FROM Sampling_Dates'''
        seasons_query = '''SELECT * FROM Season'''
        plots_results = self.cur.execute(plots_query).fetchall()
        plots_df = pd.DataFrame(plots_results, columns=[description[0] for description in self.cur.description])
        location_results = self.cur.execute(location_query).fetchall()
        location_df = pd.DataFrame(location_results, columns = [description[0] for description in self.cur.description])
        Plots_ids = []
        location_ids = []
        Treatments_ids = []
        Sample_Date_ids = []
        Seasons_ids = []

        for ind in self.rootScanDF.index:
            for i in range(len(location_df)):
                if self.rootScanDF.iloc[ind]["Location"] == location_df.iloc[i]["Location"]:
                    location_id = location_df.iloc[i]["id"]
                    location_ids.append(location_id)
        self.rootScanDF["Location_id"] = location_ids

        for record in self.rootScanDF.index:
            for ind in range(len(plots_df)):
                if self.rootScanDF.iloc[record]["Location_id"] == plots_df.iloc[ind]["Location_id"] and self.rootScanDF.iloc and int(self.rootScanDF.iloc[record]['Plot']) == int(plots_df.iloc[ind]['Plot_Number']):
                    plot_id = plots_df.iloc[ind]['id'] 
                    Plots_ids.append(plot_id)
        self.rootScanDF['Plots_id'] = Plots_ids

        seasons_results = self.cur.execute(seasons_query).fetchall()
        seasons_df = pd.DataFrame(seasons_results, columns = [description[0] for description in self.cur.description])
        for i in self.rootScanDF.index:
            for s in range(len(seasons_df)):
                year_mix = str(self.rootScanDF.iloc[i]["Year"]) + " " + str(self.rootScanDF.iloc[i]["Season"])
                if year_mix == seasons_df.iloc[s]["Year/Season Mix"]:
                    season_id = seasons_df.iloc[s]['id']
                    Seasons_ids.append(season_id)
        self.rootScanDF['Season_id'] = Seasons_ids

        treatments_results = self.cur.execute(treatments_query).fetchall()
        treatments_df = pd.DataFrame(treatments_results, columns=[description[0] for description in self.cur.description])
        for x in self.rootScanDF.index:
            for y in range(len(treatments_df)):
                if self.rootScanDF.iloc[x]["Location_id"] == treatments_df.iloc[y]["Location_id"] and self.rootScanDF.iloc[x]['Plots_id'] == treatments_df.iloc[y]['Plots_id']:
                    treatment_id = treatments_df.iloc[y]['id']
                    Treatments_ids.append(treatment_id)
        self.rootScanDF['Treatments_id'] = Treatments_ids

        sample_date_results = self.cur.execute(sample_date_query).fetchall()
        sample_date_df = pd.DataFrame(sample_date_results, columns =[description[0] for description in self.cur.description])
        for date in self.rootScanDF.index:
            for d in range(len(sample_date_df)):
                if self.rootScanDF.iloc[date]["Location_id"] == sample_date_df.iloc[d]["Location_id"] and self.rootScanDF.iloc[date]["Plots_id"] == sample_date_df.iloc[d]["Plots_id"] and str(self.rootScanDF.iloc[date]['Date']) == str(sample_date_df.iloc[d]['Sample_Date']):
                    sample_date_id = sample_date_df.iloc[d]['id']
                        #sample_date = sample_date_df.iloc[d]['Sample_Date']
                        #print('index = ' + str(self.rootScanDF.index.get_loc(d)) + ', Sample_date = ' + str(self.rootScanDF.iloc[d]['Sample Date']) + ' Sample_Date = ' + str(sample_date))
                    Sample_Date_ids.append(sample_date_id)
        self.rootScanDF['Sample_Date_id'] = Sample_Date_ids

    def addSamples(self):
        for record in self.rootScanDF.index:
            plot = int(self.rootScanDF.iloc[record]['Plots_id'])
            locat_id = int(self.rootScanDF.iloc[record]["Location_id"])
            treat = int(self.rootScanDF.iloc[record]['Treatments_id'])
            smpl_date = int(self.rootScanDF.iloc[record]['Sample_Date_id'])
            ssn = int(self.rootScanDF.iloc[record]['Season_id'])
            name = self.rootScanDF.iloc[record]['Sample Id']
            self.cur.execute('''INSERT INTO Root_Scan_Samples (
                        Plots_id,
                        Location_id,
                        Treatments_id,
                        Sample_Date_id,
                        Season_id,
                        Sample_Name)
                        VALUES (?, ?, ?, ?, ?, ?)''', (
                        plot,
                        locat_id,
                        treat,
                        smpl_date,
                        ssn,
                        name,)
                       )
            self.conn.commit()

    def addResults(self):
        root_scan_df = self.rootScanDF
        root_sample_query = "SELECT * FROM Root_Scan_Samples"
        root_sample_df = self.cur.execute(root_sample_query).fetchall()
        root_sample_df = pd.DataFrame(root_sample_df, columns =[description[0] for description in self.cur.description])
        root_sample_ids = []
        for ind in root_scan_df.index:
            for i in root_sample_df.index:
                if root_scan_df.iloc[ind]['Sample Id'] == root_sample_df.iloc[i]['Sample_Name']:
                    root_id = root_sample_df.iloc[i]['id']
                    root_sample_ids.append(root_id)
        root_scan_df['Root_Scan_Samples_id'] = root_sample_ids
        root_scan_df.drop(['Sample Id', 'Date', 'Seeding', 'Treatment', 'Location_identity', 'Location'], axis = 1, inplace = True)
        root_scan_df = root_scan_df.iloc[:,[71, 67, 66, 69, 70, 68, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 
                                            24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 
                                            50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]]
        root_scan_df.drop(['Plot', 'Season', 'Year'], axis = 1, inplace = True)
        root_scan_df.to_sql('Root_Scan_Data', self.conn, if_exists='append', index=False)
        self.conn.commit()
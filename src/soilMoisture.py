import sqlite3
import pandas as pd

class soilMoisture:

    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()

    def addSoilMoisture(self, filename):
        soil_m_df = pd.read_excel(filename)
        soil_m_df.drop(['BP', 
                     'Seeding',
                     'Fert. Treatment',
                     'Till. Treatment',
                     'Soil Tin Number',
                     'Grass Dry Weight (g)',
                     'Non-Grass Dry Weight (g)',
                     'Other Dry Weight (g)',
                     'Litter Dry Weight (g)',
                     'Root Dry Weight (g)'], axis = 1, inplace = True)
        wet_lst = list(soil_m_df['Soil Wet Weight (g)'])
        wet_lst_corrected = []
        dry_lst = list(soil_m_df['Soil Dry Weight (g)'])
        dry_lst_corrected = []
        for wet_entry in wet_lst:
            if str(wet_entry) == '.':
                wet_lst_c = float('nan')
                wet_lst_corrected.append(wet_lst_c)
            else:
                wet_lst_corrected.append(wet_entry)
        for dry_entry in dry_lst:
            if str(dry_entry) == '.':
                dry_lst_c = float('nan')
                dry_lst_corrected.append(dry_lst_c)
            else:
                dry_lst_corrected.append(dry_entry)
        soil_m_df['Soil Wet Weight (g)'] = wet_lst_corrected
        soil_m_df['Soil Dry Weight (g)'] = dry_lst_corrected
        plots_query = '''SELECT * FROM Plots'''
        treatments_query = '''SELECT * FROM Treatments'''
        sample_date_query = '''SELECT * FROM Sampling_Dates'''
        seasons_query = '''SELECT * FROM Season'''
        plots_results = self.cur.execute(plots_query).fetchall()
        plots_df = pd.DataFrame(plots_results, columns=[description[0] for description in self.cur.description])
        Plots_ids = []
        Treatments_ids = []
        Sample_Date_ids = []
        Seasons_ids = []
        sm_lst = []
        for record in soil_m_df.index:
            for ind in range(len(plots_df)):
                if soil_m_df.iloc[record]['Block #'] == plots_df.iloc[ind]['Block'] and soil_m_df.iloc[record]['Plot #'] == plots_df.iloc[ind]['Plot']:
                    #print('Success! Block: ' + str(soil_m_df.iloc[record]['Block #']) + ' and Plot: ' + str(soil_m_df.iloc[record]['Plot #']) + ' Found!' + 
                            #'Plot_id = ' + str(plots_df.iloc[ind]['id']))
                    plot_id = plots_df.iloc[ind]['id'] 
                    Plots_ids.append(plot_id)
        soil_m_df['Plots_id'] = Plots_ids
        treatments_results = self.cur.execute(treatments_query).fetchall()
        treatments_df = pd.DataFrame(treatments_results, columns=[description[0] for description in self.cur.description])
        for x in soil_m_df.index:
            for y in range(len(treatments_df)):
                if soil_m_df.iloc[x]['Plots_id'] == treatments_df.iloc[y]['Plots_id']:
                    treatment_id = treatments_df.iloc[y]['id']
                    Treatments_ids.append(treatment_id)
                    #print('index = ' + str(soil_m_df.index.get_loc(x)) + ', Plots_id = ' + str(soil_m_df.iloc[x]['Plots_id']) + ' treatment_id = ' + str(treatment_id))
        soil_m_df['Treatments_id'] = Treatments_ids
        sample_date_results = self.cur.execute(sample_date_query).fetchall()
        sample_date_df = pd.DataFrame(sample_date_results, columns =[description[0] for description in self.cur.description])
        for d in range(len(sample_date_df)):
            if str(soil_m_df.iloc[d]['Sample Date']) == str(sample_date_df.iloc[d]['Sample_Date']):
                sample_date_id = sample_date_df.iloc[d]['id']
                    #sample_date = sample_date_df.iloc[d]['Sample_Date']
                    #print('index = ' + str(soil_m_df.index.get_loc(d)) + ', Sample_date = ' + str(soil_m_df.iloc[d]['Sample Date']) + ' Sample_Date = ' + str(sample_date))
                Sample_Date_ids.append(sample_date_id)
        soil_m_df['Sample_Date_id'] = Sample_Date_ids
        seasons_results = self.cur.execute(seasons_query).fetchall()
        seasons_df = pd.DataFrame(seasons_results, columns = [description[0] for description in self.cur.description])
        for i in soil_m_df.index:
            for s in range(len(seasons_df)):
                if soil_m_df.iloc[i]['Year/Season Mix'] == (str(seasons_df.iloc[s]['Year']) + ' ' + str(seasons_df.iloc[s]['Season'])):
                    season_id = seasons_df.iloc[s]['id']
                    Seasons_ids.append(season_id)
        soil_m_df['Season_id'] = Seasons_ids
        for sm in soil_m_df.index:
            if soil_m_df.iloc[sm]['Soil Wet Weight (g)'] == float('nan'):
                sm_lst.append(float('nan'))
            else:
                sm_lst.append(((soil_m_df.iloc[sm]['Soil Wet Weight (g)'] - soil_m_df.iloc[sm]['Soil Dry Weight (g)']) / soil_m_df.iloc[sm]['Soil Dry Weight (g)']) * 100)
        soil_m_df['Soil_Moisture'] = sm_lst
        for data_id in soil_m_df.index:
            plot_id = int(soil_m_df.iloc[data_id]['Plots_id'])
            treat_id = int(soil_m_df.iloc[data_id]['Treatments_id'])
            smpl_date_id = int(soil_m_df.iloc[data_id]['Sample_Date_id'])
            ssn_id = int(soil_m_df.iloc[data_id]['Season_id'])
            wet_s = float(soil_m_df.iloc[data_id]['Soil Wet Weight (g)'])
            wet_d = float(soil_m_df.iloc[data_id]['Soil Dry Weight (g)'])
            soil_m = float(soil_m_df.iloc[data_id]['Soil_Moisture'])
            self.cur.execute('''INSERT INTO Soil_Moisture (
                        Plots_id,
                        Treatments_id,
                        Sample_Date_id,
                        Season_id,
                        Soil_Wet_Weight_g,
                        Soil_Dry_Weight_g,
                        Soil_Moisture)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                        plot_id,
                        treat_id,
                        smpl_date_id,
                        ssn_id,
                        wet_s,
                        wet_d,
                        soil_m,)
                       )
        self.conn.commit()
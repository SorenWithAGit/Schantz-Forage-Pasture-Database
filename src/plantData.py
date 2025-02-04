import sqlite3
import pandas as pd

class plantData:

    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
    
    def addData(self, filename):
        grass_df = pd.read_excel(filename)
        grass_df.drop(['BP', 
                        'Seeding',
                        'Fert. Treatment',
                        'Till. Treatment',
                        'Soil Tin Number',
                        'Soil Wet Weight (g)',
                        'Soil Dry Weight (g)'], axis = 1, inplace = True)
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
        for record in grass_df.index:
            for ind in range(len(plots_df)):
                if grass_df.iloc[record]['Block #'] == plots_df.iloc[ind]['Block'] and grass_df.iloc[record]['Plot #'] == plots_df.iloc[ind]['Plot']:
                    #print('Success! Block: ' + str(grass_df.iloc[record]['Block #']) + ' and Plot: ' + str(grass_df.iloc[record]['Plot #']) + ' Found!' + 
                            #'Plot_id = ' + str(plots_df.iloc[ind]['id']))
                    plot_id = plots_df.iloc[ind]['id'] 
                    Plots_ids.append(plot_id)
        grass_df['Plots_id'] = Plots_ids
        treatments_results = self.cur.execute(treatments_query).fetchall()
        treatments_df = pd.DataFrame(treatments_results, columns=[description[0] for description in self.cur.description])
        for x in grass_df.index:
            for y in range(len(treatments_df)):
                if grass_df.iloc[x]['Plots_id'] == treatments_df.iloc[y]['Plots_id']:
                    treatment_id = treatments_df.iloc[y]['id']
                    Treatments_ids.append(treatment_id)
                    #print('index = ' + str(grass_df.index.get_loc(x)) + ', Plots_id = ' + str(grass_df.iloc[x]['Plots_id']) + ' treatment_id = ' + str(treatment_id))
        grass_df['Treatments_id'] = Treatments_ids
        sample_date_results = self.cur.execute(sample_date_query).fetchall()
        sample_date_df = pd.DataFrame(sample_date_results, columns =[description[0] for description in self.cur.description])
        for d in range(len(sample_date_df)):
            if str(grass_df.iloc[d]['Sample Date']) == str(sample_date_df.iloc[d]['Sample_Date']):
                sample_date_id = sample_date_df.iloc[d]['id']
                sample_date = sample_date_df.iloc[d]['Sample_Date']
                #print('index = ' + str(grass_df.index.get_loc(d)) + ', Sample_date = ' + str(grass_df.iloc[d]['Sample Date']) + ' Sample_Date = ' + str(sample_date))
                Sample_Date_ids.append(sample_date_id)
        grass_df['Sample_Date_id'] = Sample_Date_ids
        seasons_results = self.cur.execute(seasons_query).fetchall()
        seasons_df = pd.DataFrame(seasons_results, columns = [description[0] for description in self.cur.description])
        for i in grass_df.index:
            for s in range(len(seasons_df)):
                if grass_df.iloc[i]['Year/Season Mix'] == (str(seasons_df.iloc[s]['Year']) + ' ' + str(seasons_df.iloc[s]['Season'])):
                    season_id = seasons_df.iloc[s]['id']
                    Seasons_ids.append(season_id)
        grass_df['Season_id'] = Seasons_ids
        gd_corrected = []
        ng_corrected = []
        od_corrected = []
        ld_corrected = []
        rd_corrected = []
        for iter in grass_df.index:
            if str(grass_df.iloc[iter]['Grass Dry Weight (g)']) == '.' and \
            str(grass_df.iloc[iter]['Non-Grass Dry Weight (g)']) == '.' and \
            str(grass_df.iloc[iter]['Other Dry Weight (g)']) == '.' and \
            str(grass_df.iloc[iter]['Litter Dry Weight (g)']) == '.' and \
            str(grass_df.iloc[iter]['Root Dry Weight (g)']) == '.':
                weight_var = float('nan')
                gd_corrected.append(weight_var)
                ng_corrected.append(weight_var)
                od_corrected.append(weight_var)
                ld_corrected.append(weight_var)
                rd_corrected.append(weight_var)
            else:
                gd_corrected.append(grass_df.iloc[iter]['Grass Dry Weight (g)'])
                ng_corrected.append(grass_df.iloc[iter]['Non-Grass Dry Weight (g)'])
                od_corrected.append(grass_df.iloc[iter]['Other Dry Weight (g)'])
                ld_corrected.append(grass_df.iloc[iter]['Litter Dry Weight (g)'])
                rd_corrected.append(grass_df.iloc[iter]['Root Dry Weight (g)'])
        grass_df['Grass Dry Weight (g)'] = gd_corrected
        grass_df['Non-Grass Dry Weight (g)'] = ng_corrected
        grass_df['Other Dry Weight (g)'] = od_corrected
        grass_df['Litter Dry Weight (g)'] = ld_corrected
        grass_df['Root Dry Weight (g)'] = rd_corrected
        for dat in grass_df.index:
            plts_id = int(grass_df.iloc[dat]['Plots_id'])
            treat_id = int(grass_df.iloc[dat]['Treatments_id'])
            smpl_id = int(grass_df.iloc[dat]['Sample_Date_id'])
            sesn_id = int(grass_df.iloc[dat]['Season_id'])
            grass_w = grass_df.iloc[dat]['Grass Dry Weight (g)']
            ngrass_w = grass_df.iloc[dat]['Non-Grass Dry Weight (g)']
            other_w = grass_df.iloc[dat]['Other Dry Weight (g)']
            litter_w = grass_df.iloc[dat]['Litter Dry Weight (g)']
            root_w = grass_df.iloc[dat]['Root Dry Weight (g)']
            self.cur.execute('''INSERT INTO Plant_Data (
                        Plots_id,
                        Treatments_id,
                        Sample_Date_id,
                        Season_id,
                        Grass_Dry_Weight_g,
                        Non_Grass_Dry_Weight_g,
                        Other_Dry_Weight_g,
                        Litter_Dry_Weight_g,
                        Root_Dry_Weight_g)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        plts_id,
                        treat_id,
                        smpl_id,
                        sesn_id,
                        grass_w,
                        ngrass_w,
                        other_w,
                        litter_w,
                        root_w,)
                       )
        self.conn.commit()
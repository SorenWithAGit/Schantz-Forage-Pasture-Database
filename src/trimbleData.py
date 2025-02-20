import sqlite3
import pandas as pd

class location:

    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()

    def addLocation(self):
        locations = ["Temple", "Riesel"]
        for loc in locations:
            self.cur.execute("""Insert INTO Location (
                                   Location)
                                   Values (?)""",(
                                       loc,)
                                    )
            self.conn.commit()


class plotCorners:
    
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
    
    def addPlotsAndCorners(self, filepath):
        corners_df = pd.read_csv(filepath)
        plots = []
        blocks = []
        plot_id = []
        location_ids = []
        str_check = str(corners_df.iloc[0,4])
        if str_check[0] == str("3"):
            for block_num in range(1, 7):
                for plt_num in range(1, 21):
                    plot = 100 * block_num + plt_num
                    plots.append(plot)
                    blocks.append(block_num)
                    location_ids.append(1)
            for i in range(1, 121):
                plot_id.append(i)
                plot_dic = {'Plot' : plots,
                            'Block' : blocks,
                            'Plot_id' : plot_id,
                            'Location_id' : location_ids}
        elif str_check[0] == str("7"):
            for block_num in range(1, 7):
                for plt_num in range(1, 21):
                    plot = 100 * block_num + plt_num
                    plots.append(plot)
                    blocks.append(block_num)
                    location_ids.append(2)
            for i in range(1, 121):
                plot_id.append(i)
        plot_dic = {'Plot' : plots,
                    'Block' : blocks,
                    'Plot_id' : plot_id,
                    'Location_id' : location_ids}
        plot_df = pd.DataFrame(data = plot_dic)
        ids = []
        loc_ids = []
        for record in corners_df.index:
            for entry_i in plot_df.index:
                if corners_df.iloc[record]['Plot'] == plot_df.iloc[entry_i]['Plot']:
                    id = plot_df.iloc[entry_i]['Plot_id']
                    ids.append(id)
            if str_check[0] == str("3"):
                loc_ids.append(1)
            elif str_check[0] == str("7"):
                loc_ids.append(2)
        corners_df['Plot_id'] = ids
        corners_df['Location_id'] = loc_ids
        corners_df.drop(labels = ['Plot'], axis = 1, inplace = True)
        plot_df.drop(labels = ['Plot_id'], axis = 1, inplace = True)
        corners_df = corners_df.iloc[:, [7, 8, 0, 1, 2, 3, 4, 5, 6]]
        plot_df['Plot_only'] = (plot_df['Plot'] - (100 * plot_df['Block']))
        for x in range(len(plot_df)):
            plt_num = int(plot_df.iloc[x]['Plot'])
            blck = int(plot_df.iloc[x]['Block'])
            plot = int(plot_df.iloc[x]['Plot_only'])
            loc_id = int(plot_df.iloc[x]['Location_id'])
            self.cur.execute('''INSERT INTO Plots (
                        Plot_Number,
                        Location_id,
                        Block,
                        Plot)
                        VALUES (?, ?, ?, ?)''', (
                        plt_num,
                        loc_id,
                        blck,
                        plot,)
                        )
        for y in range(len(corners_df)):
            plt_id = int(corners_df.iloc[y]['Plot_id'])
            name = str(corners_df.iloc[y]['Name'])
            code = corners_df.iloc[y]['Code']
            lati = corners_df.iloc[y]['Latitude']
            long = corners_df.iloc[y]['Longitude']
            nort = corners_df.iloc[y]['Northing']
            east = corners_df.iloc[y]['Easting']
            elev = corners_df.iloc[y]['Elevation']
            loc = int(corners_df.iloc[y]['Location_id'])
            self.cur.execute('''INSERT INTO Plot_Corners (
                        Plot_id,
                        Location_id,
                        Name,
                        Code,
                        Latitude,
                        Longitude,
                        Northing,
                        Easting,
                        Elevation)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        plt_id,
                        loc,
                        name,
                        code,
                        lati,
                        long,
                        nort,
                        east,
                        elev,)
                        )   
        self.conn.commit()


class samplingPoints:

    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()


    def addSamplingPoints(self, csv):
        sampling_points_df = pd.read_csv(csv)
        sample_dates = []
        plots = []
        for record in sampling_points_df.index:
            point_seperated = str(sampling_points_df.iloc[record]['point_ID']).split('_')
            sample_date = point_seperated[0]
            sample_dates.append(sample_date)
            plot = point_seperated[1].replace('-', '')
            plots.append(plot)
        sampling_points_df['Sample_Date'] = sample_dates
        sampling_points_df['Plot'] = plots
        sampling_points_df = sampling_points_df.iloc[:, [7, 6, 0, 1, 2, 3, 4, 5]]
        sampling_points_df.drop(['point_ID'], axis = 1, inplace = True)
        sampling_points_df['Sample_Date'] = pd.to_datetime(sampling_points_df['Sample_Date'])
        plots_query = '''SELECT * FROM Plots'''
        treatments_query = '''SELECT * FROM Treatments'''
        sample_date_query = '''SELECT * FROM Sampling_Dates'''
        plots_results = self.cur.execute(plots_query).fetchall()
        plots_df = pd.DataFrame(plots_results, columns=[description[0] for description in self.cur.description])


        location_ids = []
        plots_ids = []
        Treatments_ids = []
        Sample_Date_ids = []
        Season_ids = []
        
        for r in sampling_points_df.index:
            if str(sampling_points_df.iloc[r]["easting"])[0] == '6':
                location_ids.append(1)
            elif str(sampling_points_df.iloc[r]["easting"])[0] == '7':
                location_ids.append(2)
        sampling_points_df["Location_id"] = location_ids

        for record in sampling_points_df.index:
            for ind in range(len(plots_df)):
                if sampling_points_df.iloc[record]["Location_id"] == plots_df.iloc[ind]["Location_id"] and int(sampling_points_df.iloc[record]['Plot']) == int(plots_df.iloc[ind]['Plot_Number']):
                    plot_id = plots_df.iloc[ind]['id'] 
                    plots_ids.append(plot_id)
        sampling_points_df['Plots_id'] = plots_ids


        sample_date_results = self.cur.execute(sample_date_query).fetchall()
        sample_date_df = pd.DataFrame(sample_date_results, columns =[description[0] for description in self.cur.description])
        for date in sampling_points_df['Sample_Date'].index:
            for dte in sample_date_df.index:
                if sampling_points_df.iloc[date]["Location_id"] == sample_date_df.iloc[dte]["Location_id"] and int(sampling_points_df.iloc[date]['Plots_id']) == int(sample_date_df.iloc[dte]['Plots_id']) and str(sampling_points_df.iloc[date]['Sample_Date']).replace(" 00:00:00", "") == str(sample_date_df.iloc[dte]['Sample_Date']):
                    sample_date_id = sample_date_df.iloc[dte]['id']
                    Sample_Date_ids.append(sample_date_id)
                    season_id = sample_date_df.iloc[dte]['Season_id']
                    Season_ids.append(season_id)
                elif sampling_points_df.iloc[date]["Location_id"] == sample_date_df.iloc[dte]["Location_id"] and int(sampling_points_df.iloc[date]['Plots_id']) == int(sample_date_df.iloc[dte]['Plots_id']) and str(sampling_points_df.iloc[date]['Sample_Date']) == "nan":
                    Sample_Date_ids.append("nan")
        sampling_points_df['Sample_Date_id'] = Sample_Date_ids
        sampling_points_df['Season_id'] = Season_ids


        treatments_results = self.cur.execute(treatments_query).fetchall()
        treatments_df = pd.DataFrame(treatments_results, columns=[description[0] for description in self.cur.description])
        for x in sampling_points_df.index:
            for y in range(len(treatments_df)):
                if sampling_points_df.iloc[x]['Plots_id'] == treatments_df.iloc[y]['Plots_id'] and sampling_points_df.iloc[x]["Location_id"] == treatments_df.iloc[y]["Location_id"] and sampling_points_df.iloc[x]['Season_id'] == treatments_df.iloc[y]['Season_id']:
                    treatment_id = treatments_df.iloc[y]['id']
                    Treatments_ids.append(treatment_id)
        sampling_points_df['Treatments_id'] = Treatments_ids


        for entry in sampling_points_df.index:
            plot_id = int(sampling_points_df.iloc[entry]['Plots_id'])
            location_id = int(sampling_points_df.iloc[entry]["Location_id"])
            seas_id = int(sampling_points_df.iloc[entry]['Season_id'])
            treat_id = int(sampling_points_df.iloc[entry]['Treatments_id'])
            smpl_id = int(sampling_points_df.iloc[entry]['Sample_Date_id'])
            lat = float(sampling_points_df.iloc[entry]['latitude'])
            lon = float(sampling_points_df.iloc[entry]['longitude'])
            north = float(sampling_points_df.iloc[entry]['northing'])
            east = float(sampling_points_df.iloc[entry]['easting'])
            elev = float(sampling_points_df.iloc[entry]['elevation'])
            self.cur.execute('''INSERT INTO Sampling_Points (
                        Plots_id,
                        Location_id,
                        Season_id,
                        Treatments_id,
                        Sample_Date_id,
                        latitude,
                        longitude,
                        northing,
                        easting,
                        elevation)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        plot_id,
                        location_id,
                        seas_id,
                        treat_id,
                        smpl_id,
                        lat,
                        lon,
                        north,
                        east,
                        elev,)
                       )
        self.conn.commit()

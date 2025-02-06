import sqlite3

class createDatabase:
    
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
        self.cur.executescript('''
            CREATE TABLE Location (
            id integer PRIMARY KEY,
            Location TEXT,
            CONSTRAINT Location UNIQUE (Location) );

            CREATE TABLE Plots (
            id INTEGER PRIMARY KEY,
            Location_id INTEGER REFERENCES Location (id),
            Plot_Number INTEGER,
            Block INTEGER,
            Plot INTEGER );

            Create Table Plot_Corners (
            id INTEGER PRIMARY KEY,
            Plot_id INTEGER REFERENCES Plots (id),
            Location_id INTEGER REFERENCES Location (id),
            Name INTEGER,
            Code TEXT,
            Latitude FLOAT,
            Longitude FLOAT,
            Northing FLOAT,
            Easting FLOAT,
            Elevation FLOAT );
            
            CREATE TABLE Season (
            id INTEGER PRIMARY KEY,
            Year INTEGER, 
            Season TEXT,
            [Year/Season Mix] TEXT,
            CONSTRAINT Year_Season UNIQUE (Year,Season) );

            CREATE TABLE Treatments (
            id INTEGER PRIMARY KEY,
            Plots_id INTEGER REFERENCES Plots (id),
            Location_id INTEGER REFERENCES Location (id),
            Seeding TEXT,
            Fertilizer_Treatment TEXT,
            Tillage_Treatment TEXT );

            CREATE TABLE Sampling_Dates (
            id INTEGER PRIMARY KEY,
            Plots_id INTEGER REFERENCES Plots (id),
            Location_id INTEGER REFERENCES Location (id),
            Treatments_id INTEGER REFERENCES Treatments (id),
            Season_id INTEGER REFERENCES Season (id),
            Sample_Date TEXT,
            CONSTRAINT Date UNIQUE (Sample_Date) );
        
            CREATE TABLE Sampling_Points (
            id INTEGER PRIMARY KEY,
            Plots_id INTEGER REFERENCES Plots (id),
            Location_id INTEGER REFERENCES Location (id),
            Treatments_id INTEGER REFERENCES Treatments (id),
            Sample_Date_id INTEGER REFERENCES Sample_date (id),
            latitude FLOAT,
            longitude FLOAT,
            northing FLOAT,
            easting FLOAT,
            elevation FLOAT );

            CREATE TABLE Soil_Moisture (
            id INTEGER PRIMARY KEY,
            Plots_id INTEGER REFERENCES Plots (id),
            Location_id INTEGER REFERENCES Location (id),
            Treatments_id INTEGER REFERENCES Treatments (id),
            Sample_Date_id INTGER REFERENCES Sample_Date (id),
            Season_id INTEGER REFERENCES Season (id),
            Soil_Wet_Weight_g FLOAT,
            Soil_Dry_Weight_g FLOAT,
            Soil_Moisture FLOAT );

            CREATE TABLE Plant_Data (
            id INTEGER PRIMARY KEY,
            Plots_id INTEGER REFERENCES Plots (id),
            Location_id INTEGER REFERENCES Location (id),
            Treatments_id INTEGER REFERENCES Treatments (id),
            Sample_Date_id INTGER REFERENCES Sample_Date (id),
            Season_id INTEGER REFERENCES Season (id),
            Grass_Dry_Weight_g FLOAT,
            Non_Grass_Dry_Weight_g FLOAT,
            Other_Dry_Weight_g FLOAT,
            Litter_Dry_Weight_g FLOAT,
            Root_Dry_Weight_g FLOAT );

            CREATE TABLE Root_Scan_Samples (
            id INTEGER PRIMARY KEY,
            Plots_id INTEGER REFERENCES Plots (id),
            Location_id INTEGER REFERENCES Location (id),
            Treatments_id INTEGER REFERENCES Treatments (id),
            Sample_Date_id INTEGER REFERENCES Sample_Date (id),
            Season_id INTEGER REFERENCES Season (id),
            Sample_Name TEXT );

            CREATE TABLE Root_Scan_Data (
            id INTEGER PRIMARY KEY,
            Root_Scan_Samples_id INTEGER REFERENCES Root_Scan_Samples (id),
            Plots_id INTEGER REFERENCES Plots (id),
            Location_id INTEGER REFERENCES Location (id),
            Treatments_id INTEGER REFERENCES Treatments (id),
            Sample_Date_id INTEGER REFERENCES Sample_Date (id),
            Season_id INTEGER REFERENCES Season (id),
            [Length(cm)] FLOAT,
            [ProjArea(cm2)] FLOAT,
            [SurfArea(cm2)] FLOAT,
            [AvgDiam(mm)] FLOAT,
            [LenPerVol(cm/m3)] FLOAT,
            [RootVolume(cm3)] FLOAT,
            [Tips] INTEGER,
            [Forks] INTEGER,
            [Crossings] INTEGER,
            [LenTotHistoClasses] FLOAT,
            [0<.L.<=0.5] FLOAT,
            [0.5<.L.<=1.0] FLOAT,
            [1.0<.L.<=1.5] FLOAT,
            [1.5<.L.<=2.0] FLOAT,
            [2.0<.L.<=2.5] FLOAT,
            [2.5<.L.<=3.0] FLAOT,
            [3.0<.L.<=3.5] FLOAT,
            [3.5<.L.<=4.0] FLOAT,
            [4.0<.L.<=4.5] FLOAT,
            [.L.>4.5] FLOAT,
            [SATotHistoClasses] FLOAT,
            [0<.SA.<=0.5] FLOAT,
            [0.5<.SA.<=1.0] FLOAT,
            [1.0<.SA.<=1.5] FLOAT,
            [1.5<.SA.<=2.0] FLOAT,
            [2.0<.SA.<=2.5] FLOAT,
            [2.5<.SA.<=3.0] FLOAT,
            [3.0<.SA.<=3.5] FLOAT,
            [3.5<.SA.<=4.0] FLOAT,
            [4.0<.SA.<=4.5] FLOAT,
            [.SA.>4.5] FLOAT,
            [PATotHistoClasses] FLOAT,
            [0<.PA.<=0.5] FLOAT,
            [0.5<.PA.<=1.0] FLOAT,
            [1.0<.PA.<=1.5] FLOAT,
            [1.5<.PA.<=2.0] FLOAT,
            [2.0<.PA.<=2.5] FLOAT,
            [2.5<.PA.<=3.0] FLOAT,
            [3.0<.PA.<=3.5] FLOAT,
            [3.5<.PA.<=4.0] FLOAT,
            [4.0<.PA.<=4.5] FLOAT,
            [.PA.>4.5] FLOAT,
            [VolTotHistoClasses] FLOAT,
            [0<.V.<=0.5] FLOAT,
            [0.5<.V.<=1.0] FLOAT,
            [1.0<.V.<=1.5] FLOAT,
            [1.5<.V.<=2.0] FLOAT,
            [2.0<.V.<=2.5] FLOAT,
            [2.5<.V.<=3.0] FLOAT,
            [3.0<.V.<=3.5] FLOAT,
            [3.5<.V.<=4.0] FLOAT,
            [4.0<.V.<=4.5] FLOAT,
            [.V.>4.5] FLOAT,
            [0<.T.<=0.5] FLOAT,
            [0.5<.T.<=1.0] FLOAT,
            [1.0<.T.<=1.5] FLOAT,
            [1.5<.T.<=2.0] FLOAT,
            [2.0<.T.<=2.5] FLOAT,
            [2.5<.T.<=3.0] FLOAT,
            [3.0<.T.<=3.5] FLOAT,
            [3.5<.T.<=4.0] FLOAT,
            [4.0<.T.<=4.5] FLOAT,
            [.T.>4.5] FLOAT);
            ''')
        self.conn.commit()

    def clear_tables(self):
        self.cur.executescript("""
            DROP TABLE IF EXISTS Plots;
            DROP TABLE IF EXISTS Plot_Corners;
            DROP TABLE IF EXISTS Season;
            DROP TABLE IF EXISTS Treatments;
            DROP TABLE IF EXISTS Sampling_Dates;
            DROP TABLE IF EXISTS Sampling_Points;
            DROP TABLE IF EXISTS Soil_Moisture;
            DROP TABLE IF EXISTS Plant_Data;
            DROP TABLE IF EXISTS Root_Scan_Samples;
            DROP TABLE IF EXISTS Root_Scan_Data;
            """)
        self.conn.commit()
    


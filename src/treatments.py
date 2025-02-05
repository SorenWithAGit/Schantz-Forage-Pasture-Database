import sqlite3
import pandas as pd

class treatments:

    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

    def addTreatments(self, filename):
        treatment_df = pd.read_csv(filename)
        for record in treatment_df.index:
            plot_id = int(treatment_df.iloc[record]['Plots_id'])
            loc_id = int(treatment_df.iloc[record]['Location_id'])
            seeding = treatment_df.iloc[record]['Seeding']
            fert = treatment_df.iloc[record]['Fert. Treatment']
            till = treatment_df.iloc[record]['Till. Treatment']
            self.cur.execute('''INSERT INTO Treatments (
                        Plots_id,
                        Location_id,
                        Seeding,
                        Fertilizer_Treatment,
                        Tillage_Treatment)
                        VALUES (?, ?, ?, ?, ?)''', (
                        plot_id,
                        loc_id,
                        seeding,
                        fert,
                        till,)
                       )
            self.conn.commit()
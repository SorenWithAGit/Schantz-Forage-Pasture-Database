import sqlite3
import pandas as pd

class seasons():

    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()

    def addSeasons(self, filename):
        df = pd.read_excel(filename, sheet_name = "Data Sheet")
        year_season = df['Year/Season Mix'].unique().tolist()
        for entry in year_season:
            year = entry.split(' ')[0]
            season = entry.split(' ')[1]
            yearSeason = entry
            self.cur.execute('''INSERT INTO Season (
                        Year,
                        Season,
                        [Year/Season Mix])
                        VALUES (?, ?, ?)''', (
                        year,
                        season,
                        yearSeason,)
                       )
            self.conn.commit()
        
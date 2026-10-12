import sqlite3
DB_NAME = "countries.db"

class CountryDatabaseManger:
    def __init__(self, db_name= "countries.db"):
        self.db_name = db_name
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS countries (
                    country_name TEXT PRIMARY KEY,
                    capital TEXT NOT NULL,
                    population INTEGER NOT NULL,
                    area REAL NOT NULL
                )
            """)
    def create(self,country):
        with self.connect() as conn:
            conn.execute("""
                INSERT INTO countries (country_name, capital, population, area)
                VALUES (?, ?, ?, ?)
            """, (country['country_name'], country['capital'], country['population'], country['area']))

    def get_all(self):
        with self.connect() as conn:
            rows = conn.execute("""
                SELECT country_name, capital, population, area FROM countries
            """).fetchall()

            return[
                {
                    'country_name': row[0],
                    'capital': row[1],
                    'population': row[2],
                    'area': row[3]
                } for row in rows
            ]
    def get_by_name(self, country_name):
        with self.connect() as conn:
            row = conn.execute("""
                SELECT country_name, capital, population, area FROM countries
                WHERE country_name = ?
            """, (country_name,)).fetchone()

            if row is None:
                return None
            return {
                'country_name': row[0],
                'capital': row[1],
                'population': row[2],
                'area': row[3]
            }
    def update(self, country_name, country):
        with self.connect() as conn:
            cursor = conn.execute("""
                UPDATE countries
                SET country_name = ?, capital = ?, population = ?, area = ?
                WHERE country_name = ?
            """, (
                country['country_name'],
                country['capital'],
                country['population'],
                country['area'],
                country_name
            ))
            return cursor.rowcount >0
        

    def delete(self, country_name):
        with self.connect() as conn:
            cursor = conn.execute("""
                DELETE FROM countries
                WHERE country_name = ?
            """, (country_name,))
            return cursor.rowcount > 0

    def insert_many(self, countries):
        with self.connect() as conn:
            cursor = conn.executemany("""
                INSERT INTO countries (country_name, capital, population, area)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(country_name) DO UPDATE SET
                    capital = excluded.capital,
                    population = excluded.population,
                    area = excluded.area
            """, [(country['country_name'], country['capital'], country['population'], country['area'])
                   for country in countries])

if __name__ == "__main__":
    from scraper import scrape_countries

    db = CountryDatabaseManger()
    countries = scrape_countries()
    db.insert_many(countries)

    print("Countries saved:", len(db.get_all()))
    print("First record:", db.get_all()[0])



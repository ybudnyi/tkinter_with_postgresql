""" Create three tables in PostgreSQL database polish.
    Create database and give it name in code bellow,
    withe username and password for PostgreDB"""

import psycopg2
import sys


class DataBase:
    # Create tables if not exist when initialize object. You must have "polish" database created
    # or change db name in code.
    def __init__(self):
        self.connect = psycopg2.connect("dbname= 'polish' user= 'postgres' password= 3337")
        self.cur = self.connect.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS polish_color 
        (id_col serial PRIMARY KEY, 
        color_name varchar NOT null)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS polish_producer 
        (id_prod serial PRIMARY KEY, 
        producer_name varchar NOT null, 
        producer_website varchar)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS polish_name 
        (id_pol serial primary key, 
        pol_name varchar NOT NULL, 
        color_id integer NOT NULL, 
        producer_id integer NOT NULL, 
        FOREIGN KEY (color_id) REFERENCES polish_color(id_col), 
        FOREIGN KEY (producer_id) REFERENCES polish_producer(id_prod))''')
        self.connect.commit()

    # Insert new data to db from gui
    def insert_data(self, name, color, producer, website=None):
        self.cur.execute(f"select color_name from polish_color where color_name='{color}'")
        x = self.cur.fetchall()
        if len(x) == 0:
            # y = x[0]
            # print(y)
            # if color not in y:
            self.cur.execute(f"INSERT INTO polish_color (color_name) VALUES ('{color}')")
            print('add color')
        self.cur.execute(f"select producer_name from polish_producer where producer_name='{producer}'")
        x2 = self.cur.fetchall()
        if len(x2) == 0:
            self.cur.execute(
                f"INSERT INTO polish_producer (producer_name, producer_website) VALUES ('{producer}', '{website}')")
            print('add producer')
        self.cur.execute(
            f"INSERT INTO polish_name (pol_name, color_id, producer_id) VALUES ('{name}', (select  id_col from "
            f"polish_color where color_name='{color}'), (select id_prod from polish_producer where producer_name='"
            f"{producer}'));")
        self.connect.commit()

    # View all entry's from table polish_name, joined with data from two others tables
    def view_all(self):
        self.cur.execute('''SELECT polish_name.id_pol, polish_name.pol_name, polish_color.color_name, 
        polish_producer.producer_name, polish_producer.producer_website FROM ((polish_name INNER JOIN polish_color ON 
        polish_name.color_id = polish_color.id_col) INNER JOIN polish_producer ON polish_name.producer_id = 
        polish_producer.id_prod) ORDER BY pol_name;''')
        al = self.cur.fetchall()
        self.connect.commit()
        return al

    # Search data with three given entry's, or only with one. Two entrys wouldn't give result
    def search_data(self, name=None, color=None, producer=None):
        if name and color and producer:
            self.cur.execute(f'''select polish_name.pol_name, polish_color.color_name, polish_producer.producer_name
    from ((polish_name
    INNER JOIN polish_color ON polish_name.color_id = polish_color.id_col)
    INNER JOIN polish_producer ON polish_name.producer_id = polish_producer.id_prod)
    WHERE (polish_name.pol_name='{name}')
    and color_id=(select polish_color.id_col where polish_color.color_name='{color}')
    and producer_id=(select polish_producer.id_prod where polish_producer.producer_name='{producer}');
    ''')
        elif name:
            self.cur.execute(f'''select polish_name.pol_name, polish_color.color_name, polish_producer.producer_name
    from ((polish_name
    INNER JOIN polish_color ON polish_name.color_id = polish_color.id_col)
    INNER JOIN polish_producer ON polish_name.producer_id = polish_producer.id_prod)
    WHERE (polish_name.pol_name='{name}');
            ''')
        elif color:
            self.cur.execute(f'''SELECT polish_name.pol_name, polish_color.color_name, polish_producer.producer_name
    FROM polish_name, polish_color, polish_producer
    WHERE color_id=(select polish_color.id_col where polish_color.color_name='{color}') and
    polish_name.producer_id=polish_producer.id_prod;
    ''')
        elif producer:
            self.cur.execute(f'''SELECT polish_name.pol_name, polish_color.color_name, polish_producer.producer_name, 
            polish_producer.producer_website FROM polish_name, polish_color, polish_producer WHERE producer_id=(
            select polish_producer.id_prod where polish_producer.producer_name='{producer}') and 
    polish_name.color_id=polish_color.id_col;
    ''')
        else:
            "'No matches found'"
        search_result = self.cur.fetchall()
        return search_result

    # print(search_data(name=None, color="'red'", producer=None))
    # Delete selected field and returns empty window. Need to refresh table to see result.
    def delete_data(self, id_for_row):
        self.cur.execute(f'delete from polish_name where id_pol ={id_for_row}')
        self.connect.commit()

    # Update data. Change data in entry window.
    def update_data(self, id_for_row, name, color, producer, website=None):
        self.cur.execute(f"UPDATE polish_name SET pol_name='{name}' WHERE id_pol={id_for_row}")
        self.cur.execute(
            f"update polish_color set color_name='{color}' where id_col=(select color_id from "
            f"polish_name where id_pol={id_for_row})")
        self.cur.execute(
            f"update polish_producer set producer_name='{producer}' where id_prod=(select producer_id from "
            f"polish_name where id_pol={id_for_row})")
        if website is not None:
            self.cur.execute(
                f"update polish_producer set producer_website='{website}' where id_prod=(select producer_id from "
                f"polish_name where id_pol={id_for_row})")
        self.connect.commit()

    # Close connection to db and close the app.
    def close(self):
        self.connect.close()
        sys.exit()

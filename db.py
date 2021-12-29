import psycopg2
import sys


def connect_table():
    connect = psycopg2.connect("dbname= 'polish' user= 'postgres' password= 3337")
    cur = connect.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS polish_color 
    (id_col serial PRIMARY KEY, 
    color_name varchar NOT null)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS polish_producer 
    (id_prod serial PRIMARY KEY, 
    producer_name varchar NOT null, 
    producer_website varchar)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS polish_name 
    (id_pol serial primary key, 
    pol_name varchar NOT NULL, 
    color_id integer NOT NULL, 
    producer_id integer NOT NULL, 
    FOREIGN KEY (color_id) REFERENCES polish_color(id_col), 
    FOREIGN KEY (producer_id) REFERENCES polish_producer(id_prod))''')
    connect.commit()
    connect.close()

# connect_table()


def insert_data(name, color, producer, website=None):
    # name = name
    # color = color
    # producer = producer
    connect = psycopg2.connect("dbname= 'polish' user= 'postgres' password= 3337")
    cur = connect.cursor()
    cur.execute(f"select color_name from polish_color where color_name='{color}'")
    x = cur.fetchall()
    if len(x) == 0:
        # y = x[0]
        # print(y)
        # if color not in y:
        cur.execute(f"INSERT INTO polish_color (color_name) VALUES ('{color}')")
        print('add color')
    cur.execute(f"select producer_name from polish_producer where producer_name='{producer}'")
    x2 = cur.fetchall()
    if len(x2) == 0:
        cur.execute(f"INSERT INTO polish_producer (producer_name, producer_website) VALUES ('{producer}', '{website}')")
        print('add producer')
    cur.execute(
      f"INSERT INTO polish_name (pol_name, color_id, producer_id) VALUES ('{name}', (select  id_col from polish_color where color_name='{color}'), (select id_prod from polish_producer where producer_name='{producer}'));")
    connect.commit()
    connect.close()

insert_data("nork","gold","man")

def view_all():
    connect = psycopg2.connect("dbname= 'polish' user= 'postgres' password= 3337")
    cur = connect.cursor()
    cur.execute('''SELECT polish_name.id_pol, polish_name.pol_name, polish_color.color_name, polish_producer.producer_name, polish_producer.producer_website
    FROM ((polish_name
    INNER JOIN polish_color ON polish_name.color_id = polish_color.id_col)
    INNER JOIN polish_producer ON polish_name.producer_id = polish_producer.id_prod)
    ORDER BY pol_name;''')
    al = cur.fetchall()
    connect.commit()
    connect.close()
    return al
#
# print(view_all())

def search_data(name=None, color=None, producer=None):
    connect = psycopg2.connect("dbname= 'polish' user= 'postgres' password= 3337")
    cur = connect.cursor()
    if name and color and producer:
        cur.execute(f'''select polish_name.pol_name, polish_color.color_name, polish_producer.producer_name
from ((polish_name
INNER JOIN polish_color ON polish_name.color_id = polish_color.id_col)
INNER JOIN polish_producer ON polish_name.producer_id = polish_producer.id_prod)
WHERE (polish_name.pol_name='{name}')
and color_id=(select polish_color.id_col where polish_color.color_name='{color}')
and producer_id=(select polish_producer.id_prod where polish_producer.producer_name='{producer}');
''')
    elif name:
        cur.execute(f'''select polish_name.pol_name, polish_color.color_name, polish_producer.producer_name
from ((polish_name
INNER JOIN polish_color ON polish_name.color_id = polish_color.id_col)
INNER JOIN polish_producer ON polish_name.producer_id = polish_producer.id_prod)
WHERE (polish_name.pol_name='{name}');
        ''')
    elif color:
        cur.execute(f'''SELECT polish_name.pol_name, polish_color.color_name, polish_producer.producer_name
FROM polish_name, polish_color, polish_producer
WHERE color_id=(select polish_color.id_col where polish_color.color_name='{color}') and
polish_name.producer_id=polish_producer.id_prod;
''')
    elif producer:
        cur.execute(f'''SELECT polish_name.pol_name, polish_color.color_name, polish_producer.producer_name, polish_producer.producer_website
FROM polish_name, polish_color, polish_producer
WHERE producer_id=(select polish_producer.id_prod where polish_producer.producer_name='{producer}') and
polish_name.color_id=polish_color.id_col;
''')
    else:
        "'No matches found'"
    search_result = cur.fetchall()
    return search_result

# print(search_data(name=None, color="'red'", producer=None))

def delete_data(id):
    connect = psycopg2.connect("dbname= 'polish' user= 'postgres' password= 3337")
    cur = connect.cursor()
    cur.execute(f'delete from polish_name where id_pol ={id}')
    connect.commit()
    connect.close()

# delete_data(6)

def update_data(id, name, color, producer, website=None):
    connect = psycopg2.connect("dbname= 'polish' user= 'postgres' password= 3337")
    cur = connect.cursor()
    cur.execute(f"UPDATE polish_name SET pol_name='{name}' WHERE id_pol={id}")
    cur.execute(f"update polish_color set color_name='{color}' where id_col=(select color_id from polish_name where id_pol={id})")
    cur.execute(f"update polish_producer set producer_name='{producer}' where id_prod=(select producer_id from polish_name where id_pol={id})")
    if website != None:
        cur.execute(
            f"update polish_producer set producer_website='{website}' where id_prod=(select producer_id from polish_name where id_pol={id})")
    connect.commit()
    connect.close()

# update_data(7, "'Tomy'", "'redy'", "'lack'", "'www.google.com'")

def close():
    sys.exit()
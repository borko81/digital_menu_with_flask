from flask import Flask, render_template
import fdb
from base64 import b64encode
from collections import defaultdict

# ---------Hard code obj id ------------------
'''
TODO: add id to url, to generate menu from different id!
'''
OBJ_ID = 2

# ----------Flas configuration ---------------
app = Flask(__name__)

# ---------Database connector ----------------
con = fdb.connect(dsn=r'C:\Users\Borko\Desktop\noto\touchsale.FDB',
                  user='SYSDBA', password='masterkey')

# ----------------SQL Selector ---------------------------
RESTAURANT_NAME = f'''
    SELECT obj.name_cyr from obj where obj.id = {OBJ_ID}
'''

SELECT = f'''
select KITS.NAME_CYR, KINDS.NAME, MENU.CENA, KITS.IMAGE, KITS.INFO
from KITS
inner join MENU
inner join KINDS on KINDS.ID = KITS.KIND_ID on MENU.KIT_ID = KITS.ID
where MENU.OBJ_ID = {OBJ_ID}
order by 1
'''

# ----------------Get result from database ----------------


def get_obj_name():
    cur = con.cursor()
    cur.execute(RESTAURANT_NAME)
    return cur.fetchone()


def get_data_from_database():
    cur = con.cursor()
    cur.execute(SELECT)
    result = defaultdict(list)
    for line in cur.fetchall():
        try:
            image = b64encode(line[3]).decode("utf-8")
        except:
            image = ''
        result[line[1]].append([line[0], line[2], image, line[4]])
    return result


def show_data():
    result = dict(sorted(get_data_from_database().items()))
    return result
# ----------------------URL's--------------------------


@app.route('/')
def index():
    return "Choice group"


@ app.route('/all')
def all_menu():
    data = {
        'recepidata': show_data(),
        'rest_name': get_obj_name()
    }
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

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
con = fdb.connect(dsn=r'path',
                  user='username', password='password')

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

SELECT_FROM_KINDS_ID = '''
select KITS.NAME_CYR, KINDS.NAME, MENU.CENA, KITS.IMAGE, KITS.INFO
from KITS
inner join MENU
inner join KINDS on KINDS.ID = KITS.KIND_ID on MENU.KIT_ID = KITS.ID
where MENU.OBJ_ID = %d and kinds.id = %d
order by 1
'''


TAKE_KINDS = f'''
select
kinds.id, kinds.name
from kits
inner join kinds on kinds.id = kits.kind_id
inner join menu
on menu.kit_id = kits.id
where MENU.OBJ_ID = {OBJ_ID} and kits.kind_id is not null
order by 2
'''

# ----------------Get result from database ----------------


def get_obj_name():
    cur = con.cursor()
    cur.execute(RESTAURANT_NAME)
    return cur.fetchone()


def get_data_from_database(kinds=None):
    cur = con.cursor()
    if kinds is None:
        cur.execute(SELECT)
    else:
        cur.execute(SELECT_FROM_KINDS_ID % (OBJ_ID, kinds))
    result = defaultdict(list)
    for line in cur.fetchall():
        try:
            image = b64encode(line[3]).decode("utf-8")
        except:
            image = ''
        result[line[1]].append([line[0], line[2], image, line[4]])
    return result


def get_kinds_from_database():
    cur = con.cursor()
    cur.execute(TAKE_KINDS)
    result = {}
    for line in cur.fetchall():
        result[line[1]] = line[0]
    return dict(sorted(result.items()))


def show_data(kinds=None):
    result = dict(sorted(get_data_from_database(kinds=kinds).items()))
    return result
# ----------------------URL's--------------------------


@app.route('/')
def index():
    data = get_kinds_from_database()
    return render_template('index.html', data=data)


@app.route('/kinds/<int:id>')
def load_kinds(id):
    data = {
        'recepidata': show_data(kinds=id),
        'rest_name': get_obj_name()
    }
    return render_template('all_menu.html', data=data)


@ app.route('/all')
def all_menu():
    data = {
        'recepidata': show_data(),
        'rest_name': get_obj_name()
    }
    return render_template('all_menu.html', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

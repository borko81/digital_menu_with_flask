from flask import Flask, render_template
# from flask_compress import Compress
import fdb
from base64 import b64encode
from collections import defaultdict

from query.queryies import queryies

# ---------Hard code obj id ------------------
'''
TODO: add id to url, to generate menu from different id!
'''
OBJ_ID = 1

# ----------Flas configuration ---------------
app = Flask(__name__)

# COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
# COMPRESS_LEVEL = 6
# COMPRESS_MIN_SIZE = 500
# Compress(app)

# ---------Database connector ----------------


def con_to_database():
    ''' Use to create connection to database, close after session finished'''
    con = fdb.connect(dsn=r'flask', user='SYSDBA', password='masterkey')
    return con

# ----------------Get result from database ----------------


def get_obj_name():
    with con_to_database() as con:
        cur = con.cursor()
        cur.execute(queryies['RESTAURANT_NAME'] % (OBJ_ID,))
        return cur.fetchone()


def get_data_from_database(kinds=None):
    with con_to_database() as con:
        cur = con.cursor()
        if kinds is None:
            cur.execute(queryies['SELECT'] % (OBJ_ID))
        else:
            cur.execute(queryies['SELECT_FROM_KINDS_ID'] % (OBJ_ID, kinds))
        result = defaultdict(list)
        for line in cur.fetchall():
            try:
                image = b64encode(line[3]).decode("utf-8")
            except TypeError:
                image = ''
            result[line[1]].append([line[0], line[2], image, line[4], line[5]])
        print(result)
        return result


def get_kinds_from_database():
    with con_to_database() as con:
        cur = con.cursor()
        cur.execute(queryies['TAKE_KINDS'] % (OBJ_ID))
        result = {}
        for line in cur.fetchall():
            try:
                image = b64encode(line[2]).decode("utf-8")
            except TypeError:
                image = ''
            result[line[1]] = [line[0], image, line[3]]
        return dict(sorted(result.items()))


def show_data(kinds=None):
    result = dict(sorted(get_data_from_database(kinds=kinds).items()))
    return result
# ----------------------URL's--------------------------


@app.route('/', methods=['GET'])
def index():
    data = get_kinds_from_database()
    return render_template('index.html', data=data)


@app.route('/kinds/<int:id>', methods=['GET'])
def load_kinds(id):
    data = {
        'recepidata': show_data(kinds=id),
        'rest_name': get_obj_name()
    }
    return render_template('all_menu.html', data=data)


@ app.route('/all', methods=['GET'])
def all_menu():
    data = {
        'recepidata': show_data(),
        'rest_name': get_obj_name()
    }
    return render_template('all_menu.html', data=data)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=False, threaded=True)

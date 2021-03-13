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


def get_cur(query, *args):
    ''' Return cur with fetch data '''
    with con_to_database() as con:
        cur = con.cursor()
        cur.execute(queryies[query] % (*args, ))
        return cur.fetchall()


def get_obj_name(OBJ_ID):
    ''' 
        Here return obj name
        not use any, maybe later!
    '''
    return get_cur('RESTAURANT_NAME', OBJ_ID)


def get_data_from_database(kinds=None):
    '''
        If kinds is none, query not include kinds name, else include.
    '''
    result = defaultdict(list)

    if kinds is None:
        data = get_cur('SELECT', OBJ_ID)
    else:
        data = get_cur('SELECT_FROM_KINDS_ID', OBJ_ID, kinds)

    for line in data:
        try:
            # If image is none, cathc TypeError and continue with empty image
            image = b64encode(line[3]).decode("utf-8")
        except TypeError:
            image = ''
        result[line[1]].append([line[0], line[2], image, line[4], line[5]])
    return result


def get_kinds_from_database():
    ''' 
        Return kinds
    '''
    result = {}

    data = get_cur('TAKE_KINDS', OBJ_ID)
    for line in data:
        try:
            image = b64encode(line[2]).decode("utf-8")
        except TypeError:
            image = ''
        result[line[1]] = [line[0], image, line[3]]
    return dict(sorted(result.items()))


def show_data(kinds=None):
    '''
        Use to return sorted alpha (name kinds), recepi
        Duck typing
    '''
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
        'rest_name': get_obj_name(OBJ_ID)
    }
    return render_template('all_menu.html', data=data)


@app.route('/all', methods=['GET'])
def all_menu():
    data = {
        'recepidata': show_data(),
        'rest_name': get_obj_name(OBJ_ID)
    }
    return render_template('all_menu.html', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)

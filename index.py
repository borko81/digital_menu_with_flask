from flask import Flask, render_template
import fdb
from base64 import b64encode
from collections import defaultdict


app = Flask(__name__)


con = fdb.connect(dsn=r'path', user='username', password='password')

SELECT = '''
select KITS.NAME_CYR, KINDS.NAME, MENU.CENA, KITS.IMAGE, KITS.INFO
from KITS
inner join MENU
inner join KINDS on KINDS.ID = KITS.KIND_ID on MENU.KIT_ID = KITS.ID
where MENU.OBJ_ID = 2
order by 1
'''


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


@ app.route('/')
def index():
    data = show_data()
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)

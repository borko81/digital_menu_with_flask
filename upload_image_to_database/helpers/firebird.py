from decouple import config
import fdb


database = {
    "host": f"{config('host')}",
    "database": f"{config('dsn')}",
    "user": f"{config('user')}",
    "password": f"{config('password')}",
}

def con_to_database():
	"""Use to create connection to database, close after session finished"""
	# Change value with corect parameter
	# dsn: path to base, if use alias may remove r
	con = fdb.connect(**database)
	return con

def insert_cur(query, *args):
	"""Insert cur data to db"""
	with con_to_database() as con:
		cur = con.cursor()
		try:
			cur.execute(query, (*args,))
			con.commit()
		except fdb.Error as e:
			print("[-]", e)
		except Exception as e:
			print('[+] Error when save first image' + str(e))
		except fdb.DatabaseError as e:
			print(str(e))
		except fdb.DataError as e:
			print(str(e))
		except fdb.IntegrityError as e:
			print(str(e))

def get_simple_id_and_name_from_db(query, *args):
	# Get id and name from db
	with con_to_database() as con:
		cur = con.cursor()
		try:
			cur.execute(query, (*args,))
		except fdb.Error as e:
			print("[-]", e)
		else:
			return cur.fetchall()
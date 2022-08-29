import fdb
from helpers.firebird import insert_cur, con_to_database, get_simple_id_and_name_from_db


def open_picture_path(path):
	with open(path, 'rb') as picture_path:
		p = picture_path.read()
	return p

def write_picture_to_db(id_name, id, query_one, query_two):
	try:
		b64_picture_name = open_picture_path(id_name)
	except:
		print('[+] Error when try to read picture')
	try:
		insert_cur(query_one, b64_picture_name, b64_picture_name, id)
	except Exception as e:
		print('[+] Error when save first image' + str(e))

	else:
		try:
			insert_cur(query_two, id, b64_picture_name, b64_picture_name, b64_picture_name)
		except Exception as e:
			print('[+] Error when save second image' + str(e))

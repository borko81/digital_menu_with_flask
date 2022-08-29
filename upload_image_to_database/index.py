from flask import Flask, render_template, request, flash, url_for, redirect
from decouple import config
from PIL import Image

import os

from helpers.firebird import *
from helpers.work_with_images import *
from helpers.queries import *
current_path = os.path.join(os.getcwd(), 'images')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['POST', 'GET'])
def index():
	recepi = get_simple_id_and_name_from_db(querys['query_get_all'])
	data = {}
	for r in recepi:
		if r[2] not in data:
			data[r[2]] = []
		data[r[2]].append(
			{'id': r[0], 'name': r[1], 'has_img': r[3]}
		)
	return render_template('index.html', data=data)


@app.route('/image', methods=['POST', 'GET'])
def image():
	if request.method == 'POST':
		
		file = request.files['filename']
		recepi_id = request.form['id_']
		print(f"[+] {recepi_id}")
		# import pdb; pdb.set_trace()

		if file.filename != '':
			path_to_image = os.path.join(current_path,file.filename)
			try:
				file.save(path_to_image)
			except:
				raise ValueError('Not success when try to save localy image path!')

			im = Image.open(path_to_image)
			width, height = im.size

			if width > 700 and height > 700:
				new_size = (400, 400)
				new_im = im.resize(new_size)
				new_im.save(path_to_image, "JPEG", optimize=True)
			elif width > 700 and height <= 700:
				new_size = (400, height)
				new_im = im.resize(new_size)
				new_im.save(path_to_image, "JPEG", optimize=True)
			elif height > 700 and width <= 700:
				new_size = (width, 400)
				new_im = im.resize(new_size)
				new_im.save(path_to_image, "JPEG", optimize=True)

			# import pdb; pdb.set_trace()
			try:
				write_picture_to_db(path_to_image, recepi_id, query, query_for_tumbnail)
				flash('Successfully')
			except:
				flash('An error acquire')
			try:
				os.remove(path_to_image)
			except:
				flash('Can not delete pucture localy.')
			finally:
				return redirect(url_for('index'))
			

		flash('Not successfully')
		return {'error': 'Atach some path to image...'}


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
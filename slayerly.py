import sqlite3, os
from flask import Flask, request, g, redirect, url_for, render_template, flash
from contextlib import closing
from utils import *

DATABASE = 'slayer.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

#get slayer lyrics
lyrics = get_lyrics('slayer')

#database setup
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

#routing
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/shorten', methods = ['POST'])
def shorten():
	slayerized = make_url_from(lyrics)
	new_url = 'slayer.ly/' + slayerized
	g.db.execute('insert into slayer (url, shortened) values (?, ?)', [request.form['url'], new_url])
	g.db.commit()
	return redirect(url_for('show_link'))

@app.route('/show_link')
def show_link():
	cur = g.db.execute('select id, url, shortened from slayer order by id desc limit 1')
	link = [dict(id=row[0], url=row[1], shortened=row[2]) for row in cur.fetchall()]
	print 'link: '
	print link
	return render_template('show_link.html', link=link)

@app.route('/<int:link_id>')
def redirect_to(link_id):
	cur = g.db.execute('select url from slayer where id=' + str(link_id))
	original = cur.fetchone()[0]
	validated = validate(original)
	return redirect(validated, code=302)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

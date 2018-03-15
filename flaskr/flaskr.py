import os,sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,escape
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
	DATABASE = os.path.join(app.root_path,'flask.db'),
	SECRET_KEY = 'djfoiweanfiosdf',
	USERNAME = 'admin',
	PASSWORD = 'as'
))
#app.route_path declare the path to our application
#app.config.from_envvar("FLASKR_SETTINGS",silent=True) use the settings
def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv
def init_db():
	with app.app_context():
	#create an app context
		db = get_db()
		with app.open_resource('schema.sql',mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.cli.command('initdb')
def initdb_command():
	init_db()
	print("Initialized the database")

def get_db():
	"""
	application text
	"""
	if not hasattr(g,'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g,'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def show_entries():
	db = get_db()
	cur = db.execute('select title,text from entries order by id desc')
	entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html',entries=entries)

@app.route('/add',methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(404)
	db = get_db()
	db.execute('insert into entries(title,text) values (?,?)',[request.form['title'],request.form['text']])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['username']:
			error = 'Invalid info'
		elif request.form['password'] != app.config['password']:
			error = 'Invalid info'
		else:
			session['logged_in'] = True
			flash('successfully logged_in')
			return redirect(url_for('show_entries'))
	return render_template('login.html',error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('successfully logout')
	return redirect(url_for('show_entries'))
if __name__ == '__main__':
	app.run()
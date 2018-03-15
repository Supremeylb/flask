

@app.route('/')
def index():
	if 'username' in session:
		return 'Logged in %s' % escape(session['username'])
	return 'You are not Logged in'

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
app.secret_key =b'h\x1d\x12\xa8\x19}\xa3s\xee\xcf\x8d4\x08\xc9w\\\xfc\xe5\x91JI\xbb\xbe)'
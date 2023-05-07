from flask import Flask, request, render_template, send_from_directory, redirect, session, url_for
import os
import uuid
import model
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "a very secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Database Configuration
db_path = os.path.join(basedir, 'database.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.add_url_rule('/cdn/<path>', 'cdn', build_only=True)

db = SQLAlchemy(app=app)

# with app.app_context():
#     db.create_all()
#     print("Database created")

# get user
def get_user(username):
    return User.query.get(username)

#User class
class User(db.Model):
    __tablename__ = 'users'
    username = db.Column('username', db.String(32), primary_key = True)
    password = db.Column('password', db.String(256))

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def check_pass(self, password):
        return check_password_hash(self.password, password)

@app.route("/")
def index():
    if 'username' in session:
        user = User.query.get(session['username'])
        if user:
            return render_template("index.html", username=session['username'])
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('upload'))
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.get(username)
        if user:
            if user.check_pass(password):
                session['username']=user.username
                return redirect(url_for('index'))
            else:
                error = 'Invalid Credentials. Please try again.'
        else:
            error = 'User not found.'
    return render_template('login.html', error=error)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect("/login")
    if request.method == 'POST':
        file = request.files["uploaded_file"]
        if file and file.content_type.startswith("image"):
            file_uuid = str(uuid.uuid4())
            basename, ext = os.path.splitext(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_uuid+"."+ext[1:]))
            result_img_name = model.process_image(file_uuid, ext)
            if result_img_name is not None:
                
                session['result_img_name'] = result_img_name
                return redirect("/results")
            
            # print('file saved')
            # session['result_img_name'] = result_img_name
            return redirect("/")

        return "File not uploaded"
    return render_template("upload_old.html")

@app.route("/cdn/<path:path>")
@app.route("/cdn/<path:path>/<download>")
def cdn(path=None, download=False):
    if 'result_img_name' in session:
        filename = session['result_img_name']
        if filename is None:
            return None
        if path is None:
            return send_from_directory("", path=filename)
        else:
            if path == 'results':
                if download:
                    return send_from_directory(directory=app.config['RESULT_FOLDER'], path=filename, as_attachment=download, download_name = "result.jpg")
                return send_from_directory(directory=app.config['RESULT_FOLDER'], path=filename)
            elif path == 'uploads':
                return send_from_directory(directory='uploads', path=filename)
    return None

@app.route("/results")
def result():
    if 'result_img_name' in session:
        filename = session['result_img_name']
        return render_template("result.html", file_name=filename)
    return redirect("/")

@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect('login')
    session.pop('username',None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()
    print("Database created")
    app.run(debug=True)

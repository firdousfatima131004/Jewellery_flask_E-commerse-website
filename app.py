from flask import Flask , request ,  render_template,session
from markupsafe import escape
from werkzeug.security import generate_password_hash,check_password_hash
from models import User
from database import session as db_session
app = Flask(__name__)
app.secret_key='JEWELLRY3SHOP45SITE'

@app.route("/")
def home():
     username=session.get('username')
     return render_template('index.html',username=username)

@app.route("/login/",methods=['GET','POST'])
def login():
     if request.method=='POST':
          email=request.form.get('email')
          password=request.form.get('password')
          user=db_session.query(User).filter_by(email=email).first()
          if user:
               if check_password_hash(user.password,password):
                    session['username']=user.username
                    session['role']=user.role
                    if user.role=='user':
                         print(user.username)
                         return render_template('login.html',username=user.username)
                    elif user.role=='admin':
                         return render_template('admin.html',username=user.username)
                    else:
                         return render_template('index.html',username=None)
               else:
                    return render_template('login.html',password_error="Wrong password")
          else:
               print("USER ERROR")
     return render_template('login.html')

@app.route("/signup/",methods=['GET','POST'])
def signup():
     if request.method=='POST':     
          uname=request.form.get('username')
          email=request.form.get('email') 
          password=request.form.get('password')
          role='user'
          hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

          new_user=User(username=uname,email=email,role=role,password=hashed_password)
          
          # new_admin=User(username="admin",email="admin@jewelerry.in",role='admin',password=generate_password_hash('admin@123'))
          # db_session.add(new_admin)
          # db_session.commit()
          try:
               db_session.add(new_user)
               db_session.commit()
               return  render_template('signup.html',success="Account Created Successfully")
          except:
               db_session.rollback()
               return render_template('signup.html',error="This email already exists!")
          
          
     return render_template('signup.html')

@app.route('/admin/')
def admin():
     return render_template('admin.html')
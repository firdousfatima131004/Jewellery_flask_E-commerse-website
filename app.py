from flask import Flask , request ,  render_template,session,redirect,url_for ,jsonify
from markupsafe import escape
from werkzeug.security import generate_password_hash,check_password_hash
from models import User , Product
from database import session as db_session
import os
import requests
import http.client
import json

app = Flask(__name__)
app.secret_key='JEWELLRY3SHOP45SITE'


# home page
@app.route("/")
def home():
     username=session.get('username')
     return render_template('index.html',username=username)


# login
@app.route("/login/",methods=['GET','POST'])
def login():
     username=session.get('username')
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
     return render_template('login.html',username=username)


#sign up
@app.route("/signup/",methods=['GET','POST'])
def signup():
     username=session.get('username')
     if request.method=='POST':     
          uname=request.form.get('username')
          email=request.form.get('email') 
          password=request.form.get('password')
          role='user'
          hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

          new_user=User(username=uname,email=email,role=role,password=hashed_password)
          
          #admin
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
          
          
     return render_template('signup.html',username=username)

# admin page
@app.route('/admin/')
def admin():
     
     if 'username' not in session or session.get('role') !='admin':
          return redirect(url_for('signup'))
     
     return render_template('admin.html')
#logout
@app.route('/logout/')
def logout():
     session.clear()
     return render_template('index.html')
     

#viewing product page
@app.route('/product/')
def products():
     username=session.get('username')
     return render_template('view_product.html',username=username)




# add_products
@app.route('/addProduct/' , methods=['GET', 'POST']    )
def add_product():
     username=session.get('username')
     if request.method == 'POST':
          ProductName = request.form.get('pname')
          productDescription = request.form.get('desc')
          productPrice = request.form.get('pprice')
          productCategory = request.form.get('category')
          img = request.files.get('img')
          
          if img:
               img.save(os.path.join("static/UserImg",img.filename))
               path = f"/static/UserImg/{img.filename}"
               data = Product(productname = ProductName ,productDesc = productDescription,productPrice = productPrice ,productCategory =productCategory ,img = path)
               
               db_session.add(data)
               db_session.commit()
               
               try:
                    db_session.add(data)
                    db_session.commit()
                    return  render_template('add_product.html',success="Product added Successfully",username=username)
               except:
                    db_session.rollback()
                    return render_template('add_product.html',error="Their is some error Kindly fill all fields!",username=username)
               
               
          
     return render_template('add_product.html',username=username)
     
     

# showing products
@app.route('/show_product/<string:category>', methods=['GET'])
def show_product(category):
    username=session.get('username')
    products = db_session.query(Product).filter_by(productCategory=category).all()
    return render_template('show_product.html', products=products, category=category,username=username)

# about us page
@app.route('/aboutus/')
def about_us():
     username=session.get('username')
     return render_template('aboutus.html',username=username)






if __name__ == '__main__':
     app.run(debug=True)
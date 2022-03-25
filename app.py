from flask import Flask
from flask import render_template
from flask import request

from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/dashboard/<name>')
def dashboard(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['name']
      return redirect(url_for('dashboard',name = user))
   else:
      user = request.args.get('name')
      return render_template('login.html')

if __name__ == '__main__':
   app.run(debug = True, port=8080)

# from markupsafe import escape
# from flask import Flask
# from flask import Flask, abort

# app = Flask(__name__)


# @app.route('/')
# @app.route('/index/')
# def hello():
#     return '<h1>Hello, World!</h1>'

# @app.route('/about/')
# def about():
#     return '<h3>This is a Flask web application.</h3>'

# @app.route('/capitalize/<word>/')
# def capitalize(word):
#     return '<h1>{}</h1>'.format(escape(word.capitalize()))

# @app.route('/add/<int:n1>/<int:n2>/')
# def add(n1, n2):
#     return '<h1>{}</h1>'.format(n1 + n2)

# @app.route('/users/<int:user_id>/')
# def greet_user(user_id):
#     users = ['Bob', 'Jane', 'Adam']
#     try:
#         return '<h2>Hi {}</h2>'.format(users[user_id])
#     except IndexError:
#         abort(404)

# if __name__ == "__main__":
#     app.run(debug=True)
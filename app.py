from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

# Create the db instance and bind immediately
db = SQLAlchemy(app)

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/register")
def register():
     return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
     return render_template("logout.html")

if __name__ == "__main__":
    app.run(debug=True)

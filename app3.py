from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pkdb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class new_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

with app.app_context():
    db.create_all()
    new_user = new_user(
        email="binamahato9814@gmail.com",
        password="333", 
        address ="st",
        city ="ktm",
        state ="sirha"
    )

    # check if already exists
  
    db.session.add(new_user)
    db.session.commit()
    print("User added successfully!")
    


# Routes
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

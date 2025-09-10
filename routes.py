from flask import render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app1 import db, Users, Profiles
from forms import RegistrationForm, LoginForm, LoadMoneyForm, SendMoneyForm

def configure_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            user = Users(username=form.username.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            profile = Profiles(age=form.age.data, user_id=user.id)
            db.session.add(profile)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                session['user_id'] = user.id
                flash('You have been logged in!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)

    @app.route("/dashboard")
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = Users.query.get(session['user_id'])
        return render_template("dashboard.html", user=user)

    @app.route("/load_money", methods=['GET', 'POST'])
    def load_money():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        form = LoadMoneyForm()
        if form.validate_on_submit():
            user = Users.query.get(session['user_id'])
            user.profile.amount += float(form.amount.data)
            db.session.commit()
            flash('Money loaded successfully!', 'success')
            return redirect(url_for('dashboard'))
        return render_template('load_money.html', title='Load Money', form=form)

    @app.route("/send_money", methods=['GET', 'POST'])
    def send_money():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        form = SendMoneyForm()
        if form.validate_on_submit():
            sender = Users.query.get(session['user_id'])
            recipient = Users.query.filter_by(username=form.username.data).first()
            amount = float(form.amount.data)
            if not recipient:
                flash('Recipient not found.', 'danger')
            elif sender.profile.amount < amount:
                flash('Insufficient funds.', 'danger')
            else:
                sender.profile.amount -= amount
                recipient.profile.amount += amount
                db.session.commit()
                flash('Money sent successfully!', 'success')
                return redirect(url_for('dashboard'))
        return render_template('send_money.html', title='Send Money', form=form)

    @app.route("/logout")
    def logout():
        session.pop('user_id', None)
        flash('You have been logged out.', 'success')
        return redirect(url_for('index'))
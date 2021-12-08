from flask import (Flask, render_template, url_for, request, abort, redirect, make_response, session, flash, abort, jsonify)
from app import bcrypt
from app import app
from app.models.user import User
from app import bcrypt


@app.route('/login', methods=['GET'])
def login():
    if not session.get('id'):
        return render_template('login.html')
    else:
        return redirect(url_for('admin'))


@app.route('/login/proses', methods=['POST'])
def proses():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        user = User()
        account = user.getOne(username)

        if account:
            if bcrypt.check_password_hash(account[2].encode('utf-8'), password):
            # if bcrypt.hashpw(password, account[2].encode('utf-8')) == account[2].encode('utf-8'):
                session['id'] = account[0]
                user = User()
                session['user'] = account
                session['login'] = True
                if user.getOneId(str(account[0])) == 'satgas':
                    flash("Selamat Datang")
                    return redirect(url_for('satgas'))
                else:
                    flash("Selamat Datang")
                    return redirect(url_for('admin'))
            else:
                flash("Username dan Password salah")
                return redirect(url_for('login'))
        else:
            flash("Pengguna tidak ditemukan")
            return redirect(url_for('login'))
            
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


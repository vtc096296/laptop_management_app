from flask import Blueprint, render_template, redirect, request, session, flash, jsonify
from models.manager import Manager
from myfunc.myfunc  import *

login = Blueprint('login', __name__)

# LOGIN
@login.route('/manager/login', methods= ['GET','POST'])
def manager_login():
    if 'user_info' in session:
        return redirect('/home/product-list')
    else:
        if request.method == 'POST':
            manager = Manager()

            username = request.form.get('username').strip()
            password = request.form.get('password').strip()

            hash_pass = hash_password(username, password)
            login = manager.validateUserAndPassWord(username, hash_pass)

            if login:
                roleid = [i[0] for i in manager.getRoleOfUser(login[0])]
                session['user_info'] = {'uid': login[0],'username':username, 'rid': roleid}

                if 5 in roleid:
                    return redirect('/manager/admin')
                else:
                    return redirect('/home/product-list')
            else:
                return redirect('/manager/login')
        return render_template('login/login.html')


# LOGOUT
@login.route('/manager/logout', methods= ['POST'])
@login_required
def manager_logout():
    if 'user_info' in session:
        session.pop('user_info')
        return redirect('/manager/login')
    else:
        return redirect('/manager/login')
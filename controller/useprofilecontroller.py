from flask import Flask, Blueprint, render_template, redirect, request, session, flash
from models.manager import Manager
from models.roles import Roles
from myfunc.myfunc  import *

user = Blueprint('user', __name__)

# USER PROFILE
@user.route('/user/user-profile/<uid>')
@login_required
def user_profile_page(uid):
    manager = Manager()
    rid = manager.getRoleOfUser(uid)
    print(rid)
    return render_template('user_profile/user_profile.html', rid = rid)


# CHANGE PASSWORD
@user.route('/user/change-password/<uid>', methods= ['POST'])
def change_pwd(uid):
    manager = Manager()
    rq = request.form

    un = session.get('user_info')['username']
    old_pwd = rq.get('old_pwd')
    hash_pass = hash_password(un, old_pwd)

    if manager.validateUserAndPassWord(un, hash_pass):
        new_pwd = rq.get('new_pwd')
        hash_pass = hash_password(un, new_pwd)
        ret = manager.updateUserPassword((hash_pass, un))

        if ret > 0:
            flash('Change Password successful !!!', 'success')
            return redirect('/user/user-profile/'+ uid)
        else:
            flash('Change Password FAILED !!!', 'success')
            return redirect('/user/user-profile/'+ uid)

    else:
        flash('Wrong old password')
        return redirect('/user/user-profile/'+ uid)


# USER Reset PASSWORD
@user.route('/user/reset-password/<uid>', methods= ['POST'])
def user_reset_pwd(uid):
    manager = Manager()
    un = session.get('user_info')['username']

    reset_pwd = hash_password(un, un)
    ret = manager.updateUserPassword((reset_pwd, un))

    if ret > 0:
        flash('Reset password successful !!', 'success')
        return redirect('/user/user-profile/' + uid)
    else:
        flash('Reset password FAILED !!!')
        return redirect('/user/user-profile/' + uid)
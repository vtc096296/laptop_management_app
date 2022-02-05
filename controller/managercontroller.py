from flask import Blueprint, render_template, redirect, request, session, flash, jsonify
from models.manager import Manager
from models.roles import Roles
from myfunc.myfunc  import *

manager = Blueprint('manager', __name__)

# ADMIN PAGE
@manager.route('/manager/admin')
@login_required
def admin_page():
    ses = session.get('user_info')

    if ses and 5 in ses['rid']:
        manager = Manager()
        role = Roles()

        r = role.getRole()
        ml = manager.getAllUser()
        role_list = role.getRole()

        uid = ses['uid']
        user_role = manager.getRoleOfUser(uid)
        username = manager.getUserNameById(uid)
        return render_template('manager/admin_page.html', ml= ml ,arr =r, role_list = role_list, user_role = user_role)
    else:
        return redirect('/manager/login')


# Do ADD NEW USER
@manager.route('/manager/add-user', methods=['POST'])
def add_user():
    manager = Manager()
    role = Roles()
    rq = request.form   
    a = []

    user_names = [i[1] for i in manager.getAllUser()]
    roles = [i[0] for i in role.getRole()]

    usr = rq.get('usr').strip()
    pwd = rq.get('pwd').strip()
    usr_role = rq.getlist('role')
    hash_pwd = hash_password(usr, pwd)

    if usr != '' and pwd != '':

        if usr_role != []:

            if usr not in user_names:

                ret = manager.createUser((usr, hash_pwd))

                if ret > 0:
                    user = manager.validateUserAndPassWord(usr, hash_pwd)

                    for roleid in roles:
                        if str(roleid) in usr_role:
                            a.append((roleid, user[0], 1))  # (role_id, user_id, checked)
                        else:
                            a.append((roleid, user[0], 0))

                    ret = role.addRoleOfUser(a)

                    if ret > 0:
                        flash('Create new user successful !!', 'success')
                        return redirect('/manager/admin')
                    else:
                        flash('Can not create user', 'error')
                        return redirect('/manager/add-user')

                else:
                    flash('Can not create user', 'error')
                    return redirect('/manager/add-user')

            else:
                flash('Username was existed !!')
                return redirect('/manager/admin')
        else:
            flash('You must choose at least one role', 'info')
            return redirect('/manager/admin')

    else:
        flash('Username or Password is empty', 'info')
        return redirect('/manager/admin')


# DELETE USER
@manager.route('/manager/delete-user/<user_name>', methods= ['POST'])
def delete_user(user_name):
    manager = Manager()
    role = Roles()

    uid = int(request.form.get('uid'))
    ret1 = manager.deleteUser(user_name)
    ret2 = role.deleteRoleOfUser(uid)


    if ret1 > 0 and ret2 > 0:
        flash('Delete '+ user_name + ' successful !!', 'sucess')
        return redirect('/manager/admin')
    else:
        flash('Can not delete '+ user_name)
        return redirect('/manager/admin')


# RESET PASSWORD
@manager.route('/manager/reset-password/<user_name>', methods= ['POST'])
def reset_pwd(user_name):
    manager = Manager()

    reset_pwd = hash_password(user_name, user_name)
    ret = manager.updateUserPassword((reset_pwd, user_name))

    if ret > 0:
        flash('Reset password of ' + user_name + ' sucessful!', 'success')
        return redirect('/manager/admin')
    else:
        flash('Reset password FAILED !!!', 'error')
        return redirect('/manager/admin')


# Edit USER ROLE PAGE
@manager.route('/manager/user-role/<uid>', methods= ['POST'])
def edit_role_page(uid):
    manager = Manager()
    role = Roles()
    role_list = role.getRole()

    user_role = manager.getRoleOfUser(uid)

    return jsonify({'uid':uid, 'user_role':user_role})


# Do Edit USER ROLE PAGE
@manager.route('/manager/edit-user-role', methods= ['POST'])
def edit_role():
    role = Roles()
    manager = Manager()

    a = []
    uid = request.form.get('uid_in_role')
    new_user_role = request.form.getlist('role')

    for r in role.getRole():
        if str(r[0]) in new_user_role: 
            a.append((1, uid, r[0]))
        else:
            a.append((0, uid, r[0]))
            
    ret = role.updateRoleOfUser(a)

    if ret > 0:
        flash('Edit Role successful !!!', 'success')
        return redirect('/manager/admin')
    else:
        flash('Edit FAILED !!! Please try again', 'error')
        return redirect('/manager/admin')

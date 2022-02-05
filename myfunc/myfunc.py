import json
import os
from hashlib import md5
from functools import wraps
from flask import g, request, redirect, url_for, session


def hash_password(un, pw):
    return md5((un + '~!@#$%^&*()_+' + pw).encode()).hexdigest()


def deleteProductFile(img, spec):
    img_default = 'static/image/products/default.png'
    try:
        # Delete img file
        if img != img_default:
            if os.path.exists(img):
                os.remove(img)
        else:
            pass
        # Delete spec file
        if os.path.exists(spec):
            os.remove(spec)
        return 1
    except:
        return 0


def writeSpecFileFromClient(path, lst=None):
    f= open('static/specification_file/spec_default.json', 'r', encoding='utf-8')
    c= json.load(f)
    f.close()
    i = 0
    if lst:
        for v in c.get('Spec').values():
            if i < len(lst):
                for key in v.keys():
                    v[key]=lst[i]
                    i+=1
            else:
                break
    s = open(path, 'w', encoding='utf-8')
    json.dump(c,s, indent=4, ensure_ascii= False)
    s.close()


def initSpecFile(path):
    f= open('static/specification_file/spec_default.json', 'r', encoding='utf-8')
    c= json.load(f)
    f.close()
    s= open(path, 'x', encoding='utf-8')
    s.close()
    s= open(path, 'w', encoding= 'utf-8')
    json.dump(c,s, indent=4 , ensure_ascii=False)
    s.close()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_info' not in session:
            return redirect('/manager/login')
        return f(*args, **kwargs)
    return decorated_function
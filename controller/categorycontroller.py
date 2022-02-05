from flask import Blueprint, render_template, redirect, request, url_for, jsonify, flash
from models.category import Category
from hashlib import md5, sha1
from datetime import datetime
import json

category = Blueprint('category', __name__)

#Msg
cate_existed = {'info': 'Category is exited !!! Please create other name'}
cate_error = {'error':'Something went wrong !!! Please try again'}
pro_existed = {'info': 'Product is exited !!! Please create other name'}

# Category list
@category.route('/home/category-list')
def category_list():
    category = Category()
    data_cate_name = category.getAllCategory()
    return render_template('category/category_list.html', cate = data_cate_name)


# Create category
@category.route('/home/createcategory', methods = ['POST'])
def createCategory():
    cate = Category()
    cate_name = request.form.get('cate_name').strip()
    data_cate_name = cate.getAllCategoryName()
    name_list = [i[0] for i in data_cate_name]
    if cate_name not in name_list:
        ret = cate.createCategory((cate_name, ))
        if ret > 0:
            cate_id = cate.getCategoryByName(cate_name)[0]
            return jsonify({'cate_id':cate_id, 'cate_name': cate_name})
        else:
            return jsonify(cate_error)
    else:
        return jsonify(cate_existed)


# Edit category
@category.route('/home/edit-category-name', methods =['POST'])
def editCategory():
    category = Category()
    cate_id = request.form.get('cate_id')
    cate_name = request.form.get('cate_name').strip()
    data_cate_name = category.getAllCategoryName()
    name = [i[0] for i in data_cate_name]
    if cate_name not in name:
        ret = category.updateCategoryNameById((cate_name, cate_id))
        if ret > 0:
            return jsonify({'cate_id': cate_id, 'cate_name':cate_name})
        else:
            return jsonify(cate_error)
    else:
        return jsonify(cate_existed)


# Delete category
@category.route('/home/delete-category-name', methods = ['POST'])
def deleteCategory():
    category = Category()
    cate_id = request.form.get('cate_id')
    ret = category.deleteCategoryById(cate_id)
    if ret > 0:
        return jsonify({'cate_id': cate_id, 'info':'Done'})
    else:
        return jsonify(cate_error)
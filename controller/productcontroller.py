from flask import Blueprint, render_template, redirect, request, url_for, jsonify, flash
from models.category import Category
from models.product import Product
from hashlib import md5, sha1
from datetime import datetime
import json
from myfunc.myfunc import *

product= Blueprint('product', __name__)

#Msg
cate_existed = {'info': 'Category is exited !!! Please create other name'}
cate_error = {'error':'Something went wrong !!! Please try again'}
pro_existed = {'info': 'Product is exited !!! Please create other name'}


# Product page
@product.route('/home/product-list', methods = ['GET'])
@login_required
def home():
    product = Product()
    pro = product.getAllProducts()
    category = Category()
    cate = category.getAllCategory()

    return render_template('product/product_list.html', pro = pro, cate = cate)


# Create product
@product.route('/home/create-product', methods=['POST'])
def create_product():
    product = Product()
    pro = product.getAllProducts()

    rfm = request.form
    rfs = request.files

    pro_name = [i[1] for i in pro]      # Product name list
    cate = rfm.get('cate_sel')          # Category Id
    pn = rfm.get('pro_name').strip()    # Product name
    bp = rfm.get('buy_price').strip()   # Buy price
    sp = rfm.get('sell_price').strip()  # Sell price
    qt = rfm.get('quantity').strip()    # Quantity
    img = rfs.get('pro_img')            # Image File
    # spec = rfs.get('pro_spec')          # Specification File

    # Check image file upload
    if img.filename =='':
        img_link = '/static/image/products/default.png' 
    else:
        img_link = '/static/image/products/' + (sha1(pn.encode())).hexdigest() + '.png'
        img.save(img_link.split('/',1)[1])

    # Specification json file upload
    spec_link = 'static/specification_file/' + (sha1(pn.encode())).hexdigest() + '.json'
    initSpecFile(spec_link)

    # Check Product name existed and commit database
    if pn not in pro_name:
        tup = (pn, bp, sp, img_link, qt, spec_link, cate)
        ret = product.createProduct(tup)
        if ret > 0:
            return redirect('/home/product-list')
        else:
            return render_template('error/data_error.html')
    else:
        return jsonify(pro_existed)
    # return redirect('/home/product-list')


# Product info table
@product.route('/home/product-info-table/<int:pid>')
@login_required
def product_info(pid):
    category = Category()
    cate = category.getAllCategory()
    
    product= Product()
    pro = product.getProductById(pid)
    
    f = open(pro[6], 'r', encoding='utf-8')
    s = json.load(f)
    f.close()

    return render_template('product/product_info.html', pro = pro, cate= cate, spec = s.get('Spec'))


# Edit product image
@product.route('/home/edit-product-img/<id>', methods=['POST'])
def edit_product_img(id):
    product = Product()
    pro = product.getProductById(id)

    img = request.files.get('img')

    s = str(datetime.now())
    img_link = '/static/image/products/' + (sha1((s+pro[1]).encode())).hexdigest() + '.png'
    img.save(img_link.split('/',1)[1])
    
    ret = product.updateProductImg((img_link, id))
    if ret > 0 :
        return jsonify({'notice':'Success!!!', 'img_link': img_link})
    else:
        return jsonify({'notice': 'Edit Failed'})


# Edit Product Info
@product.route('/home/product-edit-info/<id>', methods = ['POST'])
def edit_product_info(id):
    product= Product()
    pro = product.getAllProducts()
    
    rq = request.form
    ci = rq.get('cate')
    pn = rq.get('pro_name').strip()
    buy = rq.get('buy').strip()
    sell = rq.get('sell').strip()
    qty = rq.get('qty').strip()
    old_name = rq.get('old_name')
    tup = (pn, buy, sell, qty, ci, id)

    name_list = [i[1] for i in pro]
    if pn in name_list and pn != old_name:
        return jsonify({'warning':'Product name existed !!'})
    else:
        ret = product.updateProductInfo(tup)
        if ret > 0:
            return jsonify({'info': 'Edit successful'})
        else:
            return jsonify({'info': 'Edit failed'})


# Edit Product specification
@product.route('/home/edit-poduct-specification/<id>', methods = ['POST'])
def edit_product_spec(id):
    product = Product()
    pro= product.getProductById(id)
    spec_link = pro[6]
    pn = pro[1]
    spec = request.form.getlist('spec[]')

    spec_file_path = 'static/specification_file/' + (sha1(pn.encode())).hexdigest() + '.json'
    writeSpecFileFromClient(spec_file_path, spec)

    return jsonify({'info': 'Save Change Complete'})


# Delete Product
@product.route('/home/delete-product/<int:id>', methods= ['POST'])
def delete_product(id):
    product = Product()
    p = product.getProductById(id)
    rsl = deleteProductFile(p[4].split('/',1)[1], p[6])
    ret = product.deleteProductById(id)
    if ret > 0 and rsl > 0:
        return redirect('/home/product-list')
    else:
        return render_template('error/data_error.html')


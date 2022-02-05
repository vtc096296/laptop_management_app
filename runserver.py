from flask import Flask
from controller.categorycontroller import category
from controller.productcontroller import product
from controller.managercontroller import manager
from controller.useprofilecontroller import user
from controller.logincontroller import login


app= Flask(__name__)
app.config['SECRET_KEY'] = '23esxtygh3qehd867yuhj234'

app.register_blueprint(category)
app.register_blueprint(product)
app.register_blueprint(manager)
app.register_blueprint(user)
app.register_blueprint(login)


if __name__ == '__main__':
    app.run(debug=True)
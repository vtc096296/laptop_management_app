from models.database import DataBase

class Product(DataBase):

    def createProduct(self, tup):
        sql = 'INSERT INTO Products(ProductName, BuyPrice, SellPrice, ImageLink, Quantity, Specification, CategoryId) VALUES (?,?,?,?,?,?,?)'
        return self.changeOne(sql, tup)

    def getAllProducts(self):
        sql = 'SELECT * FROM Products'
        return self.getAll(sql)

    def getProductById(self, id):
        sql = 'SELECT * FROM Products WHERE ProductId = ?'
        return self.getOne(sql, (id, ))
    
    def getProductSpecById(self, id):
        sql = 'SELECT Specification FROM Products WHERE ProductId = ?'
        return self.getOne(sql, (id,))

    def updateProductInfo(self, tup):
        sql= '''UPDATE Products SET ProductName = ?, BuyPrice = ?, SellPrice = ?,
                Quantity = ?, CategoryId = ? WHERE ProductId = ?'''
        return self.changeOne(sql, tup)

    def updateProductImg(self,tup):
        sql = '''UPDATE Products SET ImageLink = ? WHERE ProductId = ?'''
        return self.changeOne(sql, tup)

    def deleteProductById(self, id):
        sql = 'DELETE FROM Products WHERE ProductId = ?'
        return self.changeOne(sql, (id, ))
from models.database import DataBase

class Category(DataBase):

    def createCategory(self, tup):
        sql = 'INSERT INTO Category(CategoryName) VALUES (?)'
        return self.changeOne(sql, tup)
    
    def getAllCategory(self):
        sql = 'SELECT * FROM Category'
        return self.getAll(sql)

    def getAllCategoryName(self):
        sql = 'SELECT CategoryName FROM Category'
        return self.getAll(sql)

    def getCategoryById(self, id):
        sql = 'SELECT * FROM Category WHERE CategoryId = ?'
        return self.getOne(sql, (id, ))

    def getCategoryByName(self, name):
        sql = 'SELECT * FROM Category WHERE CategoryName = ?'
        return self.getOne(sql, (name, ))

    def updateCategoryNameById(self, tup):
        sql = 'UPDATE Category SET CategoryName = ? WHERE CategoryId = ?'
        # tup = (CategoryName, CategoryId)
        return self.changeOne(sql, tup)

    def deleteCategoryById(self, id):
        sql = 'DELETE FROM Category WHERE CategoryId = ?'
        return self.changeOne(sql, (id,))
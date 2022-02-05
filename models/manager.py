from models.database import DataBase

class Manager(DataBase):

    def validateUserAndPassWord(self, un, pw):
        sql = 'SELECT * FROM ManagerAccount WHERE UserName = ? AND PassWord = ?'
        return self.getOne(sql, (un,pw))

    def getRoleOfUser(self, uid):
        sql = '''SELECT Role.*, UserInRole.UserId, UserInRole.Checked FROM Role JOIN UserInRole 
            ON Role.RoleId = UserInRole.RoleId AND UserInRole.UserId = ? AND Checked = 1'''
        return self.getAll2(sql, (uid,))

    def getAllUser(self):
        sql = 'SELECT * FROM ManagerAccount'
        return self.getAll(sql)

    def getUserNameById(self, id):
        sql = 'SELECT UserName FROM ManagerAccount WHERE ManagerId = ?'
        return self.getOne(sql, (id, ))

    def createUser(self, tup):
        sql = 'INSERT INTO ManagerAccount(Username, PassWord) VALUES (?,?)'
        return self.changeOne(sql, tup)

    def updateUserPassword(self, tup):
        sql = 'UPDATE ManagerAccount SET PassWord = ? WHERE UserName = ?'
        return self.changeOne(sql, tup)

    def deleteUser(self, user_name):
        sql = 'DELETE FROM ManagerAccount WHERE UserName = ?'
        return self.changeOne(sql, (user_name, ))
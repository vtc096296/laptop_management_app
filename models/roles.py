from models.database import DataBase

class Roles(DataBase):
    
    def getRole(self):
        sql = 'SELECT * FROM Role'
        return self.getAll(sql)

    def addRoleOfUser(self, arr):
        sql = 'INSERT INTO UserInRole(RoleId, UserId, Checked) VALUES (?,?,?)'
        return self.changeMany(sql, arr)

    def updateRoleOfUser(self, arr):
        sql = 'UPDATE UserInRole SET Checked = ? WHERE UserId = ? AND RoleId = ?'
        return self.changeMany(sql, arr)
    
    def deleteRoleOfUser(self, uid):
        sql = 'DELETE FROM UserInRole WHERE UserId = ?'
        return self.changeOne(sql, (uid, ))
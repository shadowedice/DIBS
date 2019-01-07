import sqlite3

class Database:
    def __init__(self):
        self.file = "database.sqlite"
        self.connection = sqlite3.connect(self.file)
        self.sqlDB = self.connection.cursor()
        
        self.sqlDB.execute("CREATE TABLE IF NOT EXISTS Users (ServerID, UserID, Admin, Mute, Iam, Twitch)")
        self.sqlDB.execute("CREATE TABLE IF NOT EXISTS SoundBoard (ServerID, Name, File, Text, Count, Mute)")
        self.sqlDB.execute("CREATE TABLE IF NOT EXISTS Christmas (ServerID, UserID, Bag INT, Gift INT, Coal INT, OpenedBags INT, TotalBags INT, DibsGifts INT)")
        self.sqlDB.execute("CREATE TABLE IF NOT EXISTS BotChannels (ServerID, ChannelID, Type)")
        
        
    def SetFields(self, table, keys, kvals, fields, fvals):
        ret = False
        if self.FieldExists(table, keys, kvals):
            #print("UPDATE {tn} SET {up} WHERE {kstr}".format(tn=table, up=self.__ColVal(fields, fvals, False),  kstr=self.__ColVal(keys, kvals, True)))
            self.sqlDB.execute("UPDATE {tn} SET {up} WHERE {kstr}".format(tn=table, up=self.__ColVal(fields, fvals, False),  kstr=self.__ColVal(keys, kvals, True)))
            self.connection.commit()
            ret = True
        else:
            ret = self.AddEntry(table, keys, kvals, fields, fvals)
        return ret

    def GetFields(self, table, keys, kvals, fields):
        #print("SELECT {c} FROM {tn} WHERE {kstr}".format(c = self.__ColStr(fields), tn = table, kstr=self.__ColVal(keys, kvals, True)))
        if kvals == 'null':
            self.sqlDB.execute("SELECT {c} FROM {tn} WHERE {kstr}".format(c = self.__ColStr(fields), tn = table, kstr=self.__ColValNull(keys, True)))
        elif kvals == 'notNull':
            self.sqlDB.execute("SELECT {c} FROM {tn} WHERE {kstr}".format(c = self.__ColStr(fields), tn = table, kstr=self.__ColValNull(keys, False)))
        else:
            self.sqlDB.execute("SELECT {c} FROM {tn} WHERE {kstr}".format(c = self.__ColStr(fields), tn = table, kstr=self.__ColVal(keys, kvals, True)))
        return self.sqlDB.fetchall()
        
    def GetField(self, table, keys, kvals, fields):
        #print("SELECT {c} FROM {tn} WHERE {kstr}".format(c = self.__ColStr(fields), tn = table, kstr=self.__ColVal(keys, kvals, True)))
        self.sqlDB.execute("SELECT {c} FROM {tn} WHERE {kstr}".format(c = self.__ColStr(fields), tn = table, kstr=self.__ColVal(keys, kvals, True)))
        return self.sqlDB.fetchone()
                
    def AddEntry(self, table, keys, kvals, fields, fvals):
        #print("INSERT INTO {tn} ({c}) VALUES ({val})".format(tn=table, c = self.__ColStr(keys + fields), val = self.__ColStr(kvals + fvals)))
        self.sqlDB.execute("INSERT INTO {tn} ({c}) VALUES ({val})".format(tn=table, c = self.__ColStr(keys + fields), val = self.__ColStr(kvals + fvals)))
        self.connection.commit()
        return True
        
    def FieldExists(self, table, keys, kvals):
        #print("SELECT * FROM {tn} WHERE {kstr}".format(tn=table, kstr=self.__ColVal(keys, kvals, True)))
        self.sqlDB.execute("SELECT * FROM {tn} WHERE {kstr}".format(tn=table, kstr=self.__ColVal(keys, kvals, True)))
        ret = self.sqlDB.fetchone()
        if ret is None:
            return False
        else:
            return True
            
    def RemoveEntry(self, table, keys, kvals):
        #print("DELETE FROM {tn} WHERE {kstr}".format(tn=table, kstr=self.__ColVal(keys, kvals, True)))
        self.sqlDB.execute("DELETE FROM {tn} WHERE {kstr}".format(tn=table, kstr=self.__ColVal(keys, kvals, True)))
        self.connection.commit()
        return True
        
    def __ColStr(self, cols):
        col = ""
        for c in cols:
            col = col + "\"{}\", ".format(c)
        return col[:-2]
        
    def __ColVal(self, cols, cvals, isKey):
        if len(cols) != len(cvals):
            return None
        else:
            ret = ""
            for x in range(len(cols)):
                ret = ret + cols[x] + "=\"{}\"".format(cvals[x])
                if x+1 != len(cols):
                    if isKey:
                        ret = ret + " AND "
                    else:
                        ret = ret + ", "
            return ret
            
    def __ColValNull(self, cols, isNull):
        ret = ""
        for x in range(len(cols)):
            if isNull:
                ret = ret + cols[x] + " IS NULL"
            else:
                ret = ret + cols[x] + " IS NOT NULL"
            if x+1 != len(cols):
                ret = ret + " AND "
        return ret  

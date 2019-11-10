import sqlite3


class Database:
    def __init__(self):
        self.file = "database.sqlite"
        self.connection = sqlite3.connect(self.file)
        self.sqlDB = self.connection.cursor()

        self.sqlDB.execute("CREATE TABLE IF NOT EXISTS Users (ServerID INT, UserID INT, Admin, Mute, Iam, Twitch)")
        self.sqlDB.execute("CREATE TABLE IF NOT EXISTS SoundBoard (ServerID INT, Name, File, Text, Count, Mute)")
        self.sqlDB.execute("CREATE TABLE IF NOT EXISTS Christmas (ServerID INT, UserID INT, Bag INT, Gift INT,"
                           " Coal INT, OpenedBags INT, TotalBags INT, DibsGifts INT)")
        self.sqlDB.execute("CREATE TABLE IF NOT EXISTS BotChannels (ServerID INT, ChannelID INT, Type)")
        self.sqlDB.execute("CREATE TABLE IF NOT EXISTS TwitchGameID (GameID, GameStr)")
        self.sqlDB.execute("CREATE TABLE IF NOT EXISTS TwitchMessages (ServerID INT, ChannelID INT, MessageID INT, "
                           "UserID INT)")

    def SetFields(self, table, keys, kvals, fields, fvals):
        ret = False
        if self.FieldExists(table, keys, kvals):
            # print("UPDATE {tn} SET {up} WHERE {kstr}".format(tn=table, up=self.__ColVal(fields, fvals, False),
            # kstr=self.__ColVal(keys, kvals, True)))
            self.sqlDB.execute("UPDATE {tn} SET {up} WHERE {kstr}".format(tn=table,
                                                                          up=self.__ColVal(fields, fvals, False),
                                                                          kstr=self.__ColVal(keys, kvals, True)))
            self.connection.commit()
            ret = True
        else:
            ret = self.AddEntry(table, keys, kvals, fields, fvals)
        return ret

    def GetFields(self, table, keys, kvals, fields, distinct=False):
        # print("SELECT {c} FROM {tn} WHERE {kstr}".format(c = self.__ColStr(fields), tn = table, kstr=self.__
        # ColVal(keys, kvals, True)))
        dist = ""

        if distinct:
            dist = " DISTINCT "

        if kvals == 'null':
            kstr = self.__ColValNull(keys, True)
        elif kvals == 'notNull':
            kstr = self.__ColValNull(keys, False)
        else:
            kstr = self.__ColVal(keys, kvals, True)

        self.sqlDB.execute("SELECT {d}{c} FROM {tn} WHERE {k}".format(d=dist, c=self.__ColStr(fields), tn=table,
                                                                      k=kstr))
        return self.sqlDB.fetchall()

    def GetField(self, table, keys, kvals, fields, distinct=False):
        # return the first field found
        fields = self.GetFields(table, keys, kvals, fields, distinct)
        if fields:
            return fields[0]
        else:
            return []

    def GetTable(self, table, fields):
        self.sqlDB.execute("SELECT {c} FROM {tn}".format(c=self.__ColStr(fields), tn=table))
        return self.sqlDB.fetchall()

    def AddEntry(self, table, keys, kvals, fields, fvals):
        # print("INSERT INTO {tn} ({c}) VALUES ({val})".format(tn=table, c = self.__ColStr(keys + fields), val =
        # self._ColStr(kvals + fvals)))
        self.sqlDB.execute("INSERT INTO {tn} ({c}) VALUES ({val})".format(tn=table, c=self.__ColStr(keys + fields),
                                                                          val=self.__ColStr(kvals + fvals)))
        self.connection.commit()
        if self.sqlDB.rowcount > 0:
            return True
        else:
            return False

    def FieldExists(self, table, keys, kvals):
        # print("SELECT * FROM {tn} WHERE {kstr}".format(tn=table, kstr=self.__ColVal(keys, kvals, True)))
        self.sqlDB.execute("SELECT * FROM {tn} WHERE {kstr}".format(tn=table, kstr=self.__ColVal(keys, kvals, True)))
        ret = self.sqlDB.fetchone()
        if ret is None:
            return False
        else:
            return True

    def RemoveEntry(self, table, keys, kvals):
        # print("DELETE FROM {tn} WHERE {kstr}".format(tn=table, kstr=self.__ColVal(keys, kvals, True)))
        self.sqlDB.execute("DELETE FROM {tn} WHERE {kstr}".format(tn=table, kstr=self.__ColVal(keys, kvals, True)))
        self.connection.commit()
        if self.sqlDB.rowcount > 0:
            return True
        else:
            return False

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
                if x + 1 != len(cols):
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
            if x + 1 != len(cols):
                ret = ret + " AND "
        return ret

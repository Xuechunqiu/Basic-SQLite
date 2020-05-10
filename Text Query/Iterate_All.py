from bsddb3 import db
DB_File = "data.db"
database = db.DB()
database.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
database.open(DB_File,None, db.DB_HASH, db.DB_CREATE)
curs = database.cursor()

#Insert key-values including duplicates …
database.put(b'key1', "value1")
database.put(b'key1', "value2")
database.put(b'key2', "value1")
database.put(b'key2', "value2")

iter = curs.first()
while (iter):
    print(curs.count()) #prints no. of rows that have the same key for the current key-value pair referred by the cursor
    print(iter)

    #iterating through duplicates
    dup = curs.next_dup()
    while(dup!=None):
        print(dup)
        dup = curs.next_dup()

    iter = curs.next()

curs.close()
database.close()

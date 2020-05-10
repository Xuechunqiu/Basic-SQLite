from bsddb3 import db
DB_File = "students.db"
database = db.DB()
database.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
database.open(DB_File,None, db.DB_BTREE, db.DB_CREATE)
curs = database.cursor()

while(True):
    name = input("Enter a student Name to look up: ")
    if(name == "q"): #Termination Condition
        break
    
    result = curs.set(name.encode("utf-8")) 
    #In the presence of duplicate key values, result will be set on the first data item for the given key. 
   
    if(result != None):
        print("List of students with this name and their marks:")
        print("Name: " + str(result[0].decode("utf-8")) + ", Mark: " + str(result[1].decode("utf-8")))
        
        #iterating through duplicates:
        dup = curs.next_dup()
        while(dup != None):
            print("Name: " + str(dup[0].decode("utf-8")) + ", Mark: " + str(dup[1].decode("utf-8")))
            dup = curs.next_dup()
    else:
        print("No Entry Found.")
            
    ToBeAdded = input("Do you want to insert the input name into the database?(Enter y for yes) ")
    
    if(ToBeAdded == "y"):
        database.put(name.encode("utf-8"), input("Insert Mark: "))

curs.close()
database.close()

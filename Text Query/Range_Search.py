from bsddb3 import db
DB_File = "students.db"
database = db.DB()
database.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
database.open(DB_File,None, db.DB_BTREE, db.DB_CREATE)
curs = database.cursor()

while(True):
    
    Starting_Name = input("Enter the Starting_Name: ")
    Ending_Name = input("Enter the Ending_Name: ")
    
    #get the record that has the smallest key greater than or equal to the Starting Name:
    result = curs.set_range(Starting_Name.encode("utf-8")) 
   
    if(result != None):
        print("List of found students:")
    
        while(result != None):
            #Checking the end condition: If the student's name comes after(or equal to) Ending_Name
            if(str(result[0].decode("utf-8")[0:len(Ending_Name)])>=Ending_Name): 
                break
            
            print("Name: " + str(result[0].decode("utf-8")) + ", Mark: " + str(result[1].decode("utf-8")))
            result = curs.next() 
    else:
        print("No student was found")
            
    NewSearch = input("Do you want to start a new search?(press y for yes) ")
    if(NewSearch != "y"): #Termination Condition
        break

curs.close()
database.close()

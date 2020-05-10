import sqlite3
import time
import hashlib

conn = None
c = None

def connect(path):
    global conn, c

    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    conn.commit()
    return

def drop_tables():
    global conn, c

    c.execute("drop table if exists demeritNotices;")
    c.execute("drop table if exists tickets;")
    c.execute("drop table if exists registrations;")
    c.execute("drop table if exists vehicles;")
    c.execute("drop table if exists marriages;")
    c.execute("drop table if exists births;")
    c.execute("drop table if exists persons;")
    c.execute("drop table if exists payments;")
    c.execute("drop table if exists users;")
    
    conn.commit()
    
def define_tables():
    global conn, c
    
    c.execute('''create table persons (
  fname		char(12),
  lname		char(12),
  bdate		date,
  bplace	char(20), 
  address	char(30),
  phone		char(12),
  primary key (fname, lname)
); ''')
    
    c.execute('''create table births (
  regno		int,
  fname		char(12),
  lname		char(12),
  regdate	date,
  regplace	char(20),
  genderegister	char(1),
  f_fname	char(12),
  f_lname	char(12),
  m_fname	char(12),
  m_lname	char(12),
  primary key (regno),
  foreign key (fname,lname) references persons,
  foreign key (f_fname,f_lname) references persons,
  foreign key (m_fname,m_lname) references persons
);''')
    
    c.execute('''create table marriages (
  regno		int,
  regdate	date,
  regplace	char(20),
  p1_fname	char(12),
  p1_lname	char(12),
  p2_fname	char(12),
  p2_lname	char(12),
  primary key (regno),
  foreign key (p1_fname,p1_lname) references persons,
  foreign key (p2_fname,p2_lname) references persons
);''')
    
    c.execute('''create table vehicles (
  vin		char(5),
  make		char(10),
  model		char(10),
  year	egister	int,
  color		char(10),
  primary key (vin)
);''')    
    
    c.execute('''create table registrations (
  regno		int,
  regdate	date,
  expiry	date,
  plate		char(7),
  vin		char(5), 
  fname		char(12),
  lname		char(12),
  primary key (regno),
  foreign key (vin) references vehicles,
  foreign key (fname,lname) references persons
);''')
    
    
    c.execute('''create table tickets (
  tno		int,
  regno		int,
  fine		int,
  violation	text,
  vdate		date,
  primary key (tno),
  foreign key (regno) references registrations
);''')
    
    c.execute('''create table demeritNotices (
  ddate		date, 
  fname		char(12), 
  lname		char(12), 
  points	int, 
  desc		text,
  primary key (ddate,fname,lname),
  foreign key (fname,lname) references persons
);''')
    
    c.execute('''create table payments (
  tno		int,
  pdate		date,
  amount	int,
  primary key (tno, pdate),
  foreign key (tno) references tickets
);''')
    
    c.execute('''create table users (
  uid		char(8),
  pwd		char(8),
  utype		char(1),	-- 'a' for agents, 'o' for officers
  fname		char(12),
  lname		char(12), 
  city		char(15),
  primary key(uid),
  foreign key (fname,lname) references persons
);''')    
    
    conn.commit()

def insert_data():
    global conn, c
    
    conn.commit()    
    
def function_name1():
    global conn, c
    
    conn.commit()
    
def function_name2():
    global conn, c
    
    conn.commit()
    
def function_name3():
    global conn, c
    
    conn.commit()    

def process_bill(provide_vin, provide_fname, provide_lname, provide_platenum):
    
    global conn, c
    
    conn.row_factory = sqlite3.Row
    
    c.execute('''SELECT r.fname, r.lname
       FROM vehicles v, registrations r
       WHERE v.vin = r.vin AND r.vin = ? AND r.plate = ?
       ORDER BY r.regdate DESC
       limit 1;''', (provide_vin, provide_platenum))
    
    name = c.fetchall()
    
    if name == []:
        print("Sorry, the name you provided is not in our database.")
    
    elif (provide_fname == name[0][0]) and (provide_lname == name[0][1]):
        #end current registration
        c.execute('''UPDATE registrations
        SET expiry = datetime('time') 
        WHERE fname = ? and lname = ?;''', (provide_fname, provide_lname))
        
        #make new registration
        new_regno = random.randint(0, 1000)
        
        c.execute('''INSERT INTO registrations(regno, regdate, expiry, plate, vin, fname, lname) 
                     VALUES (?, datetime('now'), datetime('now', '1 year'), ?, ?, ?, ?);''', (new_regno, provide_platenum, provide_vin, provide_fname, provide_lname))
        
    
    conn.commit()
    return     

def process_payment(ticketnum, amount):
    global conn, c
    
    c.execute('''SELECT tno FROM tickets;''')
    
    tno = c.fetchall()
    
    for t in tno:
        if t==ticketnum:
            c.execute('''SELECT sum(amount) 
            FROM payments
            WHERE tno = ?;''', ticketnum)
            
            total = c.fetchall()
            
            c.execute('''SELECT fine 
            FROM tickets
            WHERE tno = ?;''', ticketnum)  
            
            fine = c.fetchall()
            
            if fine > (total+amount): #sum of those payments cannot exceed the fine amount of ticket
                c.execute('''INSERT INTO payments(tno, pdate, amount
                VALUES (?, datetime('now'), ?);''', (ticketnum, amount))
                
            
    conn.commit()
    
def get_driver_abstract(fname, lname):
    global conn, c
    
    c.execute('''SELECT count(t.tno)
    FROM registrations r, tickets t
    WHERE r.regno = t.regno 
    and r.fname = ? and r.lname = ?;''', (fname, lname))
    
    num_tickets = c.fetchall()
    
    print(num_tickets)
    
    print("The number of ticket is %d" % num_tickets[0])
    
    c.execute('''SELECT count(*)
    FROM demeritNotices d
    WHERE d.fname = ? and d.lname = ?;''', (fname, lname))
    
    num_dnotices = c.fetchall()
    
    print(num_dnotices)
    
    print("The number of demerit notices is %d" % num_dnotices[0])
    
    c.execute('''SELECT COALESCE(SUM(d.points),0)
    FROM demeritNotices d
    WHERE d.fname = ? and d.lname = ?
    and d.ddate >= datetime('now', '-2 years');''', (fname, lname))
    
    points_2years = c.fetchall()
    
    print(points_2years)
    
    print("The total number of demerit points received within 2 years is %d" % points_2years[0])
    
    c.execute('''SELECT COALESCE(SUM(d.points),0)
    FROM demeritNotices d
    WHERE d.fname = ? and d.lname = ?;''', (fname, lname))
    
    points_lifetime = c.fetchall()
    
    print(points_lifetime)
    
    print("The total number of demerit points received within life time is %d" % points_lifetime[0])
    
    check = input("Would you like to see the tickets ordered form te latest to the oldest?(Y/N): ")
    if check == 'Y' or check == 'y':
        c.execute('''SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model
        FROM tickets t, vehicles v, registrations r
        WHERE t.regno = r.regno and r.vin = v.vin
        and r.fname = ? and r.lname = ?
        ORDER BY t.vdate DESC;''', (fname, lname))
        
        tickets_infor = c.fetchall()
        
        ticketsNum = 0
        for t in tickets_infor:
            ticketsNum += 1
            if ticketsNum <= 5:
                print(t)
            else:
                see_more = input("Would you like to see more tickets information?(Y/N): ")
                if see_more == 'y' or see_more == 'Y':
                    print(t)
                    
        print(ticketsNum)
        
    conn.commit()
    
def function_name7():
    global conn, c
    
    conn.commit()
    
def function_name8():
    global conn, c
    
    conn.commit()
 

def main():
    global conn, c
    
    #path = input("Enter the name of database: ")
    path="./a3.db"
    
    connect(path)
    drop_tables()
    define_tables()
    insert_data()
    
    #4
    user_vin = input("Please provide the vin of a car: ")
    currentowner_fname = input("Please provide the first name of the current owner: ")
    currentowner_lname = input("Please provide the last name of the current owner: ")
    plate_number = input("Please provide a plate number for the new registration: ")
    process_bill(user_vin, currentowner_fname, currentowner_lname, plate_number)
    
    #5
    ticket_number = input("Please input a valid ticket number: ")
    amount = ("Please input the amount you would like to pay:")
    process_payment(ticket_number, amount)
    
    #6
    driver_fname = input("Please enter the first name of the driver: ")
    driver_lname = input("Please enter the last name of the driver: ")
    get_driver_abstract(driver_fname, driver_lname)
    
    
    conn.commit()
    conn.close()
    return

if __name__ == "__main__":
    main()
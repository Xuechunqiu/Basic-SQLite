import sqlite3
import time
import hashlib
import datetime
import getpass
import re

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
    try:
        c.execute("drop table if exists demeritNotices;")
        c.execute("drop table if exists marriages;")
        c.execute("drop table if exists births;")
        c.execute("drop table if exists payments;")
        c.execute("drop table if exists tickets;")
        c.execute("drop table if exists registrations;")
        c.execute("drop table if exists vehicles;")
        c.execute("drop table if exists users;")
        c.execute("drop table if exists persons;")
    except sqlite3.Error as e:
        print('Error:', e.args[0])  
    
    conn.commit()
    
def define_tables():
    global conn, c
    try:
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
        
        
    except sqlite3.Error as e:
        print('Error:', e.args[0])    
    
    conn.commit()

def insert_data():
    global conn, c
    
    try:
        c.executescript('''
        insert into persons values ('Michael','Fox','1961-06-09','Edmonton, AB','Manhattan, New York, US', '212-111-1111');
        insert into persons values ('Walt', 'Disney', '1901-12-05', 'Chicago, US', 'Los Angeles, US', '213-555-5555');
        insert into persons values ('Lillian', 'Bounds', '1899-02-15', 'Spalding, Idaho', 'Los Angeles, US', '213-555-5556');
        insert into persons values ('John', 'Truyens', '1907-05-15', 'Flanders, Belgium', 'Beverly Hills, Los Angeles, US', '213-555-5558');
        insert into persons values ('Mickey', 'Mouse', '1928-01-05', 'Disneyland, FL', 'Anaheim, US', '714-555-5551');
        insert into persons values ('Minnie', 'Mouse', '1928-02-04', 'Anaheim, US', 'Anaheim, US', '714-555-5551');
        insert into persons values ('Amalia', 'Kane', '1928-07-03', 'Marvin Plains, OK', 'Toronto, ON', '534-529-7567');
        insert into persons values ('Horace', 'Combs', '1965-10-02', 'Anaheim, US', 'Anaheim, US', '500-986-3991');
        insert into persons values ('Wendy', 'Ballard', '1953-05-15', 'Halifax, NS', 'Fort McMurray, AB', '203-347-1629');
        insert into persons values ('Stacey', 'Long', '1953-05-15', 'Halifax, NS', 'Fort McMurray, AB', '203-347-1629');
        insert into persons values ('Mia', 'Warner', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Davood','Rafiei',date('now','-21 years'),'Iran','100 Lovely Street,Edmonton,AB', '780-111-2222');
        insert into persons values ('Throw', 'Away', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q2', 'BothSameParent', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q2', 'OnlyMother', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q2', 'OnlyFather', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q2', 'NULLFather', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('MF', 'MGrandFather', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('MF', 'FGrandFather', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q3', 'MGDaughter', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q3', 'MGSon', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q3', 'FGDaughter', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q3', 'FGSon', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q3', 'MGDaughterD', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q3', 'MGSonSon', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q3', 'FGDaughterD', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q3', 'FGSonSon', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q4', 'MFYoung', '2015-07-22', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q4', 'MFMid', '2001-08-15', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q4', 'MFOld', '1989-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q4', 'MFOld2', '1989-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q5', 'OutOfDate', '1989-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q5', 'Single20', '1989-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q5', 'Multi20', '1989-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q6', 'MarOld', '1989-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q6', 'MarNew', '1989-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q6', 'MarMid', '1989-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q7', 'NoTicket', '1989-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        insert into persons values ('Q9', 'CarnoTick', '1989-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
        
        
        
        insert into births values (100,'Mickey', 'Mouse', '1928-02-05', 'Anaheim, US', 'M', 'Walt', 'Disney', 'Lillian', 'Bounds');
        insert into births values (200,'Minnie', 'Mouse', '1928-02-04', 'Anaheim, US', 'F', 'Walt', 'Disney', 'Lillian', 'Bounds');
        insert into births values (300,'Michael', 'Fox', '1961-06-09', 'Edmonton, AB', 'M', 'John', 'Truyens', 'Amalia', 'Kane');
        insert into births values (400,'Q2', 'BothSameParent', '1953-05-15', 'Halifax, NS', 'F', 'John', 'Truyens', 'Amalia', 'Kane');
        insert into births values (500,'Q2', 'OnlyMother', '1944-12-25', 'St John, NB', 'F', 'Davood', 'Rafiei', 'Amalia', 'Kane');
        insert into births values (600,'Q2', 'OnlyFather', '1944-12-25', 'St John, NB', 'M', 'John', 'Truyens', 'Mia', 'Warner');
        insert into births values (700,'Michael', 'Fox', '1961-06-09', 'Edmonton, AB', 'M', NULL, NULL, 'Amalia', 'Kane');
        insert into births values (800,'Q2', 'NULLFather', '1944-12-25', 'St John, NB', 'F', NULL, NULL, 'Mia', 'Warner');
        insert into births values (900,'John', 'Truyens', '1944-12-25', 'St John, NB', 'F', 'MF', 'FGrandFather', 'Stacey', 'Long');
        insert into births values (101,'MF', 'FGrandFather', '1944-12-25', 'St John, NB', 'M', 'Davood', 'Rafiei', 'Horace', 'Combs');
        insert into births values (102,'Amalia', 'Kane', '1944-12-25', 'St John, NB', 'M', 'MF', 'MGrandFather', 'Minnie', 'Mouse');
        insert into births values (103,'MF', 'MGrandFather', '1944-12-25', 'St John, NB', 'M', 'Davood', 'Rafiei', 'Horace', 'Combs');
        insert into births values (104,'Q3', 'MGDaughter', '1944-12-25', 'St John, NB', 'M', 'MF', 'MGrandFather', 'Stacey', 'Long');
        insert into births values (105,'Q3', 'MGSon', '1944-12-25', 'St John, NB', 'M', 'MF', 'MGrandFather', 'Throw', 'Away');
        insert into births values (106,'Q3', 'FGDaughter', '1944-12-25', 'St John, NB', 'M', 'MF', 'FGrandFather', 'Stacey', 'Long');
        insert into births values (107,'Q3', 'FGSon', '1944-12-25', 'St John, NB', 'M', 'MF', 'FGrandFather', 'Throw', 'Away');
        insert into births values (108,'Q3', 'MGDaughterD', '1944-12-25', 'St John, NB', 'M', 'Throw', 'Away', 'Q3', 'MGDaughter');
        insert into births values (109,'Q3', 'MGSonSon', '1944-12-25', 'St John, NB', 'M', 'Q3', 'MGSon', 'Throw', 'Away');
        insert into births values (110,'Q3', 'FGDaughterD', '1944-12-25', 'St John, NB', 'M', 'Throw', 'Away', 'Q3', 'FGDaughter');
        insert into births values (111,'Q3', 'FGSonSon', '1944-12-25', 'St John, NB', 'M', 'Q3', 'FGSon', 'Throw', 'Away');
        insert into births values (112,'Q4', 'MFYoung', '1944-12-25', 'St John, NB', 'M', 'Michael', 'Fox', 'Throw', 'Away');
        insert into births values (113,'Q4', 'MFMid', '1944-12-25', 'St John, NB', 'M', 'Michael', 'Fox', 'Throw', 'Away');
        insert into births values (114,'Q4', 'MFOld', '1944-12-25', 'St John, NB', 'M', 'Michael', 'Fox', 'Throw', 'Away');
        insert into births values (115,'Q4', 'MFOld2', '1944-12-25', 'St John, NB', 'M', 'Michael', 'Fox', 'Throw', 'Away');
        
        
        
        insert into marriages values (200, '1925-07-13', 'Idaho, US', 'Walt', 'Disney', 'Lillian', 'Bounds');
        insert into marriages values (201, '1969-05-03', 'Los Angeles, US', 'Lillian', 'Bounds', 'John', 'Truyens');
        insert into marriages values (202, '2000-05-03', 'Los Angeles, US', 'Michael', 'Fox', 'Q6', 'MarOld');
        insert into marriages values (203, '2001-07-01', 'Los Angeles, US', 'Q6', 'MarMid', 'Michael', 'Fox');
        insert into marriages values (204, '2003-10-09', 'Los Angeles, US', 'Michael', 'Fox', 'Q6', 'MarNew');
        
        
        insert into vehicles values ('U200', 'Chevrolet', 'Camaro', 1969, 'red');
        insert into vehicles values ('U201', 'Toyoto', 'Corolla', 2012, 'red');
        insert into vehicles values ('U202', 'Toyoto', 'RAV4', 2013, 'red');
        insert into vehicles values ('U203', 'Kia', 'Cube', 2013, 'red');
        
        insert into vehicles values ('U300', 'Mercedes', 'SL 230', 1964, 'black');
        insert into vehicles values ('U301', 'Audi', 'A4', 2013, 'black');
        insert into vehicles values ('U302', 'Toyoto', 'RAV4', 2012, 'black');
        insert into vehicles values ('U303', 'Mercedes', 'SL 230', 2014, 'black');
        insert into vehicles values ('U400', 'Chevrolet', 'Camaro', 2012, 'black');
        
        
        insert into vehicles values ('U500', 'Chevrolet', 'Camaro', 1969, 'white');
        insert into vehicles values ('U501', 'Audi', 'A4', 2012, 'white');
        insert into vehicles values ('U502', 'Chevrolet', 'Camaro', 2012, 'white');
        insert into vehicles values ('U503', 'Toyoto', 'Corolla', 2012, 'white');
        insert into vehicles values ('U504', 'Chevrolet', 'Camaro', 2014, 'white');
        insert into vehicles values ('U505', 'Audi', 'A4', 2013, 'white');
        insert into vehicles values ('U506', 'Audi', 'A4', 2014, 'white');
        insert into vehicles values ('U507', 'Audi', 'A4', 2015, 'white');
        insert into vehicles values ('U508', 'Audi', 'A4', 2016, 'white');
        insert into vehicles values ('U509', 'Audi', 'A4', 2014, 'white');
        insert into vehicles values ('U510', 'Chevrolet', 'Camaro', 2012, 'white');
        insert into vehicles values ('U601', 'Toyota', '123', 2019, 'maroon');
        insert into vehicles values ('U600', 'Porsche', '911', 2014, 'maroon');
        
        
        
        
        insert into registrations values (300, '1964-05-26','1965-05-25', 'DISNEY','U300', 'Walt', 'Disney');
        insert into registrations values (302, '1980-01-16','1981-01-15', 'LILLI','U200', 'Lillian', 'Bounds');
        insert into registrations values (301, '1981-06-26','2020-07-15', 'M7F8J2','U400', 'Wendy', 'Ballard');
        insert into registrations values (303, '1991-01-26','2007-07-25', 'Z7F9J2','U500', 'Davood', 'Rafiei');
        insert into registrations values (304, '2012-01-26','2020-07-25', 'Z7F9J2','U201', 'John', 'Truyens');
        insert into registrations values (305, '2013-01-26','2021-07-25', 'Z7F9J2','U202', 'Minnie', 'Mouse');
        insert into registrations values (306, '1913-01-26','2018-07-25', 'Z7F9J2','U203', 'Amalia', 'Kane');
        insert into registrations values (307, '2013-01-26','2020-07-25', 'Z7F9J2','U301', 'Amalia', 'Kane');
        insert into registrations values (308, '2012-01-26','2001-07-25', 'Z7F9J2','U302', 'Horace', 'Combs');
        insert into registrations values (311, '2012-01-26','2008-07-25', 'Z7F9J2','U501', 'Horace', 'Combs');
        insert into registrations values (309, '2012-01-26','2030-07-25', 'Z7F9J2','U502', 'Davood', 'Rafiei');
        insert into registrations values (310, '2013-01-26','2021-07-25', 'Z7F9J2','U505', 'Stacey', 'Long');
        
        insert into registrations values (312, '2019-01-26','2031-07-25', 'Z7F9J2','U506', 'Mia', 'Warner');
        insert into registrations values (313, '2019-02-26','2021-07-25', 'Z7F9J2','U507', 'Mia', 'Warner');
        insert into registrations values (314, '2019-03-26','2041-07-25', 'Z7F9J2','U508', 'Davood', 'Rafiei');
        insert into registrations values (315, '2019-04-26','2025-07-25', 'Z7F9J2','U509', 'Davood', 'Rafiei');
        insert into registrations values (316, '2019-04-26','2025-07-25', 'Z7F9J2','U510', 'Q9', 'CarnoTick');
        
        insert into registrations values (317, '2019-04-26','2025-07-25', 'Z7F9J2','U600', 'Q7', 'NoTicket');
        insert into registrations values (318, '2012-01-26','2020-07-25', 'Z7F9J2','U506', 'John', 'Truyens');
        
        
        insert into tickets values (400,300,4,'speeding','1964-08-20');
        insert into tickets values (401,302,10,'speeding','2019-08-20');
        insert into tickets values (402,304,10,'speeding','2018-08-20');
        insert into tickets values (403,305,15,'speeding','2019-08-20');
        insert into tickets values (404,306,30,'speeding','2017-08-20');
        insert into tickets values (405,307,30,'speeding','2019-09-21');
        insert into tickets values (406,305,20,'speeding','2019-01-20');
        insert into tickets values (407,305,60,'speeding','2019-04-20');
        
        insert into tickets values (408,312,10,'speeding','2019-04-20');
        insert into tickets values (409,312,10,'speeding','2019-05-20');
        insert into tickets values (410,312,10,'red liGht pass in toronto','2019-06-20');
        insert into tickets values (411,313,10,'speeding','2019-07-20');
        insert into tickets values (412,313,10,'speeding','2019-08-20');
        
        insert into tickets values (413,314,10,'speeding','2019-04-20');
        insert into tickets values (414,314,12,'passed in red light of calgary','2019-05-20');
        insert into tickets values (415,315,14,'speeding','2019-06-20');
        insert into tickets values (416,315,15,'dasin rEd lIght VIOLATION','2019-07-20');
        insert into tickets values (440,303,10,'speeding','2019-05-20');
        insert into tickets values (441,314,50,'speeding','2019-07-20');
        insert into tickets values (442,309,10,'speeding','2019-06-20');
        
        insert into demeritNotices values ('1964-08-20', 'Walt', 'Disney', 2, 'Speeding');
        insert into demeritNotices values ('2014-08-20', 'Q5', 'OutOfDate', 3, 'Speeding');
        insert into demeritNotices values ('2015-08-20', 'Q5', 'OutOfDate', 10, 'Speeding');
        insert into demeritNotices values ('2016-08-20', 'Q5', 'OutOfDate', 1, 'Speeding');
        insert into demeritNotices values ('2011-08-20', 'Q5', 'OutOfDate', 4, 'Speeding');
        insert into demeritNotices values ('2010-08-20', 'Q5', 'OutOfDate', 2, 'Speeding');
        insert into demeritNotices values ('2019-08-20', 'Q5', 'Single20', 20, 'Drunk Driving');
        insert into demeritNotices values ('2019-01-20', 'Q5', 'Multi20', 3, 'Drunk Driving');
        insert into demeritNotices values ('2019-04-20', 'Q5', 'Multi20', 15, 'Drunk Driving');
        insert into demeritNotices values ('2019-10-05', 'Q5', 'Multi20', 7, 'Drunk Driving');
        
        INSERT INTO payments VALUES (407, '2019-01-04', 10);
        
        INSERT INTO users VALUES ('Mf1', 'Michael1', 'a', 'Michael','Fox', 'New York');
        INSERT INTO users VALUES ('Wd*', 'Walt-123', 'a', 'Walt', 'Disney', 'Chicago');
        INSERT INTO users VALUES ('Lb11', 'Lilli?/', 'o', 'Lillian', 'Bounds', 'Los Angeles');
        INSERT INTO users VALUES ('Mm%23', 'Mickey', 'a', 'Mickey', 'Mouse', 'Anaheim');
        INSERT INTO users VALUES ('456', '456', 'a', 'Davood', 'Rafiei', 'Edmonton');
        INSERT INTO users VALUES ('123', '123', 'o', 'Mickey', 'Mouse', 'Anaheim');
    
        ''')
    except sqlite3.Error as e:
        print('Error:', e.args[0])    
    
    conn.commit()    

def login():
    
    global conn, c
    
    check_userid = False
    C = False
    while not check_userid:
        try:
            userid = input('Enter the user id: ')
            if len(userid) > 8:
                print ("Sorry, the user id should not more than 8")
            else:
                check_userid = True
                a = c.execute('''select uid, pwd from users;''')
                b = {}
                for infor in a:
                    b[infor[0]] = infor[1]
                
                if userid in b.keys():
                    password = getpass.getpass('Enter your password(your passward will be hidden): ')
                    assert len(password)<=8, "The length of password should less than 8 characters."            
                    if password == b[userid]:
                        C = True
                    else:
                        print('Wrong password,please try again')
                else:
                    print('Wrong username,please try again')
                
        except AssertionError as e:
                print(e.args[0])
        except:
            print("The information you entered is invalid, please try again.")
        
    conn.commit()
    return C, userid  

def registrate_birth(user_id):
    global conn, c
    
    try:
        print("To registrate the birth, please follow the guide: ")
    #---------input the baby name----------------------------------------
        unique = False
        while not unique:
            while True:
                try:
                    fn = input("please enter the first name(length <= 12): ")
                    assert len(fn) <= 12, "The name you entered exceeds the capacity(12 characters), please try again."
                    assert re.match("^[A-Za-z0-9-]*$", fn), "The name you entered contains some characters not alphabets, digits or -, please try again."
                    
                    ln = input("please enter the last name(length <= 12): ")
                    assert len(ln) <= 12, "The name you entered exceeds the capacity(12 characters), please try again."
                    assert re.match("^[A-Za-z0-9-]*$", ln), "The name you entered contains some characters not alphabets, digits or -, please try again."
                    break;
                except AssertionError as e:
                    print(e.args[0])
                except:
                    print("You enter something wrong, please enter again")            
            
            c.execute("SELECT fname,lname From persons WHERE lower(fname) = lower(?) And lower(lname) = lower(?) ;", (fn,ln))
            check = c.fetchall()
            if check != []:
                print("The name has already been used, please use another one! ")
            else: 
                unique = True 
                
    #----------GENDER----------------------------------            
        while True:    
            g = input("please enter your gender(M/F) < We will choose the first letter of the word> : ")
            if g[0] in ['m','f','M','F']:
                gender = g[0].upper()
                break
            else:
                print("You enter something wrong, please enter again")
                
    #---------Baby's BIRTH DATE---------------------------------  
        while True:
            bd = input("please enter your birth date(YYYY-MM-DD, i.e. 2000-01-01): ")
            try:
                bd = datetime.datetime.strptime(bd, '%Y-%m-%d').date()
                break
            except:
                print ("Invaild date, enter again!")
        
    #----------BIRTH PLACE--------------------------------------
        while True:
            bp = input("please enter your birth place(length <= 20): ")
            if bp.isalpha() and len(bp) <= 20:
                break
            else:
                print("Your birth place is wrong, please enter again")
                
            
    #-------MOTHER's NAME------------------------------------------
        while True:
            m_fn  = input("please enter your mother first name(length <= 12): ")
            if re.match("^[A-Za-z0-9-]*$", m_fn) and len(m_fn) <= 12:
                break
            else:
                print("You enter something wrong, please enter again")
                    
            
        while True:        
            m_ln  = input("please enter your mother last name(length <= 12): ")
            if re.match("^[A-Za-z0-9-]*$", m_ln) and len(m_ln) <= 12:
                break
            else:
                print("You enter something wrong, please enter again")
            
        c.execute("SELECT fname,lname FROM persons WHERE lower(fname) = lower(?) and lower(lname) = lower(?) ;", (m_fn, m_ln))
        mother = c.fetchall()        
        if mother == []:
            print("mother does not exist.\n")
                            
            #-------MOTHER BIRTH DATE--------------------                 
            while True: 
                m_bd = input("please enter mother's birth date(YYYY-MM-DD): ")
                if m_bd == '':
                    break
                else:
                    try:
                        m_bd = datetime.datetime.strptime(m_bd, '%Y-%m-%d').date()
                        break
                    except:
                        print ("Invaild date, enter again!")  
                    
            #----------M BIRTH PLACE--------------------------------          
            while True:
                m_bp = input("please enter mother's birth place(length <= 20): ")
                if m_bp == '':
                    break
                else:
                    if m_bp.isalpha() and len(m_bp) <=20:
                        break
                    else:
                        print("Your birth place is wrong, please enter again")
                             
            #----------MOTHER'S ADDRESS---------------------                   
            while True:
                m_address = input("please enter mother's address(length <= 30): ")
                if m_address == '':
                    break
                else:
                    if len(m_address) <= 30:
                        break
                    else:
                        print("Your address out of the range, please enter again")
                    
            #-------MOTHER PHONE NUMBER---------------------------
            while True:
                m_phone = input("please enter mother's phone number(XXXXXXXXXX): ")
                
                if m_phone == '':
                    break
                else:
                    if len(m_phone)<=12 and m_phone.isdigit():
                        m_phone = str(m_phone[0:3]) + '-' + str(m_phone[3:6]) + '-' + str(m_phone[6:])
                        break
                    else:
                        print("The phone number you entered is wrong, please enter again.")
                            
            c.execute('''INSERT INTO persons VALUES(?,?,?,?,?,?);''',(m_fn,m_ln,m_bd,m_bp,m_address,m_phone))
            
            print("Mother's name is successfully added into database.\n")
                        
    
        #----------FATHER'S NAME-----------------------
        while True:
            f_fn  = input("please enter your father first name(length <= 12): ")
            if re.match("^[A-Za-z0-9-]*$", f_fn) and len(f_fn) <= 12:
                break
            else:
                print("You enter something wrong, please enter again")
            
        while True:
            f_ln  = input("please enter your father last name(length <= 12): ")
            if re.match("^[A-Za-z0-9-]*$", f_ln) and len(f_ln) <= 12:
                break
            else:
                print("You enter something wrong, please enter again")
            
        c.execute("SELECT fname,lname FROM persons WHERE lower(fname) = lower(?) and lower(lname) = lower(?);",(f_fn, f_ln))
        father = c.fetchall()
        if father == []:
            print("father does not exist.\n")  
                        
            #----------FATHER BIRTH DATE--------------------                    
            while True:
                f_bd = input ("please enter father's birth date(YYYY-MM-DD): ")
                if f_bd == '':
                    break
                else:
                    try:
                        f_bd = datetime.datetime.strptime(f_bd, '%Y-%m-%d').date()
                        break
                    except:
                        print ("Invaild date, enter again!")
    
            #----------FATHER'S BIRTH PLACE-------------------------                 
            while True:
                f_bp = input("please enter father's birth place: ")
                if f_bp == '':
                    break
                else:
                    if f_bp.isalpha() and len(f_bp) <= 20:
                        break
                    else:
                        print("Your birth place is wrong, please enter again")
                        
                        
            #----------FATHER'S ADDRESS---------------------
            while True:
                f_address = input("please enter father's address: ")
                if f_address == '':
                    break
                else:
                    if len(f_address) <= 30:
                        break
                    else:
                        print("Your address out of the range, please enter again")
            
            #-------FATHER PHONE NUMBER--------------------------------------
            while True:
                f_phone = input("please enter father's phone number(XXXXXXXXXX): ")
                if f_phone != '':
                    if len(f_phone)<=12 and f_phone.isdigit():
                        f_phone = str(f_phone[0:3]) + '-' + str(f_phone[3:6]) + '-' + str(f_phone[6:])
                        break
                    else:
                        print("The phone number you entered is wrong, please enter again.")
                else:
                    break
                    
            c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?);",(f_fn,f_ln,f_bd,f_bp,f_address,f_phone))
            print("Father's information has successfully added into database.\n")
        
        c.execute("SELECT fname,lname FROM persons WHERE fname=:first and lname=:last;",{"first":m_fn, "last":m_ln})
        mother = c.fetchall()
        m_fn = mother[0][0]
        m_ln = mother[0][1]
        
        c.execute("SELECT fname,lname FROM persons WHERE fname=:first and lname=:last;",{"first":f_fn, "last":f_ln})
        father = c.fetchall()
        f_fn = father[0][0]
        f_ln = father[0][1]    
        
        c.execute("SELECT address,phone FROM persons WHERE fname=:first and lname=:last;",{"first":m_fn, "last":m_ln})   
        infor = c.fetchall()
        address = infor[0][0]
        phone = infor[0][1]
    
    #make new registration
        c.execute('''SELECT max(regno) FROM births;''')
        regno = c.fetchall()
        rn = regno[0][0]+1
        
    #REGISTRATION PLACE
        #user_id = input("please enter your uid: ")
        c.execute("SELECT city FROM users WHERE uid =?;",(user_id,))
        rp = c.fetchall()
        rp=rp[0][0]
        
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?);",(fn,ln,bd,bp,address,phone))
            
        c.execute('''INSERT INTO births VALUES (?,?,?,date('now'),?,?,?,?,?,?);''', (rn,fn,ln,rp,gender,f_fn,f_ln,m_fn,m_ln))
        print("New birth has successfully added into database.\n")
    
    except sqlite3.Error as e:
        print('Error:', e.args[0])    
    
    conn.commit()


def registrate_marriage(user_id):
    global conn, c
    try:
        #---------PATRNER 1 NAME-------------------------------    
        while True:
            p_fn  = input("please enter the first name of partner1(length <= 12): ")
            if re.match("^[A-Za-z0-9-]*$", p_fn) and len(p_fn) <= 12:
                break
            else:
                print("You enter something wrong, please enter again")
                
        while True:        
            p_ln  = input("please enter the last name of partner1(length <= 12): ")
            if re.match("^[A-Za-z0-9-]*$", p_ln) and len(p_ln) <= 12:
                break
            else:
                print("You enter something wrong, please enter again")
                
    #---------PATRNER 2 NAME------------------------------------     
       
        while True:
            p2_fn  = input("please enter the first name of partner2(length <= 12): ")
            if re.match("^[A-Za-z0-9-]*$", p2_fn) and len(p2_fn)<=12:
                break
            else:
                print("You enter something wrong, please enter again")
                
        while True:
            p2_ln  = input("please enter the last name of partner2(length <= 12): ") 
            if re.match("^[A-Za-z0-9-]*$", p2_ln) and len(p2_ln) <=12:
                break
            else:
                print("You enter something wrong, please enter again")
            
        
        c.execute('''SELECT fname,lname FROM persons WHERE lower(fname) = lower(?) and lower(lname) = lower(?);''',(p_fn, p_ln))
        partner1 = c.fetchall()
        c.execute('''SELECT fname,lname FROM persons WHERE lower(fname) = lower(?) and lower(lname) = lower(?) ;''',(p2_fn, p2_ln))
        partner2 = c.fetchall()
    
        #----------CHECK PARTNER 1----------------------------------    
        if (partner1 == []):
            print("partner1 does not exist.\n")
    
            #-----------p1 BIRTH DATE----------------------------                
            while True:        
                p_bd = input("please enter partner1's birth date(YYYY-MM-DD): ")
                if p_bd == '':
                    break
                else:
                    try:
                        p_bd = datetime.datetime.strptime(p_bd, '%Y-%m-%d').date() 
                        break
                    except:
                        print ("Invaild date, enter again!")  
    
            #----------PARTNER 1 BIRTH PLACE-----------------                
            while True:
                p_bp = input("please enter partner1's birth place(length <= 20): ")
                if p_bp == '':
                    break
                else:
                    if p_bp.isalpha() and len(p_bp)<= 20:
                        break
                    else:
                        print("Your birth place is wrong, please enter again")
                        
            #----------PARTNER 1 ADDRESS----------------------                    
            while True:
                p_address = input("please enter partner1's address(length <= 30): ")
                if p_address == '':
                    break
                else:
                    if len(p_address) <= 30:
                        break
                    else:
                        print("Your address out of the range, please enter again")
            
            #----------PARTNER 1 PHONE NUMBER---------------------        
            while True:
                p_phone = input("please enter partner1's phone number(XXXXXXXXXX): ")
                if p_phone == '':
                    break
                else:
                    if len(p_phone)<=12 and p_phone.isdigit():
                        p_phone = str(p_phone[0:3]) + '-' + str(p_phone[3:6]) + '-' + str(p_phone[6:])
                        break
                    else:
                        print("The phone number you entered is something wrong, please enter again")
            
            c.execute('''INSERT INTO persons VALUES(?,?,?,?,?,?);''',(p_fn,p_ln,p_bd,p_bp,p_address,p_phone))
            print("Partner1's information has successfully added.\n")
    
        #---------CHECK PARTNER 2--------------------------------        
        if (partner2 == []):
            print("Partner2 does not exist.\n")
    
            #----------p2 BIRTH DATE-------------------- 
            while True:        
                p2_bd = input("please enter partner2's birth date(YYYY-MM-DD): ")
                if p2_bd == '':
                    break
                else:
                    try:
                        p2_bd = datetime.datetime.strptime(p2_bd, '%Y-%m-%d').date()
                        break
                    except:
                        print ("Invaild date, enter again!")
    
        #----------p2 BIRTH PLACE--------------------------- 
            while True:
                p2_bp = input("please enter partner2's birth place(length <= 20): ")
                if p2_bp == '':
                    break
                else:
                    if p2_bp.isalpha() and len(p2_bp) <= 20:
                        break
                    else:
                        print("Your birth place is wrong, please enter again")
                        
                    
        #----------PARTNER 2 ADDRESS------------------------------------
            while True:
                p2_address = input("please enter partner2's address(length <= 20): ")
                if p2_address == '':
                    break
                else:
                    if len(p2_address) <= 20:
                        break
                    else:
                        print("Your address out of the range, please enter again")
            
        #----------PARTNER 2 PHONE NUMBER-----------------------------        
            while True:
                p2_phone = input("please enter partner2's phone number(XXXXXXXXXX): ")
                if p2_phone == '':
                    break
                else:
                    if len(p2_phone)<=12 and p2_phone.isdigit():
                        p2_phone = str(p2_phone[0:3]) + '-' + str(p2_phone[3:6]) + '-' + str(p2_phone[6:])
                        break
                    else:
                        print("You enter something wrong, please enter again")        
            
            c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?);",(p2_fn,p2_ln,p2_bd,p2_bp,p2_address,p2_phone))
            print("Partner2's information has successfully added!\n")
        
        #make new registration
        c.execute('''SELECT max(regno) FROM marriages;''')
        regno = c.fetchall()
        rn = regno[0][0]+1
        
        #REGISTRATION PLACE
        #user_id = input("please enter your uid: ")
        c.execute("SELECT city FROM users WHERE uid =?;",(user_id,))
        rp = c.fetchall()
        rp=rp[0][0]    
        
        c.execute("INSERT INTO marriages VALUES(?,date('now'),?,?,?,?,?);", (rn,rp,p_fn,p_ln,p2_fn,p2_ln))
        print("Marriage registrates successfully!\n")
    
    except sqlite3.Error as e:
        print('Error:', e.args[0])
        
    conn.commit()

def renew_vehicle():
    global conn, c
    try:
        while True:
            ren = input("please enter your registration number: ") #provide an existing registration number
            
            c.execute("""SELECT regno FROM registrations WHERE regno = ? ;""", (ren,))
            check = c.fetchall()
            if check != []:
                break
            else:
                print("Invaild registration number, please enter again")
                exit = input("Would you like to exit? (Y/y for yes, others for no): ")
                if exit == 'Y' or exit == 'y':
                    return
            
            
        c.execute("SELECT expiry FROM registrations WHERE regno = ?;", (ren,))
        old = c.fetchall()
        old_e = datetime.datetime.strptime(old[0][0], '%Y-%m-%d').date()
                               
        if old_e <= datetime.datetime.now().date(): #if the current registration either has expired or expires today.
            c.execute('''UPDATE registrations
                    SET expiry = date('now', '+1 year')
                    WHERE regno = ?;
                    ''',(ren,))
            print("The new expiry date has updated.\n")
        else:
            c.execute('''UPDATE registrations
                    SET expiry = date(?, '+1 year')
                    WHERE regno = ?;
                    ''',(old_e,ren))
            print("The new expiry date updates to one year later.\n")
    
    except sqlite3.Error as e:
        print('Error:', e.args[0])
        
    conn.commit() 

def process_bill():
    
    global conn, c
    try:
        exit = False
        while not exit:
            while True:
                try:
                    provide_vin = input("Please provide the vin of a car: ")
                    assert provide_vin != '' and len(provide_vin)<=5, "Please enter the valid vin which should be less or equal to 5 characters."
                    break
                except AssertionError as e:
                    print(e.args[0])
                except:
                    print("The information you entered is invalid, please try again.")    
            
            c.execute('''SELECT r.fname, r.lname
               FROM vehicles v, registrations r
               WHERE v.vin = r.vin AND lower(r.vin) = lower(?)
               ORDER BY r.regdate DESC
               limit 1;''', (provide_vin,))
            
            name = c.fetchall()
            
            if name == []:
                print("Sorry, the vin you provided doesn't belong to anyone in our database.")
                E = input("Would like to exit this function? (Y/y for yes, other for no): )")
                if E == 'Y' or E == 'y':
                    exit = True
                    
            else:
                while True:
                    try:
                        provide_platenum = input("Please provide a plate number for the new registration: ")
                        assert provide_platenum != '' and len(provide_platenum)<=7, "Please enter the valid plate number which should be less or equal to 7 characters."
                        break
                    except AssertionError as e:
                        print(e.args[0])
                    except:
                        print("The information you entered is invalid, please try again.")
                        
                while True:
                    try:
                        provide_fname = input("Please provide the first name of the current owner: ")
                        provide_lname = input("Please provide the last name of the current owner: ")            
                        assert len(provide_fname)<=12 and re.match("^[A-Za-z0-9-]*$", provide_fname), "Please enter the valid first name which should be less or equal to 12 characters."
                        assert len(provide_lname)<=12 and re.match("^[A-Za-z0-9-]*$", provide_lname), "Please enter the valid last name which should be less or equal to 12 characters."
                        break
                    except AssertionError as e:
                        print(e.args[0])
                    except:
                        print("The information you entered is invalid, please try again.")        
                
                if (provide_fname.lower() == name[0][0].lower()) and (provide_lname.lower() == name[0][1].lower()):
                    #end current registration
                    c.execute('''UPDATE registrations
                    SET expiry = date('now') 
                    WHERE lower(fname) = lower(?) and lower(lname) = lower(?);''', (provide_fname, provide_lname))
                    
                    #make new registration
                    c.execute('''SELECT max(regno) FROM registrations;''')
                    regno = c.fetchall()
                    new_regno = regno[0][0]+1
                    
                    while True:
                        try:
                            Nowner_fname = input("The information you provided is valid.\nProcessing a bill of sale...\nPlease enter the first name of new owner: ")
                            Nowner_lname = input("Please enter the last name of new owner: ")
                            assert len(Nowner_fname)<=12 and re.match("^[A-Za-z0-9-]*$", Nowner_fname), "Please enter the valid first name which should be less or equal to 12 characters."
                            assert len(Nowner_lname)<=12 and re.match("^[A-Za-z0-9-]*$", Nowner_lname), "Please enter the valid last name which should be less or equal to 12 characters."
                            break
                        except AssertionError as e:
                            print(e.args[0])
                        except:
                            print("The information you entered is invalid, please try again.")
                    
                    c.execute('''select fname, lname from persons
                    where lower(fname) = lower(?) and lower(lname) = lower(?);''', (Nowner_fname, Nowner_lname))
                    if c.fetchall() == []:
                        print("Sorry, the new owner name you entered is not in our database.\nProcess cancelled.\n")
                    else:
                        c.execute('''INSERT INTO registrations(regno, regdate, expiry, plate, vin, fname, lname) VALUES (?, date('now'), date('now', '+1 year'), ?, ?, ?, ?);''', (new_regno, provide_platenum, provide_vin, Nowner_fname, Nowner_lname))
                        
                        print("New registration is successfully updated.\n")
                    exit = True
                else:
                    print("The name you provided does not match.")
                    E = input("Would like to exit this function? (Y/y for yes, other for no): )")
                    if E == 'Y' or E == 'y':
                        exit = True                    
    except sqlite3.Error as e:
        print('Error:', e.args[0])
        
    conn.commit()

def process_payment():
    global conn, c
    try:
        while True:
            try:
                ticketnum = input("Please input a valid ticket number: ")
                assert ticketnum.isdigit(), "You should enter a int type ticket number."
                ticketnum = int(ticketnum)
                break
            except AssertionError as e:
                print(e.args[0])
            except:
                print("The information you entered is invalid, please try again.")
        
        c.execute('''SELECT tno FROM tickets;''')
        
        tno = c.fetchall()
        
        if tno == []:
            print("There is no tickets in our database.")
        else:
            if ((ticketnum,) in tno):
                print("The ticket number you provided is valid.\nProcessing continue...")
            
                while True:
                    try:
                        amount = input("Please input the amount you would like to pay:")
                        assert amount.isdigit(), "You should enter a int type ticket number."
                        amount = int(amount)
                        break
                    except AssertionError as e:
                        print(e.args[0])
                    except:
                        print("The information you entered is invalid, please try again.")            
                    
                c.execute('''SELECT COALESCE(sum(amount),0) 
                FROM payments;''')
                isempty = c.fetchone()
                
                if isempty[0]==0: #empty
                    c.execute('''INSERT INTO payments(tno, pdate, amount) VALUES (?, date('now'), ?);''', (ticketnum, amount))            
                else:
                    c.execute('''SELECT COALESCE(sum(amount),0) 
                    FROM payments
                    WHERE tno = ?;''', (ticketnum,))
                    
                    total = c.fetchall()
                    
                    c.execute('''SELECT fine 
                    FROM tickets
                    WHERE tno = ?;''', (ticketnum,)) 
                    
                    fine = c.fetchall()
                    
                    if fine == []:
                        print("There is no fine for this ticket.")
                    elif fine[0][0] >= (total[0][0]+amount): #sum of those payments cannot exceed the fine amount of ticket
                        today = datetime.date.today().strftime("%Y-%m-%d")
                        c.execute('''select * from payments where pdate = ? and tno = ?;''', (today,ticketnum))
                        if c.fetchall() == []:
                            c.execute('''INSERT INTO payments(tno, pdate, amount) VALUES (?, date('now'), ?);''', (ticketnum, amount))
                            print("You have successfully paid $%d for the fine.\n" % amount)
                        else:
                            print("You can not pay the fine at the same day. Process cancel.\n")
                    else:
                        print("The amount you are going to pay exceed the fine. Process cancel.\n")
                            
            else:
                print("The ticket number is invalid. Process ends.")
    
    except sqlite3.Error as e:
        print('Error:', e.args[0])
        
    conn.commit()
    
def get_driver_abstract():
    global conn, c
    try:
        while True:
            try:
                fname = input("Please enter the first name of the driver: ")
                lname = input("Please enter the last name of the driver: ")
                assert len(fname)<=12 and re.match("^[A-Za-z0-9_]*$", fname), "Please enter the valid first name which should be less or equal to 12 characters."
                assert len(lname)<=12 and re.match("^[A-Za-z0-9_]*$", lname), "Please enter the valid last name which should be less or equal to 12 characters."
                break
            except AssertionError as e:
                print(e.args[0])
            except:
                print("The information you entered is invalid, please try again.")            
        
        c.execute('''SELECT *
        FROM registrations r
        WHERE lower(r.fname) = lower(?) and lower(r.lname) = lower(?);''', (fname, lname))
        isdriver = c.fetchall()
        
        if isdriver==[]:
            print("Provided driver name is invalid.\n")
        else:
            print("%s %s's abstract is listed below:" % (fname,lname))
            
            c.execute('''SELECT count(t.tno)
            FROM registrations r, tickets t
            WHERE r.regno = t.regno 
            and lower(r.fname) = lower(?) and lower(r.lname) = lower(?);''', (fname, lname))
            
            num_tickets = c.fetchall()
            
            print("The number of ticket is %d" % num_tickets[0][0])
            
            c.execute('''SELECT count(*)
            FROM demeritNotices d
            WHERE lower(d.fname) = lower(?) and lower(d.lname) = lower(?);''', (fname, lname))
            
            num_dnotices = c.fetchall()
            
            print("The number of demerit notices is %d" % num_dnotices[0][0])
            
            c.execute('''SELECT COALESCE(SUM(d.points),0)
            FROM demeritNotices d
            WHERE lower(d.fname) = lower(?) and lower(d.lname) = lower(?)
            and d.ddate >= datetime('now', '-2 years');''', (fname, lname))
            
            points_2years = c.fetchall()
            
            print("The total number of demerit points received within 2 years is %d" % points_2years[0][0])
            
            c.execute('''SELECT COALESCE(SUM(d.points),0)
            FROM demeritNotices d
            WHERE lower(d.fname) = lower(?) and lower(d.lname) = lower(?);''', (fname, lname))
            
            points_lifetime = c.fetchall()
            
            print("The total number of demerit points received within life time is %d" % points_lifetime[0][0])
            
            check = input("Would you like to see the tickets ordered from the latest to the oldest?\n(Y/y for yes, other for no): ")
            if check == 'Y' or check == 'y':
                c.execute('''SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model
                FROM tickets t, vehicles v, registrations r
                WHERE t.regno = r.regno and r.vin = v.vin
                and lower(r.fname) = lower(?) and lower(r.lname) = lower(?)
                ORDER BY t.vdate DESC;''', (fname, lname))
            else:
                c.execute('''SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model
                FROM tickets t, vehicles v, registrations r
                WHERE t.regno = r.regno and r.vin = v.vin
                and lower(r.fname) = lower(?) and lower(r.lname) = lower(?);''', (fname, lname))            
                
            tickets_infor = c.fetchall()
            
            ticketsNum = 0
            seemore = False
            for t in tickets_infor:
                ticketsNum += 1
                if ticketsNum <= 5:
                    print("tno: %d, vdate: %s, violation: %s, fine: %d, regno: %d, make: %s, model: %s" % (t[0],t[1],t[2],t[3],t[4],t[5],t[6]))
                else:
                    if seemore == False:
                        see_more = input("Would you like to see more tickets information?\n(Y/y for yes, other for no): ")
                        if see_more == 'y' or see_more == 'Y':
                            seemore = True
                            print("tno: %d, vdate: %s, violation: %s, fine: %d, regno: %d, make: %s, model: %s" % (t[0],t[1],t[2],t[3],t[4],t[5],t[6]))
                        else:
                            print("Process end.\n")
                            break
                    else:
                        print("tno: %d, vdate: %s, violation: %s, fine: %d, regno: %d, make: %s, model: %s" % (t[0],t[1],t[2],t[3],t[4],t[5],t[6]))
                        
            print("Tickets are all printed.\n")
    
    except sqlite3.Error as e:
        print('Error:', e.args[0])    
        
    conn.commit()
    
def issue_ticket():
    # traffic officer
    global conn, c
    try:
        check = False
        while check == False:
            try:
                regnumber = input ("please provide the registration number: ")
                assert regnumber.isdigit(), "The registration number you entered contains some non-digit characters, please try again."
                regnumber = int(regnumber)
                
                #check if the regnumber is in database
                c.execute('''select regno from registrations where regno = ?;''',((regnumber,)))
                
                check1 = c.fetchall()
                
                if check1 != []:
                    check = True
                else:
                    print("Sorry, the number not exist,please try again: ")
                    
            except AssertionError as e:
                print(e.args[0])
            except:
                print("The information you entered is invalid, please try again.")
                
        c.execute('''select fname, lname, make,model,year,color
                   FROM registrations,vehicles
                   WHERE registrations.vin =vehicles.vin and registrations.regno =?;''',(regnumber,))
        detail = c.fetchall()
        
        print("For the corresponding registration number %d:\nThe name of the driver is %s %s, the make is %s, the model is %s, the year is %s, the color is %s.\n" % (regnumber, detail[0][0], detail[0][1], detail[0][2], detail[0][3], detail[0][4], detail[0][5]))
        
                
        #make new registration
        c.execute('''SELECT max(tno) FROM tickets;''')
        t = c.fetchall()
        tno = t[0][0]+1
        
        while True:
            try:
                date = input("please provide the date, YYYY-MM-DD, i.e.2000-01-01(if nothing input,it recorded today's date): ")
                if date != '':
                    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                    assert type(date)==datetime.date, "The date you entered is invalid, please try again."
                break
            except AssertionError as e:
                print(e.args[0])
            except:
                print("The information you entered is invalid, please try again.")
        while True:        
            try:
                Vtext = input ("please provide the violation text: ")
                assert Vtext != '', "Text can not be empty."
                break
            except AssertionError as e:
                print(e.args[0])
            except:
                print("The information you entered is invalid, please try again.")
        while True:        
            try:
                amount = input ("please provide the fine amount: ")
                assert amount.isdigit(), "The amount you entered should be an integer."
                amount = int(amount)
                break
            except AssertionError as e:
                print(e.args[0])
            except:
                print("The information you entered is invalid, please try again.")        
                
        if date =='':
            c.execute ('''INSERT INTO tickets VALUES(?,?,?,?,date('now'));''',(tno,regnumber,amount,Vtext))
        else:
            c.execute ('''INSERT INTO tickets VALUES(?,?,?,?,?);''',(tno,regnumber,amount,Vtext,date))
        
        print("Ticket issued successfully!\n")
            
    except sqlite3.Error as e:
        print('Error:', e.args[0])
        
    conn.commit()
    
def find_car_owner():
    global conn, c
    
    while True:
        try:
            make = input ("Please provide the make of the car: ")
            assert len(make)<=10, "The make should less than 10 characters."
            model = input ("Please provide the model of the car: ")
            assert len(model)<=10, "The model should less than 10 characters."
            year = input ("Please provide the year of the car: ")
            assert year == '' or year.isdigit(), "The year should only contain digits."
            color = input ("Please provide the color of the car: ")
            assert len(color)<=10, "The color should less than 10 characters."
            plate = input ("Please provide the plate of the car: ")
            assert len(plate)<=7, "The plate should less than 7 characters."
            break
        except AssertionError as e:
            print(e.args[0])
        except:
            print("The information you entered is invalid, please try again.")
        
    c.execute('''
    select distinct v.make, v.model, v.year, v.color, r.plate
    from vehicles v,registrations r
    where r.vin = v.vin and (lower(v.make) = lower(?) or lower(v.model) = lower(?) or v.year = ? or lower(v.color) = lower(?) or lower(r.plate) = lower(?));''',
    (make, model, year, color, plate))
    
    allmatch = c.fetchall() # allmatch will contain all match cases for each information(make, ...., plate)
    
    if allmatch == []: #no match car
        print("\nSorry, the car has no owner\n")
    else:
        allmatch_format = [] #allmatch_format contains all elements from allmatch but in string format and also lower case (to handle string case insensetive)
        for i in allmatch:
            temp = []
            for j in i:
                j = str(j).lower() #make all elements to be string with lowercase
                temp.append(j)
            allmatch_format.append(temp)
                        
        infor = []
        infor.append(make.lower())
        infor.append(model.lower())
        infor.append(year.lower())
        infor.append(color.lower())
        infor.append(plate.lower())
        
        validinfor = [] # valid information only contains the information provided by the user
        for i in infor:
            if i!='':
                validinfor.append(i)
        
        strictmatch = [] #strictmatch will contain all match cases for all information provided
        for i in range(len(allmatch_format)):
            if set(validinfor).issubset(set(allmatch_format[i])):
                strictmatch.append(allmatch[i])
        print(strictmatch)
        
        if len(strictmatch)<4:
            for i in range(len(strictmatch)):
                match = strictmatch[i]
                
                c.execute ('''
                    select distinct r.fname,r.lname,r.regdate,r.expiry,v.make,v.model,v.year,v.color,r.plate
                    from registrations r, vehicles v
                    where r.vin = v.vin and lower(v.make) = lower(?) and lower(v.model) = lower(?) and v.year = ? and lower(v.color) = lower(?) and lower(r.plate) = lower(?)
                    order by r.regdate desc limit 1;''', (match[0],match[1],match[2],match[3],match[4]))
                
                
                showinfor = c.fetchall() # show infor contains all information we need to show to the user
                        
                print("%d. The car that make is %s, model is %s, year is %s, color is %s, plate is %s" % (i+1, showinfor[0][4], showinfor[0][5], showinfor[0][6], showinfor[0][7], showinfor[0][8]))
                
                print (" -- The name of its owner is %s %s,the registration date is %s,the expiry date is %s.\n" % (showinfor[0][0],showinfor[0][1],showinfor[0][2],showinfor[0][3]))
                
        else:
            print ("There are 4 or more macthes.")
            num = 0
            for car in strictmatch:
                num += 1
                print("%d. The car make is %s, model is %s, year is %s, color is %s, plate is %s." % (num, car[0], car[1], car[2], car[3], car[4]))
            
            choose = True
            while choose:
                tem_choose = input("\nwhich one you want to go through the detail: ")
                if tem_choose == '':
                    print("Sorry, The number you chosen is invaild. Please try again!")
                else:
                    tem_choose = int(tem_choose)
                    if (tem_choose > (len(strictmatch))) or (tem_choose <=0):
                        print ("Sorry, The number you chosen is invaild. Please try again!")
                    else:
                        choose = False
                        tem_choose -= 1
                        match = strictmatch[tem_choose]
                        
                        c.execute ('''
                        select distinct r.vin,r.fname,r.lname,r.regdate,r.expiry
                        from registrations r, vehicles v
                        where r.vin = v.vin and lower(v.make) = lower(?) and lower(v.model) = lower(?) and v.year = ? and lower(v.color) = lower(?) and lower(r.plate) = lower(?)
                        order by r.regdate desc;''', (match[0],match[1],match[2],match[3],match[4]))
                        
                        showinfor_all = c.fetchall() # show infor contains all information we need to show to the user (will have duplicate vin)
                        
                        vin = ''
                        showinfor = [] # only keep one information for each vin
                        for i in showinfor_all:
                            if vin != i[0]:
                                showinfor.append(i)
                                vin = i[0]
                        
                        print("For the car that make is %s, model is %s, year is %s, color is %s, plate is %s.\nTotal have %d qualified car owner.\n" % (match[0], match[1],match[2],match[3],match[4], len(showinfor)))
                        
                        for n in range(len(showinfor)):
                            print ("%d.The name of owner is %s %s,the registration date is %s,the expiry date is %s.\n" % (n+1,showinfor[n][1],showinfor[n][2],showinfor[n][3],showinfor[n][4]))                    
    print("Process end.")
        
    conn.commit()
 

def main():
    global conn, c
    
    try:
        print("Welcome!")
        path = input("Enter the name of database: ")
        
        connect(path)
        drop_tables()
        
        defineT = input("Would you like to define the table?(Y/y for yes, other for no):")
        if defineT == 'Y' or defineT == 'y':
            define_tables()
        
        insertD = input("Would you like to insert data?(Y/y for yes, other for no): ")
        if insertD == 'Y' or insertD == 'y':
            insert_data()
        
        exit = True
        again = True
        while (exit and again):
            #log in
            islogin = False
            while not islogin:
                result = login() # login() return (T/F, userid)
                islogin = result[0]
                if islogin == False:
                    again = input("Would you like to log in again?(Y/y for yes, other for no): ")
                    if (again != 'Y') and (again != 'y'):
                        again = False
                        break  
            
            while islogin:
                userid = result[1]
                #officers or agents?
                c.execute('''Select utype From users where uid = ?;''', (userid,))
                utype = c.fetchall()
                isagent = False
                isofficer = False
                if utype[0][0] == 'a':
                    isagent = True
                elif utype[0][0] == 'o':
                    isofficer = True
                
                while isagent:
                    agent_step = input("Welcome to our database system, we have following functionalities for agents:\n1. Birth Registration\n2. Marriage Registration\n3. Renew vehicle registration\n4. Process a bill\n5. process a payment for tickets\n6. Get driver's abstract\n7. Log out\n8. Exit\nWhich function would you like to use?(please input the option's number, i.e.1): ")
                    if agent_step.isdigit() and len(agent_step)==1:
                        if agent_step == '1':
                            registrate_birth(userid)
                        elif agent_step == '2':
                            registrate_marriage(userid)
                        elif agent_step == '3':
                            renew_vehicle()
                        elif agent_step == '4':
                            process_bill()
                        elif agent_step == '5':
                            process_payment()
                        elif agent_step == '6':
                            get_driver_abstract()
                        elif agent_step == '7':
                            isagent = False
                            islogin = False
                        elif agent_step == '8':
                            isagent = False
                            islogin = False
                            exit = False
                    else:
                        print("Invalid process number.")
                
                while isofficer:
                    officer_step = input("Welcome to our database system, we have following functionalities for officers:\n1. Issue a ticket\n2. Find the owner of the car\n3. Log out\n4. Exit\nWhich function would you like to use?(please input the option's number, i.e.1): ")
                    if officer_step.isdigit() and len(officer_step)==1: 
                        if officer_step == '1':
                            issue_ticket()
                        elif officer_step == '2':
                            find_car_owner()
                        elif officer_step == '3':
                            isofficer = False
                            islogin = False
                        elif officer_step == '4':
                            isofficer = False
                            islogin = False
                            exit = False                    
                    else:
                        print("Invalid process number.")
        
        print("Bye!")
      
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print('Error:', e.args[0])
    except:
        print("The enter is invalid.\n")    
    return

if __name__ == "__main__":
    main()

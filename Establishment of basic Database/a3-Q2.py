import sqlite3
import time
import random
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
    c.execute("drop table if exists marriages;")
    c.execute("drop table if exists births;")
    c.execute("drop table if exists payments;")
    c.execute("drop table if exists tickets;")
    c.execute("drop table if exists registrations;")
    c.execute("drop table if exists vehicles;")
    c.execute("drop table if exists users;")
    c.execute("drop table if exists persons;")
    
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
    INSERT INTO users VALUES ('Lb11', 'Lillian?/', 'o', 'Lillian', 'Bounds', 'Los Angeles');
    INSERT INTO users VALUES ('Mm%23', 'Mickey', 'a', 'Mickey', 'Mouse', 'Anaheim');

    ''')
    
    conn.commit()    
    
def registrate_birth():
    global conn, c
    
    fn = raw_input("please enter your first name: ")
    ln = raw_input("please enter your last name: ")
    gender = raw_input("please enter your gender: ")
    bd = raw_input("please enter your birth date: ")
    bp = raw_input("please enter your birth place: ")
    m_fn  = raw_input("please enter your mother first name: ")
    m_ln  = raw_input("please enter your mother last name: ")
    f_fn  = raw_input("please enter your father first name: ")
    f_ln  = raw_input("please enter your father last name: ")
    #rd = datetime.date(datetime.now())
    
    invaild = True
    #while(invaild):
    #       rn = random.randint(100,1000) 
    #        c.execute('''SELECT regno FROM births WHERE regno=?;''',rn)
    #        vaild = c.fetchall()
    #        if vaild != None:
    #            invaild = True
            
    c.execute("SELECT fname,lname FROM persons WHERE fn=:first and ln=:lname;",{"first":m_fn, "last":m_ln})
    mother = c.fetchall()
    c.execute("SELECT fname,lname FROM persons WHERE fn=:first and ln=:lname;",{"first":f_fn, "last":f_ln})
    father = c.fetchall()
    if (mother == None) or (father == None):
        if mother == None:
            print("mother does not exist")
            m_fn = raw_input("please enter mother's first name: ")
            m_ln = raw_input("please enter mother's last name: ")
            m_bd = raw_input("please enter mother's birth date: ")
            m_bp = raw_input("please enter mother's birth place: ") 
            m_address = raw_input("please enter mother's address: ")
            m_phone = raw_input("please enter mother's phone number: ")
            c.execute("INSERT INTO persons VALE(?,?,?,?,?,?)",(m_fn,m_ln,m_bd,m_bp,m_address,m_phone))
            
        else:
            f_fn = raw_input("please enter father's first name: ")
            f_ln = raw_input("please enter father's last name: ")
            f_bd = raw_input("please enter father's birth date: ")
            f_bp = raw_input("please enter father's birth place: ") 
            f_address = raw_input("please enter father's address: ")
            f_phone = raw_input("please enter father's phone number: ")
            c.execute("INSERT INTO persons VALE(?,?,?,?,?,?);",(f_fn,f_ln,f_bd,f_bp,f_address,f_phone))
            
    
    c.execute("INSERT INTO birth value(?,?,?,?,?,?,?,?,?,?,?,?,?);", (rn,fn,ln,rd,rp,gender,bd,bp,f_fn,f_ln,m_fn,m_ln))
    c.execute("SELECT address,phone FROM persons WHERE fname=:first and lname=:lname;",{"first;":m_fn, "last":m_ln})
    infor = c.fetchall()
    address = infor[0]
    phone = infor[1]
    c.execute("INSERT INTO persons VALE(?,?,?,?,?,?);",(fn,ln,bd,bp,address,phone))
    
    conn.commit()
    
def registrate_marriage():
    global conn, c
    
    p_fn  = raw_input("please enter your first name: ")
    p_ln  = raw_input("please enter your last name: ")
    p1_fn  = raw_input("please enter your partners first name: ")
    p1_ln  = raw_input("please enter your partners last name: ")    
    rd = datetime.date(datetime.now())
    c.execute("SELECT address FROM persons WHERE fnname=:first and lname=:lname;",{"first":p_fn, "last":p_ln})
    rp = c.fetchall()
    
    invaild = False
    while not invaild:
            rn = int(str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))) 
            c.execute("SELECT regno FROM maggrrages WHERE regno=?;",(rn,))
            vaild = c.fetchall()
            if vaild != None:
                invaild = True
    
    c.execute("INSERT INTO birth value(,?,?,?,?,?,?);", (rn,rd,rp,p_fn,p_ln,p1_fn,p2_ln)) 
    
    conn.commit()
    
def renew_vehicle():
    global conn, c
    
    ren = raw_input("please enter your registration number: ")
    ty = datetime.date(datetime.now()).year
    tm = datetime.date(datetime.now()).month
    td = datetime.date(datetime.now()).day
    ey = ty + 1
    c.execute("SELECT expiry FROM registrations WHERE regno = ?;", (ren,))
    old_e = c.fetchall()
    y = int(old_e[0:3])
    m = int(old_e[5:6])
    d = int(old_e[8:9])
    if datetime.date(y,m,d) >= datetime.date(datetime.now()):
        ey = ty + 1
        edate = str(ey) + '-' + str(tm) + '-' + str(td)
    else:
        edate = str(y+1) + '-' + str(m) + '-' + str(d)
    
    c.execute('''UPDATE registrations
                SET expiry = ?
                WHERE regno = ren;
                ''', (edate,))
    
    conn.commit()    

def process_bill():
    
    global conn, c
    
    provide_vin = raw_input("Please provide the vin of a car: ")
    provide_fname = raw_input("Please provide the first name of the current owner: ")
    provide_lname = raw_input("Please provide the last name of the current owner: ")
    provide_platenum = raw_input("Please provide a plate number for the new registration: ")    
    
    conn.row_factory = sqlite3.Row
    
    c.execute('''SELECT r.fname, r.lname
       FROM vehicles v, registrations r
       WHERE v.vin = r.vin AND r.vin = ? AND r.plate = ?
       ORDER BY r.regdate DESC
       limit 1;''', (provide_vin, provide_platenum))
    
    name = c.fetchall()
        
    if (provide_fname == name[0][0]) and (provide_lname == name[0][1]):
        #end current registration
        c.execute('''UPDATE registrations
        SET expiry = date('now') 
        WHERE fname = ? and lname = ?;''', (provide_fname, provide_lname))
        
        #make new registration
        invalid_regno = True
        while(invalid_regno):
            new_regno = random.randint(100, 1000)
            c.execute('''SELECT regno FROM registrations;''')
            regno = c.fetchall()
            for r in regno:
                if r != regno:
                    invalid_regno = False
        
        Nowner_fname = raw_input("The information you provided is valid.\nProcessing a bill of sale...\nPlease enter the first name of new owner: ")
        Nowner_lname = raw_input("Please enter the last name of new owner: ")
        
        c.execute('''INSERT INTO registrations(regno, regdate, expiry, plate, vin, fname, lname) VALUES (?, date('now'), date('now', '+1 year'), ?, ?, ?, ?);''', (new_regno, provide_platenum, provide_vin, Nowner_fname, Nowner_lname))
        print("New registration is successfully updated.")
    
    else:
        print("Sorry, the name you provided is not in our database.")
    
    conn.commit()
    return     

def process_payment():
    global conn, c
    
    ticketnum = int(raw_input("Please input a valid ticket number: "))
    
    c.execute('''SELECT tno FROM tickets;''')
    
    tno = c.fetchall()
    
    tinvalid = True
    for t in tno:
        if (t[0]==ticketnum):
            tinvalid = False
            
            print("The ticket number you provided is valid. Processing continue...")
            amount = int(raw_input("Please input the amount you would like to pay:"))
            
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
                
                if fine[0][0] > (total[0][0]+amount): #sum of those payments cannot exceed the fine amount of ticket
                    c.execute('''INSERT INTO payments(tno, pdate, amount) VALUES (?, date('now'), ?);''', (ticketnum, amount))
                    print("You have successfully paid $%d for the fine." % amount)
                else:
                    print("The amount you are going to pay exceed the fine. Process cancel.")
                    
    if tinvalid:
        print("The ticket number is invalid. Process ends.")
                
            
    conn.commit()
    
def get_driver_abstract():
    global conn, c
    
    fname = raw_input("Please enter the first name of the driver: ")
    lname = raw_input("Please enter the last name of the driver: ")    
    
    c.execute('''SELECT *
    FROM registrations r
    WHERE r.fname = ? and r.lname = ?;''', (fname, lname))
    isdriver = c.fetchall()
    
    if isdriver==[]:
        print("Provided driver name is invalid.")
    else:
        print("%s %s's abstract is listed below:" % (fname,lname))
        
        c.execute('''SELECT count(t.tno)
        FROM registrations r, tickets t
        WHERE r.regno = t.regno 
        and r.fname = ? and r.lname = ?;''', (fname, lname))
        
        num_tickets = c.fetchall()
        
        print("The number of ticket is %d" % num_tickets[0][0])
        
        c.execute('''SELECT count(*)
        FROM demeritNotices d
        WHERE d.fname = ? and d.lname = ?;''', (fname, lname))
        
        num_dnotices = c.fetchall()
        
        print("The number of demerit notices is %d" % num_dnotices[0][0])
        
        c.execute('''SELECT COALESCE(SUM(d.points),0)
        FROM demeritNotices d
        WHERE d.fname = ? and d.lname = ?
        and d.ddate >= datetime('now', '-2 years');''', (fname, lname))
        
        points_2years = c.fetchall()
        
        print("The total number of demerit points received within 2 years is %d" % points_2years[0][0])
        
        c.execute('''SELECT COALESCE(SUM(d.points),0)
        FROM demeritNotices d
        WHERE d.fname = ? and d.lname = ?;''', (fname, lname))
        
        points_lifetime = c.fetchall()
        
        print("The total number of demerit points received within life time is %d" % points_lifetime[0][0])
        
        check = raw_input("Would you like to see the tickets ordered form te latest to the oldest?\n(Y/y for yes, other for no): ")
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
                    print("tno: %d, vdate: %s, violation: %s, fine: %d, regno: %d, make: %s, model: %s" % (t[0],t[1],t[2],t[3],t[4],t[5],t[6]))
                else:
                    see_more = raw_input("Would you like to see more tickets information?\n(Y/y for yes, other for no): ")
                    if see_more == 'y' or see_more == 'Y':
                        print("tno: %d, vdate: %s, violation: %s, fine: %d, regno: %d, make: %s, model: %s" % (t[0],t[1],t[2],t[3],t[4],t[5],t[6]))
            print("Tickets are all printed.")
        else:
            print("Process end.")
        
    conn.commit()
    
def function_name7():
    global conn, c
    
    conn.commit()
    
def function_name8():
    global conn, c
    
    conn.commit()
 

def main():
    global conn, c
    
    #path = raw_input("Enter the name of database: ")
    path="./a3.db"
    
    connect(path)
    drop_tables()
    define_tables()
    insert_data()
    
    #log in
    
    
    #1
    #registrate_birth()
    
    #2
    
    #3
    
    #4
    process_bill()
    
    #5
    process_payment()
    
    #6
    get_driver_abstract()
    
    #7
    
    #8
    
    conn.commit()
    conn.close()
    return

if __name__ == "__main__":
    main()
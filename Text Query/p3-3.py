#case insensitive
#partial matching
#output=brief

from bsddb3 import db
import re

def exact_match(curs, search_data):
    result = curs.set(search_data.encode("utf-8"))
    
    rowid = []
    
    print("Searching for " + search_data + "...")
    if(result != None):
        print("List of found records:")
        
        print(str(result[0].decode("utf-8")) + ' is found in row ' + str(result[1].decode("utf-8")))
        
        rowid.append(str(result[1].decode("utf-8")))
        
        #iterating through duplicates:
        dup = curs.next_dup()
        while(dup != None):
            print(str(dup[0].decode("utf-8")) + ' is found in row ' + str(dup[1].decode("utf-8")))
            rowid.append(str(dup[1].decode("utf-8")))
            dup = curs.next_dup()
    else:
        print("No record was found in subj field")
    
    return rowid

def partial_match(curs, search_data):
    result = curs.set_range(search_data.encode("utf-8"))
    
    rowid = []
    
    print("Searching for " + search_data + " in subj...")
    if(result != None):
        print("List of found records:")
        
        while(result != None):
            #Checking the end condition
            if (str(result[0].decode("utf-8")[0:len(search_data)])>search_data):
                break
        
            print(str(result[0].decode("utf-8")) + ' is found in row ' + str(result[1].decode("utf-8")))
            
            rowid.append(str(result[1].decode("utf-8")))
            
            result = curs.next()
    else:
        print("No record was found in subj field")
        
    return rowid

def main():
    re_file = "re.idx"
    db_re = db.DB()
    db_re.open(re_file,None, db.DB_HASH, db.DB_CREATE)
    curs_re = db_re.cursor()
    
    te_file = "te.idx"
    db_te = db.DB()
    db_te.open(te_file,None, db.DB_BTREE, db.DB_CREATE)
    curs_te = db_te.cursor()
    
    em_file = "em.idx"
    db_em = db.DB()
    db_em.open(em_file,None, db.DB_BTREE, db.DB_CREATE)
    curs_em = db_em.cursor()
    
    da_file = "da.idx"
    db_da = db.DB()
    db_da.open(da_file,None, db.DB_BTREE, db.DB_CREATE)
    curs_da = db_da.cursor()
    
    #print(db_re.keys())
    #print(db_te.keys())
    #print(db_em.keys())
    #print(db_da.keys())
    
    #3
    #subj : term%
    #enter = input("Please enter your command: ")
    #enter = 'subj:gas body  :you'
    enter = 'subj  : gas you%'
    #enter = 'bcc:derryl.cleaveland@enron.com  cc:jennifer.medcalf@enron.com'
    #enter = 'date>2000/09/22'
    #enter = 'confidential%'
    #enter = 'confidential'
    #enter = 'subj:gas body:you'
    #enter = 'from:phillip.allen@enron.com'
    #enter = 'to:bs_stone@yahoo.com'
    #enter = 'to:phillip.allen@enron.com'
    #enter = 'to:kenneth.shulklapper@enron.com  to:keith.holst@enron.com'
    #enter = 'date:2001/03/15'
    #enter = 'date>2001/03/10'
    #enter = 'bcc:derryl.cleaveland@enron.com  cc:jennifer.medcalf@enron.com'
    #enter = 'body:stock  confidential shares   date<2001/04/12'
    #enter = 'confidential date<2001/04/12'
    enter = enter.lower()
    
    command = '\s*output\s*=\s*full|output\s*=\s*brief'
    
    commRegex = re.compile(command, re.I) #re.I -> ignore case, re.X -> verbose
    
    result = re.search(commRegex, enter)
    
    #default mode is full
    out_mode = None
    
    if result is not None:
        out_mode = result.group()
        query = re.split(out_mode, enter)[0]
    else:
        query = enter
    #print(query)
    
    expression = """
    (\s*date\s*)(:|>|<|>=|<=)(\s*\d\d\d\d/\d\d/\d\d)| #dateQuery
    (from|to|cc|bcc)(\s*)(:)(\s*)([0-9a-zA-Z_-]+.[0-9a-zA-Z_-]*)@([0-9a-zA-Z_-]+.[0-9a-zA-Z_-]*)| #emailQuery
    ((subj | body)\s*:\s*)?([0-9a-zA-Z_-]+)(%)? #termQuery
    """
    expRegex = re.compile(expression, re.X)
    result = re.finditer(expRegex, query)
    query_list = []
    for q in result:
        q = q.group()
        q = re.sub(' ', '', q)
        print(q)
        signexp = ':|>=|<=|>|<' #order is matter, make sure '<=' and '>=' search before '<' and '>'
        signRegex = re.compile(signexp, re.I)
        sign = re.search(signRegex, q)
        if sign is not None:
            sign = sign.group()
        split_q = re.split(':|>=|<=|>|<', q)
        split_q.append(sign)
        query_list.append(split_q)
    print(query_list)
    
    # ignore the case 'confidential%' for now
    total_rid = []
    t = 1
    for q in query_list:
        
        if len(q) == 3:
            field = q[0]
            search_data = q[1]
            sign = q[2]
            print(field, search_data, sign)
            print("Searching for " + search_data + " in " + field + "...")
            
            if field == 'subj':
                curs = curs_te
                search_data = 's-' + search_data
            elif field == 'body':
                curs = curs_te
                search_data = 'b-' + search_data            
            elif field == 'date':
                curs = curs_da
            elif field in ['from', 'to', 'cc', 'bcc']:
                curs = curs_em
                search_data = field + '-' + search_data
                
            if sign == ':':
                result = curs.set(search_data.encode("utf-8"))
                rowid = []
                if(result != None):
                    print("List of found records:")
                    
                    print(str(result[0].decode("utf-8")) + ' is found in row ' + str(result[1].decode("utf-8")))
                    
                    rowid.append(str(result[1].decode("utf-8")))
                    
                    #iterating through duplicates:
                    dup = curs.next_dup()
                    while(dup != None):
                        print(str(dup[0].decode("utf-8")) + ' is found in row ' + str(dup[1].decode("utf-8")))
                        
                        rowid.append(str(dup[1].decode("utf-8")))
                        
                        dup = curs.next_dup()
                else:
                    print("No record was found")            
                
            elif sign in ['<', '>', '<=', '>=']: #do range search
                
                if (sign == '>' or sign == '>='):
                    result = curs.set_range(search_data.encode("utf-8")) #the smallest key greater than or equal to the specified key
                    
                    if (sign=='>'): #except itself
                        result = curs.next()
                else:
                    result = curs.first()
                
                rowid = []
                if(result != None):
                    print("List of found records:")
                        
                    while (result != None):
                        
                        #check ending condition
                        if (sign=='<'):
                            if (result[0].decode("utf-8") >= search_data):
                                break
                        elif (sign=='<='):
                            if (result[0].decode("utf-8") > search_data):
                                break
                        
                        print(str(result[0].decode("utf-8")) + ' is found in row ' + str(result[1].decode("utf-8")))
                        
                        rowid.append(str(result[1].decode("utf-8")))         
                        
                        result = curs.next()
                        
                else:
                    print("No record was found")
            
        elif len(q) == 2:
            #handle partial matching
            search_data = q[0]
            
            ispartial = False
            if re.search(r'%', search_data) != None: #% in the end -> partial matching
                ispartial = True
                
                split_q = re.split('%', search_data)
                partial_term = split_q[0]
                search_data = partial_term
            
            print(search_data)
            
            curs = curs_te
            # subj
            search_data_subj = 's-' + search_data
            # body
            search_data_body = 'b-' + search_data        
            
            if ispartial:
                #search subj
                rowid = partial_match(curs, search_data_subj)
                #search body
                rowid2 = partial_match(curs, search_data_body)
                
            else:
                #search subj
                rowid = exact_match(curs, search_data_subj)
                #search body
                rowid2 = exact_match(curs, search_data_body)
                
            for i in rowid2:
                if i not in rowid:
                    rowid.append(i)
                
        temp = []
        if t == 1:
            previous = rowid
        else:    
            for r in previous:
                if r in rowid:
                    temp.append(r)
            previous = temp
        
        print('pre---', previous, 'current---', rowid)
        
        print('t---', t)
        t += 1
        
    #having rowid, we can match records
    curs = curs_re
    
    total_rid = previous
    total_rid.sort()
    print('total rid----', total_rid)
    print('total len---', len(total_rid))
    
    if out_mode == None:
        print("(The output mode is not given, so the default mode will be used.)")
        out_mode = 'output=brief'
        
    for r in total_rid:
        result = curs.set(r.encode("utf-8"))
        
        if out_mode == 'output=full':
            print('The full record in row ' + str(result[0].decode("utf-8")) + ' is:\n' + str(result[1].decode("utf-8")))
        elif out_mode == 'output=brief':
            print('Row id: ' + r + '') #row id + the subject field of all matching emails
            
    
    curs_re.close()
    curs_te.close()
    curs_em.close()
    curs_da.close()
    
    db_re.close()
    db_te.close()
    db_em.close()
    db_da.close()

if __name__ == "__main__":
    main()
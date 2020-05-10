from bsddb3 import db
import xml.etree.ElementTree as ET
import re
import sys

def main():
    #parse on xml file by name
    #file_name = input("Please enter the name of a xml type file: ")
    #mydoc = ET.parse(file_name)
    #root = mydoc.getroot()
    string = []
    for line in sys.stdin:
        string.append(line)
    root = ET.fromstringlist(string)
    
    #create_files
    terms_file = open("terms.txt", "w+")
    email_file = open("emails.txt", "w+")
    dates_file = open("dates.txt", "w+")
    recs_file = open("recs.txt", "w+")
        
    for mail in root.findall('mail'):
        items_row = mail.find('row').text
        
        #get terms
        items_sub = mail.find('subj').text
            
        items_body = mail.find('body').text
        
        if items_sub is not None:
            #print(items_sub)
            words = re.sub("[^0-9a-zA-Z_-]", " ", items_sub).split()
            for t in words:
                if re.match("^[0-9a-zA-Z_-]*$", t) and len(t)>2:
                    terms_file.write('s-' + (t).lower() + ':' + items_row + '\n')
                    #print('s-' + (t).lower() + ': ' + items_row + '\n')
        
        if items_body is not None:
            #print(items_body)
            words = re.sub("[^0-9a-zA-Z_-]", " ", items_body).split()
            for t in words:
                if re.match("^[0-9a-zA-Z_-]*$", t) and len(t)>2:
                    terms_file.write('b-' + (t).lower() + ':' + items_row + '\n')
                    
        #get email address
        items_from = mail.find('from').text
        items_to = mail.find('to').text
        items_cc = mail.find('cc').text
        items_bcc = mail.find('bcc').text
        
        if items_from is not None:
            items_from = re.sub(",", " ", items_from).split()
            for f in items_from:
                email_file.write('from-' + (f).lower() + ':' + items_row + '\n')
        if items_to is not None:
            items_to = re.sub(",", " ", items_to).split()
            for t in items_to:
                email_file.write('to-' + (t).lower() + ':' + items_row + '\n')
        if items_cc is not None:
            items_cc = re.sub(",", " ", items_cc).split()
            for cc in items_cc:
                email_file.write('cc-' + (cc).lower() + ':' + items_row + '\n')
        if items_bcc is not None:
            items_bcc = re.sub(",", " ", items_bcc).split()
            for b in items_bcc:
                email_file.write('bcc-' + (b).lower() + ':' + items_row + '\n')
                
        #get dates
        items_date = mail.find('date').text
        
        if items_date is not None:
            dates_file.write(items_date + ':' + items_row + '\n')
                
    
    #get records
    row = []
    for r in root.iter('row'):
        row.append(r.text)
    r = 0
    for line in string:
        if re.search('<mail>', line):
            recs_file.write(row[r] + ':' + line)
            r+=1
    
    print("Done!")
    
    #close files
    terms_file.close()
    email_file.close()
    dates_file.close()
    recs_file.close()
    return

if __name__ == "__main__":
    main()
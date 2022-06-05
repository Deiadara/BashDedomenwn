import mysql.connector
import csv
import random
import math
from faker import Faker
import datetime

from mysql.connector import Error

proj_num = 60
researcher_num = 1000
org_num = 30

orgs = ["Εταιρεία","Πανεπιστήμιο","Ερευνητικό Κέντρο"]
projects = ["ΔΙΑΓΡΑΜΜΑΤΑ ΡΟΗΣ", "JORDAN BLOCKS","ΡΟΤΟΡΕΣ", "CONSENSUS ΑΛΓΟΡΙΘΜΟΣ", "ΠΡΩΤΟΚΟΛΟ ΑΣΦΑΛΕΙΑΣ ΣΥΝΑΛΛΑΓΩΝ IEEE", "ΑΝΑΠΤΥΞΗ GHIDRA DECOMPILER ΣΕ C",
 "ΕΡΓΑΛΕΙΑ ΜΗΧΑΝΩΝ","BLOCKCHAIN","JAVA ENGINE","JAVASCIRPT ENGINE","C# ENGINE","C++ ENGINE","PYTHON ENGINE","ΑΝΑΠΤΥΞΗ ΠΑΙΧΝΙΔΙΟΥ ΣΕ UNITY"
 ,"ΑΝΑΠΤΥΞΗ ΛΟΓΙΣΜΙΚΟΥ ΓΙΑ SITE ΠΟΛΥΤΕΧΝΕΙΟΥ", "ΑΝΑΠΤΥΞΗ ΠΑΙΧΝΙΔΙΟΥ ΣΕ UNREAL ENGINE", "ΔΗΜΙΟΥΡΓΙΑ COMPILER ΣΕ ML", "ΔΗΜΙΟΥΡΓΙΑ COMPILER ΣΕ C++",
 "ΜΟΝΤΕΛΟΠΟΙΗΣΗ ΝΕΥΡΟΝΙΚΩΝ ΔΙΚΤΥΩΝ","ΑΝΑΛΥΣΗ ΔΕΔΟΜΕΝΩΝ ΠΟΛΥΤΕΧΝΕΙΟΥ","ΑΝΑΠΤΥΞΗ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ ΣΕ SQL", "ΚΑΤΑΣΚΕΥΗ ΤΡΟΧΩΝ ΓΙΑ ΑΕΡΟΣΚΑΦΗ",
 "ΕΝΗΜΕΡΩΣΗ ΔΕΥΤΕΡΟΒΑΘΜΙΑΣ ΕΚΠΑΙΔΕΥΣΗΣ ΓΙΑ ΤΟ ΠΟΛΥΤΕΧΝΕΙΟ", "ΕΛΕΓΧΟΣ ΚΤΗΡΙΩΝ ΓΙΑ ΑΝΤΟΧΗ ΣΕ ΣΕΙΣΜΟΥΣ", "ΜΕΤΕΟΡΩΛΟΓΙΚΑ ΔΙΑΓΡΑΜΜΑΤΑ", "ΚΥΚΛΩΜΑ ΜΕΤΑΤΡΟΠΗΣ ΗΛΙΑΚΗΣ ΣΕ ΗΛΕΚΤΡΙΚΗ ΕΝΕΡΓΕΙΑ",
 "ΤΕΧΝΙΤΗ ΝΟΗΜΟΣΥΝΗ ΣΕ ΟΧΗΜΑ ΤΗΣ PROM","ΠΑΡΟΥΣΙΑΣΗ ΒΑΣΙΚΩΝ ΜΕΘΟΔΩΝ ΚΡΥΠΤΟΓΡΑΦΙΑΣ","ΕΠΑΓΓΕΛΜΑΤΙΚΟΣ ΠΡΟΣΑΝΑΤΟΛΙΣΜΟΣ", "ΑΠΟΚΡΥΠΤΟΓΡΑΦΙΣΗ LEET 1337 ΓΡΑΦΗΣ",
 "ΚΑΤΑΣΚΕΥΗ ΜΑΚΕΤΑΣ ΜΕ ΠΡΟΤΥΠΟ ΤΗΝ ΕΥΡΩΠΑΙΚΗ ΑΡΧΙΤΕΚΤΟΝΙΚΗ", "ΜΕΛΕΤΗ ΑΔΥΝΑΜΙΩΝ ΤΗΣ DIFFIE - HELLMAN ΜΕΘΟΔΟΥ", "ΔΗΜΙΟΥΡΓΙΑ ΜΙΚΡΟΕΠΕΞΕΡΓΑΣΤΗ 8086",
  "ΚΑΤΑΣΚΕΥΗ ΜΑΚΕΤΑΣ ΜΕ ΠΡΟΤΥΠΟ ΤΗΝ ΙΑΠΩΝΙΚΗ ΑΡΧΙΤΕΚΤΟΝΙΚΗ","ΕΡΕΥΝΑ DNA ΓΙΑ ΕΠΙΠΛΟΚΕΣ COVID", "ΕΡΕΥΝΑ ΤΩΝ ΕΠΙΔΡΑΣΕΩΝ ΤΟΥ COVID ΣΤΟ ΜΥΟΣΚΕΛΕΤΙΚΟ ΣΥΣΤΗΜΑ"
  ,"ΕΡΕΥΝΑ RNA ΓΙΑ ΕΠΙΠΛΟΚΕΣ COVID","ΕΡΕΥΝΑ ΑΜΙΝΟΞΕΩΝ","ΑΝΑΛΥΣΗ ΧΗΜΙΚΗΣ ΟΥΣΙΑΣ C38XM", "ΑΝΑΛΥΣΗ ΧΗΜΙΚΗΣ ΟΥΣΙΑΣ D322a", "ΜΕΛΕΤΗ ΠΟΡΕΙΑΣ ΤΟΥ ΚΟΜΗΤΗ ZEN35",
  "MEΛΕΤΗ ΤΡΟΧΙΑΣ ΤΟΥ ΦΕΓΓΑΡΙΟΥ ΓΙΑ ΑΠΟΚΛΙΣΕΙΣ","ΔΗΜΙΟΥΡΓΙΑ ΑΕΡΟΔΥΝΑΜΙΚΗΣ ΚΑΜΠΙΝΑΣ ΑΥΤΟΚΙΝΗΤΟΥ","ΔΗΜΙΟΥΡΓΙΑ ΑΕΡΟΔΥΝΑΜΙΚΗΣ ΚΑΜΠΙΝΑΣ ΑΕΡΟΠΛΑΝΟΥ",
  "ΕΡΕΥΝΑ ΕΠΙΠΛΟΚΗΣ LASER ΣΤΟ ΑΝΘΡΩΠΙΝΟ ΔΕΡΜΑ","ΜΕΛΕΤΗ ΑΚΤΙΝΩΝ Z", "ΔΗΜΙΟΥΡΓΙΑ ΠΛΑΣΜΑΤΙΚΟΥ ΥΛΙΚΟΥ ΓΙΑ ΕΦΑΡΜΟΓΗ ΣΕ ΜΙΚΡΟΥΠΟΛΟΓΙΣΤΕΣ" , "ΔΗΜΙΟΥΡΓΙΑ ΚΒΑΝΤΙΚΟΥ ΥΠΟΛΟΓΙΣΤΗ"
  ,"ΕΦΑΡΜΟΓΗ ΝΕΥΡΟΝΙΚΩΝ ΔΙΚΤΥΩΝ ΣΕ ΧΗΜΙΚΕΣ ΑΝΑΛΥΣΕΙΣ", "ΑΝΑΛΥΣΗ ΜΕΘΟΔΟΥ ANDERSON ΚΑΙ ΝΕΥΡΩΝΙΚΩΝ ΔΙΚΤΥΩΝ", "ΒΕΛΤΙΣΤΟΠΟΙΗΣΗ ΜΕΘΟΔΟΥ MONTE CARLO", 
  "ΑΝΑΛΥΣΗ ΚΡΥΠΤΟΓΡΑΦΥΜΕΝΟΥ ΗΧΗΤΙΚΟΥ ΜΗΝΥΜΑΤΟΣ XSM23", "ΜΕΤΡΗΣΗ ΠΑΛΜΩΝ ΜΕ ΕΦΑΡΜΟΓΗ ΚΙΝΗΤΟΥ", "ΗΛΕΚΤΡΟΝΙΚΟ ΟΞΥΜΕΤΡΟ ΚΙΝΗΤΟΥ", "ΕΡΓΑΛΕΙΟ ΒΕΛΤΙΩΣΗΣ ΑΝΑΛΥΣΗΣ ΕΙΚΟΝΩΝ",
  "ΒΕΛΤΙΣΤΟΠΟΙΗΣΗ ΠΟΛΥΠΛΟΚΟΤΗΤΑΣ ΤΟΥ ΑΛΓΟΡΙΘΜΟΥ PAPAZAX","ΑΝΑΠΤΥΞΗ FRONT END ΓΙΑ ΤΟ START-UP HELENIC PC 32", "ΜΕΛΕΤΗ ΠΑΡΑΛΛΗΛΩΝ ΔΙΕΡΓΑΣΙΩΝ ΣΕ ΚΒΑΝΤΙΚΟ ΠΕΡΙΒΑΛΛΟΝ",
  "ΚΑΤΑΣΚΕΥΗ ΣΕΝΣΟΡΑ ΚΙΝΔΥΝΟΥ ΓΙΑ ΠΥΡΗΝΙΚΕΣ ΚΕΦΑΛΕΣ", "ΑΛΓΟΡΙΘΜΟΣ PACKET EXCHANGE ΓΙΑ ΑΥΤΟΜΑΤΟΠΟΙΗΜΕΝΑ ΣΥΣΤΗΜΑΤΑ"]
#60

programmes = ["ΟΙΚΟΛΟΓΙΚΗ ΕΞΩΡΥΞΗ ΟΡΥΚΤΩΝ", "ΑΝΑΝΕΩΣΙΜΕΣ ΠΗΓΕΣ ΕΝΕΡΓΕΙΑΣ", "ΕΛΑΧΙΣΤΟΠΟΙΗΣΗ ΡΙΣΚΟΥ ΚΑΙ ΚΙΝΔΥΝΩΝ", "ΓΝΩΣΗ ΧΩΡΙΣ ΣΥΝΟΡΑ",
"ΓΕΝΕΤΙΚΑ ΤΡΟΠΟΠΟΙΗΜΕΝΑ ΥΛΙΚΑ","ΕΛΑΧΙΣΤΟΠΟΙΗΣΗ ΕΝΕΡΓΕΙΑΚΟΥ ΚΟΣΤΟΥΣ", "ΕΦΑΡΜΟΓΕΣ ΜΗΧΑΝΙΚΗΣ ΜΑΘΗΣΗΣ", "ΒΕΛΤΙΣΤΟΠΟΙΗΣΗ ΠΟΛΥΠΛΟΚΟΤΗΤΑΣ ΑΛΓΟΡΙΘΜΩΝ",
"ΑΝΑΛΥΣΗ ΗΧΟΥ", "ΑΝΑΛΥΣΗ ΕΙΚΟΝΑΣ", "ΕΠΕΞΕΡΓΑΣΙΑ ΚΕΙΜΕΝΟΥ", "ΠΡΟΛΗΨΗ ΗΧΟΡΥΠΑΝΣΗΣ","ΥΒΡΙΔΙΚΑ ΟΧΗΜΑΤΑ", "ΗΛΕΚΤΡΙΚΑ ΟΧΗΜΑΤΑ", "ΑΠΟΘΗΚΕΥΣΗ ΕΝΕΡΓΕΙΑΣ"
"ΝΑΝΟΤΕΧΝΟΛΟΓΙΑ","ΜΗΧΑΝΙΚΗ ΚΑΤΑΓΜΑΤΟΣ", "ΑΥΤΟΣΥΝΑΡΜΟΛΟΓΗΣΗ", "ΑΝΙΧΝΕΥΣΗ ΑΣΘΕΝΙΩΝ", "ΜΕΙΩΣΗ ΤΑΞΗΣ ΔΥΝΑΜΙΚΩΝ ΣΥΣΤΗΜΑΤΩΝ", "ΑΥΤΟΝΟΜΑ ΣΥΣΤΗΜΑΤΑ",
"ΚΡΥΟΣΥΝΤΗΡΗΣΗ","ΠΡΟΣΘΕΤΙΚΑ ΕΞΑΡΤΗΜΑΤΑ", "ΘΕΡΑΠΕΙΑ LASER", "ΑΕΡΟΔΥΝΑΜΙΚΗ ΚΑΤΑΣΚΕΥΗ ΕΞΑΡΤΗΜΑΤΩΝ", "ΑΚΟΥΣΤΙΚΗ", "ΔΙΑΣΤΗΜΙΚΑ ΣΥΣΤΗΜΑΤΑ" ,
"ΜΗ ΕΠΑΝΔΡΩΜΕΝΑ ΑΕΡΙΑ ΣΥΣΤΗΜΑΤΑ", "ΜΕΘΟΔΟΙ ΠΕΠΕΡΑΣΜΕΝΩΝ ΣΤΟΙΧΕΙΩΝ", "ΣΧΕΔΙΑΣΜΟΣ ΜΕ ΚΑΘΟΔΗΓΗΣΗ ΔΕΔΟΜΕΝΩΝ", "ΑΕΡΟΕΛΑΣΤΙΚΟΤΗΤΑ", "ΚΒΑΝΤΙΚΟΙ ΥΠΟΛΟΓΙΣΤΕΣ"
,"ΕΛΑΧΙΣΤΟΠΟΙΗΣΗ ΣΦΑΛΜΑΤΩΝ ΣΤΗΝ ΔΙΑΔΩΣΗ ΣΗΜΑΤΩΝ","ΕΦΑΡΜΟΓΕΣ ΠΛΑΣΜΑΤΟΣ","ΜΕΛΕΤΗ ΡΕΥΣΤΩΝ ΚΑΙ ΤΥΡΒΩΔΩΝ ΡΟΩΝ","ΜΗΧΑΝΕΣ ΠΥΡΟΚΡΟΤΗΣΗΣ"]
#35



f = ["ΔΙΑΚΡΙΤΑ ΜΑΘΗΜΑΤΙΚΑ","ΑΛΓΕΒΡΑ","ΡΟΜΠΟΤΙΚΗ","ΜΗΧΑΝΙΚΗ ΔΙΑΣΤΗΜΑΤΟΣ","ΒΙΟΙΑΤΡΙΚΗ","ΑΓΓΛΙΚΗ ΓΛΩΣΣΑ","ΒΙΟΜΗΧΑΝΙΚΗ ΧΗΜΕΙΑ",
"ΕΠΙΣΤΗΜΗ ΥΠΟΛΟΓΙΣΤΩΝ","ΜΗΧΑΝΙΚΗ ΡΕΥΣΤΩΝ", "ΗΛΕΚΤΡΙΚΕΣ ΜΗΧΑΝΕΣ", "ΠΡΟΧΩΡΗΜΕΝΑ ΜΑΘΗΜΑΤΙΚΑ", "ΑΡΧΙΤΕΚΤΟΝΙΚΗ", "ΕΠΙΣΤΗΜΗ ΥΛΙΚΩΝ",
"ΠΟΛΕΟΔΟΜΙΑ","ΚΒΑΝΤΟΜΗΑΧΝΙΚΗ","ΠΥΡΗΝΙΚΗ ΤΕΧΝΟΛΟΓΙΑ","ΕΠΙΚΟΙΝΩΝΙΕΣ","ΝΑΥΤΙΚΗ ΜΗΧΑΝΟΛΟΓΙΑ","ΗΛΕΚΤΡΟΝΙΚΗ", "ΠΕΡΙΒΑΛΛΟΝΤΙΚΗ ΜΗΧΑΝΙΚΗ"]
#20

def org_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):
        orgname = fake.company()
        FLname = orgname.split(" ")
        abbreviation = ""
        for i in range(len(FLname)):
            abbreviation+=FLname[i][0]
        zip1 = fake.bothify(text='#####')
        street = fake.street_name()
        city = fake.city()
        x = random.choice([2, 3])
        phones = [-1,-1,-1]
        for i in range(x):
            phones[i] = fake.bothify(text='##########')
        startdate1 = fake.date()
            
        startdate = filter(str.isdigit, startdate1)
        startdate = "".join(startdate)
        x = random.choice([0, 1, 2])
        orgtype = orgs[x]
        money_their = fake.bothify(text='#####.##')
        if(x==2):
            money_other = fake.bothify(text = '######.##')
        else:
            money_other = 0
        mySql_insert_query = """INSERT INTO organization (abbreviation,
                                                          orgname, zip,
                                                          street, city,
                                                          phone1, phone2,
                                                          phone3, startdate,
                                                          orgtype, money_their,
                                                          money_other) 
                           VALUES 
                           (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        record = (abbreviation, orgname,zip1, street,city,phones[0],
                  phones[1],phones[2], startdate, orgtype, money_their, 
                  money_other)                   
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query,record)
        connection.commit()
        print(cursor.rowcount, "Record inserted succcefully into org table")
        

def researcher_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):
        researcher_name = fake.name()
        FLname = researcher_name.split(" ")
        name1 = FLname[0]
        name2 = FLname[1]
        x = random.choice([0,1])
        if(x==0):
            gender = "Male"
        else:
            gender = "Female"
        date_of_birth = fake.date()
        date_of_birth = filter(str.isdigit, date_of_birth)    
        date_of_birth = "".join(date_of_birth)
        mySql_insert_query = """INSERT INTO researcher (researcher_name,
                                                          surname, gender,
                                                          date_of_birth) 
                           VALUES 
                           (%s,%s,%s,%s) """
        record = (name1,name2,gender,date_of_birth)                   
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query,record)
        connection.commit()
        print(cursor.rowcount, "Record inserted succcefully into researcher table")



def programme_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):
        programme_name = programmes[i]
        address = str(i)
        mySql_insert_query = """INSERT INTO programme (name,address) 
                           VALUES 
                           (%s,%s) """
        record = (programme_name,address)                   
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query,record)
        connection.commit()
        print(cursor.rowcount, "Record inserted succcefully into programme table")



def works_for_org_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):
        org_id = math.ceil(random.uniform(0,org_num))
        researcher_id = i+1
        hiring_date = fake.date()
        hiring_date = filter(str.isdigit, hiring_date)    
        hiring_date = "".join(hiring_date)
        mySql_insert_query = """INSERT INTO works_for_org (organization_id,
                                                       researcher_id,
                                                       hiring_date) 
                           VALUES 
                           (%s,%s,%s) """
        record = (org_id,researcher_id,hiring_date)                   
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query,record)
        connection.commit()
        print(cursor.rowcount, "Record inserted succcefully into works_for_org table")



def project_generate(records,cursor):
    fake = Faker(['el_GR'])
    for j in range(20):
        for i in range(records):
            project_name =projects[i] +" " + str(j+1) 
            abstract = fake.sentence(4)
            org_id = math.ceil(random.uniform(0,org_num))
            programme_id = math.ceil(random.uniform(0,35))
            amount = fake.bothify(text="2#####")
        
            year1 = math.ceil(random.uniform(2005,2022))
            month1 = math.ceil(random.uniform(0,12))
            day1 = math.ceil(random.uniform(0,28))
            
            year2 = math.ceil(random.uniform(year1+1,year1+3))
            month2 = math.ceil(random.uniform(0,12))
            day2 = math.ceil(random.uniform(0,28))
        
            startdate = str(year1)
            if(month1<10):
                startdate+=str(0)
            startdate+=str(month1)
            if(day1<10):
                startdate+=str(0)
            startdate+=str(day1)
        
        
            enddate = str(year2)
            if(month2<10):
                enddate+=str(0)
            enddate+=str(month2)
            if(day2<10):
                enddate+=str(0)
            enddate+=str(day2)
        
            sql_select_query = """select * from works_for_org where organization_id = %s"""
        
            cursor.execute(sql_select_query, (org_id,))
            record = cursor.fetchall()
            if(len(record)==0):
                scientific_supervisor_id=-1
            else:
                idx = math.ceil(random.uniform(-0.99,len(record)-1))
                scientific_supervisor_id = record[idx][2]
            mySql_insert_query = """INSERT INTO project (project_title, abstract,
                                                        org_id, programme_id,
                                                        amount, start_date,
                                                        finish_date,
                                                        scientific_supervisor_id)
                           VALUES 
                           (%s,%s,%s,%s,%s,%s,%s,%s) """
            record = (project_name,abstract,org_id,programme_id,amount,startdate
                  ,enddate,scientific_supervisor_id)                   
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query,record)
            connection.commit()
            print(cursor.rowcount, "Record inserted succcefully into project table")



def works_in_project_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):
        project_id = i+1
        
        my_query = """ SELECT a.project_id,a.scientific_supervisor_id, b.researcher_id FROM project a INNER JOIN works_for_org b ON a.org_id = b.organization_id WHERE a.project_id = %s 
        """
        cursor.execute(my_query,(i+1,))
        record = cursor.fetchall()
        
        length = len(record)
        x = math.ceil(random.uniform(max(length-2,0),length-1))
        
        for _ in range(x):
            if(record[_][2] != record[0][1]):
                mysql_insert_query1 = """ INSERT INTO works_in_project(project_id,
                                            researcher_id)
                                        VALUES
                                        (%s,%s)"""
                record4 = (i+1,record[_][2])
                cursor.execute(mysql_insert_query1,record4)
        
        connection.commit()
        print(cursor.rowcount, "Record inserted succcefully into works_in_project table")



def member_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):
        member_name = fake.name()
        mySql_insert_query = """INSERT INTO member (member_name) 
                           VALUES 
                           (%s) """
        record = ((member_name,))                   
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query,record)
        connection.commit()
        print(cursor.rowcount, "Record inserted succcefully into member table")



def management_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):
        member_id = random.choice([1,2,3,4,5,6,7,8,9,10])
        mySql_insert_query = """INSERT INTO management (member_id,project_id) 
                           VALUES 
                           (%s,%s) """
        record = (member_id,i+1)                   
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query,record)
        connection.commit()
        print(cursor.rowcount, "Record inserted succcefully into management table")
        
        
        
def scientific_field_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):
        field_name = f[i]
        mySql_insert_query = """INSERT INTO scientific_field (field_name) 
                           VALUES 
                           (%s) """
        record = ((field_name,))                   
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query,record)
        connection.commit()
        print(cursor.rowcount, "Record inserted succcefully into scientific_field table")
        
def field_of_project_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):
        project_id = i+1
        times = math.ceil(random.uniform(0.1,14))
        field_id = math.ceil(random.uniform(0.1,14))
        for j in range(times):
            if(field_id == 0):
                field_id = 1
            mySql_insert_query = """INSERT INTO field_of_project (project_id,scientific_field_id) 
                           VALUES 
                           (%s,%s) """
            record = (project_id,field_id)                   
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query,record)
            connection.commit()
            print(cursor.rowcount, "Record inserted succcefully into field_of_project table")
            field_id = (field_id +1)%15


def evaluates_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):
        project_id = i+1
        researcher_id = math.ceil(random.uniform(0.1,researcher_num))
        grade = math.ceil(random.uniform(0,100))
        
        sql_select_query1 = """select * from project where 
                            project_id= %s"""
        
        cursor.execute(sql_select_query1, (i+1,))
        record1 = cursor.fetchall()
        date = record1[0][6]
        
        
        
        mySql_insert_query = """INSERT INTO evaluates (project_id,researcher_id,
                                grade,evaluation_date) 
                           VALUES 
                           (%s,%s,%s,%s) """
        record = (project_id,researcher_id,grade,date)                   
        cursor.execute(mySql_insert_query,record)
        connection.commit()
        print(cursor.rowcount, "Record inserted succcefully into evaluates table")
        
        

def deliverable_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):
        title = "Task: "+fake.word()+" " +fake.word() 
        abstract = fake.sentence(5)
        project_id =i+1
        grade = math.ceil(random.uniform(0,100))
        
        sql_select_query1 = """select * from project where 
                            project_id= %s"""
        
        cursor.execute(sql_select_query1, (i+1,))
        record1 = cursor.fetchall()
        #date = fake.bothify(text="20230#1#")
        date = fake.date_between(record1[0][6],record1[0][7])
        
        
        
        mySql_insert_query = """INSERT INTO deliverable (title,project_id,
                                date,abstract,grade) 
                           VALUES 
                           (%s,%s,%s,%s,%s) """
        record = (title,project_id,date,abstract,grade)                   
        cursor.execute(mySql_insert_query,record)
        connection.commit()
        print(cursor.rowcount, "Record inserted succcefully into deliverables table")
        
def years_generate(records,cursor):
    fake = Faker(['el_GR'])
    for i in range(records):        
        year1 = 2005+i
        month1 = 1
        day1 = 1  
        
        startdate = str(year1)
        if(month1<10):
            startdate+=str(0)
        startdate+=str(month1)
        if(day1<10):
            startdate+=str(0)
        startdate+=str(day1)
        mySql_insert_query = """INSERT INTO years (year_id) 
                           VALUES 
                           (%s) """
        record = (startdate,)                
        cursor.execute(mySql_insert_query,record)
        connection.commit()
        print(cursor.rowcount, "Record inserted succcefully into years table")


try:
    connection = mysql.connector.connect(host = 'localhost',
                                         database = 'Project',
                                         user = 'root',
                                         password = 'sql_fr00tz!2')
    
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ",record)
        org_generate(org_num,cursor)
        researcher_generate(researcher_num,cursor)
        programme_generate(35,cursor)
        works_for_org_generate(researcher_num,cursor)
        project_generate(proj_num,cursor)
        works_in_project_generate(proj_num*20,cursor)
        member_generate(10,cursor)
        management_generate(proj_num, cursor)
        scientific_field_generate(20,cursor)
        field_of_project_generate(proj_num*20,cursor)
        evaluates_generate(proj_num*20,cursor)
        deliverable_generate(5*proj_num,cursor)
        years_generate(50,cursor)

except Error as e:
    print("Error while connecting to MySQL",e)
finally:
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
import string
from flask import Flask, render_template, request
import mysql.connector
import csv
import random
import math
from faker import Faker
from datetime import datetime
from mysql.connector import Error


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'yolo'

    sql_user = 'root'
    sql_password = 'sql_fr00tz!2'
    sql_host = 'localhost'
    sql_db = 'Project'

    connection = mysql.connector.connect(host = 'localhost',
                                     database = 'Project',
                                     user = 'root',
                                     password = 'sql_fr00tz!2')

    
    #@app.route("/",methods = ["GET","POST"])
    #def home():
     #   return render_template("home.html")
    
    #@app.route("/project/<name>")
    #def project(name):
    #    return render_template("project.html",name = name)
    #HOME PAGE QUERIES ON PROJECTS
    @app.route("/",methods=["GET","POST"])
    def dashboard():
        cursor = connection.cursor()

        member_query = """SELECT member.member_name FROM member
        """
        cursor.execute(member_query)
        members = cursor.fetchall()
        #members.append('')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        min_dur = request.form.get('min_dur')
        max_dur = request.form.get('max_dur')
        member = request.form.get('add_member')
        if(start_date== None or start_date=='' ):
            start_date = datetime.strptime('1900-01-01', '%Y-%m-%d')
        if(end_date== None or end_date== ''):
            end_date = datetime.strptime('3000-01-01', '%Y-%m-%d')
        if(min_dur== None or min_dur==''):
            min_dur = 0
        if(max_dur== None or max_dur == ''):
            max_dur = 10000
        if(member== ''):
            mquery = ''
        else:
            mquery = 'AND member.member_name = %s'
        
        #end_query = """GROUP BY project.id"""

        my_query1 = """ SELECT project.project_title, project.abstract, project.start_date,
        project.finish_date, member.member_name, project.amount, project.project_id FROM 
        project LEFT JOIN management ON
        project.project_id = management.project_id LEFT JOIN 
        member ON management.member_id = member.member_id 
        WHERE project.start_date > %s AND project.finish_date < %s
        AND DATEDIFF(project.finish_date,project.start_date)/365> %s 
        AND DATEDIFF(project.finish_date,project.start_date)/365 < %s
        """
        if(member==''):
            cursor.execute(my_query1,(start_date,end_date,min_dur,max_dur))
        else:
            cursor.execute(my_query1+mquery,(start_date,end_date,min_dur,max_dur,member))
        results1 = cursor.fetchall()
        return render_template("dashboard.html", results = results1,members = members, q_name = "project", term1 = "project_id",none = "none")
    

    #PAGE WITH ALL RESEARCHERS WORKING IN PROJECT WITH ID=<id>
    @app.route("/project/<id>",methods=["GET","POST"])
    def project(id):
        cursor = connection.cursor()
        my_query = """SELECT project.project_title, researcher.researcher_name, researcher.surname, researcher.researcher_id FROM project INNER JOIN works_in_project ON project.project_id = works_in_project.project_id INNER JOIN researcher ON researcher.researcher_id = works_in_project.researcher_id WHERE project.project_id = %s and project.scientific_supervisor_id != researcher.researcher_id
        """
        my_query2 = """ SELECT researcher.researcher_name, researcher.surname, researcher.researcher_id FROM project INNER JOIN researcher ON researcher.researcher_id = project.scientific_supervisor_id WHERE project.project_id = %s
        """
        my_query3="""SELECT d.project_id, d.title, d.abstract, d.date,d.grade FROM deliverable d WHERE d.project_id =%s
        """
        my_query4 = """SELECT e.evaluation_id, e.researcher_id, e.grade, e.evaluation_date FROM evaluates e WHERE e.project_id = %s
        """
        cursor.execute(my_query,(id,))
        results = cursor.fetchall()
        cursor.execute(my_query2,(id,))
        super = cursor.fetchall()
        cursor.execute(my_query3,(id,))
        deli = cursor.fetchall()
        cursor.execute(my_query4,(id,))
        eva = cursor.fetchall()
        return render_template("project.html",results = results,ii = id,q_name="works_in_project",q_name1 = "deliverable", q_name2 = "evaluates",term1="works_in_project_id",
        term2 = "title",term3="evaluation_id",pp="project",superr = super,deli = deli, eva = eva)

    #PAGE LISTING ALL RESEARCHERS
    @app.route("/researchers", methods = ["GET","POST"])
    def researchers():
        cursor = connection.cursor()

        my_query = """SELECT researcher.researcher_name, researcher.surname, researcher.researcher_id FROM researcher ORDER BY researcher.surname
        """
        cursor.execute(my_query)
        results = cursor.fetchall()


        return render_template("researchers.html", results = results, table = "researcher",term1 = "researcher_id")
    
    #PAGE LISTING ALL PROJECTS RESEARCHER WITH ID=<id> WORKS IN
    @app.route("/researcher/<id>", methods = ["GET","POST"])
    def researcher(id):
        cursor = connection.cursor()

        my_query = """SELECT project.project_title, project.project_id from project INNER JOIN works_in_project ON works_in_project.project_id = project.project_id WHERE works_in_project.researcher_id = %s 
        """
        my_query1 = """SELECT researcher.researcher_name, researcher.surname FROM researcher where researcher.researcher_id = %s
        """
        cursor.execute(my_query,(id,))
        results = cursor.fetchall()

        cursor.execute(my_query1,(id,))
        results1 = cursor.fetchall()


        return render_template("researcher.html", results = results, id = id, results1 = results1)


    @app.route("/organizations", methods = ["GET","POST"])
    def organizations():
        cursor = connection.cursor()

        my_query = """SELECT organization.organization_id, organization.orgname FROM organization ORDER BY organization.orgname
        """
        cursor.execute(my_query)
        results = cursor.fetchall()

        return render_template("organizations.html", results = results, term1 = "organization_id", term2 = "none", table = "organization")
    
    @app.route("/organization/<id>", methods = ["GET","POST"])
    def organization(id):
        cursor = connection.cursor()

        my_query = """SELECT project.project_title,project.project_id FROM project where project.org_id = %s
        """
        my_query1 = """SELECT researcher.researcher_name, researcher.surname,researcher.researcher_id FROM works_for_org INNER JOIN researcher ON 
        works_for_org.researcher_id = researcher.researcher_id where works_for_org.organization_id = %s
        """

        cursor.execute(my_query, (id,))
        results = cursor.fetchall()
        cursor.execute(my_query1, (id,))
        results1 = cursor.fetchall()

        return render_template("organization.html", results = results, results1 = results1, table1 ="works_for_org",id1 = "researcher_id",id2 = "organization_id",ii=id)

    @app.route("/members", methods = ["GET","POST"])
    def members():
        cursor = connection.cursor()

        my_query = """SELECT member.member_id, member.member_name FROM member ORDER BY member.member_id
        """
        cursor.execute(my_query)
        results = cursor.fetchall()

        return render_template("members.html", results = results, term1 = "member_id", table = "member")

    @app.route("/member/<id>", methods = ["GET","POST"])
    def member(id):
        cursor = connection.cursor()

        my_query = """SELECT project.project_title, project.project_id FROM member INNER JOIN management ON member.member_id = management.member_id INNER JOIN project ON project.project_id= management.project_id  WHERE member.member_id =%s       """
        cursor.execute(my_query,(id,))
        results = cursor.fetchall()

        return render_template("member.html", results = results, term1 = "project_id", table = "project", id = id )
    @app.route("/programmes", methods = ["GET","POST"])
    def programmes():
        cursor = connection.cursor()

        my_query = """SELECT programme.programme_id,programme.name, programme.address FROM programme ORDER BY programme.name
        """
        cursor.execute(my_query)
        results = cursor.fetchall()

        return render_template("programmes.html", results = results, term1 = "programme_id", table = "programme")

    @app.route("/programme/<id>", methods = ["GET","POST"])
    def programme(id):
        cursor = connection.cursor()

        my_query = """SELECT project.project_title, project.project_id FROM project WHERE project.programme_id= %s         """
        cursor.execute(my_query,(id,))
        results = cursor.fetchall()

        return render_template("programme.html", results = results, term1 = "project_id", table = "project", id = id )



    @app.route("/wonderkid", methods = ["GET","POST"])
    def wonderkid():
        cursor = connection.cursor()

        my_query = """SELECT a.researcher_name, a.surname, COUNT(b.project_id) FROM researcher a INNER JOIN works_in_project b ON a.researcher_id = b.researcher_id INNER JOIN project c ON c.project_id = b.project_id WHERE c.finish_date > CURDATE() AND DATEDIFF(CURDATE(),a.date_of_birth) /365 < 40 GROUP BY a.researcher_id ORDER BY COUNT(b.project_id) DESC
        """

        cursor.execute(my_query)
        results = cursor.fetchall()


        return render_template("wonderkid.html", results = results)


    @app.route("/least_deliverables", methods = ["GET","POST"])
    def deliverables():
        cursor = connection.cursor()
        view_query = """CREATE OR REPLACE VIEW no_deliverables (project_id, project_title, finish_date, start_date )
AS
SELECT a.project_id, a.project_title, a.finish_date, a.start_date
FROM project a 
WHERE a.project_id NOT IN 
(SELECT c.project_id FROM deliverable c WHERE c.date>CURDATE())"""
        my_query = """SELECT r.researcher_id, r.researcher_name,r.surname, COUNT(b.project_id) 
FROM researcher r INNER JOIN works_in_project w ON r.researcher_id = w.researcher_id 
INNER JOIN no_deliverables b ON w.project_id = b.project_id
GROUP BY r.researcher_id
ORDER BY COUNT(b.project_id) DESC 
        """
        cursor.execute(view_query)
        cursor.execute(my_query)
        results = cursor.fetchall()
        top = []
        for i in range(len(results)):
            if(results[i][3] > 4):
                top.append(results[i])

        return render_template("least_deliverables.html", results = top)
    @app.route("/highest_financial_aid", methods = ["GET","POST"])
    def finance():
        cursor = connection.cursor()

        my_query = """SELECT c.orgname, b.member_id, SUM(a.amount)
FROM project a INNER JOIN management b  ON b.project_id = a.project_id  
INNER JOIN organization c ON a.org_id = c.organization_id WHERE c.orgtype = "Εταιρεία" 
group by a.org_id, b.member_id 
ORDER BY SUM(a.amount) DESC
        """
        cursor.execute(my_query)
        results = cursor.fetchall()

        top = []
        for i in range(5):
            my_query2 = """ SELECT a.member_name FROM member a WHERE a.member_id = %s
            """
            cursor.execute(my_query2,(results[i][1],))
            results2 = cursor.fetchall()

            top.append((results[i][2], results[i][0], results2[0][0]))

        return render_template("highest_financial_aid.html", results = top)
    @app.route("/input", methods =["GET","POST"])
    def input():
        cursor = connection.cursor()
        return render_template("input.html")
    @app.route("/input_company", methods =["GET","POST"])
    def input_company():
        abbreviation = request.form.get('abbreviation')
        orgname = request.form.get('orgname')
        zip = request.form.get('zip')
        street = request.form.get('street')
        city = request.form.get('city')
        phone1 = request.form.get('phone1')
        phone2 = request.form.get('phone2')
        phone3 = request.form.get('phone3')
        money = request.form.get('money_their')
        start_date = request.form.get('start_date')

        if(abbreviation!=None  and abbreviation!='' and
        orgname!=None  and orgname!='' and
        zip!=None  and zip!='' and
        street!=None  and street!='' and
        city!=None  and city!='' and
        phone1!=None  and phone1!='' and
        phone2!=None  and phone2!='' and
        phone3!=None  and phone3!='' and
        money!=None  and money!='' and
        start_date!=None  and start_date!=''):
            mySql_insert_query = """INSERT INTO organization (abbreviation,
                                                              orgname, zip,
                                                              street, city,
                                                              phone1, phone2,
                                                              phone3, startdate,
                                                              orgtype, money_their,
                                                              money_other) 
                                VALUES 
                                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            record = (abbreviation, orgname,zip, street,city,phone1,
                      phone2,phone3, start_date, 'Company', money, 
                      0)

            cursor = connection.cursor()
            cursor.execute(mySql_insert_query,record)
            connection.commit()
            return render_template("success.html")


        
        return render_template("input_company.html")
    @app.route("/input_research_center", methods =["GET","POST"])
    def input_research_center():
        abbreviation = request.form.get('abbreviation')
        orgname = request.form.get('orgname')
        zip = request.form.get('zip')
        street = request.form.get('street')
        city = request.form.get('city')
        phone1 = request.form.get('phone1')
        phone2 = request.form.get('phone2')
        phone3 = request.form.get('phone3')
        money = request.form.get('money_their')
        money1 = request.form.get('money_other')
        start_date = request.form.get('start_date')

        orgtype = "Research center"
        if(abbreviation!=None  and abbreviation!='' and
        orgname!=None  and orgname!='' and
        zip!=None  and zip!='' and
        street!=None  and street!='' and
        city!=None  and city!='' and
        phone1!=None  and phone1!='' and
        phone2!=None  and phone2!='' and
        phone3!=None  and phone3!='' and
        money!=None  and money!='' and
        start_date!=None  and start_date!=''):
            mySql_insert_query = """INSERT INTO organization (abbreviation,
                                                              orgname, zip,
                                                              street, city,
                                                              phone1, phone2,
                                                              phone3, startdate,
                                                              orgtype, money_their,
                                                              money_other) 
                                VALUES 
                                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            record = (abbreviation, orgname,zip, street,city,phone1,
                      phone2,phone3, start_date, orgtype, money, 
                      money1)

            cursor = connection.cursor()
            cursor.execute(mySql_insert_query,record)
            connection.commit()
            return render_template("success.html")


        
        return render_template("input_research_center.html")
    @app.route("/input_university", methods =["GET","POST"])
    def input_university():
        abbreviation = request.form.get('abbreviation')
        orgname = request.form.get('orgname')
        zip = request.form.get('zip')
        street = request.form.get('street')
        city = request.form.get('city')
        phone1 = request.form.get('phone1')
        phone2 = request.form.get('phone2')
        phone3 = request.form.get('phone3')
        money = request.form.get('money_their')
        start_date = request.form.get('start_date')

        if(abbreviation!=None  and abbreviation!='' and
        orgname!=None  and orgname!='' and
        zip!=None  and zip!='' and
        street!=None  and street!='' and
        city!=None  and city!='' and
        phone1!=None  and phone1!='' and
        phone2!=None  and phone2!='' and
        phone3!=None  and phone3!='' and
        money!=None  and money!='' and
        start_date!=None  and start_date!=''):
            mySql_insert_query = """INSERT INTO organization (abbreviation,
                                                              orgname, zip,
                                                              street, city,
                                                              phone1, phone2,
                                                              phone3, startdate,
                                                              orgtype, money_their,
                                                              money_other) 
                                VALUES 
                                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            record = (abbreviation, orgname,zip, street,city,phone1,
                      phone2,phone3, start_date, 'University', money, 
                      0)

            cursor = connection.cursor()
            cursor.execute(mySql_insert_query,record)
            connection.commit()
            return render_template("success.html")

    @app.route("/input_project", methods =["GET","POST"])
    def input_project():
        cursor = connection.cursor()
        query = """ select organization.organization_id, organization.orgname FROM organization 
        """
        cursor.execute(query)
        orgs = cursor.fetchall()
        title = request.form.get('title')
        abstract = request.form.get('abstract')
        org_id = request.form.get('org_id')
        programme_id = request.form.get('programme_id')
        amount = request.form.get('amount')
        scientific_supervisor_id = request.form.get('scientific_supervisor_id')
        finish_date = request.form.get('finish_date')
        start_date = request.form.get('start_date')
        print(start_date)
        print(finish_date)


        if(title!=None  and title!='' and
        abstract!= None and abstract!= ''and
        org_id!=None  and org_id!='' and
        programme_id!=None  and programme_id!='' and
        amount!=None  and amount!='' and
        finish_date!=None and finish_date !='' and
        scientific_supervisor_id!=None  and scientific_supervisor_id!='' ):
            try:
                mySql_insert_query = """INSERT INTO project (project_title,
                                                              abstract,org_id ,
                                                              programme_id, amount,
                                                              scientific_supervisor_id, start_date,
                                                              finish_date) 
                                VALUES 
                                (%s,%s,%s,%s,%s,%s,%s,%s) """
                record = (title, abstract,org_id, programme_id,amount,scientific_supervisor_id,start_date,
                      finish_date)
                cursor.execute(mySql_insert_query,record)
                connection.commit()
            except mysql.connector.Error as err:
                return render_template("error.html", message = "Something went wrong: {}".format(err))
        return render_template("input_project.html",orgs = orgs)

    @app.route("/input_member", methods =["GET","POST"])
    def input_member():
        cursor = connection.cursor()
        name = request.form.get('name')


        if(name !=None and name !=''):
            try:
                mySql_insert_query = """INSERT INTO member (member_name) 
                                VALUES 
                                (%s) """
                record = (name,)
                cursor.execute(mySql_insert_query,record)
                connection.commit()
            except mysql.connector.Error as err:
                return render_template("error.html", message = "Something went wrong: {}".format(err))
        return render_template("input_member.html")
    @app.route("/input_programme", methods =["GET","POST"])
    def input_programme():
        cursor = connection.cursor()
        name = request.form.get('name')
        address = request.form.get('address')


        if(name !=None and name !=''):
            try:
                mySql_insert_query = """INSERT INTO programme (name, address) 
                                VALUES 
                                (%s,%s) """
                record = (name,address)
                cursor.execute(mySql_insert_query,record)
                connection.commit()
            except mysql.connector.Error as err:
                return render_template("error.html", message = "Something went wrong: {}".format(err))      
        return render_template("input_programme.html")
    @app.route("/success")
    def success():
        return render_template("success.html")


    @app.route("/deletion/<table>/<term1>/<id1>",methods =["GET","POST"])
    def deletion(table,term1,id1):
        cursor = connection.cursor()
        myquery = """DELETE FROM """ + table + """ WHERE """ + table +"""."""+term1+"""= %s"""
        cursor.execute(myquery,(id1,))
        connection.commit()
        return render_template("deletion.html")

    @app.route("/oloidia", methods = ["GET","POST"])
    def oloidia():
       cursor = connection.cursor()
       view_query = """CREATE OR REPLACE VIEW projects_per_organization_per_year (organization_id, organization_name, projects, yearr)
AS
SELECT o.organization_id, o.orgname, COUNT(*), y.year_id as yearr 
FROM organization o INNER JOIN project p ON o.organization_id = p.org_id
INNER JOIN years y ON DATEDIFF(y.year_id,p.start_date)>0 and DATEDIFF(y.year_id,p.finish_date)<0
GROUP BY o.organization_id, yearr"""
       cursor.execute(view_query)
       my_query = """select o.organization_name, o.organization_id, o.projects, o.yearr FROM 
projects_per_organization_per_year o INNER JOIN projects_per_organization_per_year y
ON o.organization_id = y.organization_id
WHERE o.projects=y.projects AND o.projects>=10 AND YEAR(o.yearr)-YEAR(y.yearr)=-1
        """
       cursor.execute(my_query)
       results = cursor.fetchall()

       return render_template("oloidia.html", results = results)

    @app.route("/hot_topic",methods = ["GET","POST"])
    def hot_topic():
        cursor =  connection.cursor()
        view_query = """CREATE OR REPLACE VIEW sci_fields_couples (first_field, second_field, projects, first_name, second_name)
AS
SELECT s.scientific_field_id as first_field, ss.scientific_field_id as second_field, COUNT(*) as projects, s.field_name as first_name, ss.field_name as second_name
FROM scientific_field s INNER JOIN scientific_field ss 
INNER JOIN field_of_project  f ON (s.scientific_field_id = f.scientific_field_id or ss.scientific_field_id = f.scientific_field_id  )
WHERE s.scientific_field_id != ss.scientific_field_id
GROUP BY s.scientific_field_id, ss.scientific_field_id
ORDER BY projects DESC;"""
        my_query = """SELECT * FROM sci_fields_couples
        """
        cursor.execute(view_query)
        cursor.execute(my_query)
        results = cursor.fetchall()
        dif =  2
        top = []
        top.append(results[0])
        if (results[1][0]!=results[0][1] or results[0][0] != results[1][1]):
            top.append(results[1])
            dif=dif-1
            if(results[2][0]!= results[1][1] or results[2][1] != results[1][0]):
                top.append(results[2])
            else:
                top.append(results[3])
        else:
            top.append(results[2])
            if(results[2][0]!= results[3][1] or results[2][1] !=results[3][0]):
                top.append(results[3])
            else:
                top.append(results[4])
        cursor.close()
        return render_template("hot_topic.html" , results = top)


    @app.route("/input_deliverable", methods =["GET","POST"])
    def input_deliverable():
        cursor = connection.cursor()
        query = """ select project.project_id, project.project_title FROM project 
        """
        cursor.execute(query)
        orgs = cursor.fetchall()
        title = request.form.get('title')
        abstract = request.form.get('abstract')
        project_id = request.form.get('project_id')
        grade = request.form.get('grade')
        date = request.form.get('date')


        if(title!=None  and title!='' and
        abstract!= None and abstract!= ''and
        project_id!=None  and project_id!='' and
        date!=None and date !='' ):
            try:
                mySql_insert_query = """INSERT INTO deliverable (project_id,
                                                              abstract,title ,
                                                              date, grade) 
                                VALUES 
                                (%s,%s,%s,%s,%s) """
                record = (project_id, abstract,title,date,grade)
                cursor.execute(mySql_insert_query,record)
                connection.commit()
            except mysql.connector.Error as err:
                return render_template("error.html", message = "Something went wrong: {}".format(err))
        return render_template("input_deliverable.html",orgs = orgs)

    @app.route("/input_researcher", methods =["GET","POST"])
    def input_researcher():
        cursor = connection.cursor()
        query = """ select project.project_id, project.project_title FROM project 
        """
        cursor.execute(query)

        query = """ select organization.organization_id, organization.orgname FROM organization
        """
        projs = cursor.fetchall()
        
        cursor.execute(query)
        orgs = cursor.fetchall()
        researcher_name = request.form.get('researcher_name')
        surname = request.form.get('surname')
        gender = request.form.get('gender')
        date_of_birth = request.form.get('date_of_birth')
        works = request.form.getlist('works')
        org = request.form.get('orgg')



        if(researcher_name!=None  and researcher_name!='' and
        surname!= None and surname!= ''and
        gender!=None  and gender!='' and
        date_of_birth!=None and date_of_birth !='' ):
            try:
                mySql_insert_query = """INSERT INTO researcher (researcher_name,
                                                              surname,gender ,
                                                              date_of_birth) 
                                VALUES 
                                (%s,%s,%s,%s) """
                record = (researcher_name,surname,gender ,date_of_birth)
                cursor.execute(mySql_insert_query,record)
                connection.commit()
                print("done")
                q = """SELECT LAST_INSERT_ID()
                """
                cursor.execute(q)
                res_id = cursor.fetchall()
                for i in range(len(works)):
                    mySql_insert_query = """INSERT INTO works_in_project (researcher_id,
                                                              project_id) 
                                VALUES 
                                (%s,%s) """
                    print("ok1")
                    record = (res_id[0][0],works[i][0])
                    print("ok2")
                    cursor.execute(mySql_insert_query,record)
                    print("ok3")
                    connection.commit()
                print("ok1 all")
                mySql_insert_query = """INSERT INTO works_for_org (researcher_id,
                                                              organization_id,hiring_date) 
                                VALUES 
                                (%s,%s,CURDATE()) """
                record = (res_id[0][0],org)
                cursor.execute(mySql_insert_query,record)
                connection.commit()
            except mysql.connector.Error as err:
                return render_template("error.html", message = "Something went wrong: {}".format(err))
        return render_template("input_researcher.html",orgs = orgs, projs = projs)

    @app.route("/input_field", methods =["GET","POST"])
    def input_field():
        cursor = connection.cursor()
        field_name = request.form.get('field_name')


        if(field_name !=None and field_name !=''):
            try:
                mySql_insert_query = """INSERT INTO scientific_field (field_name) 
                                VALUES 
                                (%s) """
                record = (field_name)
                cursor.execute(mySql_insert_query,record)
                connection.commit()
            except mysql.connector.Error as err:
                return render_template("error.html", message = "Something went wrong: {}".format(err))      
        return render_template("input_field.html")



    @app.route("/interesting", methods = ["GET","POST"])
    def interesting():
        cursor = connection.cursor()
        query = """select * from scientific_field 
        """
        cursor.execute(query)
        results = cursor.fetchall()
        field_id = request.form.get('field_id')
        record1 = []
        if(field_id != None and field_id != ''):

            query2 = """SELECT p.project_title, r.researcher_name, r.surname FROM 
            field_of_project fp INNER JOIN project p ON p.project_id = fp.project_id
            INNER JOIN works_in_project wp ON p.project_id = wp.project_id
            INNER JOIN researcher r ON wp.researcher_id = r.researcher_id
            WHERE p.start_date < CURDATE() and p.finish_date> CURDATE() and fp.scientific_field_id = %s
            ORDER BY p.project_title
            """
            record = (field_id,)
            cursor.execute(query2,record)
            record1 = cursor.fetchall()
        return render_template("interesting.html",results = results , records = record1)



    return app
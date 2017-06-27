#
#
#
#
# This web Application stores the student information into the database and performs operations on the information
# and displays it as per the requirement
# There are two roles Admin and Student
# Admin is protected with a userId and password who can enter the secured information of students like marks
# Student can retrieve his/her information using the roll number provided by the college
# Application displays the students marks information for given particular semester
#
#





from flask import Flask,render_template,request,redirect,url_for
import sqlite3

#
# the subject names of 8 semesters is stored in "sub" list of lists
#

sub=[['ENGLISH','MATHS-1','MATHS-2','PHYSICS-1','CP','ES'], \
     ['PHYSICS-2', 'MATHS-3', 'DS', 'CHEMISTRY', 'DRAWING', 'ANS'],\
     ['OOPS','MFCS','STLD','BEE','ADS','SS'],\
     ['JAVA','P&S','DBMS','CO','FLAT','DAA'],\
     ['CN','PE-1','OS','SE','MEFA','APL'],\
     ['WT','CD','PE-2','PE-3','.NET&C#','INFS'],\
     ['LINUX','PE-4','PE-5','OE-1','SL','STTL'],\
     ['MS','OE-2','OE-3','PW','SMNR','EDS']]



#
# object is created for student data base
#
app=Flask(__name__)


#
# Directing to home page
# Redirecting to home page
#

@app.route('/')
def main():
    return redirect(url_for('home'))

#
# Directing to home page
# Returning home page template
#

@app.route('/home')
def home():
    return render_template("home.html")


#
# Directing to adminpage when admin button is clicked
# Returning adminpage template
#

@app.route('/adminpage',methods=['POST','GET'])
def adminpage():
    return render_template("adminpage.html")



#
# Directing to studentpage when student button is clicked
# Returns studentpage
#

@app.route('/studentpage',methods=['POST','GET'])
def studentpage():
    return render_template("studentpage.html")



#
# Directing to resultpage from studentpage after entering id and semester
# Retreives id,semester from studentpage and stores in id,sem
# Checks whether id present in studentinfo table
# Retreives data from marklist table for given id and semester
# Connects to student database
# Fetches the result and stores the result
# Checks whether the given semester details are present in database
# Creates a cur object to store the result of the query
# Retreives data from marklist table for given id and semester
#

@app.route('/studentlogin',methods=['POST','GET'])
def studentlogin():
    id=request.form['rollno']
    sem=request.form['sem']
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('select id from studentinfo where id=?',[id])
    result=cur.fetchall()
    if result==[]:
        return 'INVALID ID!!!'
    conn.commit()
    conn.close()
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('select id from marklist where semester=?', [sem])
    result = cur.fetchall()
    if result==[]:
        return 'DATA NOT YET UPDATED...'
    conn.commit()
    conn.close()
#
# Creating a tuple "t" with id and sem
# Retrieves data from marklist table for given id and semester
#

    conn = sqlite3.connect('students.db')
    cur=conn.cursor()
    t=[id,sem]
    cur.execute("select * from marklist where id=? and semester=?",t)
    result=cur.fetchall()
    conn.commit()
    conn.close()

#
# Connects to database to retreive name and cgpa of student
# Retreives data from studentinfo table for given id
# Stores name,cpga of student in "nm","cgpa".
#
    conn = sqlite3.connect('students.db')
    cur1 = conn.cursor()
    cur1.execute('select name,cgpa from studentinfo where id=?',[id])
    nam=cur1.fetchone()
    conn.close()
    nm=nam[0]
    cgpa=nam[1]

#
# Connects to database to find sgpa of given id and semester
# Retreives data from findgpa table for given id and semester
# Stores sgpa of student in a semester in "sgpa".
#
    conn = sqlite3.connect('students.db')
    cur2 = conn.cursor()
    cur2.execute('select gpa from findgpa where id=? and semester=?', [id,sem])
    spa= cur2.fetchone()
    conn.close()
    sgpa=spa[0]
    return render_template('results.html',r=result,n=nm,i=id,s=sem,cg=cgpa,sg=sgpa)



#
# Directs to adminlogin page from adminpage after validating userid and password
# Retreives userid from adminpage and storing in "userid".
# Retreives password from adminpage and storing in "password".
# Validates userid and password
#

@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    userid=request.form['id']
    password=request.form['password']
    dic={"admin1":"admin1","admin2":"admin2","admin3":"admin3"}
    if userid in dic.keys():
        if dic[userid]==password:
            return render_template("adminlogin.html",id=userid,pw=password)
        else:
            return  "error : invalid password"
    else:
        return "error : invalid user id or password"


#
# Directing to studentinfo page from adminlogin page when addstudent is selected
#

@app.route('/addstudent/<s>',methods=['POST','GET'])
def addstudent(s='acf'):

    return render_template('studentinfo.html',s=s)


#
# finds Year of the student from the given roll number
# enters the students information int the database
#


@app.route('/studentinfo',methods=['POST','GET'])
def studentinfo():
    name=request.form['name']
    i=request.form['rollno']
    k=i[:2]
    if k=='16':
        y=1
    elif k=='15':
        y=2
    elif k=='14':
        y=3
    elif k=='13':
        y=4
    else:
        return "invalid Roll Number"
    t=(i,name,y,0.0)
    conn = sqlite3.connect('students.db')
    conn.execute("insert into studentinfo values(?,?,?,?)",t)
    conn.commit()
    return redirect(url_for('addstudent',s='added'))






@app.route('/updatestudent',methods=['POST','GET'])
def updatestudent(sta=''):
    return render_template('update.html',k=sta)


#
# collects information about the student  marks in the particular semester from the web page
# and calculates the grades ,gradepoints ,CGPA(Cummulative Grade Point Average) and SGPA(Summative Grade Point Average)
# stores all the information into the database
#

@app.route('/dataset',methods=['POST','GET'])
def dataset():
    l=[]
    l.append(float(request.form['m0']))
    l.append(float(request.form['m1']))
    l.append(float(request.form['m2']))
    l.append(float(request.form['m3']))
    l.append(float(request.form['m4']))
    l.append(float(request.form['m5']))
    s = int(request.form['s'])
    k = request.form['r']

    g=[]
    gp=[]
    sgp=0.0
    for i in range(6):
        if l[i]>=85:
            g.append('O')
            gp.append(10)
        elif l[i]>=70:
            g.append('A')
            gp.append(9)
        elif l[i]>=60:
            g.append('B')
            gp.append(8)
        elif l[i]>=55:
            g.append('C')
            gp.append(7)
        elif l[i]>=50:
            g.append('D')
            gp.append(6)
        elif l[i]>=40:
            g.append('P')
            gp.append(5)
        else:
            g.append('F')
            gp.append(0)
        sgp=sgp+gp[i]
    sgp=format(sgp/6,'.3f')


    conn = sqlite3.connect('students.db')
    for j in range(6):
        li=[k,sub[s-1][j],l[j],g[j],gp[j],s]
        conn.execute('insert into marklist values(?,?,?,?,?,?)',li)
    conn.commit()
    conn.close()

    p=[k,s,sgp]
    conn = sqlite3.connect('students.db')
    conn.execute('insert into findgpa values(?,?,?)',p)
    conn.commit()
    conn.close()

    conn = sqlite3.connect('students.db')
    cur1=conn.cursor()
    cur1=conn.execute('select count(*) from findgpa where id=?',[k])
    c=cur1.fetchone()

    d=int(c[0])
    conn.commit()
    conn.close()


    conn = sqlite3.connect('students.db')
    cur2=conn.cursor()
    cur2 = conn.execute('select sum(gpa) from findgpa where id=?', [k])
    sum = cur2.fetchone()
    summ=float(sum[0])
    conn.commit()
    conn.close()


    f=[format(summ/d,'.3f'),k]
    conn = sqlite3.connect('students.db')
    conn.execute('update studentinfo set cgpa=? where id=?',f)
    conn.commit()
    conn.close()

    return redirect(url_for('updatestudent',sta='added'))

#
# This directs to the page where the marks of the student of a particular
# sends all the student details as parameters to the web page
# web page displays the subjects of particular semester where marks to be entered by the admin
#


@app.route('/updatedata',methods=['POST','GET'])
def updatedata():
    rollno = request.form['id']
    sem=request.form['sem']
    a=int(sem)
    r=[rollno]
    conn = sqlite3.connect('students.db')
    cur=conn.cursor()
    cur.execute(" select id from studentinfo where id=?",r)
    r=cur.fetchone()
    if r!=None:
        return render_template('enterdata.html',r=rollno,s=sem,sub=sub[a-1])
    else:
        return redirect(url_for('updatestudent',sta='invalid id'))



#
# if the name of the module is __main__ the application starts running
# the Debug mode is enabled by setting debug=True
#

if __name__=="__main__":
    app.run(debug=True)

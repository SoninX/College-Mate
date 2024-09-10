from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, request, redirect, session
import datetime
from DBConnection import Db
import random, demjson

app = Flask(__name__)
app.secret_key = "abc"
path1 = r"C:\Users\HP\Desktop\KJC\II SEM\Mini Project\e-edu\static\student_photos\\"
path = r"C:\Users\HP\Desktop\KJC\II SEM\Mini Project\e-edu\static\staff_photos\\"
path2 = r"C:\Users\HP\Desktop\KJC\II SEM\Mini Project\e-edu\static\syllabus\\"
path3 = r"C:\Users\HP\Desktop\KJC\II SEM\Mini Project\e-edu\static\notes\\"
path4 = r"C:\Users\HP\Desktop\KJC\II SEM\Mini Project\e-edu\static\qp\\"


@app.route('/')
def index():
    return render_template("login_index.html")


@app.route('/login', methods=['get', 'post'])
def login():
    if request.method == "POST":
        username = request.form['textfield']
        password = request.form['textfield2']
        db = Db()
        res = db.selectOne("select * from login where username ='" + username + "'and password ='" + password + "'")
        if res is not None:
            session['lg'] = 'lin'
            if res['usertype'] == 'admin':

                return redirect('/admin_home')
            elif res['usertype'] == 'staff':
                session['lid'] = res['login_id']
                return redirect('/staff_home')
            elif res['usertype'] == 'company':
                session['lid'] = res['login_id']
                return redirect('/company_home')
            elif res['usertype'] == 'student':
                session['lid'] = res['login_id']
                db = Db()
                q = db.selectOne("select * from student where stud_id='" + str(res['login_id']) + "'")
                session['course_id'] = q['stud_course_id']
                session['sem'] = q['semester']
                return redirect('/student_home')
            else:
                return '''<script>alert("INVALID USER");window.location ="/login"</script>'''
        else:
            return '''<script>alert("INVALID USER");window.location ="/login"</script>'''
    return render_template('contact.html')


# ---------------------------------------------------------
#    Admin
# ---------------------------------------------------------
@app.route('/admin_home')
def admin_home():
    if session['lg'] == 'lin':
        return render_template('admin/admin_index.html')
    else:
        return redirect('/')


@app.route('/add_department', methods=['get', 'post'])
def add_department():
    if session['lg'] == 'lin':

        if request.method == "POST":
            department = request.form['textfield']
            db = Db()
            qry = db.selectOne("select * from department where dept_name='" + department + "'")
            if qry is not None:
                return '<script> alert("Already added ");window.location = "/add_department"</script>'
            else:
                db.insert("insert into department VALUES ('','" + department + "')")
                return '<script> alert("added sucessfully");window.location = "/add_department"</script>'
        else:
            return render_template('admin/add department.html')
    else:
        return redirect('/')


@app.route('/view_department')
def view_department():
    if session['lg'] == 'lin':

        db = Db()
        res = db.select("select * from department")
    else:
        return redirect('/')

    return render_template('admin/view department.html', data=res)


@app.route('/department_delete/<aid>')
def department_delete(aid):
    if session['lg'] == 'lin':
        db = Db()
        db.delete("delete from  department where dept_id='" + aid + "'")
        return redirect('/view_department')
    else:
        return redirect('/')


@app.route('/add_staff', methods=['get', 'post'])
def add_staff():
    if session['lg'] == 'lin':
        if request.method == "POST":
            staff_name = request.form['textfield']
            gender = request.form['RadioGroup1']
            place = request.form['textfield4']
            dept = request.form['select']
            post = request.form['textfield2']
            pin = request.form['textfield3']
            qualification = request.form['textfield1']
            mobile_number = request.form['textfield5']
            email = request.form['textfield6']
            photo = request.files['fileField']
            passwd = random.randint(0000, 9999)
            d = datetime.datetime.now().strftime("%y%m%d%H%M%S")
            photo.save(path + d + '.jpg')
            staff_photo = "/static/staff_photos/" + d + '.jpg'
            db = Db()
            qry = db.selectOne("select * from login where username='" + email + "'")
            if qry is not None:
                return '<script> alert("Email Already Exist ");window.location = "/add_staff"</script>'
            q = db.insert("insert into login VALUES ('','" + email + "','" + str(passwd) + "','staff')")
            db.insert("insert into staff VALUES ('" + str(
                q) + "','" + staff_name + "','" + gender + "','" + place + "','" + email + "','" + str(
                staff_photo) + "','" + post + "','" + pin + "','" + qualification + "','" + dept + "','" + mobile_number + "')")
            import smtplib

            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            s.login("eedu07212@gmail.com", "cjwfhugnvxbcijow")
            msg = MIMEMultipart()  # create a message.........."
            msg['From'] = "eedu07212@gmail.com"
            msg['To'] = email
            msg['Subject'] = "Your Password for E-EDU Website"
            body = "Your Password is:- - " + str(passwd)
            msg.attach(MIMEText(body, 'plain'))
            s.send_message(msg)

            return '<script> alert("added sucessfully");window.location = "/admin_home"</script>'
        else:
            db = Db()
            a = db.select("select * from department")
            return render_template('admin/add staff.html', data=a)
    else:
        return redirect('/')


@app.route('/view_staff')
def view_staff():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select("select * from staff,department where staff.dept_id = department.dept_id")
        return render_template('admin/staff view.html', data=res)
    else:
        return redirect('/')


@app.route('/delete_staff/<aid>')
def delete_staff(aid):
    if session['lg'] == 'lin':
        db = Db()
        db.delete("delete from staff where staff_id ='" + aid + "'")
        db.delete("delete from login where login_id ='" + aid + "'")
        return redirect('/view_staff')
    else:
        return redirect('/')


@app.route('/edit_staff_view/<sid>', methods=['get', 'post'])
def edit_staff_view(sid):
    if session['lg'] == 'lin':
        if request.method == "POST":
            staff_name = request.form['textfield']
            gender = request.form['RadioGroup1']
            place = request.form['textfield4']
            dept = request.form['select']
            post = request.form['textfield2']
            pin = request.form['textfield3']
            qualification = request.form['textfield1']
            mobile_number = request.form['textfield5']
            email = request.form['textfield6']
            photo = request.files['fileField']

            d = datetime.datetime.now().strftime("%y%m%d%H%M%S")
            photo.save(path + d + '.jpg')
            staff_photo = "/static/staff_photos/" + d + '.jpg'

            db = Db()
            if request.files != None:
                if photo.filename != "":
                    db.update(
                        "update staff set staff_name ='" + staff_name + "',dept_id='" + dept + "',staff_mob='" + mobile_number + "',photo='" + str(
                            staff_photo) + "',staff_gender='" + gender + "',staff_post='" + post + "',staff_pin='" + pin + "',staff_qualification='" + qualification + "',dept_id='" + dept + "',staff_place='" + place + "'where staff_id='" + sid + "'")
                    return '<script> alert("updated sucessfully");window.location = "/view_staff"</script>'
                else:
                    db.update(
                        "update staff set staff_name ='" + staff_name + "',dept_id='" + dept + "',staff_mob='" + mobile_number + "',staff_gender='" + gender + "',staff_post='" + post + "',staff_pin='" + pin + "',staff_qualification='" + qualification + "',dept_id='" + dept + "',staff_place='" + place + "'where staff_id='" + sid + "'")
                    return '<script> alert("updated sucessfully");window.location = "/view_staff"</script>'
            else:
                db.update(
                    "update staff set staff_name ='" + staff_name + "',dept_id='" + dept + "',staff_mob='" + mobile_number + "',staff_gender='" + gender + "',staff_post='" + post + "',staff_pin='" + pin + "',staff_qualification='" + qualification + "',dept_id='" + dept + "',staff_place='" + place + "'where staff_id='" + sid + "'")
                return '<script> alert("updated sucessfully");window.location = "/view_staff"</script>'

        else:
            db = Db()
            res = db.selectOne("select * from staff where staff_id='" + sid + "'")
            res1 = db.select("select * from department")
            return render_template('admin/edit add staff.html', data=res, data1=res1)
    else:
        return redirect('/')


@app.route('/add_student', methods=['get', 'post'])
def add_student():
    if session['lg'] == 'lin':
        if request.method == "POST":
            student_name = request.form['textfield']
            course_id = request.form['cn']

            gender = request.form['RadioGroup1']
            student_mob_no = request.form['textfield4']
            email = request.form['textfield5']
            student_place = request.form['textfield1']
            student_post = request.form['textfield2']
            student_pin = request.form['textfield3']
            student_semester = request.form['select1']
            student_batch = request.form['textfield6']
            Reg_no = request.form['textfield7']
            photo = request.files['fileField']
            passwd = random.randint(0000, 9999)
            d = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            photo.save(path1 + d + '.jpg')
            pp = "/static/student_photos/" + d + '.jpg'
            db = Db()
            qry = db.selectOne("select * from login  where username='" + email + "'")
            if qry is not None:
                return '<script> alert("Email Already Exist ");window.location = "/add_student"</script>'
            q = db.insert("insert into login values('','" + email + "','" + str(passwd) + "','student')")
            db.insert("insert into student VALUES ('" + str(
                q) + "','" + student_name + "','" + gender + "','" + student_place + "','" + student_post + "','" + student_pin + "','" + course_id + "','" + email + "','" + student_semester + "','" + student_batch + "','" + student_mob_no + "','" + Reg_no + "','" + str(
                pp) + "')")
            import smtplib

            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            s.login("eedu07212@gmail.com", "cjwfhugnvxbcijow")
            msg = MIMEMultipart()  # create a message.........."
            msg['From'] = "eedu07212@gmail.com"
            msg['To'] = email
            msg['Subject'] = "Your Password for E-EDU Website"
            body = "Your Password is:- - " + str(passwd)
            msg.attach(MIMEText(body, 'plain'))
            s.send_message(msg)
            return '<script> alert("added sucessfully");window.location = "/admin_home"</script>'
        else:
            db = Db()
            a = db.select("select * from course")
            return render_template('admin/add student.html', data=a)
    else:
        return redirect('/')


@app.route('/update_student/<sid>', methods=['get', 'post'])
def update_student(sid):
    if session['lg'] == 'lin':
        if request.method == "POST":
            student_name = request.form['textfield']
            course_id = request.form['cn']

            gender = request.form['RadioGroup1']
            student_mob_no = request.form['textfield4']
            email = request.form['textfield5']
            student_place = request.form['textfield1']
            student_post = request.form['textfield2']
            student_pin = request.form['textfield3']
            student_semester = request.form['select1']
            student_batch = request.form['textfield6']
            Reg_no = request.form['textfield7']
            photo = request.files['fileField']
            passwd = random.randint(0000, 9999)
            d = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            photo.save(path1 + d + '.jpg')
            pp = "/static/student_photos/" + d + '.jpg'
            db = Db()
            if request.files != None:
                if photo.filename != "":
                    db.update(
                        "update student set stud_name = '" + student_name + "',stud_gender ='" + gender + "',stud_place ='" + student_place + "',stud_post='" + student_post + "',stud_pin='" + student_pin + "',stud_course_id='" + course_id + "',semester='" + student_semester + "',batch='" + student_batch + "',stud_mob='" + student_mob_no + "',photo='" + str(
                            pp) + "' where stud_id='" + sid + "'")
                    return '<script> alert("updated sucessfully");window.location = "/view_student#aaa"</script>'
                else:
                    db.update(
                        "update student set stud_name = '" + student_name + "',stud_gender ='" + gender + "',stud_place ='" + student_place + "',stud_post='" + student_post + "',stud_pin='" + student_pin + "',stud_course_id='" + course_id + "',stud_email='" + email + "',semester='" + student_semester + "',batch='" + student_batch + "',stud_mob='" + student_mob_no + "' where stud_id='" + sid + "'")
                    return '<script> alert("updated sucessfully");window.location = "/view_student#aaa"</script>'
            else:
                db.update(
                    "update student set stud_name = '" + student_name + "',stud_gender ='" + gender + "',stud_place ='" + student_place + "',stud_post='" + student_post + "',stud_pin='" + student_pin + "',stud_course_id='" + course_id + "',stud_email='" + email + "',semester='" + student_semester + "',batch='" + student_batch + "',stud_mob='" + student_mob_no + "' where stud_id='" + sid + "'")
            return '<script> alert("updated sucessfully");window.location = "/view_student#aaa"</script>'
        else:
            db = Db()
            res = db.selectOne("select * from student where stud_id='" + sid + "'")
            res1 = db.select("select * from course")
            return render_template('admin/update_student.html', data=res, data1=res1)
    else:
        return redirect('/')


@app.route('/view_student')
def view_student():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select("select * from student,course where student.stud_course_id=course.course_id")
        print(res)
        return render_template('admin/view student.html', data=res)
    else:
        return redirect('/')


@app.route('/delete_student/<aid>')
def delete_student(aid):
    if session['lg'] == 'lin':
        db = Db()
        db.delete("delete from student where stud_id ='" + aid + "'")
        return redirect('/view_student')
    else:
        return redirect('/')


@app.route('/add_course', methods=['get', 'post'])
def add_course():
    if session['lg'] == 'lin':
        if request.method == "POST":
            department_name = request.form['select']
            semester = request.form['select1']
            course_name = request.form['textfield']
            db = Db()
            qry = db.selectOne(
                "select * from course where dept_id = '" + department_name + "' and course_name = '" + course_name + "' and sem ='" + semester + "' ")
            if qry is not None:
                return '<script> alert("Already Exist ");window.location = "/add_course"</script>'
            db.insert(
                "insert into course VALUES ('','" + course_name + "','" + department_name + "','" + semester + "')")
            return '<script> alert("added sucessfully");window.location = "/admin_home"</script>'
        else:
            db = Db()
            a = db.select("select * from department")
            print(a)
            return render_template('admin/course add.html', data=a)
    else:
        return redirect('/')


@app.route('/view_course')
def view_course():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select("select * from course,department where course.dept_id=department.dept_id")
        return render_template('admin/course view.html', data=res)
    else:
        return redirect('/')


@app.route('/course_delete/<aid>')
def course_delete(aid):
    if session['lg'] == 'lin':
        db = Db()
        db.delete("delete from course WHERE course_id='" + aid + "'")
        return redirect('/view_course')
    else:
        return redirect('/')


@app.route('/add_subject', methods=['get', 'post'])
def add_subject():
    if session['lg'] == 'lin':
        if request.method == "POST":
            subject_name = request.form['textfield']
            syllabus = request.files['file']
            d = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            syllabus.save(path2 + d + '.pdf')
            syllabus = "/static/syllabus/" + d + '.pdf'
            db = Db()
            qry = db.selectOne("select * from subject  where sub_name = '" + subject_name + "'")
            if qry is not None:
                return '<script> alert("Already Exist ");window.location = "/add_subject"</script>'
            db.insert("insert into subject VALUES('','" + subject_name + "','" + str(syllabus) + "')")
            return '<script> alert("added sucessfully");window.location = "/admin_home"</script>'
        else:
            db = Db()
            a = db.select("select * from course")
            return render_template('admin/subject add.html', data=a)
    else:
        return redirect('/')


@app.route('/view_subject')
def view_subject():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select("select * from subject")
        return render_template('admin/subject view.html', data=res)
    else:
        return redirect('/')


@app.route('/delete_subject/<aid>')
def delete_subject(aid):
    db = Db()
    db.delete("delete from subject WHERE sub_id='" + aid + "'")
    return redirect('/view_subject')


@app.route('/complaint_view')
def complaint_view():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select("select * from complaint,student where complaint.student_id = student.stud_id")
        return render_template('admin/complaint view.html', data=res)
    else:
        return redirect('/')


@app.route('/complaint_reply/<cid>', methods=['get', 'post'])
def complaint_reply(cid):
    if session['lg'] == 'lin':
        if request.method == "POST":
            send_reply = request.form['textarea']
            db = Db()
            db.update(
                "update complaint set reply='" + send_reply + "',reply_date=curdate() where complaint_id='" + cid + "'")
            return '<script>alert("added sucessfully");window.location = "/admin_home"</script>'
        else:
            return render_template('admin/complaint reply.html')
    else:
        return redirect('/')


@app.route('/view_rating_and_review')
def view_rating_and_review():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select("select * from review,student where review.uid = student.stud_id")
        # res = db.select(qry)
        print(res)

        ar_rt = []

        for im in range(0, len(res)):
            val = str(res[im]['rating'])
            ar_rt.append(val)
        fs = "/static/star/full.jpg"
        hs = "/static/star/half.jpg"
        es = "/static/star/empty.jpg"
        arr = []

        for rt in ar_rt:
            print(rt)
            a = float(rt)

            if a >= 0.0 and a < 0.4:
                print("eeeee")
                ar = [es, es, es, es, es]
                arr.append(ar)

            elif a >= 0.4 and a < 0.8:
                print("heeee")
                ar = [hs, es, es, es, es]
                arr.append(ar)

            elif a >= 0.8 and a < 1.4:
                print("feeee")
                ar = [fs, es, es, es, es]
                arr.append(ar)

            elif a >= 1.4 and a < 1.8:
                print("fheee")
                ar = [fs, hs, es, es, es]
                arr.append(ar)

            elif a >= 1.8 and a < 2.4:
                print("ffeee")
                ar = [fs, fs, es, es, es]
                arr.append(ar)

            elif a >= 2.4 and a < 2.8:
                print("ffhee")
                ar = [fs, fs, hs, es, es]
                arr.append(ar)

            elif a >= 2.8 and a < 3.4:
                print("fffee")
                ar = [fs, fs, fs, es, es]
                arr.append(ar)

            elif a >= 3.4 and a < 3.8:
                print("fffhe")
                ar = [fs, fs, fs, hs, es]
                arr.append(ar)

            elif a >= 3.8 and a < 4.4:
                print("ffffe")
                ar = [fs, fs, fs, fs, es]
                arr.append(ar)

            elif a >= 4.4 and a < 4.8:
                print("ffffh")
                ar = [fs, fs, fs, fs, hs]
                arr.append(ar)

            elif a >= 4.8 and a <= 5.0:
                print("fffff")
                ar = [fs, fs, fs, fs, fs]
                arr.append(ar)
            print(arr)
        # return render_template('admin/adm_view_apprating.html',data=re33,r1=ar,ln=len(ar55))
        return render_template('admin/view ratings and review.html', resu=res, r1=arr, ln=len(arr))
    else:
        return redirect('/')


@app.route('/course_allocation', methods=['get', 'post'])
def course_allocation():
    if session['lg'] == 'lin':
        if request.method == "POST":
            subject_name = request.form['select']
            course_name = request.form['select2']
            semester = request.form['select3']
            db = Db()
            qry = db.selectOne(
                "select * from suballocatecourse  where course_id = '" + course_name + "' and sems = '" + semester + "' and subject_id = '" + subject_name + "'")
            if qry is not None:
                return '<script> alert("Already Exist ");window.location = "/course_allocation"</script>'

            db.insert(
                "insert into suballocatecourse VALUES ('','" + course_name + "','" + subject_name + "','" + semester + "')")
            return '<script> alert("added sucessfully");window.location = "/admin_home"</script>'
        else:
            db = Db()
            a = db.select("select *  from subject")
            b = db.select("select * from course")
            return render_template('admin/course allocation.html', data=a, data1=b)
    else:
        return redirect('/')


@app.route('/alloc_staff/<aid>/<did>', methods=['get', 'post'])
def alloc_staff(aid, did):
    if request.method == 'POST':
        s_alloc = request.form["staff"]
        db = Db()
        qry = db.selectOne("select * from  subject_alloc where suballoccourseid='" + aid + "' ")
        if qry is not None:
            return '''<script>alert("Already Allocated"); window.location ='/course_allocation_view'</script>'''

        db.insert("insert into subject_alloc VALUES ('','" + aid + "','" + s_alloc + "')")
        return '''<script>alert("added sucessfully"); window.location ='/course_allocation_view'</script>'''
    else:
        db = Db()
        res = db.select(
            "select * from staff,department where staff.dept_id =department.dept_id and staff.dept_id = '" + did + "'")
    return render_template('admin/staff_alloc.html', data=res)


@app.route('/course_allocation_view')
def course_allocation_view():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select("select * from suballocatecourse,course,`subject` where suballocatecourse.course_id = course.course_id and suballocatecourse.subject_id=subject.sub_id")
        return render_template('admin/course allocation view.html', data=res)
    else:
        return redirect('/')


@app.route('/delete_course_allocation/<aid>')
def delete_course_allocation(aid):
    if session['lg'] == 'lin':
        db = Db()
        db.delete("delete from suballocatecourse WHERE suballoc_courseid ='" + aid + "'")
        return redirect('/course_allocation_view')
    else:
        return redirect('/')


@app.route('/delete_staff_allocation/<aid>')
def delete_staff_allocation(aid):
    if session['lg'] == 'lin':

        db = Db()
        db.delete("delete from staff_allocation WHERE staff_allocation_id ='" + aid + "'")
        return redirect('/course_allocation_view')
    else:
        return redirect('/')


@app.route('/update_course_allocation/<aid>', methods=['get', 'post'])
def update_course_allocation(aid):
    if session['lg'] == 'lin':
        if request.method == "POST":
            subject_name = request.form['select']
            course_name = request.form['select2']
            semester = request.form['select3']
            db = Db()
            db.update(
                "update suballocatecourse set course_id='" + course_name + "',subject_id='" + subject_name + "',sems='" + semester + "' where suballoc_courseid='" + aid + "'")
            return '<script> alert("updated sucessfully");window.location = "/course_allocation_view"</script>'
        else:
            db = Db()
            res = db.selectOne("select * from suballocatecourse where suballoc_courseid='" + aid + "'")
            a = db.select("select *  from subject")
            c = db.select("select * from course")

            return render_template('admin/update_course allocation.html', data=a, data2=res, data3=c)
    else:
        return redirect('/')


@app.route('/view_alloc_staff/<scid>/<did>', methods=['get', 'post'])
def view_alloc_staff(scid, did):
    if session['lg'] == 'lin':
        if request.method == "POST":
            staff = request.form['select2']
            db = Db()
            db.insert("insert into subject_alloc VALUES ('','" + scid + "','" + staff + "')")
            return '<script> alert("allocated sucessfully");window.location = "/course_allocation_view"</script>'

        else:
            db = Db()
            res = db.select("select * from staff where dept_id='" + did + "'")
            return render_template('admin/view allocate staff.html', data1=res)
    else:
        return redirect('/')


# =================================================================================================================
#                                             STAFF MODULE
# =================================================================================================================
@app.route('/staff_home')
def staff_home():
    if session['lg'] == 'lin':
        return render_template('staff/staff_index.html')
    else:
        return redirect('/')


@app.route('/staff_profile')
def staff_view():
    if session['lg'] == 'lin':

        db = Db()
        res = db.selectOne(
            "select * from department,staff WHERE department.dept_id = staff.dept_id and staff.staff_id ='" + str(
                session['lid']) + "'")
        # res1 = db.selectOne("select dept_name from department,staff WHERE department.dept_id = staff.dept_id")
        return render_template('staff/staff_profile.html', data=res)
    else:
        redirect('/')


@app.route('/upload_notes/<aid>', methods=['get', 'post'])
def upload_notes(aid):
    if session['lg'] == 'lin':
        if request.method == 'POST':
            # subject = request.form['select']
            details = request.form['textarea']
            notes = request.files['fileField']
            db = Db()
            d = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            notes.save(path3 + d + '.pdf')
            pp = "/static/notes/" + d + '.pdf'
            db.insert("insert into studymaterials values ('','" + aid + "','" + details + "','" + str(pp) + "')")
            return '<script> alert("added sucessfully");window.location = "/staff_home"</script>'
        else:
            db = Db()
            r = db.select("select * from subject")
            return render_template('staff/upload_notes.html', data=r)
    else:
        return redirect('/')


@app.route('/notes_view/<aid>')
def notes_view(aid):
    if session['lg'] == 'lin':
        db = Db()
        session['aid'] = aid
        res = db.select("select * from studymaterials where subject_id ='" + aid + "'")
        return render_template('staff/notes_view.html', data=res)
    else:
        return redirect('/')


@app.route('/notes_delete/<aid>')
def notes_delete(aid):
    if session['lg'] == 'lin':
        db = Db()
        db.delete("delete  from studymaterials where mid = '" + aid + "' ")
        return '''<script>alert("delete");window.location='/allocated_subjects'</script>'''
    else:
        return redirect('/')


@app.route('/upload_previous_question_paper/<aid>', methods=['get', 'post'])
def upload_previous_question_paper(aid):
    if session['lg'] == 'lin':
        if request.method == 'POST':
            qp = request.files['fileField']
            year = request.form['year']
            db = Db()
            d = datetime.datetime.now().strftime("%y%m%d%H%M%S")
            qp.save(path4 + d + '.pdf')
            pp = "/static/qp/" + d + '.pdf'
            db.insert("insert into previous_qp values ('','" + aid + "','" + str(pp) + "','" + year + "')")
            return '<script> alert("added sucessfully");window.location = "/staff_home"</script>'
        else:

            return render_template('staff/upload_previous_question_paper.html')
    else:
        return redirect('/')


@app.route('/previous_question_paper_view/<aid>')
def previous_question_paper_view(aid):
    if session['lg'] == 'lin':
        db = Db()
        res = db.select("select * from previous_qp where subid ='" + aid + "'")
        return render_template('staff/previous_question_paper_view.html', data=res)
    else:
        return redirect('/')


@app.route('/previous_question_paper_delete/<aid>')
def previous_question_paper_delete(aid):
    if session['lg'] == 'lin':
        db = Db()
        db.delete("delete  from previous_qp where pid = '" + aid + "' ")
        return '''<script>alert("deleted");window.location='/allocated_subjects';</script>'''
    else:
        return redirect('/')


@app.route('/allocated_subjects')
def allocated_subject():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select(
            "select * from subject_alloc,suballocatecourse,subject where suballocatecourse.suballoc_courseid = subject_alloc.suballoccourseid and suballocatecourse.subject_id = subject.sub_id and subject_alloc.staff_id ='" + str(
                session['lid']) + "'")
        # print("select * from subject_alloc,suballocatecourse,subject where suballocatecourse.course_id = subject_alloc.suballoccourseid and suballocatecourse.subject_id = subject.sub_id and subject_alloc.staff_id ='"+str(session['lid'])+"'")
        return render_template('staff/allocated_subjects.html', data=res)
    else:
        return redirect('/')


@app.route('/sclass/<i>')
def sclass(i):
    if session['lg'] == "lin":
        db = Db()
        res = db.select("select * from class where class.subject_alloc_id='" + i + "'")
        d = datetime.datetime.now().strftime("%Y-%m-%d")
        return render_template('student/classview.html', data=res, d=d)
    return redirect('/')


@app.route('/attendence/<cid>/<sem>/<c>', methods=['get', 'post'])
def attendence(cid, sem, c):
    if request.method == 'POST':
        sid = request.form.getlist('check')
        sid2 = request.form.getlist(('sid'))
        db = Db()
        print(sid2)
        print(sid)
        qry = db.select("select * from attendence where attendence_date=curdate() and class_id='" + cid + "'")
        print(qry)
        if len(qry) > 0:
            return '''<script> alert('Already attendence marked'); window.location="/class_schedule_view#aaa"</script>'''
        else:
            for i in sid2:
                if i in sid:

                    db.insert(
                        "insert into attendence VALUES ('','" + str(i) + "','present',curdate(),'" + str(cid) + "')")
                    # return '''<script> alert('added sucessfully'); window.location="/allocated_subjects"</script>'''
                else:

                    db.insert(
                        "insert into attendence VALUES ('','" + str(i) + "','absent',curdate(),'" + str(cid) + "')")
            return '''<script> alert('added sucessfully'); window.location="/class_schedule_view#aaa"</script>'''




    else:
        db = Db()
        # res = db.select("select * from student  where semester ='" + str(session['sem']) + "' and stud_course_id= '" + str(session['cid']) + "'")
        res = db.select(
            "select * from student  where semester ='" + str(sem) + "' and stud_course_id= '" + str(c) + "'")

    return render_template('staff/attendence.html', data=res)


@app.route('/attendence_view', methods=['get', 'post'])
def attendence_view():
    if request.method == "POST":
        d = request.form['d']
        db = Db()
        res = db.select(
            "select * from attendence,student,class,subject_alloc,suballocatecourse,subject where attendence.student_id=student.stud_id and attendence.class_id=class.cid and class.subject_alloc_id=subject_alloc.suballoc_courseid and subject_alloc.suballoccourseid=suballocatecourse.suballoc_courseid and suballocatecourse.subject_id=subject.sub_id and subject_alloc.staff_id='" + str(
                session['lid']) + "' and attendence.attendence_date='" + d + "'")

        return render_template('staff/attendence_view.html', data=res)

    else:
        db = Db()
        # res = db.select("select * from student,attendence  where semester ='" + str(session['sem']) + "' and stud_course_id= '" + str(session['course_id']) + "' and attendence.student_id = student.stud_id ")
        res = db.select(
            "select * from attendence,student,class,subject_alloc,suballocatecourse,subject where attendence.student_id=student.stud_id and attendence.class_id=class.cid and class.subject_alloc_id=subject_alloc.suballoc_courseid and subject_alloc.suballoccourseid=suballocatecourse.suballoc_courseid and suballocatecourse.subject_id=subject.sub_id and subject_alloc.staff_id='" + str(
                session['lid']) + "'")

        return render_template('staff/attendence_view.html', data=res)


@app.route('/class_schedule', methods=['get', 'post'])
def class_schedule():
    if session['lg'] == 'lin':
        if request.method == 'POST':
            subject = request.form['select']
            time = request.form['time']
            date = request.form['date']
            db = Db()

            db.insert("insert into class VALUES ('','" + subject + "','" + time + "','" + date + "')")
            return '<script> alert("added sucessfully");window.location = "/staff_home"</script>'
        else:
            db = Db()
            res = db.select(
                "select sub_name,subject_alloc.suballoc_courseid from subject,suballocatecourse,subject_alloc where subject.sub_id=suballocatecourse.subject_id and suballocatecourse.suballoc_courseid=subject_alloc.suballoccourseid and staff_id='" + str(
                    session['lid']) + "'")
            print(res)
            return render_template('staff/class_schedule.html', data=res)
    else:
        return redirect('/')


@app.route('/class_schedule_view')
def class_schedule_view():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select(
            "select * from subject,suballocatecourse,class,subject_alloc where subject.sub_id = suballocatecourse.subject_id and class.subject_alloc_id = subject_alloc.suballoc_courseid and subject_alloc.staff_id='" + str(
                session['lid']) + "' and suballocatecourse.suballoc_courseid=subject_alloc.suballoccourseid")

        return render_template('staff/class_schedule_view.html', data=res)
    else:
        return redirect('/')


@app.route('/class_schedule_delete/<aid>')
def class_schedule_delete(aid):
    if session['lg'] == 'lin':
        db = Db()

        db.delete("delete from class where cid='" + aid + "'")
        return '''<script>alert("deleted"); window.location='/class_schedule_view'</script>'''
    else:
        return redirect('/')


@app.route('/class_schedule_edit/<aid>', methods=['get', 'post'])
def class_schedule_edit(aid):
    if session['lg'] == 'lin':
        if request.method == 'POST':
            subject = request.form['select']
            time = request.form['time']
            date = request.form['date']
            db = Db()

            db.update(
                "update class  set subject_alloc_id ='" + subject + "',time='" + time + "',date='" + date + "' where cid='" + aid + "'")
            print(
                "update class  set subject_alloc_id ='" + subject + "',time='" + time + "',date='" + date + "' where cid='" + aid + "'")
            return '<script> alert("updated sucessfully");window.location = "/staff_home"</script>'
        else:

            db = Db()
            res = db.select(
                "select * from subject,suballocatecourse,subject_alloc where subject.sub_id=suballocatecourse.subject_id and suballocatecourse.suballoc_courseid=subject_alloc.suballoccourseid and staff_id='" + str(
                    session['lid']) + "'")
            print(res, "eeeeeeeeeeeee")
            res1 = db.selectOne(
                "select * from class, subject_alloc where class.subject_alloc_id = subject_alloc.suballoc_courseid and class.cid ='" + aid + "'")

            return render_template('staff/class_schedule_edit.html', data=res1, data1=res)
    else:
        return redirect('/')


@app.route('/staff_view_rating_and_review')
def staff_view_rating_and_review():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select("select * from review,student where review.uid = student.stud_id")
        ar_rt = []

        for im in range(0, len(res)):
            val = str(res[im]['rating'])
            ar_rt.append(val)
        fs = "/static/star/full.jpg"
        hs = "/static/star/half.jpg"
        es = "/static/star/empty.jpg"
        arr = []

        for rt in ar_rt:
            print(rt)
            a = float(rt)

            if a >= 0.0 and a < 0.4:
                print("eeeee")
                ar = [es, es, es, es, es]
                arr.append(ar)

            elif a >= 0.4 and a < 0.8:
                print("heeee")
                ar = [hs, es, es, es, es]
                arr.append(ar)

            elif a >= 0.8 and a < 1.4:
                print("feeee")
                ar = [fs, es, es, es, es]
                arr.append(ar)

            elif a >= 1.4 and a < 1.8:
                print("fheee")
                ar = [fs, hs, es, es, es]
                arr.append(ar)

            elif a >= 1.8 and a < 2.4:
                print("ffeee")
                ar = [fs, fs, es, es, es]
                arr.append(ar)

            elif a >= 2.4 and a < 2.8:
                print("ffhee")
                ar = [fs, fs, hs, es, es]
                arr.append(ar)

            elif a >= 2.8 and a < 3.4:
                print("fffee")
                ar = [fs, fs, fs, es, es]
                arr.append(ar)

            elif a >= 3.4 and a < 3.8:
                print("fffhe")
                ar = [fs, fs, fs, hs, es]
                arr.append(ar)

            elif a >= 3.8 and a < 4.4:
                print("ffffe")
                ar = [fs, fs, fs, fs, es]
                arr.append(ar)

            elif a >= 4.4 and a < 4.8:
                print("ffffh")
                ar = [fs, fs, fs, fs, hs]
                arr.append(ar)

            elif a >= 4.8 and a <= 5.0:
                print("fffff")
                ar = [fs, fs, fs, fs, fs]
                arr.append(ar)
            print(arr)
        # return render_template('admin/adm_view_apprating.html',data=re33,r1=ar,ln=len(ar55))
        return render_template('staff/view ratings and review.html', resu=res, r1=arr, ln=len(arr))
    else:
        return redirect('/')


@app.route('/staff_view_suggestion')
def staff_view_suggestion():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select("select * from suggestions,student where suggestions.u_id = student.stud_id")
        return render_template('staff/view suggestions.html', data=res)
    else:
        return redirect('/')


@app.route('/view_students/<cid>/<sem>', methods=['get', 'post'])
def view_students(cid, sem):
    db = Db()
    session['cid'] = cid
    session['s'] = sem

    return render_template('staff/viewstudent.html')


@app.route('/mayor_mayor_councillor_chat', methods=['post'])
def mayor_mayor_councillor_chat():
    a = session['lid']
    db = Db()
    res = db.select("select * from student  where semester ='" + str(session['s']) + "' and stud_course_id= '" + str(
        session['cid']) + "'")
    # print("select * from student  where semester ='" + str(session['s']) + "' and stud_course_id= '" + str(session['cid']) + "'")
    v = {}
    if len(res) > 0:
        v["status"] = "ok"
        v['data'] = res
    else:
        v["status"] = "error"

    rw = demjson.encode(v)
    print(rw)
    return rw


@app.route('/chatsnd', methods=['post'])
def chatsnd():
    # if session['lg'] == "lin":
    c = session['lid']
    b = request.form['n']
    print(b, )
    m = request.form['m']
    print(m, "hhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    db = Db()
    q2 = "insert into disscussion(from_id,to_id,message,date) values('" + str(c) + "','" + str(
        b) + "','" + m + "',curdate())"
    res = db.insert(q2)
    v = {}
    if int(res) > 0:
        v["status"] = "ok"

    else:
        v["status"] = "error"

    r = demjson.encode(v)

    return r


# else:
#     return render_template("login.html")
@app.route('/chatrply', methods=['post'])
def chatrply():
    # if session['lg'] == "lin":
    print("...........................")
    c = session['lid']
    b = request.form['n']
    print("<<<<<<<<<<<<<<<<<<<<<<<<")
    print(b)
    t = Db()
    qry2 = "select * from disscussion ORDER BY chat_id ASC ";
    res = t.select(qry2)
    print(res)

    v = {}
    if len(res) > 0:
        v["status"] = "ok"
        v['data'] = res
        v['id'] = c
    else:
        v["status"] = "error"
    rw = demjson.encode(v)
    return rw


# else:
#     return render_template("login.html")

@app.route('/v_call/<cid>')
def v_call(cid):
    db = Db()
    # res = db.select("select * from student,suballocatecourse WHERE suballocatecourse.course_id = student.stud_course_id and student.stud_course_id = '"+str(session['cid'])+"' ")
    return render_template('staff/index.html')


# ====================exam==================================


@app.route('/Exam_schedule', methods=['get', 'post'])
def Exam_schedule():
    if session['lg'] == "lin":
        if request.method == "POST":
            subject = request.form['textfield']
            date = request.form['textfield2']
            time = request.form['textfield3']
            m = request.form['textfield4']
            db = Db()
            q = db.selectOne(
                "select * from exam where subject_alloc_id='" + subject + "' and date='" + date + "' and time='" + time + "' and marks='" + m + "'")
            if q is None:
                db.insert("insert into exam VALUES ('','" + date + "','" + time + "','" + subject + "','" + m + "')")
                return '''<script>alert('scheduled');window.location="/Exam_schedule"</script>'''
            else:
                return '''<script>alert('Already scheduled');window.location="/Exam_schedule"</script>'''
        else:
            db = Db()
            q = db.select(
                "select * from subject,suballocatecourse,subject_alloc,course where course.course_id=suballocatecourse.course_id and suballocatecourse.subject_id=subject.sub_id and subject_alloc.staff_id='" + str(
                    session['lid']) + "' and subject_alloc.suballoccourseid=suballocatecourse.suballoc_courseid")
            d = db.selectOne("select date_add(curdate(),interval 1 day) as d")
            return render_template('staff/Exam_add.html', data=q, data2=d['d'])
    return redirect('/')


@app.route('/viewexamschedule', methods=['get', 'post'])
def viewexamschedule():
    db = Db()
    if session['lg'] == "lin":
        if request.method == 'POST':
            res = db.select(
                "select * from subject,suballocatecourse,subject_alloc,course,exam where course.course_id=suballocatecourse.course_id and suballocatecourse.subject_id=subject.sub_id and subject_alloc.staff_id='" + str(
                    session[
                        'lid']) + "' and subject_alloc.suballoccourseid=suballocatecourse.suballoc_courseid and exam.subject_alloc_id=subject_alloc.suballoc_courseid and exam.date='" +
                request.form['d'] + "'")
            d = datetime.datetime.now().strftime("%Y-%m-%d")
            return render_template('staff/Exam_view.html', data=res, d=d)
        res = db.select(
            "select * from subject,suballocatecourse,subject_alloc,course,exam where course.course_id=suballocatecourse.course_id and suballocatecourse.subject_id=subject.sub_id and subject_alloc.staff_id='" + str(
                session[
                    'lid']) + "' and subject_alloc.suballoccourseid=suballocatecourse.suballoc_courseid and exam.subject_alloc_id=subject_alloc.suballoc_courseid")
        d = datetime.datetime.now().strftime("%Y-%m-%d")
        print(str(d))
        dd = str(d)
        return render_template('staff/Exam_view.html', data=res, d=d)
    return redirect('/')


@app.route('/scheduledelete/<i>')
def scheduletdelete(i):
    db = Db()
    if session['lg'] == "lin":
        db.delete("delete from exam where exam_id='" + i + "'")
        return '''<script>alert('deleted successfully');window.location="/viewexamschedule#aaa"</script>'''
    return redirect('/')


# =================questions=================


@app.route('/add_QandA/<eid>/<m>', methods=['get', 'post'])
def add_QandA(eid, m):
    if session['lg'] == "lin":
        if request.method == "POST":
            db = Db()
            q = db.selectOne("select sum(marks) as s from question where exam_id='" + eid + "'")
            mrk = q['s']
            # mrk=int(mark)
            if mrk is None:
                mrk = 0
            total = int(m) - int(mrk)

            question = request.form['textarea']
            t = request.form['s']
            correct = request.form['textfield5']
            marks = request.form['textfield6']
            print(mrk, "jjjjjjjjjjjjjjjjjjjjjjjjjjj")
            print(total, "total")
            print(m, "total mark")
            if int(mrk) == int(m):
                return '''<script>alert('Limit exceeding!!!!');window.location="/add_QandA/''' + eid + '''/''' + m + '''"</script>'''
            else:
                if total > 0:
                    if mrk == 0:
                        qq = db.selectOne(
                            "select * from question where question='" + question + "' and exam_id='" + eid + "' and exam_type='" + t + "'")
                        if qq is None:
                            if t == 'MCQ':
                                option1 = request.form['textfield']

                                option2 = request.form['textfield2']
                                option3 = request.form['textfield3']
                                option4 = request.form['textfield4']

                                db = Db()
                                db.insert(
                                    "insert into question VALUE('','" + eid + "','" + question + "','" + option1 + "','" + option2 + "','" + option3 + "','" + option4 + "','" + correct + "', '" + marks + "','" + t + "')")
                                return '''<script>alert('Added');window.location="/add_QandA/''' + eid + '''/''' + m + '''"</script>'''
                            else:
                                db = Db()
                                db.insert(
                                    "insert into question VALUE('','" + eid + "','" + question + "','','','','','" + correct + "', '" + marks + "','" + t + "')")
                                return '''<script>alert('Added');window.location="/add_QandA/''' + eid + '''/''' + m + '''"</script>'''
                        else:
                            return '''<script>alert('Already added');window.location="/add_QandA/''' + eid + '''/''' + m + '''"</script>'''

                    elif int(marks) <= int(m):
                        if int(total) >= int(marks):
                            qq = db.selectOne(
                                "select * from question where question='" + question + "' and exam_id='" + eid + "' and exam_type='" + t + "'")
                            if qq is None:
                                if t == 'MCQ':
                                    option1 = request.form['textfield']

                                    option2 = request.form['textfield2']
                                    option3 = request.form['textfield3']
                                    option4 = request.form['textfield4']

                                    db = Db()
                                    db.insert(
                                        "insert into question VALUE('','" + eid + "','" + question + "','" + option1 + "','" + option2 + "','" + option3 + "','" + option4 + "','" + correct + "', '" + marks + "','" + t + "')")
                                    return '''<script>alert('Added');window.location="/add_QandA/''' + eid + '''/''' + m + '''"</script>'''
                                else:
                                    db = Db()
                                    db.insert(
                                        "insert into question VALUE('','" + eid + "','" + question + "','','','','','" + correct + "', '" + marks + "','" + t + "')")
                                    return '''<script>alert('Added');window.location="/add_QandA/''' + eid + '''/''' + m + '''"</script>'''
                            else:
                                return '''<script>alert('Already added');window.location="/add_QandA/''' + eid + '''/''' + m + '''"</script>'''
                        else:
                            return '''<script>alert('Limit exceeding!!!!');window.location="/add_QandA/''' + eid + '''/''' + m + '''"</script>'''

                    else:
                        return '''<script>alert('Invalid mark');window.location="/add_QandA/''' + eid + '''/''' + m + '''"</script>'''

                else:
                    return '''<script>alert('Limit exceeding!!!!');window.location="/add_QandA/''' + eid + '''/''' + m + '''"</script>'''


        else:
            db = Db()
            q = db.selectOne("select sum(marks) as s from question where exam_id='" + eid + "'")
            if q['s'] is None:

                return render_template('Staff/Question_add.html', d="No question added")
            else:
                return render_template('Staff/Question_add.html', d=q['s'])
    return redirect('/')


@app.route('/view_question/<ij>')
def view_question(ij):
    if session['lg'] == "lin":
        db = Db()
        res = db.select("select * from question where exam_id='" + ij + "'")
        m = []
        e = []
        for i in res:
            if i['exam_type'] == 'MCQ':
                m.append(i)
            else:
                e.append(i)
        session['qid'] = ij
        return render_template('Staff/Question_view.html', data=m, data1=e)
    return redirect('/')


@app.route('/quedelete/<i>')
def quedelete(i):
    db = Db()
    if session['lg'] == "lin":
        db.delete("delete from question where qid='" + i + "'")
        return '''<script>alert('deleted successfully');window.location="/view_question/''' + str(
            session['qid']) + '''"</script>'''
    return redirect('/')


@app.route('/op/<i>')
def op(i):
    if session['lg'] == "lin":
        if i == 'MCQ':
            return render_template('Staff/options.html', data="1")
        else:
            return render_template("Staff/options.html")
    return redirect('/')


# ============================result=====================

@app.route('/viewres/<eid>/<cid>', methods=['get', 'post'])
def viewres(eid, cid):
    db = Db()
    if session['lg'] == "lin":
        # q=db.select("select * from subject_alloc left join suballocatecourse on subject_alloc.suballoccourseid=suballocatecourse.suballoc_courseid and subject_alloc.staff_id='"+str(session['lid'])+"' left join student on suballocatecourse.course_id=student.stud_course_id left join result on student.stud_id=result.studid and result.examid='"+str(eid)+"'")
        q = db.select(
            "select * from student left join result on student.stud_id=result.studid and result.examid='" + str(
                eid) + "' where student.stud_course_id='" + str(cid) + "' ")
        return render_template('staff/viewres.html', data=q)
    return redirect('/')


# =================================================================================================================
#                                 STUDENT MODULE
# ===============================================================================================================
@app.route('/student_home')
def student_home():
    if session['lg'] == "lin":

        return render_template('student/student_index.html')
    else:
        return redirect('/')


@app.route('/student_profile')
def student_profile():
    if session['lg'] == "lin":
        db = Db()
        res = db.selectOne(
            "select * from student,course where student.stud_course_id =course.course_id and stud_id ='" + str(
                session['lid']) + "'")
        return render_template('student/student_profile.html', data=res)
    else:
        return redirect('/')


@app.route('/subjects_view')
def subjects_view():
    if session['lg'] == "lin":
        db = Db()
        res = db.select(
            "select course.course_name,subject.sub_name,suballocatecourse.suballoc_courseid,subject_alloc.suballoc_courseid,subject_alloc.suballoccourseid as s  from suballocatecourse join course on suballocatecourse.course_id=course.course_id join `subject` on suballocatecourse.subject_id=subject.sub_id  join subject_alloc on subject_alloc.suballoccourseid=suballocatecourse.suballoc_courseid where  suballocatecourse.course_id= '" + str(
                session['course_id']) + "' ")
        # print("select course.course_name,subject.sub_name,suballoc_courseid from suballocatecourse join course on suballocatecourse.course_id=course.course_id join `subject` on suballocatecourse.subject_id=subject.sub_id and suballocatecourse.course_id= '"+str(session['course_id'])+"' ")
        return render_template('student/subjects_view.html', data=res)
    else:
        return redirect('/')


@app.route('/notes_download', methods=['get', 'post'])
def notes_download():
    if session['lg'] == "lin":
        if request.method == "POST":
            sub = request.form['subjects']
            db = Db()
            res = db.select("select * from subject")
            res1 = db.select(
                "select * from studymaterials,subject where studymaterials.subject_id = subject.sub_id and subject.sub_id='" + sub + "' ")
            print(res, "yyyyyyyyyyyyyyyy")
            return render_template('student/notes_download.html', data1=res1, data=res)
        else:

            db = Db()
            res = db.select("select * from subject")
        return render_template('student/notes_download.html', data=res)
    else:
        return redirect('/')


@app.route('/question_paper_download', methods=['get', 'post'])
def question_paper_download():
    if session['lg'] == "lin":
        if request.method == "POST":
            sub = request.form['qp']
            db = Db()
            res = db.select("select * from subject")
            res1 = db.select(
                "select * from previous_qp,subject where previous_qp.subid = subject.sub_id and subject.sub_id = '" + sub + "' ")
            return render_template('student/question_paper_download.html', data1=res1, data=res)
        else:

            db = Db()
            res = db.select("select * from subject")
        return render_template('student/question_paper_download.html', data=res)
    else:
        return redirect('/')


@app.route('/send_complaints', methods=['get', 'post'])
def send_complaints():
    if session['lg'] == "lin":
        if request.method == "POST":
            complaint = request.form['textarea']
            db = Db()
            db.insert("insert into complaint VALUES ('','" + str(
                session['lid']) + "','" + complaint + "',curdate(),'pending','pending')")
            return '<script> alert("added sucessfully");window.location = "/student_home"</script>'

        return render_template('student/send_complaints.html')
    else:
        return redirect('/')


@app.route("/student_complaint_view")
def student_complaint_view():
    if session['lg'] == "lin":

        db = Db()
        res = db.select("select * from complaint")
        return render_template('student/complaint_view.html', data=res)
    else:
        return redirect('/')


@app.route('/send_ratings_and_review', methods=['get', 'post'])
def send_ratings_and_review():
    if session['lg'] == "lin":
        if request.method == "POST":
            rt = request.form['star']
            review = request.form['review']

            db = Db()
            db.insert(
                "insert into review VALUES ('','" + str(session['lid']) + "','" + rt + "','" + review + "',curdate())")
            return '<script> alert("added sucessfully");window.location = "/student_home"</script>'
        return render_template('student/rate.html')
    else:
        return redirect('/')


@app.route('/suggestion', methods=['get', 'post'])
def suggestion():
    if session['lg'] == "lin":
        if request.method == "POST":
            suggestion = request.form['textarea']
            db = Db()
            db.insert(
                "insert into suggestions VALUES ('','" + str(session['lid']) + "','" + suggestion + "',curdate())")
            return '<script> alert("added sucessfully");window.location = "/student_home"</script>'
        return render_template('student/suggestion.html')
    else:
        return redirect('/')


@app.route('/staffview')
def staffview():
    if session['lg'] == "lin":
        return render_template('student/staffview.html')
    else:
        return redirect('/')


@app.route('/mayor_mayor_councillor_chat1', methods=['post'])
def mayor_mayor_councillor_chat1():
    if session['lg'] == "lin":
        a = session['lid']
        db = Db()
        res = db.select(
            "select * from suballocatecourse,subject_alloc,staff where suballocatecourse.suballoc_courseid=subject_alloc.suballoccourseid and subject_alloc.staff_id = staff.staff_id and suballocatecourse.course_id = '" + str(
                session['course_id']) + "' and suballocatecourse.sems = '" + str(session['sem']) + "'")
        v = {}
        if len(res) > 0:
            v["status"] = "ok"
            v['data'] = res
        else:
            v["status"] = "error"

        rw = demjson.encode(v)
        print(rw)
        return rw
    else:
        return redirect('/')


@app.route('/chatsnd1', methods=['post'])
def chatsnd1():
    if session['lg'] == "lin":
        # if session['lg'] == "lin":
        c = session['lid']
        b = request.form['n']
        print(b, )
        m = request.form['m']
        print(m, "hhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        db = Db()
        q2 = "insert into disscussion(from_id,to_id,message,date) values('" + str(c) + "','" + str(
            b) + "','" + m + "',curdate())"
        res = db.insert(q2)
        v = {}
        if int(res) > 0:
            v["status"] = "ok"

        else:
            v["status"] = "error"

        r = demjson.encode(v)

        return r
    else:
        return redirect('/')
    # else:
    #     return render_template("login.html")


@app.route('/chatrply1', methods=['post'])
def chatrply1():
    # if session['lg'] == "lin":
    print("...........................")
    c = session['lid']
    b = request.form['n']
    print("<<<<<<<<<<<<<<<<<<<<<<<<")
    print(b)
    t = Db()
    qry2 = "select * from disscussion ORDER BY chat_id ASC ";
    res = t.select(qry2)
    print(res)

    v = {}
    if len(res) > 0:
        v["status"] = "ok"
        v['data'] = res
        v['id'] = c
    else:
        v["status"] = "error"
    rw = demjson.encode(v)
    return rw


# else:
#     return render_template("login.html")

@app.route('/v_call_s')
def v_call_S():
    return render_template('student/index.html')


@app.route('/staffsview/<aid>')
def staffsview(aid):
    db = Db()
    res = db.selectOne(
        "select * from subject_alloc,staff where  subject_alloc.staff_id = staff.staff_id and subject_alloc.suballoccourseid='" + aid + "'")
    return render_template('student/staffsview.html', data=res)


# ==========================Attend exam===================

@app.route('/view_exmnotification')
def view_exmnotification():
    if session['lg'] == "lin":
        db = Db()
        res = db.select("select * from subject,suballocatecourse,subject_alloc,course,staff,exam where exam.subject_alloc_id=subject_alloc.suballoc_courseid and staff.Staff_id=subject_alloc.staff_id  and course.course_id=suballocatecourse.course_id and suballocatecourse.subject_id=subject.sub_id and subject_alloc.suballoccourseid=suballocatecourse.suballoc_courseid and suballocatecourse.course_id= '" + str(
                session['course_id']) + "' and sems='" + str(session['sem']) + "'")
        d = datetime.datetime.now().strftime("%Y-%m-%d")
        q = []
        for i in res:
            qq = db.selectOne("select * from result where examid='" + str(i['exam_id']) + "' and studid='" + str(
                session['lid']) + "'")
            if qq is None:
                q.append({'sub_name': i['sub_name'], 'date': i['date'], 'time': i['time'], 'eid': i['exam_id'],
                          'status': 'pending', 'marks': i['marks']})
            else:
                q.append({'sub_name': i['sub_name'], 'date': i['date'], 'time': i['time'], 'eid': i['exam_id'],
                          'status': 'attended', 'marks': i['marks']})
        return render_template('student/viewexamnotification.html', data=q, d=d)
    return redirect('/')


@app.route('/attend_exam/<i>', methods=['get', 'post'])
def attend_exam(i):
    db = Db()
    if session['lg'] == "lin":
        res = db.select("select * from question where exam_id='" + i + "'")
        if request.method == "POST":
            answer = request.form['radio']
            row = res[session['cnt']]
            correctanswer = row['correct']
            examtype = row['exam_type']
            if examtype == "MCQ":
                if answer == correctanswer:
                    session['mark'] = session['mark'] + int(row['marks'])
                session['cnt'] = session['cnt'] + 1
            elif examtype == "Briefly explain":
                import spacy
                nlp = spacy.load("en_core_web_lg")
                doc1 = nlp(correctanswer)
                doc2 = nlp(answer)
                similar = doc1.similarity(doc2)
                print("Sim  ", similar)
                mark_Secured = int(row['marks']) * round(similar, 2)
                session['mark'] = session['mark'] + mark_Secured
                session['cnt'] = session['cnt'] + 1
            if session['cnt'] < len(res):
                return render_template('student/attendexam.html', data=res[session['cnt']])
            else:
                score = session['mark']
                examid = i
                studid = session['lid']
                db = Db()
                res = db.selectOne(
                    "select * from result where studid='" + str(studid) + "' and examid='" + examid + "'")
                if res is None:
                    db = Db()
                    db.insert("insert into result values(null, '" + examid + "', '" + str(studid) + "', '" + str(
                        score) + "')")
                else:
                    db = Db()
                    db.update(
                        "UPDATE  result set mark='" + str(score) + "' where examid='" + examid + "' and studid='" + str(
                            studid) + "'")
                return '''<script>alert('exam finished');window.location="/student_home"</script>'''
        session['cnt'] = 0
        session['mark'] = 0
        return render_template('student/attendexam.html', data=res[session['cnt']])
    else:
        return redirect('/')


# =====================result===============


@app.route('/view_result/<eid>/<m>')
def view_result(eid, m):
    db = Db()
    if session['lg'] == "lin":
        res = db.selectOne(
            "select result.mark from result where studid='" + str(session['lid']) + "' and examid ='" + str(eid) + "' ")
        return render_template('student/viewresult.html', data=res, m=m)
    return redirect('/')


# ===========================================================================
#    Company Module
#============================================================================
@app.route('/company_home')
def company_home():
    if session['lg']=='lin':
        return render_template('company/company_index.html')
    else:
        return redirect('/')


@app.route('/company_registration', methods=['GET', 'POST'])
def company_registration():
    if request.method == "POST":
        name = request.form['textfield1']
        password = request.form['password']
        company_type = request.form['textfield2']
        company_location = request.form['textfield3']
        email_id = request.form['textfield4']
        hr_name = request.form['textfield5']
        hr_number = request.form['textfield6']
        hr_email = request.form['textfield7']
        company_code = request.form['textfield01']

        if email_exists(email_id):
            return '<script> alert("Email already exists. Please use a different email."); window.location="/company_registration"</script>'

        db = Db()
        q = db.insert("INSERT INTO login VALUES('', '" + email_id + "', '" + password + "', 'company')")
        db.insert("INSERT INTO company VALUES('" + str(
            q) + "','" + name + "','" + company_type + "','" + company_location + "','" + email_id + "','" + hr_name + "','" + hr_number + "','" + hr_email + "','" + company_code + "')")
        return '<script> alert("Registration successful"); window.location="/"</script>'
    else:
        return render_template('admin/company_registration.html')

def email_exists(email):
    db = Db()
    result = db.select("SELECT username FROM login WHERE username = '" + email + "'")
    return len(result) > 0



@app.route('/event_calendar', methods=['GET', 'POST'])
def event_calendar():
    if request.method == 'POST':
        company_code = request.form['company_code']
        event_title = request.form['event_title']
        event_description = request.form['event_description']
        event_date = request.form['event_date']
        event_time = request.form['event_time']

        db = Db()
        db.insert("INSERT INTO event_calendar VALUES ('','" + company_code + "','" + event_title + "','" + event_description + "','" + event_date + "','" + event_time + "')")
        return '<script> alert("Event added successfully"); window.location="/event_calendar"</script>'
    else:
        db = Db()
        companies = db.select("SELECT company_code, company_name FROM company")
        events = db.select("SELECT * FROM event_calendar")
        return render_template('company/event_calendar.html', companies=companies, events=events)


@app.route('/event_calendar_c', methods=['GET'])
def event_calendar_c():
    db = Db()
    companies = db.select("SELECT company_code, company_name FROM company")
    events = db.select("SELECT * FROM event_calendar")
    return render_template('company/event_calendar_c.html', companies=companies, events=events)

@app.route('/view_student_c')
def view_student_c():
    if session['lg'] == 'lin':
        db = Db()
        res = db.select("select * from student,course where student.stud_course_id=course.course_id")
        print(res)
        return render_template('company/view_student_c.html', data=res)
    else:
        return redirect('/')


@app.route('/send_mail/<aid>')
def send_mail(aid):
    if 'lg' in session and session['lg'] == 'lin':
        db = Db()
        student_data = db.selectOne("SELECT stud_email FROM student where stud_id ='" + aid + "'")

        if student_data:
            email = student_data['stud_email']
            # passwd = generate_random_password()

            import smtplib
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            s.login("eedu07212@gmail.com", "cjwfhugnvxbcijow")

            msg = MIMEMultipart()
            msg['From'] = "eedu07212@gmail.com"
            msg['To'] = email
            msg['Subject'] = "Your Password for E-EDU Website"
            body = "Your Password is: "
            msg.attach(MIMEText(body, 'plain'))
            s.send_message(msg)
            s.quit()
            return redirect('/view_student_c')
        else:
            return "Student data not found"
    else:
        return redirect('/')


#============================================================================
@app.route('/logout')
def logout():
    session.clear()
    session['lg'] = ""
    return redirect('/')


if __name__ == '__main__' :
    debug = "true"
    app.run(port=1234)

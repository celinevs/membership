from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='D:\KULIAH\modern web\membership UTS')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Membership.sqlite3'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zlQGYYYPfWxGQUaYuFcPDaOOYMmICWQv@autorack.proxy.rlwy.net:34163/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

app.secret_key = 'my_super_secret_key_123'

db= SQLAlchemy(app)

@app.route('/')

def home():
    return render_template('index.html')

@app.route('/aboutus')

def about_us():
    return render_template('aboutus.html')

@app.route('/register', methods=['POST','GET'])

def register():
    if request.method == 'POST':
        user = request.form['name']
        membership_type = request.form['travel']

        new_member = Member(name=user, membership_type=membership_type)

        # Tambahkan ke database
        try:
            db.session.add(new_member)
            db.session.commit()
            flash('New member registered successfully!', 'success')
            return render_template('register.html', alert_message="New member registered successfully!")
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        return render_template('register.html')

# Search member by id
@app.route('/attendance_search', methods=['POST', 'GET'])
def search_member():
    if request.method == 'POST':
        member_id = request.form['member_id']
        member = Member.query.get(member_id)

        if member:
            return render_template('attendance_confirm.html', member=member)
        else:
            return render_template('attendance_search.html', alert_message="Member not found")
    else:
        return render_template('attendance_search.html')

# Confirm member attendance
@app.route('/attendance_confirm/<int:member_id>', methods=['POST', 'GET'])
def confirm_member(member_id):
    member = Member.query.get_or_404(member_id)
    current_time = datetime.now()

    if member.last_attendance and (current_time - member.last_attendance) < timedelta(minutes=2):
        flash('You cannot attend again within 2 minutes of your last attendance.', 'error')
        return render_template('attendance_search.html', alert_message="You cannot attend again within 2 minutes of your last attendance.")

    new_attendance = Attendance(member_id=member.id, date=current_time)
    
    try:
        member.attendance_count += 1
        member.last_attendance = current_time
        db.session.add(new_attendance)
        db.session.commit()

        if member.attendance_count % 5 == 0:
            payment = 100000 if member.membership_type == 'bus' else 50000
            new_payment = FeePayment(member_id=member.id, amount=payment * 5)
            db.session.add(new_payment)
            db.session.commit()
            payment_id = new_payment.id
            return render_template('pay.html', member=member, total=payment * 5, payment_id=payment_id)

        return render_template('attendance_confirm.html', member=member, alert_message=f"Attendance confirmed for {member.name}. Total attendance: {member.attendance_count}")
    except Exception as e:
        return f"An error occurred: {e}"

    
# Confirm member attendance
@app.route('/payment_confirm/<int:payment_id>', methods=['POST', 'GET'])

def confirm_payment(payment_id):
    pay = FeePayment.query.get_or_404(payment_id)
    pay.status = 'Paid'
    db.session.commit()
    fee = db.session.query(FeePayment, Member).join(Member, FeePayment.member_id == Member.id).all()
    
    return render_template('payment.html', fee=fee, alert_message=f"Payment Success")
        
@app.route('/members')
def show_members():
    # Query all members from the database
    members = Member.query.all()

    # Pass the members to the template
    return render_template('members.html', members=members)

@app.route('/payment')
def show_payment():
    # Query all members from the database
    fee = db.session.query(FeePayment, Member).join(Member, FeePayment.member_id == Member.id).all()
    # Pass the members to the template
    return render_template('payment.html', fee=fee)

@app.route('/show_attendance')
def show_attendance():
    attendance_records = db.session.query(Attendance, Member).join(Member, Attendance.member_id == Member.id).all()
    # Render template or provide functionality for showing attendance
    return render_template('show_attendance.html', attendance_records=attendance_records)

@app.route('/<usr>')
def user(usr):
    return f'<h1>{usr}</h1>'


class Member(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    membership_type = db.Column(db.String(20))
    attendance_count = db.Column(db.Integer, default=0)
    last_attendance = db.Column(db.DateTime)

    def __init__(self, name, membership_type):
        self.name = name
        self.membership_type = membership_type

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    timestamp = db.Column(db.DateTime)
    
    def __init__(self, member_id, date):
        self.member_id = member_id
        self.timestamp = date

class FeePayment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Unpaid')

    def __init__(self, member_id, amount):
        self.member_id = member_id
        self.amount = amount


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


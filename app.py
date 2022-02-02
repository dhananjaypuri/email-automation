# from dataclasses import dataclass
# from email.policy import default
from re import L
from urllib.parse import uses_fragment
from flask import Flask, redirect , render_template, request , sessions
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import pytz
import smtplib
from email.message import EmailMessage

from zmq import Message


app = Flask(__name__);

app.secret_key = "nssjhsjhsjsh";
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db';

db = SQLAlchemy(app);

migrate = Migrate(app, db);

eid = "dhananjay.singer.puri@gmail.com";
password = "lrrgaafmduiifylv";

def send_mail(mess_to , body):
    msg = EmailMessage();

    msg['To'] = mess_to;
    msg['Subject'] = "Fill Survey"
    msg['From'] = eid;
    msg.set_content(body);

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(eid, password);
        smtp.send_message(msg);

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True);
    uname = db.Column(db.String(200) , nullable=False);
    email = db.Column(db.String(200) , nullable=False);
    score = db.relationship('Scores');

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key= True);
    srvops = db.Column(db.Integer, nullable = True);
    slmr = db.Column(db.Integer, nullable = True);
    techcap = db.Column(db.Integer, nullable = True);
    gc = db.Column(db.Integer, nullable = True);
    si = db.Column(db.Integer, nullable = True);
    overallrate = db.Column(db.Integer, nullable = True);
    datesent = db.Column(db.DateTime, default=datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')));
    daterec = db.Column(db.DateTime);
    replied = db.Column(db.Boolean, nullable = False, default = False);
    remarks = db.Column(db.Text , nullable=True);
    uid = db.Column(db.Integer, db.ForeignKey('user.id'));

@app.route('/', methods=['GET', 'POST'])
def home():
    
    return "This is home";

@app.route('/sendmail', methods=['GET', 'POST'])
def sendmail():

    user = User.query.all();
    emailList = [];
    for item in user:
        emailList.append(item.email);
    for email in emailList:
        user = User.query.filter_by(email=email).first();
        todayDate = datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata'));
        user_score = Scores(datesent=datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')), uid=user.id);
        db.session.add(user_score);
        db.session.commit();
        
        user2 = User.query.filter_by(email=email).first();
        score2 = Scores.query.filter_by(uid=user2.id, datesent=todayDate).first();
        print(score2.id);
        body = f'''Hi {user.uname}, \n\nRequest you to please fill the below survey.\n\n Link : http://127.0.0.1:8000/survey?uname={user.uname}&id={score2.id} \n\nRegards\nDhananjay Puri''';
        send_mail(email, body);
        print(body);
    
    return "hi";

@app.route('/sendmail2/<dt>', methods=['GET', 'POST'])
def sendmail2(dt):
    dtList = str(dt).split('-');
    newdate = datetime.datetime(int(dtList[0]),int(dtList[1]),int(dtList[2])).date();
    scores = Scores.query.all();
    emailList = [];

    for score in scores:

        datesent = score.datesent.date();
        if(datesent == newdate and score.replied == False):
            # print("Dates are equal");
            user = User.query.filter_by(id=score.uid).first();
            emailList.append(user.email);
        else:
            continue;

    laterdate = newdate + datetime.timedelta(days=1);

    for email in emailList:
        user = User.query.filter_by(email=email).first();
        score = Scores.query.filter_by(uid=user.id).all();
        for item in score:
            userdate = item.datesent.date();
            if(userdate == newdate and item.replied == False):
                user_score = Scores(datesent=laterdate, uid=user.id);
                db.session.add(user_score);
                db.session.commit();

                user2 = User.query.filter_by(email=email).first();
                print("User id" ,(user2.id));
                scorenew = Scores.query.filter_by(uid=user2.id).all();
                for val in scorenew:
                    if(val.datesent.date() == laterdate):
                        body = f'''Hi {user.uname}, \n\nRequest you to please fill the below survey.\n\n Link : http://127.0.0.1:8000/survey?uname={user.uname}&id={val.id} \n\nRegards\nDhananjay Puri''';
                        print(body); 
                        send_mail(email, body);
                    else:
                        continue;

 
                # body = f'''Hi {user.uname}, \n\nRequest you to please fill the below survey.\n\n Link : http://127.0.0.1:8000/survey?uname={user.uname}&id={score2.id} \n\nRegards\nDhananjay Puri''';
                # send_mail(email, body);
                # print(body);                
            else:
                continue;
            
        
    return "This is sendmail 2";


@app.route('/survey', methods=['GET', 'POST'])
def fill_survey():

    if(request.method == 'POST'):
        try:
            srvops = request.form.get('srvops', default=0, type=int);
            slmr = request.form.get('slmr', default=0, type=int);
            techcap = request.form.get('techcap', default=0, type=int);
            gc = request.form.get('gc', default=0, type=int);
            si = request.form.get('si', default=0, type=int);
            overallrate = request.form.get('overallrate', default=0, type=int);
            remarks = request.form.get('remarks');
            daterec = datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata'));

            id = int(request.form.get('id'));

            score = Scores.query.filter_by(id=id).first();
            score.srvops = int(srvops);
            score.slmr = int(slmr);
            score.techcap = int(techcap);
            score.gc = int(gc);
            score.si = int(si);
            score.overallrate = int(overallrate);
            score.remarks = remarks;
            score.replied = True;
            score.daterec = daterec;

            db.session.add(score);
            db.session.commit();
            return redirect('/');

        except Exception as e:
            print(e);

    id = request.args.get('id', default=None, type=int);
    uname = request.args.get('uname', default=None, type=str);
    user = User.query.filter_by(uname=uname).first();
    score = Scores.query.filter_by(id=id).first();
    return render_template('survey.html', score=score);



if(__name__ == '__main__'):
    app.run(debug=True, port=8000);
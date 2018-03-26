#!/usr/bin/python
from flask import Flask, jsonify, request, json, render_template
from datetime import datetime
from services import email_service
import requests as req
from services.dev import CONFIG_dev
from services.prod import CONFIG_prod
import MySQLdb
import json as simplejson
from google.appengine.api import users
import logging
app = Flask(__name__)
Templates = [
    {
        "id":1,
        "date":"2018-04-25",
        "text": "ceci est un test",
        "reccurence": "tous les jours",
        "user": 'kestuf@test.com',
    },
    {
        "id":2,
        "date":"2018-04-25",
        "text": "ceci est un test",
        "reccurence": "Une seule fois",
        "user": 'kestuf@test.com',

    },
    {
        "id":3,
        "date":"2018-05-05",
        "text": "ceci est un test",
        "reccurence": "tous les Mois",
        "user": 'kestuf@test.com',
    }
]

def check_auth():
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        print("my nick: "+nickname)
        logout_url = users.create_logout_url('/')
        greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(ickname, logout_url)
        return greeting
    else:
        login_url = users.create_login_url('/')
        greeting = '<a href="{}">Sign in</a>'.format(login_url)
        return greeting

def get_user_connect():
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        return nickname 
    else:
        return "idk@kestuf.com"

#dont forget when prod to add:  unix_socket=CONFIG_prod[u"db"][u"unix_socket"],
def connect():
    con = MySQLdb.connect(unix_socket=CONFIG_prod[u"db"][u"unix_socket"],
                        host=CONFIG_prod[u"db"][u"host"],    
                        user=CONFIG_prod[u"db"][u"user"],         
                        passwd=CONFIG_prod[u"db"][u"password"],           
                        db=CONFIG_prod[u"db"][u"database"])
    cursor = con.cursor()
    return cursor, con

no_reply = ""

"""
As her name indicates, this method allow to get all mail templates in database
"""
@app.route('/api/templates', methods=['GET'])
def get_all_mail_templates():
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM Form ORDER BY date DESC")
        items = []
        for row in cursor.fetchall():
            #print(row)
            items.append({
                'id' : row[0],
                'date' : row[1],
                'text' : row[2],
                'reccurence' : row[3],
                'user' : row[4]
            })
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))     
    return jsonify(items)    


"""
Help to retrieve all users in db
""" 
@app.route('/api/users', methods = ['GET'])    
def get_all_users():
    try:
        cursor, con = connect()    
        cursor.execute("SELECT * FROM Manager")
        items = []
        for row in cursor.fetchall():
            print(row)
            items.append({
                'id' : row[0],
                'email' : row[1]
            })
        con.commit()
    except TypeError as e:
        print(e)     
    return jsonify(items) 
    


"""
This method help to activate the template mail who will be used to send mail to all users
"""
@app.route('/api/template/yes', methods=['POST'])
def mail_activate():
    req.reset_activate_mail()
    print(request.data)
    response = json.loads(request.data)
    identifiant = response['id']
    toggle = response['togg']
    value = ""
    print(toggle)
    if toggle == True:
        value = 1
    else:
        value = 0
    #Connect to the db
    print(value)
    try:
        cursor, con = connect()
        cursor.execute("UPDATE mydb.Form SET activate =" +str(value)+" WHERE id = "+str(identifiant)+" ")
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to insert: {}'.format(unicode(e).encode(u'utf-8')))
    print("great")

    """
    Send mail after insert on database
    Do a GET request to take the last row insert in db, help to hand the 
    recipients could be a table? if yes? pass him a table of the 2 persons
    """
    result = req.splitResult()
    for row in result:
        try:
            row = row.split(",")  
            #recipient = "andresse.njeungoue@devoteamgcloud.com, andressegeofried@gmail.com"
            #print(recipient)
            list1 = req.shuffle2emails(row[0],row[1]) 
            recipients = list1[0][0] +","+list1[1][0]
            subject = "Kestuf N: (test) "
            text = req.activate_mail()
            body = render_template('body_mail.html', pers1 = list1[0][0], pers2 = list1[1][0], body_plus = text)
            try:
                email_service.send(recipients, subject, body)
            except BaseException, e:
                logging.error(u'Failed to send error mail: {}'.format(unicode(e).encode(u'utf-8')))
        except BaseException, e:
            logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    
    #Templates.append(mail_template)
    return "yes"

"""
This method help to add one mail template in the Form's table
"""
@app.route('/api/template', methods=['POST'])
def add_one_mail_template():
    #print(request.data)
    mail_template = json.loads(request.data)
    date = mail_template['date']
    text = mail_template['text']
    reccurence = mail_template['recurrence']
    user = get_user_connect()
    print("userConnect: "+user)

    #Connect to the db
    cursor, con = connect()
    Form = """
    INSERT INTO Form(date, text, reccurence, user)
    VALUES
        (%s, %s, %s, %s)
        """
    cursor.execute(Form, (date, text, reccurence, user))
    con.commit()

    """
    Send mail after insert on database
    Do a GET request to take the last row insert in db, help to hand the 
    recipients could be a table? if yes? pass him a table of the 2 persons
    """    
    try:  
        #recipient = "andresse.njeungoue@devoteamgcloud.com, andressegeofried@gmail.com"
        #print(recipient)
        recipients = req.retieve_manager_mails()
        print("string: "+recipients)
        subject = " Kestuff nouveau template "
        #body = render_template('body_mail.html', pers1 = list1[0][0], pers2 = list1[1][0], body_plus = text)
        body = render_template('edit_form_notif_mail.html', body_plus = text)
        try:
            email_service.send(recipients, subject, body)
        except BaseException, e:
            logging.error(u'Failed to send error mail: {}'.format(unicode(e).encode(u'utf-8')))
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))

    Templates.append(mail_template)
    return jsonify({"mail Templates":Templates})


"""
This method help to add one user in the database
"""
@app.route('/api/user', methods=['POST'])
def add_one_user():
    #print("la request: " +request.data)
    req = request.data
    try:
        cursor, con = connect()
        Manager = "INSERT INTO Manager(email) VALUES (%s)"
        cursor.execute(Manager, [req])
        con.commit()
        treat = []
        treat = get_all_users()

    except TypeError as e:
        print(e)
    return treat

@app.route('/api/user/<int:id>', methods=['DELETE'])
def del_one_user(id):
    print("la request: " +request.data)
    req = request.data
    try:
        cursor, con = connect()
        Manager = "DELETE FROM Manager WHERE email = (%s)"
        cursor.execute(Manager, [req])
        con.commit()
        treat = []
        treat = get_all_users()

    except TypeError as e:
        print(e)
    return treat


if(__name__) == "__main__":
    app.run(debug=True, port=5003)
#!/usr/bin/python
from services.dev import CONFIG_dev
from services.prod import CONFIG_prod
import MySQLdb

def connect():
    con = MySQLdb.connect(unix_socket=CONFIG_prod[u"db"][u"unix_socket"],
                        host=CONFIG_prod[u"db"][u"host"],    
                        user=CONFIG_prod[u"db"][u"user"],         
                        passwd=CONFIG_prod[u"db"][u"password"],           
                        db=CONFIG_prod[u"db"][u"database"])
    cursor = con.cursor()
    return cursor, con


def shuffle2emails(id,jd):
    id = str(id)
    ida = str(id)
    table = []
    i = 1
    while i <= 2:

        try:
            cursor, con = connect()
            cursor.execute( "SELECT email FROM mydb.Users where id ="+ida+"" )    
            for row in cursor.fetchall():
                table.append(row)
            con.commit()
        except TypeError as e:
            print(e)
        
        ida = str(jd)
        i = i+1
    #print(type(table))
    #print ('this table:{0} '.format(table))
    return table

def getTheRow():
    id = 0
    try:
        cursor, con = connect()
        cursor.execute("SELECT count from mydb.Users where id = 1 LIMIT 1")
        for row in cursor.fetchall():
            id = row
        con.commit()
    except TypeError as e:
        print(e)

    #print('we are on: {0}'.format(id))
    return " ".join(str(x) for x in id)

def getUserMeetWho():
    user_meet = ""
    count = getTheRow()
    count = int(count) +1
    print(count)
    counter = count_users()
    counter = int(counter) - 1
    print(counter)
    if count > counter:
        count = 1
        print(str(count))
        
    else:
        pass
    
    try:
        cursor, con = connect()
        cursor.execute("UPDATE mydb.Users SET count =" +str(count)+" ")
        con.commit()
        print("great")
    except BaseException, e:
        logging.error(u'Failed to insert: {}'.format(unicode(e).encode(u'utf-8')))
    
    try:
        cursor, con = connect()
        cursor.execute("SELECT user_must_meet_user from mydb.Users where id ="+str(count)+"") 
        for row in cursor.fetchall():
            print(row)
            user_meet = row
        con.commit()
    except TypeError as e:
        print(e)
        
    #print(type(user_meet[0]) is str)
    return user_meet[0]


def test():
    for x in range(0, 3):
        print x


def splitResult():
    result = getUserMeetWho()
    result = result.split(";")
    #print(result)
    return result
    #while i < lenght:
    """
    for row in result:
        row = row.split(",")
        list1 = shuffle2emails(row[0],row[1])
        print(list1[0][0])
        print(type(list1[0][0]))
        string = list1[0][0] +","+list1[1][0]
        print(string)
    """

def retieve_manager_mails():
    #length = count_manager()
    recipient = "andressegeofried@gmail.com"
    emails = ""
    try:
        cursor, con = connect()
        cursor.execute("SELECT email from mydb.Manager")
        for row in cursor.fetchall():
            #print(row[0])
            emails += recipient +str(", "+row[0])
            recipient = ""
        con.commit()
    except TypeError as e:
        print(e)
    print(emails)
    return emails

def count_manager():
    length = ""
    try:
        cursor, con = connect()
        cursor.execute("SELECT count(*) from mydb.Manager")
        for row in cursor.fetchall():
            length = row[0]
        con.commit()
    except TypeError as e:
        print(e)
    return str(length)


def count_users():
    length = ""
    try:
        cursor, con = connect()
        cursor.execute("SELECT count(*) from mydb.Users")
        for row in cursor.fetchall():
            length = row[0]
        con.commit()
    except TypeError as e:
        print(e)
    return str(length)
"""
Query who help to retrieve the activate mail
"""
def reset_activate_mail():
    try:
        cursor, con = connect()
        cursor.execute("UPDATE mydb.Form SET activate = 0")
        for row in cursor.fetchall():
            print(str(row[0]))
        con.commit()
    except TypeError as e:
        print(e)

def activate_mail():
    try:
        cursor, con = connect()
        cursor.execute("SELECT text FROM mydb.Form where activate = 1")
        for row in cursor.fetchall():
            print(str(row[0]))
        con.commit()
    except TypeError as e:
        print(e)
    return str(row[0])

if __name__ == '__main__':
    #count_users()
    #reset_activate_mail()
    #activate_mail()
    #count_manager()
    #retieve_manager_mails()
    #test()
    #splitResult()
    getUserMeetWho()
    #getTheRow()
    #shuffle2emails(1,2)
import pymysql # pip install pymysql
import re
import datetime

# DB
DBNAME = ''
PASSWORD = ''
TABLENAME = ''

# Others
TEXTPATH = ''
MYNAME = ''
YOURNAME = ''



def FindFirstMatch(str, c):
    for i in range(len(str)):
        if str[i] == c:
            return i;


def ReadTalks(path):
    f = open(path, 'r', encoding='utf-8-sig')

    return f.readlines()


# [(sender, receiver, time, msg), ...]
def InsertTalks(table, elems):
    conn = pymysql.connect(host='localhost', user='root', password=PASSWORD, db=DBNAME, charset='utf8')
    cursor = conn.cursor()
    sql = 'insert into ' + table + ' (Sender, Receiver, Time, Text) values (%s, %s, %s, %s)'
    cursor.executemany(sql, elems)
    conn.commit()
    conn.close()


# ex) 2016-06-10 01:50 PM
def ConvertDateTimeFormat(time):
    return datetime.datetime.strptime(time, '%Y-%m-%d %I:%M %p').strftime('%Y-%m-%d %H:%M')


# Incomplete code that is inefficient and hard to read
def XtractElems(talks):
    elems = []
    for talk in talks:
        i = FindFirstMatch(talk, ',')

        if i == None:
            print('flag line')
            continue

        datetimes = talk[:i].split(' ')
        year = datetimes[0][:-1]
        month = datetimes[1][:-1]
        day = datetimes[2][:-1]
        ampm = datetimes[3]
        time = datetimes[4]

        j = FindFirstMatch(talk[i:], ':')
        senderMsg = talk[i:]

        sender = senderMsg[2:j].strip()
        msg = senderMsg[j+1:].strip()

        if ampm == '오전':
            ampm = 'AM'
        else:
            ampm = 'PM'

        if sender == '회원님':
            sender = MYNAME
            receiver = YOURNAME
        else:
            sender = YOURNAME
            receiver = MYNAME

        elems.append((
            sender,
            receiver,
            ConvertDateTimeFormat(year + '-' + month + '-' + day + ' ' + time + ' ' + ampm),
            msg))

    return elems


# main()
talks = ReadTalks(TEXTPATH)
elems = XtractElems(talks)
InsertTalks(TABLENAME, elems)

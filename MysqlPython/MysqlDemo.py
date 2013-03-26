#-*- encoding:gb2312 -*-
'''
Created on 2012-1-11
@author: xiaojay
'''

import MySQLdb as mysql

def fetchRes(conn=None):
    """Fetches up to maxrows as a tuple(how=0) 
    as dictionaries, key=column or table.column if duplicated(how=1)
    as dictionaries, key=table.column (how=2)"""
    conn.query("select * from authors order by author_id")
    if conn==None : return
    """
    connection 对象可以返回两种result，分别是store_result和use_result
    store_result 将结果集存回client端，而use_result则是结果集保存在server端，
    并且维护了一个连接，会占用server资源。此时，不可以进行任何其他的查询。
    建议使用store_result，除非返回结果集（result set）过大或是无法使用limit的情形
    """
    r = conn.store_result()
    print conn.affected_rows()
    
    """
    how=2 ,返回一个元组，里面的元素是dict
    """
    res = r.fetch_row(maxrows=100,how = 2)
    
    for item in res :
        for key in item.keys():
            print key , item[key]
    
    """
    res = r.fetch_row(100,0)
    
    for author_id , author_last , author_first , country in res :
        print "ID : %s , Author_last : %s , Author_First : %s , Counry : %s" \
        % (author_id , author_last , author_first , country )
     """   

def fetchfromUse_result(conn):
    conn.query("select * from authors order by author_id")
    r = conn.use_result()
    """
    每次fetch，游标都会移动
    """
    res = r.fetch_row(3,0)
    print "*"*20
    printAuthors(res)
    """
    由于采用的是use_result返回结果集，所以在fetch所有的条目之前，不能进行任何的query操作。
    """
    res = r.fetch_row(3,0)
    print "*"*20
    printAuthors(res)

def Cursor(conn=None):
    "mysql本身不支持游标（Cursor），但是MySQLdb对Cursor进行了仿真"
    if conn == None : return 
    cur = conn.cursor()
    """
    调用execute方法，执行单条sql语句
    """
    cur.execute("select * from authors order by author_id")
    
    """
    游标cursor具有fetchone、fetchmany、fetchall三个方法提取数据
    每个方法都会导致游标游动，所以必须关注游标的位置"
    """
    resall = cur.fetchall()
    printAuthors(resall)
    
    print "*"*25
    """
    scroll方法使得游标进行卷动，
    mode指定相对当前位置(relative)还是以绝对位置(absolute)
    """
    cur.scroll(value=2,mode="absolute")
    
    resall = cur.fetchall()
    printAuthors(resall)
    
    
    """
    调用executemany方法
    这个方法很好用，数据库性能瓶颈很大一部分就在于网络IO和磁盘IO
    将多个insert放在一起，只执行一次IO，可以有效的提升数据库性能
    """
    args = [('aaaaaa','bbbbbb','cccccc'),('dddddd','eeeeee','ffffff'),('gggggg','hhhhhh','iiiiii')]
    sqltext = "insert into authors (author_last,author_first,country) values (%s,%s,%s)"
    cur.executemany(sqltext,args)
    cur.close()
    fetchRes(conn)
        

def printAuthors(res):
    for author_id , author_last , author_first , country in res :
        print "ID : %s , Author_last : %s , Author_First : %s , Counry : %s" \
        % (author_id , author_last , author_first , country )  
        
#建立mysql连接，指定host、用户名、密码、默认数据库
db = mysql.Connect(host = "localhost", user = "root" , passwd = "peterbbs" , db = "bookstore")

if db.open : 
    print "Database is open."
else :
    print "Fail to open database"
fetchRes(db)
#db.query("insert into authors (author_last , author_first , country) values ('Zhang','Jam','China')")
#Cursor(db)
#fetchRes(db)
#fetchfromUse_result(db)



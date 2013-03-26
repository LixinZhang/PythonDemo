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
    connection ������Է�������result���ֱ���store_result��use_result
    store_result ����������client�ˣ���use_result���ǽ����������server�ˣ�
    ����ά����һ�����ӣ���ռ��server��Դ����ʱ�������Խ����κ������Ĳ�ѯ��
    ����ʹ��store_result�����Ƿ��ؽ������result set����������޷�ʹ��limit������
    """
    r = conn.store_result()
    print conn.affected_rows()
    
    """
    how=2 ,����һ��Ԫ�飬�����Ԫ����dict
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
    ÿ��fetch���α궼���ƶ�
    """
    res = r.fetch_row(3,0)
    print "*"*20
    printAuthors(res)
    """
    ���ڲ��õ���use_result���ؽ������������fetch���е���Ŀ֮ǰ�����ܽ����κε�query������
    """
    res = r.fetch_row(3,0)
    print "*"*20
    printAuthors(res)

def Cursor(conn=None):
    "mysql����֧���α꣨Cursor��������MySQLdb��Cursor�����˷���"
    if conn == None : return 
    cur = conn.cursor()
    """
    ����execute������ִ�е���sql���
    """
    cur.execute("select * from authors order by author_id")
    
    """
    �α�cursor����fetchone��fetchmany��fetchall����������ȡ����
    ÿ���������ᵼ���α��ζ������Ա����ע�α��λ��"
    """
    resall = cur.fetchall()
    printAuthors(resall)
    
    print "*"*25
    """
    scroll����ʹ���α���о���
    modeָ����Ե�ǰλ��(relative)�����Ծ���λ��(absolute)
    """
    cur.scroll(value=2,mode="absolute")
    
    resall = cur.fetchall()
    printAuthors(resall)
    
    
    """
    ����executemany����
    ��������ܺ��ã����ݿ�����ƿ���ܴ�һ���־���������IO�ʹ���IO
    �����insert����һ��ִֻ��һ��IO��������Ч���������ݿ�����
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
        
#����mysql���ӣ�ָ��host���û��������롢Ĭ�����ݿ�
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



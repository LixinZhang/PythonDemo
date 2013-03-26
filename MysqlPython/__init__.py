#-*- encoding:gb2312 -*-
import PyMysql

"""
authors ���ű�ܼ򵥡�
+--------------+-------------+------+-----+---------+----------------+
| Field        | Type        | Null | Key | Default | Extra          |
+--------------+-------------+------+-----+---------+----------------+
| author_id    | int(11)     | NO   | PRI | NULL    | auto_increment |
| author_last  | varchar(50) | YES  |     | NULL    |                |
| author_first | varchar(50) | YES  | MUL | NULL    |                |
| country      | varchar(50) | YES  |     | NULL    |                |
+--------------+-------------+------+-----+---------+----------------+
������Ҫ�����в�������Ըñ�
"""

def printAuthors(res,mode=0,lines=0):
    """
    ��ʽ�����
    """
    print "*"*20, " lines: ",lines ," ","*"*20
    if mode==0  :
        for author_id , author_last , author_first , country in res :
            print "ID : %s , Author_last : %s , Author_First : %s , Country : %s" \
            % (author_id , author_last , author_first , country )
    else :
        for item in res :
            print "-----------"                
            for key in item.keys():
                print key ," : ",item[key]

#��������
mysql = PyMysql.PyMysql()
mysql.newConnection(
        host="localhost", 
        user="root", 
        passwd="peterbbs", 
        defaultdb="bookstore")
""
#����sql���
sqltext = "select * from authors order by author_id "
#����query����,�õ�result
lines , res = mysql.query(sqltext, mode=PyMysql.STORE_RESULT_MODE)
#��ȡ����
data = mysql.fetch_queryresult(res, maxrows=20, how=0, moreinfo=False)
#��ӡ
printAuthors(data,0,lines)

#��ʾ���в���
sqltext = "insert into authors (author_last,author_first,country) values (%s,%s,%s)"
args = [('aaaaaa','bbbbbb','cccccc'),('dddddd','eeeeee','ffffff'),('gggggg','hhhhhh','iiiiii')]
lines ,cur = mysql.execute(sqltext,args,mode=PyMysql.DICTCURSOR_MODE,many=True)
print "*"*20, lines ,"�б����� ","*"*20

sqltext = "select * from authors order by author_id "
#����cursor.execute����,�õ�result
lines ,cur = mysql.execute(sqltext,mode=PyMysql.DICTCURSOR_MODE)
#��ȡ����
data = mysql.fetch_executeresult(cur, mode=PyMysql.FETCH_MANY, rows=20)
#��ӡ
printAuthors(data,1,lines)

#�ر�����
mysql.closeConnnection()
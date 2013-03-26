#-*- encoding:gb2312 -*-
import PyMysql

"""
authors 这张表很简单。
+--------------+-------------+------+-----+---------+----------------+
| Field        | Type        | Null | Key | Default | Extra          |
+--------------+-------------+------+-----+---------+----------------+
| author_id    | int(11)     | NO   | PRI | NULL    | auto_increment |
| author_last  | varchar(50) | YES  |     | NULL    |                |
| author_first | varchar(50) | YES  | MUL | NULL    |                |
| country      | varchar(50) | YES  |     | NULL    |                |
+--------------+-------------+------+-----+---------+----------------+
本文主要的所有操作都针对该表。
"""

def printAuthors(res,mode=0,lines=0):
    """
    格式化输出
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

#建立连接
mysql = PyMysql.PyMysql()
mysql.newConnection(
        host="localhost", 
        user="root", 
        passwd="peterbbs", 
        defaultdb="bookstore")
""
#定义sql语句
sqltext = "select * from authors order by author_id "
#调用query方法,得到result
lines , res = mysql.query(sqltext, mode=PyMysql.STORE_RESULT_MODE)
#提取数据
data = mysql.fetch_queryresult(res, maxrows=20, how=0, moreinfo=False)
#打印
printAuthors(data,0,lines)

#演示多行插入
sqltext = "insert into authors (author_last,author_first,country) values (%s,%s,%s)"
args = [('aaaaaa','bbbbbb','cccccc'),('dddddd','eeeeee','ffffff'),('gggggg','hhhhhh','iiiiii')]
lines ,cur = mysql.execute(sqltext,args,mode=PyMysql.DICTCURSOR_MODE,many=True)
print "*"*20, lines ,"行被插入 ","*"*20

sqltext = "select * from authors order by author_id "
#调用cursor.execute方法,得到result
lines ,cur = mysql.execute(sqltext,mode=PyMysql.DICTCURSOR_MODE)
#提取数据
data = mysql.fetch_executeresult(cur, mode=PyMysql.FETCH_MANY, rows=20)
#打印
printAuthors(data,1,lines)

#关闭连接
mysql.closeConnnection()
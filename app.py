from flask import Flask, render_template, request, jsonify
from service.question_service import question_service_instance
from model import question_template
import pymysql
from flask_cors import *
from model import test_question_template

app = Flask(__name__)

# 解决跨域请求资源被拦截问题
CORS(app, supports_credentials=True, resources=r"/*")

# 打开数据库连接
conn = pymysql.connect(host='localhost', user='root', password='123456', database='flask', port=3306, charset='utf8')
# 获取游标
cur = conn.cursor()

# 获取登录页面

@app.route('/')
def denglu():
    return render_template('login.html')

@app.route('/registerHTML')
def zhuce():
    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/hangyeHTML')
def hangye():
    return render_template('hangye.html')

@app.route('/zhuanjiaHTML')
def zhuanjia():
    return render_template('zhuanjia.html')

@app.route('/qaHTML')
def qa():
    return render_template('qa.html', ctx=None)

@app.route('/userHTML')
def user():
    return render_template('user_table.html')

# 获取所有用户
@app.route('/user', methods=['POST', 'GET'])
def getUser():
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    username = request.args.get("key[username]")
    if((username == None) or (username == '')):
        # sql语句
        sql = 'select * from user limit %s , %s;' % ((page - 1) * limit, limit)
    else:
        sql = 'select * from user where username like %s limit %s , %s;' % ("'%"+username+"%'", (page - 1) * limit, limit)

    jsonData = []

    #执行sql
    cur.execute(sql)
    while 1:
        res = cur.fetchone()
        if res is None:
            # 表示已经取完结果集
            break
        result = {}
        result['username'] = res[0]
        result['password'] = res[1]
        result['phone'] = res[2]
        result['email'] = res[3]
        jsonData.append(result)
    head = {}
    head['status'] = 0
    head['message'] = ""
    head['total'] = getCount('user', username)
    head['rows'] = jsonData
    return jsonify(head)

# 添加用户数据
@app.route('/addUser', methods=['POST', 'GET'])
def addUser():
    name = request.args.get("name")
    password = request.args.get("password")
    tel = request.args.get("tel")
    email = request.args.get("email")

    sql = 'insert into user values (%s, %s, %s, %s);'%("'"+name+"'", "'"+password+"'", "'"+tel+"'", "'"+email+"'")
    cur.execute(sql)
    conn.commit()

    return render_template('user_table.html')

# 编辑用户数据
@app.route('/preEditUser', methods=['POST', 'GET'])
def preEditUser():
    data = {}
    name = request.form.get('name')
    password = request.form.get('password')
    tel = request.form.get('tel')
    email = request.form.get('email')
    data['name'] = name
    data['password'] = password
    data['tel'] = tel
    data['email'] = email
    return jsonify(data)
# 编辑用户数据
@app.route('/editUser', methods=['POST', 'GET'])
def editUser():
    newName = request.args.get("name")
    newPassword = request.args.get("password")
    newTel = request.args.get("tel")
    newEmail = request.args.get("email")
    oldName = request.args.get("oldName")
    oldPassword = request.args.get("oldPassword")
    oldTel = request.args.get("oldTel")
    oldEmail = request.args.get("oldEmail")
    sql = 'update user set username = %s,password = %s,phone = %s,email = %s where username = %s and password = %s and phone = %s and email = %s;'%("'"+newName+"'", "'"+newPassword+"'", "'"+newTel+"'", "'"+newEmail+"'","'"+oldName+"'", "'"+oldPassword+"'", "'"+oldTel+"'", "'"+oldEmail+"'")
    cur.execute(sql)
    conn.commit()
    return render_template('user_table.html')

# 删除用户数据
@app.route('/deleteUser', methods=['POST', 'GET'])
def deleteUser():
    data = {}
    data['code'] = 0
    data['msg'] = '查询成功'
    username = request.form.get('username')
    password = request.form.get('password')
    phone = request.form.get('phone')
    email = request.form.get('email')
    # SQL 删除语句
    sql = 'delete from user where username = %s and password = %s and phone = %s and email = %s;' %("'"+username+"'", "'"+password+"'","'"+phone+"'","'"+email+"'")
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交修改
        conn.commit()
        data['status'] = "success"
    except:
        # 发生错误时回滚
        conn.rollback()
        data['status'] = "failure"
    return jsonify(data)

# 获取表的数据量
def getCount(tableName,colName):
    if((colName == None) or (colName == '')):
        # sql语句
        sql = 'select count(*) from %s ;' % (tableName)
    else:
        sql = 'select count(*) from %s where username like %s;' % (tableName, "'%" + colName + "%'")

    # 执行sql
    cur.execute(sql)
    while 1:
        res = cur.fetchone()
        if res is None:
            # 表示已经取完结果集
            break
        count = res[0]
    return count


# 登录验证
@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    data = {}
    sql = 'select username from user where username = %s and password = %s;'%("'"+username+"'", "'"+password+"'")
    cur.execute(sql)
    while 1:
        res = cur.fetchone()
        if res is None:
            # 表示已经取完结果集
            break
        if(res[0] is not None):
            data['status'] = 'success'
        else:
            data['status'] = 'fail'
    return jsonify(data)

# 注册
@app.route('/register', methods=['POST', 'GET'])
def register():
    username = request.form.get("username")
    print(username)
    password = request.form.get("password")
    phone = request.form.get("phone")
    email = request.form.get("email")
    data = {}
    sql = 'insert into user values (%s, %s, %s, %s);'%("'"+username+"'", "'"+password+"'", "'"+phone+"'", "'"+email+"'",)
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交修改
        conn.commit()
        data['status'] = "success"
    except:
        # 发生错误时回滚
        conn.rollback()
        data['status'] = "failure"
    return jsonify(data)

# 问答
@app.route('/qa', methods=['POST', 'GET'])
def qa1():
    question = request.args.get("question")

    answer, entity1,entity2,cql1,cql2,cql3 = test_question_template.test_get_answer(question)


    return render_template('qa.html', ctx={"a": answer,"q":question,"b":entity1,"c":entity2,"d":cql1,"e":cql2,"f":cql3})


if __name__ == '__main__':
    app.run(host='0.0.0.0')

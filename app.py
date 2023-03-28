from flask import Flask, render_template # flask를 불러옴 
from pymongo import MongoClient

app = Flask(__name__) # flask를 실행 


# client = MongoClient("mongodb+srv://jisung4012:wltjd4011!@jisung0.ayoemb4.mongodb.net/?retryWrites=true&w=majority")
# db = client.test

doc = {'name':'bobby','age':21}
# db.users.insert_one(doc)


# << GET : 메인페이지('/') >>  
@app.route('/') # 라우팅 
def print_hello(): # callback함수 
    # 일단은 그냥 index페이지 띄우는데, 원래는 
    # 로그인이 됐을 시에는 index.html 
    # 관리자 로그인일 시 아닐 시 둘 다.. 파악! 
    # 아닐 시 login.html
    return render_template('index.html')


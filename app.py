from flask import Flask, render_template, request, redirect, url_for, flash # flask를 불러옴 
# flask : flask연결 
# render_template : 템플릿 엔진 페이지 띄워줌 
# request : 데이터 처리 객체 담당! 

from pymongo import MongoClient

app = Flask(__name__) # flask를 실행 


client = MongoClient('localhost', 27017)
userDB = client['user'] # 회원 db (관리자 사용자 싹 다 하나로 구분없이 모을게요!)
usercol = userDB['users'] # 회원 users column

playerDB = client['player'] # 축구선수 db
playercol = playerDB['players'] # 축구선수 column



# << GET : 메인페이지('/') >>  
@app.route('/') # 라우팅 
def print_hello(): # callback함수 
    # 일단은 그냥 index페이지 띄우는데, 원래는 
    # 로그인이 됐을 시에는 index.html 
    # 관리자 로그인일 시 아닐 시 둘 다.. 파악! 
    # 아닐 시 login.html
    return render_template('index.html')


@app.route('/register/index', methods = ['GET'])
def player_register_page():
    return render_template('register.html')


# << GET : 회원가입 페이지('/sign-up/index') >> 
@app.route('/sign-up/index', methods = ['GET'])
def sign_up_page():
    return render_template('signUp.html')

# << POST : 회원가입 로직처리('/api/new') >> 
@app.route('/api/new', methods = ['POST'])
def save_user():
    user_id = request.form['userID'] # user ID 가져옴
    user_pw = request.form['userPW'] # user password 가져옴 
    user_role = request.form['role'] # role 가져옴
    user = { # user 객체 
        'userID' : user_id,
        'userPW' : user_pw,
        'userRole' : user_role,
    }
    # 중복검사! 
    arr = []
    for x in usercol.find({'userID' : user_id}):
        arr.append(x)

    if len(arr) >= 1:
        return "중복된 id가 있습니다...!"
    else:
        usercol.insert_one(user)
        return redirect(url_for('login_page'))


# 선수 등록 


@app.route('/login/index', methods = ['GET'])
def login_page():
    return render_template('login.html')
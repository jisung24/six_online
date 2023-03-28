from flask import Flask, render_template, request, redirect, json ,url_for, flash, jsonify, session, make_response # flask를 불러옴 

# flask : flask연결 
# render_template : 템플릿 엔진 페이지 띄워줌 
# request : 데이터 처리 객체 담당! 
 
from pymongo import MongoClient
from flask_jwt_extended import *
from flask_jwt_extended import JWTManager
import jwt
from datetime import datetime
from datetime import timedelta
import datetime
from functools import wraps
import hashlib

app = Flask(__name__) # flask를 실행 

JWT_SECRET_KEY = 'G6'
jwt = JWTManager(app)

client = MongoClient('localhost', 27017)
userDB = client['user'] # 회원 db (관리자 사용자 싹 다 하나로 구분없이 모을게요!)
usercol = userDB['users'] # 회원 users column

playerDB = client['player'] # 축구선수 db
playercol = playerDB['players'] # 축구선수 column


SECRET_KEY = 'G6'


# << GET : 메인페이지('/') >>  
# 메인페이지 : ❗️로그인 한 role이 admin!!!!!!!
@app.route('/', methods = ['GET']) # 라우팅 
# @jwt_required() # jwt가 필요하다~ 
def print_hello(): # callback함수 
    # 사용자 전용...! 
    # cur_user = get_jwt_identity()
    # if cur_user is None:
    #     return "USER ONLY"
    # else:
    #     return "Hi" + cur_user
    result = playercol.find({}, {"_id" : 0})
    # dic = json.loads(result)
    # print(dic)
    arr = []
    for x in result:
        arr.append(x)

    # 그냥 쉽게 생각하지 그랬어...... 하
    return render_template('index.html', playerArr = arr)





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

    # 저장하기 전에 hash로 단방향 암호화해서 저장한다! 
    # 로그인 할 때 bcrypt로 해석해서 로그인! 
    pw_hash = hashlib.sha256(user_pw.encode('utf-8')).hexdigest()

    user = { # user 객체 
        'userID' : user_id,
        'userPW' : pw_hash,
        'userRole' : user_role,
    }
    # 중복검사! 
    arr = []
    for x in usercol.find({'userID' : user_id}):
        arr.append(x)

    if len(arr) >= 1:
        return "중복된 id가 있습니다...!"
    else:
        usercol.insert_one(user) #insert_many 사용하면 한 번에..! 
        return redirect(url_for('login_page'))


# 선수 등록 : ❗️로그인 한 role이 admin!!!!!!!
@app.route('/player', methods = ['POST'])
def player_register():
    player_id = request.form['player_id']
    player_name = request.form['player_name']
    player_team = request.form['player_team']
    player_back_number = request.form['player_back_number']
    player_position = request.form['player_position']
    player_age = request.form['player_age']

    player = {
        'player_id' : player_id,
        'player_name' : player_name,
        'player_team' : player_team,
        'player_back_number' : player_back_number,
        'player_position' : player_position,
        'player_age' : player_age
    }

    playerArr = []
    for x in playercol.find({'player_id' : player_id}):
        player.append(x)

    if len(playerArr) >= 1:
        return "중복된 선수 id가 있습니다...!"
    else:
        playercol.insert_one(player)
        return redirect(url_for('print_hello'))
    

@app.route('/login/index', methods = ['GET'])
def login_page():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# 로그인을 하고 jwt를 발급받는 코드!!!!!! 
# ❗️access token 생성해야함❗️
@app.route('/api/login', methods = ['POST'])
def login_proc():
    # return "Dwdawdawdawdawdawd"
    
    input_data = request.form
    # 입력한 id와 pw를 받아옴!
    userID = input_data['userID']
    userPW = input_data['userPW']
    # 똑같이 암호화! 한 후 암호화 돼 있는 db속 비번과 비교한다.
    pw_hash = hashlib.sha256(userPW.encode('utf-8')).hexdigest()

    # 암호화 한 후 찾아주기 
    result = usercol.find_one({ 'userID' : userID, 'userPW' : pw_hash }, {'_id' : 0})
    # 🔴 저렇게 찾아주자...! 
    # mongodb에 있는 _id 는 ObjectID이거 출력하지 맣자.. => error
    # {}면 
    # None 처리 방법!!!!! 
    if result is not None:
        role_receive = result['userRole']
        payload = {
            'id': userID,
            'role' : role_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10000)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'role': role_receive,'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 일단 관리자는 이따가..













# argument of type 'NoneType' is not iterable : 객체에서 얻어오는 과정에서 나오는 error
# None은 아무것도 return하지 않음..! 
# result is not None로 해주니까 처리가 됨! 

# id pw 비교작업이 끝난 로그인 할 때
# ❗️missing authorization header flask❗️


# 'JWTManager' object has no attribute 'encode'

# 이유없이 안 뜸... 


# Object of type Cursor is not JSON serializable
# result = playercol.find({}, {"_id" : 0})
    # return jsonify(list(result))
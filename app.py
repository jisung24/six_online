from flask import Flask, render_template, request, redirect, json ,url_for, flash, jsonify, session, make_response # flask를 불러옴 

# flask : flask연결 
# render_template : 템플릿 엔진 페이지 띄워줌 
# request : 데이터 처리 객체 담당! 
 
from pymongo import MongoClient
from flask_jwt_extended import *
import jwt
import datetime
import hashlib

app = Flask(__name__) # flask를 실행 

JWT_SECRET_KEY = 'G6'

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
    try:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)  
        result = playercol.find({}, {"_id" : 0})
    # dic = json.loads(result)
    # print(dic)
        arr = []
        for x in result:
            arr.append(x)

    # 그냥 쉽게 생각하지 그랬어...... 하
        return render_template('index.html', playerArr = arr)
    except jwt.ExpiredSignatureError:
        return redirect("http://localhost:5000/")
    except jwt.exceptions.DecodeError:
        return redirect("http://localhost:5000/")





@app.route('/register/index', methods = ['GET'])
def player_register_page():
    return render_template('register.html')


# << GET : 회원가입 페이지('/sign-up/index') >> 
@app.route('/sign-up/index', methods = ['GET'])
def sign_up_page():
    return render_template('signUp.html')

# 🔴 회원가입 🔴 로직처리('/api/new') >> 
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
        'userLikes' : []
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


# 🔴 선수 등록 🔴 : ❗️로그인 한 role이 admin!!!!!!!
@app.route('/player', methods = ['POST'])
def player_register():
    player_id = request.form['player_id']
    player_photo = request.form['player_photo']
    player_name = request.form['player_name']
    player_team = request.form['player_team']
    player_back_number = request.form['player_back_number']
    player_position = request.form['player_position']
    player_age = request.form['player_age']

    player = {
        'player_id' : player_id,
        'player_photo' : player_photo, # 문자열 
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
    


# 로그인 페이지 
@app.route('/login/index', methods = ['GET'])
def login_page():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

# 로그인을 하고 jwt를 발급받는 코드!!!!!! 
# ❗️access token 생성해야함❗️
@app.route('/api/login', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['userID']
    password_receive = request.form['userPW']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = usercol.find_one({'userID': username_receive, 'userPW': pw_hash})

    if result is not None: # result 찾았음 
        print(f"result >> {result}") # user 찾아짐! 
        payload = {
            'userID': username_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    # ❗️찾는 거, 찾지 못 하는 거 돌아가긴 해!❗️
    else:
        return jsonify({'result' : 'fail'})
# 일단 관리자는 이따가..



# 🔴 선수 검색 🔴
# /players ? player_name = "dwadaw"
# 즉, url에 파라미터와 값을 함께 전달하는 형식 
# 글자 부분으로 입력하면 바로 값 return해줌 
@app.route('/players', methods=['GET'])
def search_result():
    search = request.args.get('player_name') # player_name받아옴 
    # db에서 검색어가 들어간 것 찾기...! 
    find_player_name = playercol.find({'$or' : [{ 'player_name' : {'$regex' : search}}]},{'_id' : 0})
    player_arr = []
    for x in find_player_name:
        player_arr.append(x)
    return render_template('index.html', playerArr = player_arr)








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


# flask run이 갑자기 안 됨 => 에러 메시지도 안 뜸!
# 다 끄고 다시 켜니까 됐음 
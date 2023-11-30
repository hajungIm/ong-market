from flask import Flask, render_template, request, flash, redirect, url_for, session, json, escape, jsonify

from database import DBhandler
import hashlib
import uuid
import math
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

import sys

application = Flask(__name__)
application.config["SECRET_KEY"]="helloosp"
application.config.from_object(config)

DB = DBhandler()

@application.route("/")
def hello():
    #return render_template("index.html")
    return redirect(url_for('view_list'))

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('hello'))

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['password']
    pw_hash=hashlib.sha256(pw.encode('utf-8')).hexdigest()
    user_name = DB.find_user(id_, pw_hash)
    if user_name:
        session['id']=id_
        session['name']=user_name
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")
    
@application.route("/reset_password", methods=['POST'])
def reset_password():
    data = request.get_json()
    user_id = data['user_id']
    new_password = data['new_password']
    
    success = DB.update_password(user_id, new_password)
    return jsonify(success=success)

@application.route("/mem_register")
def mem_register():
    return render_template("mem_register.html")

@application.route("/id_check", methods=['POST'])
def id_check():
    data = request.get_json()
    user_id = data['user_id']

    is_duplicate = DB.user_duplicate_check(user_id)
    return jsonify(success=is_duplicate)

@application.route("/mem_register_final")
def mem_register_final():
    return render_template("mem_register_final.html")

@application.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    validateNum = data.get('validateNum')
    email = data.get('email')
    
    send_email_function(validateNum, email)
    
    return jsonify({"message": "Email sent successfully"})

def send_email_function(content, receiver_email):
    sender_email = config.SENDER_EMAIL
    sender_email_password = config.EMAIL_PASSWORD
    
    message = MIMEMultipart()
    message["From"] = "Ong-market Service"
    message["To"] = receiver_email
    message["Subject"] = "ong market service email"
    
    email_body = f"""
    <html>
        <body>
            <div style="font-family: Arial, sans-serif; font-size: 14px;">
                <p>옹 마켓 가입 인증번호는</p>
                <h1><i>{content}</i></h1>
                <p>입니다.</p>
                <br>
                <p>감사합니다.</p>
                <p>Ong-market Service Team</p>
            </div>
        </body>
    </html>
    """

    # HTML 본문을 MIMEText 객체로 생성
    body = MIMEText(email_body, "html")
    message.attach(body)
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['password']
    pw_hash=hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data,pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("mem_register.html")
@application.route("/list")
def view_list():
    page = request.args.get("page", 1, type=int)
    selected_option = request.args.get("select_place", "all")
    per_page=5
    start_idx=per_page* (page - 1)
    end_idx=start_idx+per_page
    
    print(f"선택 된 장소값: {selected_option}")
    
    switcher = {
        'non': '비대면',
        'all': '모두',
        'mainGate': '정문',
        'ecc': 'ECC',
        'art': '조형예술관',
        'asan': '아산공학관',
        'newEng': '신공학관',
        'edu': '교육관',
        'library': '중앙도서관',
        'eHouse': '기숙사(E-house)',
        'iHouse': '기숙사(I-house)',
        'science': '종합과학관',
        'posco': '포스코관',
        'student': '학관',
    }
    
    if selected_option == "non":
        data = DB.get_items_bytransaction("비대면 (택배, 우편)")  # read the table
    elif selected_option == "all":
        data = DB.get_items_bytransaction("대면")
    else:
        data = DB.get_items_bylocation(selected_option)

    category = switcher.get(selected_option)
        
    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))

    # OrderedDict의 키 리스트 생성
    data_keys = list(data.keys())

    # 데이터가 없거나 비어있는 경우 처리
    # if not data_keys:
    #     return render_template("list.html", datas=[], page=page, chat_room_ids=[], page_count=0, total=0, like_items = [], select_place=category)
    
    item_counts = len(data_keys)
    data_slice_keys = data_keys[start_idx:end_idx]

    # 슬라이스된 키를 사용하여 데이터 추출
    data_slice = [data[key] for key in data_slice_keys] or []

    # 각 행에 대한 데이터 딕셔너리 생성
    rows = [{'data_{}'.format(i): item} for i, item in enumerate(data_slice, start=start_idx)]

    page_count = math.ceil(item_counts / per_page)

    #찜한 목록 FE로 넘기기
    user_id = session.get('id')
    if user_id is None:
        user_id="no session"

    like_items = DB.get_like_items(user_id) or []
    
    user_key, user_data = DB.find_user_by_id(user_id)
    chat_rooms_data = DB.get_chat_rooms_for_user(user_id)  or []
    
    chat_room_ids = [chat_room['chatRoomId'] for chat_room in chat_rooms_data]

    return render_template("list.html", user_id=user_id, datas=data_slice, user_key=user_key, chat_room_ids=chat_room_ids, rows=rows, page=page, page_count=page_count, total=item_counts, like_items = like_items,
        select_place=category, selected_option = selected_option)

    return render_template("list.html", datas=data_slice, rows=rows, page=page, page_count=page_count, total=item_counts, like_items = like_items)


@application.route("/review_list")
def review_list():
    # 현재 로그인한 사용자의 ID를 얻어옵니다.
    user_id = session.get('id')

    # 사용자 ID를 기반으로 리뷰를 가져옵니다.
    data = DB.get_reviews(user_id)

    page = request.args.get("page", 1, type=int)
    per_page = 5
    start_idx = per_page * (page - 1)
    end_idx = start_idx + per_page
    
    data_keys = []

    if data is not None:
        data_keys = list(data.keys())
        # 'data_keys'를 사용한 코드 계속 진행
    else:
        # 'data'가 None인 경우를 처리합니다.
        print("Data가 None입니다. 이 경우를 적절히 처리하세요.")

    # 데이터가 없거나 비어있는 경우 처리
    if not data_keys:
        return render_template("review_list.html", datas=[], page=page, page_count=0, total=0)

    item_counts = len(data_keys)
    data_slice_keys = data_keys[start_idx:end_idx]

    # 슬라이스된 키를 사용하여 데이터 추출
    data_slice = [data[key] for key in data_slice_keys]

    # 각 행에 대한 데이터 딕셔너리 생성
    rows = [{'data_{}'.format(i): item} for i, item in enumerate(data_slice, start=start_idx)]

    page_count = math.ceil(item_counts / per_page)

    return render_template("review_list.html", datas=data_slice, rows=rows, page=page, page_count=page_count, total=item_counts)


@application.route("/reg_item")
def reg_item():
    return render_template("reg_item.html")

# @application.route("/reg_review")
# def reg_review():
#     return render_template("reg_review.html")


@application.route("/reg_review/<itemId>")
def reg_review_init(itemId):
    item = DB.find_item_by_id(itemId)
    return render_template("reg_review.html", data=item)

@application.route("/submit_review_post/<itemId>", methods=['POST'])
def submit_review(itemId):
    user_id = session.get("id")
    item = DB.find_item_by_id(itemId)
    createdAt=request.args.get("reviewRegDate")
    reviewId = itemId
    
    image_file=request.files["itemImg"]
    file_extension = image_file.filename.rsplit('.',1)[1].lower()
    image_file_path = "images/regReview/{}.{}".format(reviewId, file_extension)
    save_path = "static/" + image_file_path
    image_file.save(save_path)

    reviewform=request.form
    DB.insert_review(reviewId, reviewform, image_file_path, user_id)
    
    review = DB.find_review_by_id(reviewId)
    
    return render_template("review_detail.html", data = item, reviewdata = review)

@application.route("/mypage")
def my_page():
    user_id = session.get('id')
    if user_id is None:
        # 사용자 ID가 세션에 없는 경우, 로그인 페이지나 오류 페이지로 리디렉트
        return redirect(url_for('login'))

    user_info = DB.get_user_info(user_id)
    

    #채팅 알람을 위한 데이터
    user_key, user_data = DB.find_user_by_id(user_id)
    chat_rooms_data = DB.get_chat_rooms_for_user(user_id)  or []
    
    chat_room_ids = [chat_room['chatRoomId'] for chat_room in chat_rooms_data]

    return render_template("mypage.html", user_info=user_info, user_key=user_key, chat_room_ids=chat_room_ids)

@application.route("/update_password", methods=["POST"])
def update_password():
    try:
        # 세션에서 사용자 ID 가져오기
        user_id = session.get("id")
        if not user_id:
            return jsonify({"message": "세션이 만료되었습니다. 다시 로그인해주세요."}), 401

        # 새로운 비밀번호 가져오기
        data = request.get_json()
        new_password = data.get('newPassword')

        # 사용자의 비밀번호 업데이트
        if DB.update_password(user_id, new_password):
            return jsonify({"success": True, "message": "비밀번호 변경이 완료되었습니다."}), 200
        else:
            return jsonify({"success": False, "message": "비밀번호 업데이트에 실패했습니다."}), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"비밀번호 변경 중 오류 발생: {str(e)}"}), 500


@application.route("/dm_to_seller", methods=['POST'])
def dm_to_seller():
    if request.method == 'POST':
        seller_id = request.form.get('sellerId')
        buyer_id = request.form.get('buyerId')
        item_data = json.loads(request.form.get('itemData', '{}'))
        seller_img = DB.get_user_Img(seller_id)
        buyer_img = DB.get_user_Img(buyer_id)
    
        chat_room = DB.get_chat_room(item_data, seller_id, seller_img, buyer_id, buyer_img)
    
        return render_template("dm.html", chat_room=chat_room, counterpartId=seller_id, counterpartImg=seller_img)

@application.route("/dm")
def dm():
    return render_template("dm.html")

@application.route('/send_msg', methods=['POST'])
def send_msg():
    data = request.json
    message = data.get('message')
    chat_room_id = data.get('chatRoomId')
    sender_id = data.get('senderId')
    timestamp = data.get('timestamp')

    DB.save_msg(chat_room_id, message, sender_id, timestamp)
    
    return jsonify({'status': 'success', 'message': '메시지 전송됨'}), 200

@application.route("/submit_item")
def reg_item_submit():
    createdAt=request.args.get("itemRegDate")
    userId=request.args.get("userId")
    itemName=request.args.get("itemName")
    price=price.args.get("price")
    status=status.args.get("status")
    description=status.args.get("description")
    transaction=status.args.get("transaction")
    location=status.args.get("location")

    
    print(createdAt, userId, itemName, price, status, description, transaction, location)
    return render_template("")

@application.route("/map")
def map():
    location_id = request.args.get('locationId')
    data = DB.find_location(location_id)
    return render_template("map.html", data=data)

#사용자가 등록한 상품 이미지는 images 폴더 아래에 있는 regItem에 들어가도록 경로 설정
@application.route("/reg_item_post", methods=['POST'])
def reg_item_submit_post():
    # item_id.txt 를 참고하여 아이템 고유 아이디 생성, 초기화 값 = -1
    item_id_path = 'item_id.txt'
    if os.path.exists(item_id_path):
        with open(item_id_path, 'r') as file:
            last_id = int(file.read().strip())
    else:
        last_id = 0

    current_id = last_id + 1

    with open(item_id_path, 'w') as file:
        file.write(str(current_id))

    image_file=request.files["itemImg"]
    file_extension = image_file.filename.rsplit('.',1)[1].lower()
    image_file_path = "images/regItem/{}.{}".format(current_id, file_extension)
    save_path = "static/" + image_file_path
    image_file.save(save_path)
    
    
    data=request.form 
    DB.insert_item(current_id, data, image_file_path)
    return redirect(url_for('item_detail', itemId=current_id))

@application.route("/find_id", methods = ['GET', 'POST'])
def find_id():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        
        user = DB.find_user_by_email(email)
        
        if user:
            session['find_user_email'] = email
            session['find_user_id'] = user.get('id')
            return jsonify(success=True)
        else:
            return jsonify(success=False)
    
    return render_template("find_id.html")

@application.route("/find_id_success")
def find_id_success():
    email = session.pop('find_user_email', None)
    user_id = session.pop('find_user_id', None)
    return render_template("find_id_success.html", user_email=email, user_id=user_id)

@application.route("/find_id_fail")
def find_id_fail():
    return render_template("find_id_fail.html")

@application.route("/find_password", methods = ['GET', 'POST'])
def find_password():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data['user_id']
        email = data['email']
        
        user = DB.find_user_by_email(email)

        if user and (user_id == user.get('id')):
            return jsonify(success=True)
        return jsonify(success=False)
        
    return render_template("find_password.html")

@application.route("/find_password_success")
def find_password_success():
    return render_template("find_password_success.html")

@application.route("/find_password_fail")
def find_password_fail():
    return render_template("find_password_fail.html")

@application.route("/item_detail/<itemId>")
def item_detail(itemId):
    item = DB.find_item_by_id(itemId)
    user_id = session.get("id")
    
    if not item:
        return "Item not found", 404
    
    item_data_json = escape(json.dumps(item))
    item_json = json.dumps(item)

    like_items = DB.get_like_items(user_id)
    like_items = sorted(like_items, key=lambda x: x['createdAt'], reverse=True)
    
    return render_template("item_detail.html", data=item, item_data_json=item_data_json, userId=user_id, like_items=like_items)

@application.route("/review_detail/<reviewId>")
def review_detail(reviewId):
    item_review = DB.find_review_by_id(reviewId)
    item = DB.find_item_by_id(reviewId)

    if not item:
        return "Item not found", 404

    return render_template("review_detail.html", data=item, reviewdata=item_review)

@application.route("/student_check")
def student_check():
    return render_template("student_check.html")

@application.route("/student_check_fail")
def student_check_fail():
    return render_template("student_check_fail.html")


@application.route("/sell_Page")
def sellPage():
    user_id = session.get("id")
    
    sold_items = DB.get_sales_items(user_id, '1')
    
    return render_template("sell_Page.html", sold_items=sold_items)


@application.route("/selling")
def sellingPage():
    user_id = session.get("id")
    
    selling_items = DB.get_sales_items(user_id, '0')
    
    return render_template("sell_Page_selling.html", selling_items=selling_items)

@application.route("/like")
def likePage():
    user_id = session.get('id')
    if user_id is None:
        # 사용자 ID가 세션에 없는 경우, 로그인 페이지나 오류 페이지로 리디렉트
        return redirect(url_for('login'))
    
    like_items = DB.get_like_items(user_id)
    like_items = sorted(like_items, key=lambda x: x['createdAt'], reverse=True)

    #채팅 알람을 위한 데이터
    user_key, user_data = DB.find_user_by_id(user_id)
    chat_rooms_data = DB.get_chat_rooms_for_user(user_id)  or []
    
    chat_room_ids = [chat_room['chatRoomId'] for chat_room in chat_rooms_data]
    return render_template("jjim_Page.html", like_items=like_items, user_key=user_key, chat_room_ids=chat_room_ids)

@application.route("/like/<item_id>", methods=['POST'])
def update_like(item_id):
    data = request.json
    flag = data.get('flag')
    user_id = session.get('id')
    
    item = DB.find_item_by_id(item_id)
    DB.update_like_to_item(item, flag)
    DB.update_like_to_user(user_id, item, flag)
    if(flag==1):
        return jsonify({"status": "success", "message": "like plus update complete"})
    
    if(flag==-1):
        return jsonify({"status": "success", "message": "like minus update complete"})
    

@application.route("/user_Page")
def userPage():
    user_id = session.get("id")
    if user_id:
        # 세션에 저장된 사용자 ID를 사용하여 사용자 정보 가져오기
        user_info = DB.get_user_info(user_id)
    return render_template("user_Page.html", user_info=user_info)

@application.route('/update_profile_image', methods=['POST'])
def update_profile_image():
    if 'profileImg' not in request.files:
        return redirect(request.url)
    image_file = request.files['profileImg']
    if image_file.filename == '':
        return redirect(request.url)
    
    user_id = session.get("id")
    
    file_extension = image_file.filename.rsplit('.',1)[1].lower()
    image_file_path = "images/profile/{}.{}".format(user_id, file_extension)
    save_path = "static/" + image_file_path
    image_file.save(save_path)
    
    DB.update_profile_image(user_id, image_file_path)
    DB.update_chats_profile_image(user_id, image_file_path)
    return jsonify(success=True)

@application.route("/chatting_list")
def chattingListPage():
    user_id = session.get('id')
    if user_id is None:
        # 사용자 ID가 세션에 없는 경우, 로그인 페이지나 오류 페이지로 리디렉트
        return redirect(url_for('login'))
    
    session['newChat'] = False
    
    chat_rooms = DB.get_chat_rooms_for_user(user_id)
    chat_rooms = sorted(chat_rooms, key=lambda x: x['lastTimestamp'], reverse=True)
    
    #채팅 알람을 위해 추가한 데이터
    user_key, user_data = DB.find_user_by_id(user_id)
    chat_rooms_data = DB.get_chat_rooms_for_user(user_id)  or []
    chat_room_ids = [chat_room['chatRoomId'] for chat_room in chat_rooms_data]
    return render_template("chatting_list.html", chat_rooms=chat_rooms, user_key=user_key, chat_room_ids=chat_room_ids)

@application.route("/chat_room/<chat_room_id>")
def chat_room_page(chat_room_id):
    chat_room_data = DB.get_chat_room_data(chat_room_id)
    
    if chat_room_data['sellerId'] == session['id']:
        counterpartId = chat_room_data['buyerId']
        counterpartImg = chat_room_data['buyerImg']
    else:
        counterpartId = chat_room_data['sellerId']
        counterpartImg = chat_room_data['sellerImg']
    
    itemID = chat_room_data['itemId']
    review_complete = DB.get_review_status_by_id(itemID)
    
    return render_template('dm.html', chat_room=chat_room_data, counterpartId=counterpartId, counterpartImg=counterpartImg, rc= review_complete)

@application.route('/complete/<chat_room_id>', methods=['POST'])
def complete_chat_room(chat_room_id):
    DB.mark_chat_room_as_complete(chat_room_id)
    return jsonify({"status": "success", "message": "Chat room marked as complete"})

@application.route('/notify_new_chat', methods=['POST'])
def notify_new_chat_room():
    session['newChat'] = True
    return jsonify(success=True)

@application.route("/keyword")
def keywordPage():
    # 세션에서 사용자 정보 가져오기
    user_id = session.get("id")
    if user_id:
        # 세션에 저장된 사용자 ID를 사용하여 사용자 정보 가져오기
        user_info = DB.get_user_info(user_id)
    return render_template("keyword.html", user_info=user_info)

@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("item_detail.html", name=name, data=data)

@application.route("/error400")
def error400():
    return render_template("error_400.html")

@application.route("/error401")
def error401():
    return render_template("error_401.html")

@application.route("/error403")
def error403():
    return render_template("error_403.html")

@application.route("/error404")
def error404():
    return render_template("error_404.html")

@application.route("/error500")
def error500():
    return render_template("error_500.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)

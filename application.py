from flask import Flask, render_template, request, flash, redirect, url_for, session, json, escape, jsonify

from database import DBhandler
import hashlib
import uuid
import math
import os

import sys

application = Flask(__name__)
application.config["SECRET_KEY"]="helloosp"

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
    
def find_user(self, id_, pw_):
    users = self.db.child("user").get()
    target_value=[]
    for res in users.each():
        value = res.val()
        if value['id'] == id_ and value['pw'] == pw_:
            return True
    return False

@application.route("/mem_register")
def mem_register():
    return render_template("mem_register.html")

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
    per_page=5
    start_idx=per_page* (page - 1)
    end_idx=start_idx+per_page
     
    data = DB.get_items()

    # OrderedDict의 키 리스트 생성
    data_keys = list(data.keys())

    # 데이터가 없거나 비어있는 경우 처리
    if not data_keys:
        return render_template("list.html", datas=[], page=page, page_count=0, total=0)
    
    item_counts = len(data_keys)
    data_slice_keys = data_keys[start_idx:end_idx]

    # 슬라이스된 키를 사용하여 데이터 추출
    data_slice = [data[key] for key in data_slice_keys]

    # 각 행에 대한 데이터 딕셔너리 생성
    rows = [{'data_{}'.format(i): item} for i, item in enumerate(data_slice, start=start_idx)]

    page_count = math.ceil(item_counts / per_page)

    return render_template("list.html", datas=data_slice, rows=rows, page=page, page_count=page_count, total=item_counts)

@application.route("/review_list")
def review_list():
    return render_template("review_list.html")


@application.route("/reg_item")
def reg_item():
    return render_template("reg_item.html")

@application.route("/reg_review")
def reg_review():
    return render_template("reg_review.html")

@application.route("/mypage")
def my_page():
    user_id = session.get('id')
    if user_id is None:
        # 사용자 ID가 세션에 없는 경우, 로그인 페이지나 오류 페이지로 리디렉트
        return redirect(url_for('login'))

    user_info = DB.get_user_info(user_id)
    return render_template("mypage.html", user_info=user_info)

# 임시로 만든 비밀번호 변경하는 엔드포인트입니다.
# 프론트에서 POST 요청으로 새로운 비밀번호를 받아 처리.
# 처리 결과를 프론트로 응답해야 함.
@application.route("/change_password", methods=["POST"])
def change_password():
    try:
        # 세션에서 사용자 ID 가져오기
        user_id = session.get("id")
        if not user_id:
            return jsonify({"message": "세션이 만료되었습니다. 다시 로그인해주세요."}), 401

        # 새로운 비밀번호 가져오기
        new_password = request.json.get("newPassword")

        # firebase 비밀번호 변경 로직
        
        #비밀번호 변경 성공
        return jsonify({"message": "비밀번호 변경이 완료되었습니다."}), 200

    #오류 발생
    except Exception as e:
        return jsonify({"message": f"비밀번호 변경 중 오류 발생: {str(e)}"}), 500


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
    return render_template("result.html", data=data, img_path=save_path)



@application.route("/find_id")
def find_id():
    return render_template("find_id.html")

@application.route("/find_id_success")
def find_id_success():
    return render_template("find_id_success.html")

@application.route("/find_id_fail")
def find_id_fail():
    return render_template("find_id_fail.html")

@application.route("/find_password")
def find_password():
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
    
    if not item:
        return "Item not found", 404
    
    item_data_json = escape(json.dumps(item))
    
    return render_template("item_detail.html", data=item, item_data_json=item_data_json)

@application.route("/review_detail")
def review_detail():
    return render_template("review_detail.html")

@application.route("/student_check")
def student_check():
    return render_template("student_check.html")

@application.route("/student_check_fail")
def student_check_fail():
    return render_template("student_check_fail.html")


@application.route("/sell_Page")
def sellPage():
    return render_template("sell_Page.html")


@application.route("/selling")
def sellingPage():
    return render_template("sell_Page_selling.html")

@application.route("/like")
def likePage():
    return render_template("jjim_Page.html")

@application.route("/user_Page")
def userPage():
     # 세션에서 사용자 정보 가져오기
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
    
    chat_rooms = DB.get_chat_rooms_for_user(user_id)
    chat_rooms = sorted(chat_rooms, key=lambda x: x['lastTimestamp'], reverse=True)
    return render_template("chatting_list.html", chat_rooms=chat_rooms)

@application.route("/chat_room/<chat_room_id>")
def chat_room_page(chat_room_id):
    chat_room_data = DB.get_chat_room_data(chat_room_id)
    
    if chat_room_data['sellerId'] == session['id']:
        counterpartId = chat_room_data['buyerId']
        counterpartImg = chat_room_data['buyerImg']
    else:
        counterpartId = chat_room_data['sellerId']
        counterpartImg = chat_room_data['sellerImg']
    
    return render_template('dm.html', chat_room=chat_room_data, counterpartId=counterpartId, counterpartImg=counterpartImg)

@application.route('/complete/<chat_room_id>', methods=['POST'])
def complete_chat_room(chat_room_id):
    DB.mark_chat_room_as_complete(chat_room_id)
    return jsonify({"status": "success", "message": "Chat room marked as complete"})

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
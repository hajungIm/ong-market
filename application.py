from flask import Flask, render_template, request, flash, redirect, url_for, session, json, escape
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
    return render_template("mypage.html")

@application.route("/dm_to_seller", methods=['GET', 'POST'])
def dm_to_seller():
    if request.method == 'POST':
        seller_id = request.form.get('sellerId')
        buyer_id = request.form.get('buyerId')
        item_data = json.loads(request.form.get('itemData', '{}'))
    
        chat_room = DB.get_chat_room(item_data, seller_id, buyer_id)
    
        return render_template("dm.html", counterpartId=seller_id, chat_room=chat_room)


@application.route("/submit_item")
def reg_item_submit():
    userId=request.args.get("userId")
    itemName=request.args.get("itemName")
    price=price.args.get("price")
    status=status.args.get("status")
    description=status.args.get("description")
    transaction=status.args.get("transaction")
    location=status.args.get("location")
    
    print(userId, itemName, price, status, description, transaction, location)
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

@application.route("/mypage")
def mypage():
    return render_template("mypage.html")

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
    return render_template("user_Page.html")

@application.route("/chatting_list")
def chattingListPage():
    return render_template("chatting_list.html")

@application.route("/keyword")
def keywordPage():
    return render_template("keyword.html")

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
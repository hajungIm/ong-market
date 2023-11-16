from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import uuid

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
    if DB.find_user(id_, pw_hash):
        session['id']=id_
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
    page = request.args.get("page", 0, type=int)
    per_page=5
    per_row=1
    row_count = int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)

    data = DB.get_items()
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    
    for i in range(row_count):#last row 
        locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])       

    return render_template("list.html", datas=data.items(),
                           row1=locals()['data_0'].items(), row2=locals()['data_1'].items(), row3=locals()['data_2'].items(), row4=locals()['data_3'].items(), row5=locals()['data_4'].items(),
                           limit=per_page, page=page+1, page_count=int((item_counts/per_page)+1),
                           total=item_counts)

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

@application.route("/dm")
def dm():
    return render_template("dm.html")


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
    # 고유 UUID 생성
    unique_id = str(uuid.uuid4())
    
    image_file=request.files["itemImg"]
    file_extension = image_file.filename.rsplit('.',1)[1].lower()
    image_file_path = "images/regItem/{}.{}".format(unique_id, file_extension)
    save_path = "static/" + image_file_path
    image_file.save(save_path)

    data=request.form 
    DB.insert_item(unique_id, data, image_file_path)
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

@application.route("/item_detail")
def item_detail():
    return render_template("item_detail.html")

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
           
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
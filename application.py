from flask import Flask, render_template, request

application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/list")
def view_list():
    return render_template("list.html")

@application.route("/reg_item")
def reg_item():
    return render_template("reg_item.html")

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

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    data=request.form
    return render_template("result.html", data=data)

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

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/mem_register")
def mem_register():
    return render_template("mem_register.html")

@application.route("/review_detail")
def review_detail():
    return render_template("review_detail.html")

@application.route("/student_check")
def student_check():
    return render_template("student_check.html")

@application.route("/student_check_fail")
def student_check_fail():
    return render_template("student_check_fail.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
    

from flask import Flask, render_template, request

application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("first_page.html")

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
    
    

from flask import Flask, render_template, request

application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/find_id")
def view_list():
    return render_template("find_id.html")

@application.route("/find_id_success")
def view_list():
    return render_template("find_id_success.html")

@application.route("/find_id_fail")
def view_list():
    return render_template("find_id_fail.html")

@application.route("/find_password")
def view_list():
    return render_template("find_password.html")

@application.route("/find_password_success")
def view_list():
    return render_template("find_password_success.html")

@application.route("/find_password_fail")
def view_list():
    return render_template("find_password_fail.html")

@application.route("/item_detail")
def view_list():
    return render_template("item_detail.html")

@application.route("/login")
def view_list():
    return render_template("login.html")

@application.route("/mem_register")
def view_list():
    return render_template("mem_register.html")

@application.route("/review_detail")
def view_list():
    return render_template("review_detail.html")

@application.route("/student_check")
def view_list():
    return render_template("student_check.html")

@application.route("/student_check_fail")
def view_list():
    return render_template("student_check_fail.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
    

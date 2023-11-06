from flask import Flask, render_template, request
import sys
application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/list")
def view_list():
    return render_template("list.html")

@application.route("/list_review")
def list_review():
    return render_template("list_review.html")


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

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    data=request.form
    return render_template("result.html", data=data)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
    
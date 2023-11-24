import pyrebase
import json
from datetime import datetime

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def insert_user(self, data, pw):
        default_profile_image = "static/images/profile/default_profile_image.png" # 디폴트 프로필 이미지 경로
        user_info={
            "id": data['id'],
            "pw": pw,
            "name": data['name'],
            "profile_image":default_profile_image
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False

    def user_duplicate_check(self, id_string):
        users=self.db.child("user").get()
        print("users###", users.val())
        if str(users.val()) == "None":
            return True
        else:
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return False
            return True

    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value = []
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return value['name']
        return False
    
    def get_user_info(self, id_):
        users = self.db.child("user").get()
        for res in users.each():
            value = res.val()
            if value['id'] == id_:
                return {
                    "id": value['id'],
                    "name": value['name'],
                    "profile_image": value['profile_image'],
                    # 다른 필요한 사용자 정보...
                }
        return None

    def insert_item(self, current_id, data, img_path):
        current_time = datetime.utcnow().isoformat() + 'Z'

        item_info = {
                "itemId": current_id,
                "userId": data['userId'],
                "itemName": data['itemName'],
                "price": data['price'],
                "status": data['status'],
                "description": data['description'],
                "transaction": data['transaction'],
                "img_path": img_path,
                "like_count": 0,
                "createdAt": current_time
            }
        if data['transaction'] == "대면":
            item_info["location"] = data['location']

        self.db.child("item").child(current_id).set(item_info)
        print(data, img_path)
        return True

    def get_items(self):
        items = self.db.child("item").get().val()
        return items

    def get_item_by_name(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value=res.val()
        return target_value

    def find_item_by_id(self, itemId):
        item = self.db.child("item").child(itemId).get()
        if item.val():
            return item.val()
        else:
            return None

    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        return reviews

    def get_reviews_by_name(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value=res.val()
        return target_value

    def insert_review(self, review_id, data, review_img_path, userId):
        current_time = datetime.utcnow().isoformat() + 'Z'

        review_info = {
            # 리뷰 form 목록 설정하기
            "userId": userId,
            "title": data['reviewTitle'],
            "review_img_path": review_img_path,
            "review": data['reviewContent'],
            "createdAt": current_time,
            "rate": data['rating']
        }

        self.db.child("review").child(review_id).set(review_info)
        return True

    def find_review_by_id(self, reviewId):
        review = self.db.child("review").child(reviewId).get()
        if review.val():
            return review.val()
        else:
            return None
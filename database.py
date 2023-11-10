import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        
    def insert_user(self, data, pw):
        user_info={
            "id": data['id'],
            "pw": pw,
            "name": data['name']
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
        
    def insert_item(self, name, data, img_path):
        item_info = {
                "userId": data['userId'],
                "itemName": data['itemName'],
                "price": data['price'],
                "status": data['status'],
                "description": data['description'],
                "transaction": data['transaction'],
                "location": data['location'],
                "img_path": img_path
            }

        self.db.child("item").child(name).set(item_info) 
        print(data, img_path)
        return True
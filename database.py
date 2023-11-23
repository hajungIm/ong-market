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
        
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value = []
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return value['name']
        return False
        
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
    
    def get_chat_room(self, item_data, seller_id, buyer_id):
        chat_room_id = f"{seller_id}_{buyer_id}_{item_data['itemId']}"
        chat_room = self.db.child("chats").child(chat_room_id).get().val()
        
        if not chat_room:
            chat_room_info = {
                "sellerId": seller_id,
                "buyerId": buyer_id,
                "itemId": item_data.get('itemId', 'Unknwon Item'),
                "itemName": item_data.get('itemName', 'Unknwon Item'),
                "itemPrice": item_data.get('price', 'Unknwon Price'),
                "imgPath": item_data.get('img_path', 'no_image.png'),
                "messages": [],
                "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.db.child("chats").child(chat_room_id).set(chat_room_info)
            chat_room = chat_room_info
            
        return chat_room
    
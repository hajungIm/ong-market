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

    def get_chat_room(self, item_data, seller_id, buyer_id):
        chat_room_id = f"{seller_id}_{buyer_id}_{item_data['itemId']}"
        chat_room = self.db.child("chats").child(chat_room_id).get().val()
        
        if not chat_room:
            chat_room_info = {
                "chatRoomId": chat_room_id,
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
    
    def save_msg(self, chat_room_id, message, sender_id, timestamp):
        new_message = {
            "senderId": sender_id,
            "text": message,
            "timestamp": timestamp
        }
        
        self.db.child("chats").child(chat_room_id).child("messages").push(new_message)
        return True

    def get_chat_rooms_for_user(self, user_id):
        chat_rooms = []
        all_chats = self.db.child("chats").get().val()
        if all_chats:
            for chat_room_id, chat_room_data in all_chats.items():
                if chat_room_data.get('sellerId') == user_id or chat_room_data.get('buyerId') == user_id:
                    chat_rooms.append(chat_room_data)
        return chat_rooms
    
    def get_chat_room_data(self, chat_room_id):
        chat_room_data = self.db.child("chats").child(chat_room_id).get().val()
        return chat_room_data
    
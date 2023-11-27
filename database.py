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
        default_profile_image = "images/profile/default_profile_image.png" # 디폴트 프로필 이미지 경로
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
    
    def find_user_by_id(self, user_id):
        users = self.db.child("user").get()
        for user in users.each():
            user_data = user.val()
            if user_data['id'] == user_id:
                return user.key(), user_data
        return None, None
    
    def find_user_by_email(self, email):
        users = self.db.child("user").get()
        for user in users.each():
            user_data = user.val()
            if user_data['email'] == email:
                return user_data['email']
        return None
    
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
    
    def get_user_Img(self, user_id):
        user_key, user_data = self.find_user_by_id(user_id)
        if user_data:
            return user_data.get('profile_image')
        return None
        
    def insert_item(self, current_id, data, img_path):

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
                "createdAt": data['itemRegDate']
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

    def get_chat_room(self, item_data, seller_id, seller_img, buyer_id, buyer_img):
        chat_room_id = f"{seller_id}_{buyer_id}_{item_data['itemId']}"
        chat_room = self.db.child("chats").child(chat_room_id).get().val()
        
        if not chat_room:
            chat_room_info = {
                "chatRoomId": chat_room_id,
                "sellerId": seller_id,
                "sellerImg": seller_img,
                "buyerId": buyer_id,
                "buyerImg": buyer_img,
                "itemId": item_data.get('itemId', 'Unknwon Item'),
                "itemName": item_data.get('itemName', 'Unknwon Item'),
                "itemPrice": item_data.get('price', 'Unknwon Price'),
                "imgPath": item_data.get('img_path', 'no_image.png'),
                "messages": [],
                "lastMessageText": "",
                "lastTimestamp": ""
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
        
        last_message_update = {
            "lastMessageText": message,
            "lastTimestamp": timestamp
        }
        self.db.child("chats").child(chat_room_id).update(last_message_update)

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
    
    def mark_chat_room_as_complete(self, chat_room_id):
        complete_update = {"complete": True}
        self.db.child("chats").child(chat_room_id).update(complete_update)
    
    def update_profile_image(self, user_id, new_image):
        user_key, user_data = self.find_user_by_id(user_id)
        if user_data:
            self.db.child("user").child(user_key).update({"profile_image": new_image})
            return True
        return False
    
    def update_chats_profile_image(self, user_id, new_image):
        chat_rooms = self.get_chat_rooms_for_user(user_id)
        for chat_room in chat_rooms:
            chat_room_id = chat_room['chatRoomId']
            
            if chat_room['sellerId'] == user_id:
                self.db.child("chats").child(chat_room_id).update({'sellerImg': new_image})
            else:
                self.db.child("chats").child(chat_room_id).update({'buyerImg': new_image})
        return True
    
    def update_like_to_item(self, item, flag):
        new_like_count = item.get('like_count', 0) + flag
        self.db.child("item").child(item['itemId']).update({"like_count": new_like_count})
        return True
    
    def update_like_to_user(self, user_id, item, flag):
        user_key, user_data = self.find_user_by_id(user_id)
        if user_data:
            like_items = user_data.get('like_items', [])
                
            if flag == 1 and item['itemId'] not in like_items:
                like_items.append(item['itemId'])
            elif flag == -1 and item['itemId'] in like_items:
                like_items.remove(item['itemId'])
            
            self.db.child("user").child(user_key).update({"like_items": like_items})
            return True
    
    def get_like_items(self, user_id):
        user_key, user_data = self.find_user_by_id(user_id)
        if user_data and 'like_items' in user_data:
            like_items_ids = user_data['like_items']
            like_items_details = []
            
            for item_id in like_items_ids:
                item = self.find_item_by_id(item_id)
                if item:
                    like_items_details.append(item)
            
            return like_items_details
        
        return []
    
import pyrebase
import json
import hashlib
from datetime import datetime
import pytz
import logging

class DBhandler:
    def __init__(self):
        # 로그 설정
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def insert_user(self, data, pw):
        default_profile_image = "images/profile/default_profile_image.png" # 디폴트 프로필 이미지 경로
        
        keyword_stat =  [0, 0, 0, 0, 0, 0, 0, 0]
        
        user_info={
            "id": data['id'],
            "pw": pw,
            "name": data['name'],
            "profile_image":default_profile_image,
            "keyword_stat": keyword_stat,
            "keyword_count": 0,
            "email": data['email'],
            "grade": 2.5
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            return True
        else:
            return False
        
    def delete_user(self, user_id):
        # 사용자 데이터 가져오기
        user_key, user_data = self.find_user_by_id(user_id)

        if user_data:
            try:
                # 사용자의 채팅 기록 삭제
                chat_rooms = self.get_chat_rooms_for_user(user_id)
                for chat_room in chat_rooms:
                    chat_room_id = chat_room['chatRoomId']
                    self.db.child("chats").child(chat_room_id).remove()

                # 사용자 데이터 삭제
                self.db.child("user").child(user_key).remove()

                return True
            except Exception as e:
                # 에러 처리를 원하는 대로 추가
                print(f"회원 탈퇴 중 오류 발생: {str(e)}")
                return False
        else:
            return False
        
    
    def user_duplicate_check(self, id_string):
        users=self.db.child("user").get()
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
                return user_data
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
                    "keyword_stat": value['keyword_stat'],
                    "keyword_count": value['keyword_count'],
                    "email": value['email'],
                    "grade": value['grade']
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
                "createdAt": data['itemRegDate'],
                "review_complete": "0",
                "completed": "0"
            }
        if data['transaction'] == "대면":
            item_info["location"] = data['location']

        self.db.child("item").child(current_id).set(item_info)
        return True
    
    def get_items(self):
        items = self.db.child("item").get().val()
        return items
    
    def get_item_by_name(self, name):
        items = self.db.child("item").get()
        target_value=""
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
    
    def find_location(self, locationId):
        location_data = self.db.child("location").child(locationId).get()
        if location_data.val():
            return location_data.val()
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
                "lastTimestamp": "01/01/1970, 00:00:00",
                "transaction": item_data.get('transaction'),
                "location": item_data.get('location')
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
        # chat_room_id에 해당하는 노드가 존재하는지 확인
        if self.db.child("chats").child(chat_room_id).get().val() is not None:
            complete_update = {"complete": True}
            self.db.child("chats").child(chat_room_id).update(complete_update)

            # itemId를 가져올 때도 노드가 존재하는지 확인
            itemId = self.db.child("chats").child(chat_room_id).child('itemId').get().val()
            if itemId:
                self.db.child("item").child(itemId).update({"completed": "1"})
                return True
            else:
                return False
        else:
            return False
    
    def update_profile_image(self, user_id, new_image):
        user_key, user_data = self.find_user_by_id(user_id)
        if user_data:
            self.db.child("user").child(user_key).update({"profile_image": new_image})
            return True
        return False
    
    def update_password(self, user_id, new_password):
        user_key, user_data = self.find_user_by_id(user_id)
        
        pw_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

        if user_data:
            self.db.child("user").child(user_key).update({"pw": pw_hash})
            return True
        else:
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
    
    def get_sales_items(self, user_id, flag):
        items = self.db.child("item").get()
        
        selling_items = []
        
        for item in items.each():
            item_data = item.val()
            if item_data is not None:
                if item_data.get('userId') == user_id and item_data.get('completed') == flag:
                    selling_items.append(item.val())
        
        return selling_items

    def insert_review(self, review_id, data, review_img_path, userId):
        seoul_timezone = pytz.timezone('Asia/Seoul')
        current_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(seoul_timezone)
        formatted_time = current_time.strftime("%d/%m/%Y, %H:%M:%S")


        # userId : reviewer, sellerId: seller
        item = self.find_item_by_id(review_id)
        sellerId=item.get('userId')
        seller_key, seller_data = self.find_user_by_id(sellerId)
        keyword_stat = seller_data.get('keyword_stat', [0]*7)
        keyword_count = seller_data.get('keyword_count')
        price=item.get('price')
        itemName=item.get('itemName')

        if 'rating' not in data:
        # 'rating' 키가 없는 경우에 대한 처리
        # 여기서는 기본값으로 0을 사용하도록 가정
            rating_value = 0
        else:
            rating_value = data['rating']

        review_info = {
            # 리뷰 form 목록 설정하기
            "reviewId": review_id,
            "userId": userId,
            "title": data['reviewTitle'],
            "review_img_path": review_img_path,
            "review": data['reviewContent'],
            "createdAt": formatted_time,
            "rate": rating_value,
            "sellerId": sellerId,
            "price": price,
            "itemName": itemName,
        }

        keyword_values = [int(data.get(f'keywordSeller{i}', "0")) for i in range(1, 6)] + [int(data.get(f'keywordItem{i}', "0")) for i in range(1, 4)]

        review_info["keyword"] = keyword_values

        for i, value in enumerate(keyword_values):
            keyword_stat[i] += value

        keyword_count+=1

        self.db.child("item").child(review_id).update({"review_complete": "1"})
        self.db.child("review").child(review_id).set(review_info)
        self.db.child("user").child(seller_key).update({"keyword_count": keyword_count})
        self.db.child("user").child(seller_key).update({"keyword_stat": keyword_stat})
        return True

    def find_review_by_id(self, reviewId):
        review = self.db.child("review").child(reviewId).get()
        if review.val():
            return review.val()
        else:
            return None
        
    def get_review_status_by_id(self, itemId):
        item_data = self.db.child("item").child(itemId).get().val()
        if item_data:
            review_complete = item_data.get('review_complete')
            return review_complete
        else:
            return None
        
    def get_reviews(self, user_id):
        #reivew_list가 list로 가져와져서 오류 수정 발생 1차 수정

        reviews_list = self.db.child("review").get().val()
        #파이어베이스에 review 번호가 1로 시작 0번 인덱스가 None이 되어 문제 발생.
        #0번 인덱스가 none인 경우 잘라내는 방식 사용
        if reviews_list and reviews_list[0] is None:
            reviews_list = reviews_list[1:]
        user_reviews = {}

        for key, value in enumerate(reviews_list):
            # 'sellerId'가 주어진 사용자 ID와 일치하는 경우
            if value.get('sellerId') == user_id:
                # 리뷰에 대응하는 상품 정보 가져오기
                item_id = value.get('reviewId')  # 'reviewId'를 아이템 ID로 가정
                item_info = self.find_item_by_id(item_id)

                if item_info:
                    # 리뷰 정보에 상품 가격과 이름 추가
                    value['price'] = item_info.get('price')
                    value['itemName'] = item_info.get('itemName')

                    # 사용자 리뷰 딕셔너리에 리뷰 추가
                    user_reviews[key] = value
        return user_reviews


    
    def get_review_by_name(self, name):
        reviews = self.db.child("review").get()
        target_value=""
        for res in reviews.each():
            key_value = res.key()
            
            if key_value == name:
                target_value=res.val()
        return target_value

    def get_items_bytransaction(self, cate):
        items = self.db.child("item").get()
        target_value=[]
        target_key=[]
        for res in items.each():
            value = res.val()
            key_value = res.key()
            if value is not None and 'transaction' in value and value['transaction'] == cate:
                target_value.append(value)
                target_key.append(key_value)
        new_dict={}
        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict
    
    def get_items_bylocation(self, cate):
        items = self.db.child("item").get()
        target_value=[]
        target_key=[]
        for res in items.each():
            value = res.val()
            key_value = res.key()
            if value is not None and 'location' in value and value['location'] == cate:
                target_value.append(value)
                target_key.append(key_value)
        new_dict={}
        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict
    
    def update_seller_grade(self, itemId, reviewData):
         
        if 'rating' not in reviewData:
        # 'rating' 키가 없는 경우에 대한 처리
        # 여기서는 기본값으로 0을 사용하도록 가정
            newRating = 0
        else:
            newRating = reviewData['rating']
        item = self.db.child("item").child(itemId).get().val()
        sellerId = item.get('userId')
        seller_key, seller_data = self.find_user_by_id(sellerId)
        
        reviewCount = seller_data.get('keyword_count', 1)
        grade = seller_data.get('grade', 2.5)
        
        newAverageGrade = ((grade * (reviewCount-1)) + float(newRating)) / (reviewCount)
        
        seller_data['grade'] = newAverageGrade
        
        self.db.child("user").child(seller_key).update(seller_data)
    
    def get_seller_grade(self, userId):
        user_key, user_data = self.find_user_by_id(userId)
        grade = user_data.get('grade', 2.5)
        return grade
    
    def update_lastCheckChatList(self, user_id):
        user_key, user_data = self.find_user_by_id(user_id)
        seoul_timezone = pytz.timezone('Asia/Seoul')
        current_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(seoul_timezone)
        formatted_time = current_time.strftime("%d/%m/%Y, %H:%M:%S")
        self.db.child("user").child(user_key).update({"lastCheckChatList": formatted_time})
        
    def is_newChat(self, user_id):
        user_key, user_data = self.find_user_by_id(user_id)
        if user_data is not None:
            last_check_time = user_data.get('lastCheckChatList', "01/01/1970, 00:00:00")
            if isinstance(last_check_time, str):
                last_check_time = datetime.strptime(last_check_time, "%d/%m/%Y, %H:%M:%S")

            chat_rooms = self.get_chat_rooms_for_user(user_id)
            
            for chat_room in chat_rooms:
                chatid = chat_room.get('chatRoomId')
                if chatid is None:
                    continue
                
                lastTimestamp = chat_room.get('lastTimestamp', "01/01/1970, 00:00:00")
                if isinstance(lastTimestamp, str):
                    lastTimestamp = datetime.strptime(lastTimestamp, "%d/%m/%Y, %H:%M:%S")
                
                print(f"Chat ID: {chatid}, Last Msg Timestamp: {lastTimestamp}, lastCheckTime: {last_check_time}")
                if lastTimestamp > last_check_time:
                    return True
        return False

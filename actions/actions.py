# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
ID = {
	'Kỹ thuật Điện tử viễn thông': 7520207,
	'Công nghệ kỹ thuật Điện, điện tử': 7510301,
	'Công nghệ thông tin': 7480201,
	'An toàn thông tin': 7480202,
	'Khoa học máy tính': 7480101,
	'Công nghệ đa phương tiện': 7329001,
    'Truyền thông đa phương tiện': 7320104,
	'Báo chí': 7320101,
	'Quản trị kinh doanh': 7340101,
	'Thương mại điện tử': 7340122,
	'Marketing': 7340115,
	'Kế toán': 7340301,
	'Công nghệ tài chính': 7340205,
    'Fintech': 7340205
}

from typing import Any, Text, Dict, List
from actions.greedy import Graph, greedy, AStar
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from mysql.connector import connect, errorcode, Error

def letsConnect(user, password):
    db_config = {
        'host': 'localhost',
        'user' : user,
        'password': password,
        'database': 'ptit'
    }
    con = None
    try:
            con = connect(**db_config)
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return con


#
class ActionSolve(Action):
    algorithm = None
    def name(self) -> Text:
        return "action_solve"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_intent = tracker.get_intent_of_latest_message()
        #debug
        print(last_intent)
        if not last_intent:
            dispatcher.utter_message(text = "Error! Tôi không hiểu!")
            return []
        
        if last_intent == 'solve_greedy' or last_intent == 'solve_A*':
            self.algorithm = 'greedy' if last_intent == 'solve_greedy' else 'A*'
            dispatcher.utter_message(text = "Tôi có một đồ thị cho trước như này. Bạn muốn tìm đường đi từ đỉnh nào đến đỉnh nào? "
                                     , image = 'https://imgur.com/a/ugzpMXP')
            
        elif last_intent == 'get_edge':
            st = next(tracker.get_latest_entity_values("start_node",), None)
            en = next(tracker.get_latest_entity_values("end_node"), None)
            #debug
            print(st, en)
            if not st or not en:
                dispatcher.utter_message(text = 'Xin hãy nói lại! Tôi không hiểu!')
                return []
            msg = 'Đáp án đường đi tôi tìm được :'
            if(self.algorithm == 'greedy'): msg += greedy(st, en)
            else: msg += AStar(st, en)
            dispatcher.utter_message(text = msg)

        return []

class ActionAboutMethod(Action):
    def name(self) -> Text:
        return "action_about_method"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_intent = tracker.get_intent_of_latest_message()
        method = next(tracker.get_latest_entity_values("method"), None)
        if last_intent == 'ask_method':
            buttons = [{"payload": "/ask_condition_enrollment", "title" : "Đối tượng dự tuyển của PTIT là gì?"},
                       {"payload": "/ask_register", "title": "Hồ sơ đăng ký"}]
            if method == 'xét tuyển kết hợp':
                msg = ''' Phương thức xét tuyển kết hợp áp dụng với các thí sinh thuộc diện đối tượng
                 dự tuyển của trường PTIT và có thêm ít nhất 1 trong các điều kiện sau:
                  Thí sinh có Chứng chỉ quốc tế SAT, trong thời hạn 02 năm (tính đến ngày xét tuyển) từ 1130/1600 trở lên hoặc ATC từ 25/36 trở lên; và có kết quả điểm trung bình chung học tập lớp 10, 11, 12 đạt từ 7,5 trở lên và có hạnh kiểm Khá trở lên;\n
Thí sinh có Chứng chỉ tiếng Anh quốc tế trong thời hạn (tính đến ngày xét tuyển) đạt IELTS 5.5 trở lên hoặc TOEFL iBT 65 trở lên hoặc TOEFL ITP 513 trở lên; và có kết quả điểm trung bình chung học tập lớp 10, 11, 12 đạt từ 7,5 trở lên và có hạnh kiểm Khá trở lên;\n
Thí sinh đạt giải Khuyến khích trong kỳ thi chọn học sinh giỏi quốc gia hoặc đã tham gia kỳ thi chọn học sinh giỏi quốc gia hoặc đạt giải Nhất, Nhì, Ba trong kỳ thi chọn học sinh giỏi cấp Tỉnh, Thành phố trực thuộc Trung ương (TW) các môn Toán, Lý, Hóa, Tin học và có kết quả điểm trung bình chung học tập lớp 10, 11, 12 đạt từ 7,5 trở lên và có hạnh kiểm Khá trở lên.\n
Là học sinh chuyên các môn Toán, Lý, Hóa, Tin học của trường THPT chuyên trên phạm vi toàn quốc (các trường THPT chuyên thuộc Tỉnh, Thành phố trực thuộc TW và các trường THPT chuyên thuộc Cơ sở giáo dục đại học) hoặc hệ chuyên thuôc các trường THPT trọng điểm quốc gia; Và có kết quả điểm trung bình chung học tập lớp 10, 11, 12 đạt từ 8,0 trở lên và có hạnh kiểm Khá trở lên\n '''
                
            elif method == 'thi tốt nghiệp THPT':
                msg = '''Phương thức xét tuyển dựa vào kết quả thi THPT áp dụng với các thí sinh thuộc diện đối tượng
                 dự tuyển của trường PTIT và các thí sinh phải tham dự kỳ thi tốt nghiệp THPT năm 2022 với các bài thi/môn thi theo tổ hợp xét tuyển tương ứng các ngành của Học viện.'''
                buttons.append({"payload": "/ask_diem_chuan", "title": "Xem điểm chuẩn các năm trước"})
            elif method == 'kỳ thi đánh giá năng lực':
                msg = '''Phương thức xét tuyển dựa vào kỳ thi đánh giá năng lực áp dụng với các thí sinh
                 thuộc diện đối tượng dự tuyển của trường PTIT và có thêm một trong những điều kiện sau:
                  Thí sinh có điểm thi đánh giá năng lực của Đại học quốc gia Hà Nội năm 2022 từ 80 điểm trở lên;\n
Thí sinh có điểm thi đánh giá năng lực của Đại học quốc gia Tp. Hồ Chí Minh năm 2022 từ 700 điểm trở lên;\n
Thí sinh có điểm thi đánh giá tư duy của Đại học Bách khoa Hà Nội năm 2022 từ 20 điểm trở lên. '''
            elif method == 'xét tuyển thẳng':
                msg = '''Phương thức xét tuyển thẳng áp dụng với các thí sinh
                 thuộc diện đối tượng dự tuyển của trường PTIT và đạt một trong các thành tích sau:
                 a) Thí sinh đạt giải Nhất, Nhì, Ba trong kỳ thi chọn học sinh giỏi quốc gia, quốc tế do Bộ Giáo dục và Đào tạo tổ chức, cử tham gia các môn Toán học, Vật lý, Hóa học hoặc Tin học;\n
b) Thí sinh đạt giải Nhất, Nhì, Ba trong Cuộc thi khoa học, kỹ thuật cấp quốc gia, quốc tế do Bộ Giáo dục và Đào tạo tổ chức, cử tham gia (Căn cứ vào đề tài dự thi của thí sinh đoạt giải, Học viện xem xét xét tuyển thẳng thí sinh vào ngành đào tạo phù hợp);\n
c) Thí sinh đạt giải Nhất, Nhì, Ba tại các kỳ thi tay nghề khu vực ASEAN, cuộc thi tay nghề quốc tế do Bộ Lao động – Thương binh Xã hội tổ chức và có kết quả thi THPT năm 2022 theo tổ hợp xét tuyển của ngành đăng ký xét tuyển đạt Ngưỡng đảm bảo chất lượng đầu vào của Học viện (Căn cứ vào lĩnh vực, nghề của thí sinh đoạt giải, Học viện xem xét xét tuyển thẳng thí sinh vào ngành đào tạo phù hợp).'''
            dispatcher.utter_message(text = msg)
        return []
class ActionAboutMajor(Action):
    def name(self) -> Text:
        return "action_about_major"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        connection = letsConnect('root', '123456')
        if connection == None:
            dispatcher.utter_message(text = 'Lỗi không mong muốn đã xảy ra. Xin hãy thử lại sau ít phút')
            return []
        print("da ket noi")
        last_intent = tracker.get_intent_of_latest_message()
        #debug
        major = next(tracker.get_latest_entity_values("major"), None)
        print(last_intent, major)

        if last_intent == 'ask_diem_chuan':
            
            if not major:
                query = "select Major_Name, Score from ptit"
            else: query = "select Score from ptit where Major_Name = (%s)"
            args = [major]
            
            cursor = connection.cursor()
            msg = 'Điểm chuẩn năm ngoái là: '
            try:
                cursor.execute(query, args)
                for row in cursor.fetchall():
                    for element in row:
                        msg += str(element)
                        if(row.index(element) != len(row) - 1): #khong phai ptu cuoi cung
                            msg += ', '
                    msg += '\n'
            except Error as e:
                print(e)
            cursor.close()
            connection.close()
            dispatcher.utter_message(text = msg)
        elif last_intent == 'ask_to_hop':
            if not major:
                query = "select Major_Name, Subject from ptit"
            else: query = "select Subject from ptit where Major_Name = (%s)"
            args = [major]
            
            cursor = connection.cursor()
            msg = 'Các tổ hợp xét là: \n'
            try:
                cursor.execute(query, args)
                for row in cursor.fetchall():
                    for element in row:
                        msg += str(element)
                        if(row.index(element) != len(row) - 1): #khong phai ptu cuoi cung
                            msg += ', '
                    msg += '\n'
            except Error as e:
                print(e)
            cursor.close()
            connection.close()
            dispatcher.utter_message(text = msg)
        elif last_intent == 'ask_chi_tieu':
            
            method = next(tracker.get_latest_entity_values("method"), None)
            if not method:
                dispatcher.utter_message(Text = 'Bạn muốn hỏi số chỉ tiêu của phương thức nào? (Điểm thi THPT, Xét kết hợp hay xét kết quả đánh giá năng lực)')
                return []

            if method == 'kỳ thi đánh giá năng lực': method = 'Nangluc'
            elif method == 'thi tốt nghiệp THPT': method = 'THPT'
            elif method == 'xét tuyển kết hợp': method = 'Kethop'
            elif method == 'xét tuyển thẳng':
                dispatcher.utter_message(Text = 'Chỉ tiêu cho xét tuyển thẳng là không giới hạn. Miễn bạn đạt đủ các điều kiện của xét tuyển thẳng thì hãy đăng ký vào PTIT ngay thôi nào!')
                return []
            if not major:
                query = "select Major_Name, (%s) from ptit"
            else: query = "select (%s) from ptit where Major_Name = (%s)"
            args = [method, major]
            cursor = connection.cursor()
            msg = 'Số chỉ tiêu là: \n'
            try:
                cursor.execute(query, args)
                for row in cursor.fetchall():
                    for element in row:
                        msg += str(element)
                        if(row.index(element) != len(row) - 1): #khong phai ptu cuoi cung
                            msg += ', '
                    msg += '\n'
            except Error as e:
                print(e)
            cursor.close()
            connection.close()
            dispatcher.utter_message(text = msg)
        return []
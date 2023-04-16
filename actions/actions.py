# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from pyuca import Collator
ck = Collator().sort_key
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
                dispatcher.utter_message(text = 'Xin hãy nói lại! Tôi không hiểu! Chú ý viết hoa chữ cái đại tên đỉnh')
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
        method_slot = tracker.get_slot('method')
        if not method_slot:
            dispatcher.utter_message('Bạn hãy nói rõ phương thức bạn muốn tìm hiểu')
            return []
        method_slot = method_slot.lower()
        print(last_intent, method, ' - ', method_slot)
        if last_intent == 'ask_method':
            msg = 'Tôi không hiểu bạn muốn hỏi phương thức tuyển sinh nào. Xin hãy nói rõ hơn!'
            buttons = [{"payload": "/ask_condition_enrollment", "title" : "Đối tượng dự tuyển của PTIT là gì?"},
                       {"payload": "/ask_register", "title": "Hồ sơ đăng ký"}]
            if method_slot == 'xét kết hợp':
                msg = ''' Phương thức xét kết hợp áp dụng với các thí sinh thuộc diện đối tượng dự tuyển của trường PTIT và có thêm ít nhất 1 trong các điều kiện sau:\n
a)Thí sinh có Chứng chỉ quốc tế SAT, trong thời hạn 02 năm (tính đến ngày xét tuyển) từ 1130/1600 trở lên hoặc ATC từ 25/36 trở lên; và có kết quả điểm trung bình chung học tập lớp 10, 11, 12 đạt từ 7,5 trở lên và có hạnh kiểm Khá trở lên;\n
b)Thí sinh có Chứng chỉ tiếng Anh quốc tế trong thời hạn (tính đến ngày xét tuyển) đạt IELTS 5.5 trở lên hoặc TOEFL iBT 65 trở lên hoặc TOEFL ITP 513 trở lên; và có kết quả điểm trung bình chung học tập lớp 10, 11, 12 đạt từ 7,5 trở lên và có hạnh kiểm Khá trở lên;\n
c)Thí sinh đạt giải Khuyến khích trong kỳ thi chọn học sinh giỏi quốc gia hoặc đã tham gia kỳ thi chọn học sinh giỏi quốc gia hoặc đạt giải Nhất, Nhì, Ba trong kỳ thi chọn học sinh giỏi cấp Tỉnh, Thành phố trực thuộc Trung ương (TW) các môn Toán, Lý, Hóa, Tin học và có kết quả điểm trung bình chung học tập lớp 10, 11, 12 đạt từ 7,5 trở lên và có hạnh kiểm Khá trở lên.\n
d)Là học sinh chuyên các môn Toán, Lý, Hóa, Tin học của trường THPT chuyên trên phạm vi toàn quốc (các trường THPT chuyên thuộc Tỉnh, Thành phố trực thuộc TW và các trường THPT chuyên thuộc Cơ sở giáo dục đại học) hoặc hệ chuyên thuôc các trường THPT trọng điểm quốc gia; Và có kết quả điểm trung bình chung học tập lớp 10, 11, 12 đạt từ 8,0 trở lên và có hạnh kiểm Khá trở lên\n '''
                
            elif method_slot == 'tốt nghiệp':
                msg = '''Phương thức xét tuyển dựa vào kết quả thi THPT áp dụng với các thí sinh thuộc diện đối tượng dự tuyển của trường PTIT và các thí sinh phải tham dự kỳ thi tốt nghiệp THPT năm 2022 với các bài thi/môn thi theo tổ hợp xét tuyển tương ứng các ngành của Học viện.'''
                buttons.append({"payload": "/ask_diem_chuan", "title": "Xem điểm chuẩn các năm trước"})
            elif method_slot == 'đánh giá năng lực':
                msg = '''Phương thức xét tuyển dựa vào kỳ thi đánh giá năng lực áp dụng với các thí sinh thuộc diện đối tượng dự tuyển của trường PTIT và có thêm một trong những điều kiện sau:\n
Thí sinh có điểm thi đánh giá năng lực của Đại học quốc gia Hà Nội năm 2022 từ 80 điểm trở lên;\n
Thí sinh có điểm thi đánh giá năng lực của Đại học quốc gia Tp. Hồ Chí Minh năm 2022 từ 700 điểm trở lên;\n
Thí sinh có điểm thi đánh giá tư duy của Đại học Bách khoa Hà Nội năm 2022 từ 20 điểm trở lên. '''
            elif method_slot == 'tuyển thẳng':
                msg = '''Phương thức xét tuyển thẳng áp dụng với các thí sinh thuộc diện đối tượng dự tuyển của trường PTIT và đạt một trong các thành tích sau:
a) Thí sinh đạt giải Nhất, Nhì, Ba trong kỳ thi chọn học sinh giỏi quốc gia, quốc tế do Bộ Giáo dục và Đào tạo tổ chức, cử tham gia các môn Toán học, Vật lý, Hóa học hoặc Tin học;\n
b) Thí sinh đạt giải Nhất, Nhì, Ba trong Cuộc thi khoa học, kỹ thuật cấp quốc gia, quốc tế do Bộ Giáo dục và Đào tạo tổ chức, cử tham gia (Căn cứ vào đề tài dự thi của thí sinh đoạt giải, Học viện xem xét xét tuyển thẳng thí sinh vào ngành đào tạo phù hợp);\n
c) Thí sinh đạt giải Nhất, Nhì, Ba tại các kỳ thi tay nghề khu vực ASEAN, cuộc thi tay nghề quốc tế do Bộ Lao động – Thương binh Xã hội tổ chức và có kết quả thi THPT năm 2022 theo tổ hợp xét tuyển của ngành đăng ký xét tuyển đạt Ngưỡng đảm bảo chất lượng đầu vào của Học viện (Căn cứ vào lĩnh vực, nghề của thí sinh đoạt giải, Học viện xem xét xét tuyển thẳng thí sinh vào ngành đào tạo phù hợp).'''
            dispatcher.utter_message(text = msg, buttons = buttons)

        #thu duc dang ky
        elif last_intent == "ask_register":
            msg = 'Tôi không hiểu bạn muốn hỏi phương thức tuyển sinh nào! Xin hãy nói cho tôi biết'
            print(method_slot)
            if method_slot == 'xét kết hợp':
                msg = '''Hồ sơ xét kết hợp bao gồm:\n
a) Phiếu đăng ký xét tuyển có xác nhận của trường THPT nơi thí sinh đang học hoặc Công an xã, phường nơi thí sinh tự do đang cư trú tại địa phương (In từ hệ thống xét tuyển);\n
b) Bản sao hợp pháp một trong các giấy tờ sau:\n
Chứng chỉ quốc tế SAT hoặcACT;\n
Chứng chỉ tiếng Anh quốc tế còntrong thời hạn (tính đến ngày xét tuyển);\n
Giấy chứng nhận đạt giải kỳ thi chọn học sinh giỏi quốc gia hoặc Giấy xác nhận đã tham gia kỳ thi chọn học sinh giỏi quốc gia hoặc Giấy chứng nhận đạt giải kỳ thi chọn học sinh giỏi cấp Tỉnh, Thành phố trực thuộc Trung ương.\n
c) Bản sao hợp lệ Học bạ THPT, trong trường hợp thí sinh chưa xin được học bạ THPT thì có thể thay thế bằng bản xác nhận kết quả học tập các môn học năm lớp 10, 11, 12 có ký và đóng dấu của trường THPT;\n
d) Bản sao hợp lệ CMND/CCCD;\n
e) Bản sao các giấy tờ ưu tiên khác (nếu có).\n
Lưu ý: Hồ sơ thí sinh nộp theo diện xét tuyển kết hợp là riêng, độc lập với đăng ký xét tuyển theo kết quả thi tốt nghiệp THPT.'''
            elif method_slot == 'đánh giá năng lực':
                msg = '''Hồ sơ xét tuyển theo kết quả kì thi đánh giá năng lực bao gồm: \n a) Phiếu đăng ký xét tuyển có xác nhận của trường THPT nơi thí sinh đang học hoặc Công an xã, phường nơi thí sinh tự do đang cư trú tại địa phương (In từ hệ thống xét tuyển);\n
b) Bản sao hợp lệ Giấy báo điểm/kết quả thi đánh giá năng lực hoặc đánh giá tư duy.\n
c) Bản sao hợp lệ CMND/CCCD;\n
d) Bản sao các giấy tờ ưu tiên khác (nếu có);'''
            elif method_slot == 'tuyển thẳng' or method_slot == 'xét tuyển thẳng':
                msg = '''Hồ sơ xét tuyển thẳng cần bao gồm:\n
Phiếu đăng ký xét tuyển thẳng có xác nhận của trường THPT nơi thí sinh đang học hoặc Công an xã, phường nơi thí sinh tự do đang cư trú tại địa phương (Phụ lục số 2);\n
Bản sao hợp lệ một trong các giấy tờ sau:\n
+ Giấy chứng nhận đoạt giải Kỳ thi chọn HSG quốc gia, quốc tế;\n
+ Giấy chứng nhận đoạt giải Cuộc thi Khoa học kỹ thuật quốc gia, quốc tế;\n
+ Giấy chứng nhận đoạt giải kỳ thi tay nghề khu vực ASEAN và thi tay nghề quốc tế;'''
            elif method_slot == 'tốt nghiệp':
                msg = '''Thí sinh thực hiện đăng ký nguyện vọng theo hướng dẫn của Bộ Giáo Dục, không cần hồ sơ gì thêm.'''
            dispatcher.utter_message(text = msg)
        #ask
        elif last_intent == 'ask_condition_enrollment':
            msg = '''Đối tượng dự tuyển chung của PTIT cần thỏa mãn các điều kiện sau: \n+) Người đã được công nhận tốt nghiệp trung học phổ thông (THPT) của Việt Nam hoặc có bằng tốt nghiệp của nước ngoài được công nhận trình độ tương đương;\n
+) Người đã có bằng tốt nghiệp trung cấp ngành nghề thuộc cùng nhóm ngành dự tuyển và đã hoàn thành đủ yêu cầu khối lượng kiến thức văn hóa cấp THPT theo quy định của pháp luật.\n
+) Có đủ sức khỏe để học tập theo quy định hiện hành;'''
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
            args = []
            if major: args.append(major)
            cursor = connection.cursor()
            msg = 'Điểm chuẩn năm ngoái là: '
            try:
                cursor.execute(query, args)
                for row in cursor.fetchall():
                    print(row)
                    for element in row:
                        msg += str(element)
                        if(row.index(element) != len(row) - 1): #khong phai ptu cuoi cung
                            msg += ': '
                    msg += '\n'
            except Error as e:
                print(e)
            cursor.close()
            connection.close()
            dispatcher.utter_message(text = msg)
        #ask_to_hop
        elif last_intent == 'ask_to_hop':
            if not major:
                query = "select Major_Name, Subject from ptit"
            else: query = "select Subject from ptit where Major_Name = (%s)"
            args = []
            if major: args.append(major)
            cursor = connection.cursor()
            msg = 'Các tổ hợp xét là: \n'
            try:
                cursor.execute(query, args)
                for row in cursor.fetchall():
                    print(row)
                    for element in row:
                        msg += str(element)
                        if(row.index(element) != len(row) - 1): #khong phai ptu cuoi cung
                            msg += ': '
                    msg += '\n'
            except Error as e:
                print(e)
            cursor.close()
            connection.close()
            dispatcher.utter_message(text = msg)

        #ask_chi_tieu
        elif last_intent == 'ask_chi_tieu':
            
            method = tracker.get_slot('method')
            print(method)
            if not method:
                dispatcher.utter_message(Text = 'Bạn muốn hỏi số chỉ tiêu của phương thức nào? (Điểm thi THPT, Xét kết hợp hay xét kết quả đánh giá năng lực)',
                                         buttons = [{"payload" : "/ask_chi_tieu{'method': 'tốt nghiệp'}", 'title': 'THPT'},
                                                    {'payload': '/ask_chi_tieu{"method": "đánh giá năng lực"}', 'title': 'Đánh giá năng lực'},
                                                    {"payload" : "/ask_chi_tieu{'method': 'xét kết hợp'}", 'title': 'THPT'},
                                                    {"payload" : "/ask_chi_tieu{'method': 'tuyển thẳng'}", 'title': 'THPT'}])

                return []

            if method == 'đánh giá năng lực': method = 'Nangluc'
            elif method == 'tốt nghiệp': method = 'THPT'
            elif method == 'xét kết hợp': method = 'Kethop'
            elif method == 'tuyển thẳng' or method == 'xét tuyển thẳng':
                dispatcher.utter_message(Text = 'Chỉ tiêu cho xét tuyển thẳng là không giới hạn. Miễn bạn đạt đủ các điều kiện của xét tuyển thẳng thì hãy đăng ký vào PTIT ngay thôi nào!')
                return []
            if not major:
                query = "select Major_Name, (%s) from ptit"
            else: query = f"select {method} from ptit where Major_Name = (%s)"
            args = [major]
            
            cursor = connection.cursor()
            msg = f'Số chỉ tiêu {method} là: \n'
            try:
                cursor.execute(query, args)
                for row in cursor.fetchall():
                    print(row)
                    for element in row:
                        msg += str(element)
                        if(row.index(element) != len(row) - 1): #khong phai ptu cuoi cung
                            msg += ': '
                    msg += '\n'
            except Error as e:
                print(e)
            cursor.close()
            connection.close()
            dispatcher.utter_message(text = msg)

        elif last_intent == 'ask_query_diem_chuan':
            compare = next(tracker.get_latest_entity_values("compare"), None)
            point = next(tracker.get_latest_entity_values("point"), None)
            if not point or not compare:
                dispatcher.utter_message("Xin lỗi. Tôi chưa thực hiện được yêu cầu này. Bạn thử viết rõ hơn xem sao!")
                return []
            a = ''
            if compare == 'lớn hơn': a = '>'
            elif compare == 'bằng': a = '='
            else: a = '<'
            #...
            query = f"select Major_Name,Score from ptit where Score {a} (%s)"
            args = [point]
            cursor = connection.cursor()
            print(compare)
            msg = f'Những ngành có điểm chuẩn {a} {point} như bạn mong muốn: \n'
            try:
                cursor.execute(query, args)
                for row in cursor.fetchall():
                    print(row)
                    for element in row:
                        msg += str(element)
                        if(row.index(element) != len(row) - 1): #khong phai ptu cuoi cung
                            msg += ': '
                    msg += '\n'
            except Error as e:
                print(e)
            cursor.close()
            connection.close()
            dispatcher.utter_message(text = msg)
        return []

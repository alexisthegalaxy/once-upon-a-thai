import sqlite3

# open connection and get a cursor
conn = sqlite3.connect('example.db')
c = conn.cursor()

# create schema for a new table
# c.execute('SHOW TABLES;')
# c.execute('CREATE TABLE IF NOT EXISTS sometable (name, age INTEGER)')
# conn.commit()

# extend schema during runtime
# c.execute('ALTER TABLE sometable ADD COLUMN gender TEXT')
# conn.commit()

# add another row
# c.execute('INSERT INTO cont values (?, ?, ?, ?) ', ('1', 'ตุ๊ก-แก', 'gecko', 'HM'))
# c.execute("INSERT INTO cont (thai, english, tones) VALUES ('ขอ-โทษ', 'sorry', 'RF');")


def find_word(thai):
    answers = list(c.execute(f"SELECT * FROM words WHERE thai = '{thai}'"))
    if answers:
        return answers[0]
    else:
        return None


def insert_word(thai, english, tones):
    if not find_word(thai):
        c.execute(f"INSERT INTO words (thai, english, tones) VALUES ('{thai}', '{english}', '{tones}')")
        conn.commit()


# insert_word('เอา-เถอะ', 'okay, alright', 'ML')
# insert_word('แก้ว', 'glass, classifier for glasses', 'F')
# insert_word('เครื่อง', 'machine, classifier for machines', 'F')
# insert_word('รูป', 'classifier for pictures and monks', 'F')
# insert_word('หลัง', 'next / classifier for house', 'R')
# insert_word('สาย', 'to be late / line, classifier for roads, rivers', 'R')
# insert_word('ผม', 'I (male)', 'R')
# insert_word('ฉัน', 'I (female)', 'R')
# insert_word('เธอ', 'she', 'M')
# insert_word('เขา', 'he, she, they', 'R')
# insert_word('มัน', 'it', 'M')
# insert_word('คุณ', 'you', 'M')
# insert_word('เรา', 'we / I (familiar)', 'M')
# insert_word('พวก-เรา', 'we', 'M')
# insert_word('นี้', 'this', 'HIGH')
# insert_word('นั่น', 'that', 'F')
# insert_word('โน่น', 'that (far)', 'F')
# insert_word('ตัว-เอง', 'self, own', 'MM')
# insert_word('ทุก-คน', 'everyone', 'HM')
# insert_word('พวก-เขา', 'they', 'FR')
# insert_word('ที่-นี่', 'here', 'FF')
# insert_word('ที่-นั่น', 'there', 'FF')
# insert_word('ไม่', 'not', 'F')
# insert_word('ของ', 'of', 'R')
# insert_word('แต่', 'but', 'LOW')
# insert_word('จะ', 'will (future)', 'LOW')
# insert_word('จาก', 'from', 'L')
# insert_word('ใน', 'in', 'M')
# insert_word('ที่', 'to, at, that', 'F')
# insert_word('กับ', 'with', 'L')
# insert_word('ใต้', 'under, south', 'F')
# insert_word('เหนือ', 'over, north', 'R')
# insert_word('เรื่อง', 'about', 'F')
# insert_word('เหมือน', 'like, as', 'R')
# insert_word('ให้', 'to, for (somebody), so that', 'F')
# insert_word('ด้วย', 'as well, with', 'F')
# insert_word('หน้า', 'in front of', 'F')
# insert_word('วัน-นี้', 'today', 'MH')
# insert_word('พรุ่ง-นี้', 'tomorrow', 'FH')
# insert_word('เมื่อ-วาน-นี้', 'yesterday', 'FMH')
# insert_word('ตอน-นี้', 'now', 'MH')
# insert_word('คืน-นี้', 'tonight', 'MH')
# insert_word('เมื่อ-คืน-นี้', 'last night', 'FMH')
# insert_word('อา-ทิตย์ห-น้า', 'next week', 'MHF')
# insert_word('ทุก-วัน', 'every day', 'HM')
# insert_word('เส-มอ', 'always', 'LR')
# insert_word('บ่อย-ๆ', 'often', 'LL')
# insert_word('บาง-ครั้ง', 'sometimes', 'MH')
# insert_word('เมื่อ-เช้า', 'this morning', 'FH')
# insert_word('ตอน-เช้า', 'in the morning', 'MH')
# insert_word('ตอน-บ่าย', 'in the afternoon', 'ML')
# insert_word('ตอน-เย็น', 'in the evening', 'MM')
# insert_word('ก่อน', 'first, before', 'L')
# insert_word('นาน', 'for a long time', 'M')
# insert_word('อา-ทิตย์', 'week', 'MH')
# insert_word('ดี', 'good', 'M')
# insert_word('ใหญ่', 'big', 'L')
# insert_word('ยาว', 'long', 'M')
# insert_word('สั้น', 'short', 'F')
# insert_word('แคบ', 'narrow', 'F')
# insert_word('ลึก', 'deep', 'R')
# insert_word('แข็ง', 'hard', 'R')
# insert_word('หิว', 'hungry, thirsty', 'R')
# insert_word('เร็ว', 'fast', 'M')
# insert_word('ง่วง', 'sleepy', 'F')
# insert_word('ดึก', 'late', 'L')
# insert_word('ใกล้', 'near', 'F')
# insert_word('โปรด', 'favorite', 'L')
# insert_word('พอ', 'enough', 'M')
# insert_word('ไกล', 'far', 'M')
# insert_word('ว่าง', 'free', 'F')
# insert_word('หล่อ', 'handsome', 'L')
# insert_word('อ้วน', 'fat, overweight', 'F')
# insert_word('เหนื่อย', 'tired', 'L')
# insert_word('สี-เงิน', 'silver', 'RM')
# insert_word('สี-ส้ม', 'orange', 'RF')
# insert_word('สี-เหลือง', 'yellow', 'RR')
# insert_word('สี-แดง', 'red', 'RM')
# insert_word('สี-ม่วง', 'purple', 'RF')
# insert_word('ที่-แล้ว', 'previous', 'FH')
# insert_word('สี-ฟ้า', 'blue', 'RH')
# insert_word('สี-เขียว', 'green', 'RR')
# insert_word('สี-ดำ', 'black', 'RM')
# insert_word('สี-ขาว', 'white', 'RR')
# insert_word('สี-เทา', 'grey', 'RM')
# insert_word('คน-เดียว', 'alone', 'MM')
# insert_word('วิ-เศษ', 'magical', 'HL')
# insert_word('สุด-ท้าย', 'last', 'LH')
# insert_word('ใจ-เย็น', 'calm, cool-headed', 'MM')
# insert_word('ใจ-ร้อน', 'hot-tempered', 'MH')
# insert_word('สี-น้ำ-ตาล', 'brown', 'RHM')
# insert_word('มี-ความ-สุข', 'to be happy', 'MML')
# insert_word('สี-ชม-พู', 'pink', 'RMM')
# insert_word('กำ-ลัง-ดี', 'just right', 'MMM')
# insert_word('สี-น้ำ-เงิน', 'dark blue', 'RHM')
# insert_word('สี', 'color', 'R')
# insert_word('เหลือง', '(yellow)', 'R')
# insert_word('ส้ม', '(orange)', 'F')
# insert_word('แดง', '(red)', 'M')
# insert_word('ม่วง', '(purple)', 'F')
# insert_word('ฟ้า', 'sky', 'H')
# insert_word('เงิน', 'money', 'M')
# insert_word('เขียว', 'green', 'R')
# insert_word('ตาล', 'sugar palm', 'M')
# insert_word('ขาว', '(white)', 'R')
# insert_word('ดำ', 'dark, black', 'M')
# insert_word('เทา', '(grey)', 'M')
# insert_word('หมา', 'dog', 'R')
# insert_word('แมว', 'cat', 'M')
# insert_word('งู', 'snake', 'M')
# insert_word('หนู', 'mouse', 'R')
# insert_word('ช้าง', 'elephant', 'H')
# insert_word('ลิง', 'monkey', 'M')
# insert_word('ปลา', 'fish', 'M')
# insert_word('นก', 'bird', 'H')
# insert_word('เสือ', 'tiger', 'R')
# insert_word('ผี-เสื้อ', 'butterfly', 'RF')
# insert_word('ตุ๊ก-แก', 'gecko', 'HM')
#
# insert_word('สอบ ', 'exam', 'L')
# insert_word('ดิน ', 'ground', 'M')
# insert_word('รถ ', 'car', 'H')
# insert_word('ไฟ ', 'fire', 'M')
# insert_word('ลม ', 'wind, air', 'M')
# insert_word('บ้าน ', 'home, house', 'F')
# insert_word('ขวด ', 'bottle', 'L')
# insert_word('เด็ก ', 'child', 'L')
# insert_word('ครู ', 'teacher', 'M')
# insert_word('หมอ ', 'doctor', 'R')
# insert_word('จีน ', 'China', 'M')
# insert_word('กล้วย ', 'banana', 'F')
# insert_word('เค้ก ', 'cake', 'H')
# insert_word('ข้าว ', 'rice', 'F')
# insert_word('น้ำ ', 'water', 'H')
# insert_word('เหล้า ', 'alcohol', 'F')
# insert_word('ลาว ', 'Laos', 'M')
# insert_word('ฝรั่ง ', 'gua', 'w')
# insert_word('บาท ', 'Baht', 'L')
# insert_word('หนัง ', 'RISING', 'm')
# insert_word('ทอง ', 'gold', 'M')
# insert_word('ไม้ ', 'tree', 'H')
# insert_word('วัน ', 'day', 'M')
# insert_word('เดือน ', 'month', 'M')
# insert_word('เสื้อ ', 'shirt', 'F')
# insert_word('ผี ', 'ghost, spirit', 'R')
# insert_word('ปี ', 'year', 'M')
# insert_word('ค่า ', 'cost', 'F')
# insert_word('เพื่อน ', 'friend', 'F')
# insert_word('ยิ้ม ', 'smile, to smile', 'H')
# insert_word('แล้ว ', 'already', 'H')
# insert_word('เยอะ ', '(too) much', 'H')
# insert_word('ทุก ', 'each', 'H')
# insert_word('อย่า ', 'dont', 'L')
# insert_word('เอง ', 'oneself', 'M')
# insert_word('เคย ', 'ever', 'M')
# insert_word('เพราะ ', 'because', 'H')
# insert_word('ใช่ ', 'yes / right?', 'F')
# insert_word('ยัง ', 'still, yet', 'M')
# insert_word('การ ', '(prefix converting verbs into nouns)', 'M')
# insert_word('กว่า ', 'more', 'L')
# insert_word('บ้าง ', 'some', 'F')
# insert_word('ว่า ', '(think, say, etc.) that', 'F')
# insert_word('พระ ', 'Buddha image, monk', 'H')
# insert_word('ตัว ', 'body', 'M')
# insert_word('แฟน ', 'lover', 'M')
# insert_word('ใจ ', 'heart, mind, spirit', 'M')
# insert_word('หัว ', 'head', 'R')
# insert_word('ผม ', 'hair', 'R')
# insert_word('ขา ', 'leg', 'R')
# insert_word('เท้า ', 'foot', 'H')
# insert_word('กิน ', 'to eat', 'M')
# insert_word('เห็น ', 'to see', 'R')
# insert_word('ดื่ม ', 'to drink', 'L')
# insert_word('คุย ', 'to talk', 'M')
# insert_word('คิด ', 'to think', 'H')
# insert_word('เรียน ', 'to study', 'M')
# insert_word('ต้อง ', 'to have to, must', 'F')
# insert_word('บอก ', 'to tell', 'L')
# insert_word('ไป ', 'to go', 'M')
# insert_word('มา ', 'to come', 'M')
# insert_word('อ่าน ', 'to read', 'L')
# insert_word('ชื่อ ', 'name, to be named', 'F')
# insert_word('เล่น ', 'to play', 'F')
# insert_word('คือ ', 'to be (equality)', 'M')
# insert_word('เป็น ', 'to be (details)', 'M')
# insert_word('ทำ ', 'to make', 'M')
# insert_word('ได้ ', 'to get, to be able', 'F')
# insert_word('นอน ', 'to sleep', 'M')
# insert_word('บิน ', 'to fly', 'M')
# insert_word('ซื้อ ', 'to buy', 'H')
# insert_word('จำ ', 'to remember', 'M')
# insert_word('ฝัน ', 'to dream', 'R')
# insert_word('เปิด ', 'to open, switch on', 'L')
# insert_word('ปิด ', 'to close, switch off', 'L')
# insert_word('ถาม ', 'to ask', 'R')
# insert_word('เชื่อ ', 'to believe', 'F')
# insert_word('เกลียด ', 'to hate', 'L')
# insert_word('กลับ ', 'to return', 'L')
# insert_word('รับ ', 'to receive', 'H')
# insert_word('ใช้ ', 'to use', 'H')
# insert_word('ศูนย์ ', '0', 'R')
# insert_word('หนึ่ง ', '1', 'L')
# insert_word('สอง ', '2', 'R')
# insert_word('สาม ', '3', 'R')
# insert_word('สี่ ', '4', 'L')
# insert_word('ห้า ', '5', 'F')
# insert_word('หก ', '6', 'L')
# insert_word('เจ็ด ', '7', 'L')
# insert_word('แปด ', '8', 'L')
# insert_word('เก้า ', '9', 'F')
# insert_word('สิบ ', '10', 'L')
# insert_word('พูด ', 'to speak', 'F')
# insert_word('นั่ง ', 'to sit', 'F')
# insert_word('มี ', 'to have', 'M')
# insert_word('อยู่ ', 'to be at', 'L')
# insert_word('ชื่อ ', 'to be called', 'F')
# insert_word('ชอบ ', 'to like', 'F')
# insert_word('รัก ', 'to love', 'H')
# insert_word('วิ่ง ', 'to run', 'F')
# insert_word('อยาก ', 'to want', 'L')
# insert_word('ควร ', 'should', 'M')
# insert_word('ไม่ ', 'not', 'F')
# insert_word('ของ ', 'of', 'R')
# insert_word('แต่ ', 'but', 'L')
# insert_word('จะ ', 'will (future)', 'L')


# insert_word('คน-ไทย', 'Thai people', 'MM')
# insert_word('ชื่อ-เล่น', 'nickname', 'FF')
# insert_word('ความ-สุข', 'happiness', 'ML')
# insert_word('หิ-มะ', 'snow', 'LH')
# insert_word('ใต้-ดิน', 'underground', 'FM')
# insert_word('ที-วี', 'TV', 'MM')
# insert_word('ข-นม', 'sweets, cake', 'LR')
#
# insert_word('อา-หาร', 'food', 'MR')
# insert_word('พิซ-ซ่า', 'pizza', 'HF')
# insert_word('เมือง-ไทย', 'Thailand', 'MM')
# insert_word('ญี่-ปุ่น', 'Japan', 'FL')
# insert_word('อัง-กฤษ', 'England, Britain', 'ML')
# insert_word('สเ-ปน', 'Spain', 'LM')
# insert_word('พ-ม่า', 'Myanmar', 'HF')
# insert_word('รถ-ไฟ', 'train', 'HM')
# insert_word('ไฟ-ฟ้า', 'electricity', 'MH')
# insert_word('ใจ-ดี', 'kind', 'MM')
# insert_word('หนัง-สือ', 'book', 'RR')
# insert_word('มะ-ม่วง', 'mango', 'HF')
# insert_word('อา-ทิตย์', 'week', 'MH')
# insert_word('อา-ยุ', 'age', 'MH')
# insert_word('ประ-เทศ', 'country', 'HF')
# insert_word('กา-แฟ', 'coffee', 'MM')
# insert_word('ต้น-ไม้', 'tree', 'FH')
# insert_word('ดอก-ไม้', 'flower', 'LH')
# insert_word('ผล-ไม้', 'fruit', 'RHH')
# insert_word('มะ-ม่วง', 'mango', 'HF')
# insert_word('มะ-ขาม', 'tamarind', 'HR')
# insert_word('คน-ขับ', 'driver', 'ML')
# insert_word('นัก-ร้อง', 'singer', 'HH')
# insert_word('เว-ลา', 'time', 'MM')
# insert_word('ภา-ษา', 'language', 'MR')
# insert_word('รา-คา', 'price', 'MM')
# insert_word('โรง-เรียน', 'school', 'MM')
# insert_word('ต-ลาด', 'market', 'LL')
# insert_word('ส-นาม', 'field', 'LR')
# insert_word('กระ-เป๋า', 'bag', 'LR')
# insert_word('หุ่น-ยนต์', 'robot', 'LM')
# insert_word('วัน-จันทร์', 'Monday', 'MM')
# insert_word('พระ-จันทร์', 'moon', 'HM')
# insert_word('อา-ศัย', 'to reside', 'MR')
# insert_word('กาง-เกง', 'trousers', 'MM')
# insert_word('รอง-เท้า', 'shoes', 'MH')
# insert_word('ถุง-เท้า', 'socks', 'RH')
# insert_word('คิด-ถึง', 'to miss, think about', 'HR')
# insert_word('คิด-มาก', 'to think too much, worry', 'HF')
# insert_word('ทำ-งาน', 'to work', 'MM')
# insert_word('มา-ถึง', 'to arrive', 'MR')
# insert_word('ตื่น-นอน', 'to get up, wake up', 'LM')
# insert_word('กลับ-บ้าน', 'to go home', 'LF')
# insert_word('เลิก-งาน', 'to finish work', 'FM')
# insert_word('ได้-ยิน', 'to hear', 'FM')
# insert_word('อยาก-ให้', 'to want (someone to do something)', 'LF')
# insert_word('ต้อง-การ', 'to want (followed by nouns)', 'FM')
# insert_word('ออก-มา', 'to come out', 'LM')
# insert_word('ขับ-รถ', 'to drive', 'LH')
# insert_word('บัน-ทึก', 'to save', 'MH')
# insert_word('ดูเ-หมือน', 'to look like', 'MR')
# insert_word('รู้-จัก', 'to know (someone)', 'HL')
# insert_word('ได้-ยิน', 'to hear', 'FM')
# insert_word('ทำ-ให้', 'to make (someone do something)', 'MF')
# insert_word('คง-จะ', 'may', 'ML')
# insert_word('เกี่ยว-กับ', 'about', 'LL')
# insert_word('ประ-มาณ', 'approximately', 'LM')
# insert_word('นิด-หน่อย', 'a little bit', 'HL')
# insert_word('ไม่-ใช่', 'no', 'FF')
# insert_word('กำ-ลัง', '[present continuous]', 'MM')
# insert_word('น่า-จะ', 'should', 'FL')
# insert_word('กรุง-เทพ', 'Bangkok', 'MF')
# insert_word('ย่อ-มาน', 'Yoman', 'FM')
# insert_word('ลอน-ดอน', 'London', 'MM')
# insert_word('อังก-ฤษ', 'England', 'ML')
# insert_word('โท-ร-ทัศน์', 'TV', 'MHH')
# insert_word('ก-รุ-ณา', 'please, kindly...', 'LHM')
# insert_word('กัด', 'to bite', 'L')
# insert_word('ลง-น-รก', 'to go to hell', 'MHH')
# insert_word('รถ-ไฟ-ฟ้า', 'skytrain', 'HMH')
# insert_word('ด็ก-ผู้-ชาย', 'boy', 'LFM')
# insert_word('มา-เล-เซีย', 'Malaysia', 'MMM')
# insert_word('แค-นา-ดา', 'Canada', 'MMM')
# insert_word('กัม-พู-ชา', 'Cambodia', 'MMM')
# insert_word('ฝ-รั่งเ-ศส', 'France', 'LLL')
# insert_word('ทำ-อา-หาร', 'to cook', 'MMR')
# insert_word('พระ-อา-ทิตย์', 'sun', 'HMH')
# insert_word('ส-นาม-บิน', 'airport', 'LRM')
# insert_word('ภา-ษา-ไทย', 'Thai language', 'MRM')
# insert_word('สับ-ปะ-รด', 'pineapple', 'LLH')
# insert_word('วัน-อา-ทิตย์', 'Sunday', 'MMH')
# insert_word('ภาพ-ยน-ตร์', 'movie (formal)', 'FHM')
# insert_word('มาก-เกิน-ไป', 'excessively', 'FMM')
# insert_word('อ-เล็ก-ซี่', 'Alexis', 'MRF')
# insert_word('วิศวกร', 'engineer', 'HLHM')
# insert_word('ส-นาม-เด็ก-เล่น', 'playground', 'LRLF')
# insert_word('รถ-ไฟ-ใต้-ดิน', 'subway, underground train', 'HMFM')
# insert_word('กาง-เกง-ขา-สั้น', 'shorts', 'MMRF')
# insert_word('ภา-ษา-อัง-กฤษ', 'English language', 'MRML')
# insert_word('เยอ-ร-ม-นี', 'Germany', 'MHHM')
# insert_word('อเ-ม-ริ-กัน', 'American', 'LMHM')
# insert_word('None', 'None', 'None')
# # get a single row
# print('all')
# c.execute('SELECT * FROM cont')
# for row in list(c):
#     print(row)
#
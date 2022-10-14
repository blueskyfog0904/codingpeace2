from flask import Flask,session, request,render_template

import cx_Oracle
import os
import sys
#연결에 필요한 기본 정보 (유저, 비밀번호, 데이터베이스 서버 주소)

def get_pw(id,pw):
    conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8")

    user_id=id
    user_pw=pw
    cursor = conn.cursor()
    sql = f"select user_pw from user1 where user_id = '{user_id}'"
    cursor.execute(sql)
    realpw = cursor.fetchone()[0]
    # print(f'확인결과>> {realpw}')
    a=False
    if user_id and user_pw :
        if pw == realpw:
            a=True #소스 추가해야함
    else:
        a=False #소스 추가해야함
    cursor.close()
    conn.close()
    return a

def get_data(id, start, finish):
    conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8")
    user_id=id
    cursor = conn.cursor()
    sql = f"select * from ANI where ANI_DATE between '{start}%' and '{finish}%' and USER_ID='{user_id}' order by ANI_DATE"
    cursor.execute(sql)
    data = cursor.fetchall()
    data_list=[]
    print(data)

    for obj in data:
        data_dic = {
            'user_id' : obj[0],
            'cam_seq': obj[1],
            'ani_date':obj[2],
            'ani_type': obj[3],
            'img_path' : obj[4]
        }
        data_list.append(data_dic)
        
    cursor.close()
    conn.close()

    return data_list

    
    
    
def insert_mem(request):
    conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8")

    id=request.form.get("USER_ID")
    pw=request.form.get("USER_PW")
    print('----안녕하세요-----') 
    print(id,pw)
    print('----성공하세요-----')
  
    cursor = conn.cursor()
    sql = f"insert into user1 values(user_seq.NEXTVAL,'{id}','{pw}','temp','temp','temp')"
    cursor.execute(sql)
    print(cursor.rowcount)
    cursor.close()
    conn.commit()
    conn.close()
    

def test(result):
    conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8")

    # with conn.cursor() as cur_ora:
    #     cur_ora.execute("select * from user1")
    #     res = cur_ora.fetchall()
    #     r = ''.join(map(str, res))
    #     print(r)
    print('----전송확인-----') 
    for i,v in result.items():
        print(i,":",v)
        print('----------')    

def mydetect():
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    # import exam
    # print(exam.test())

#     import detect
#     wei ='./runs/train/peace_results11/weights/best.pt'
#     img =1920
#     conf = 0.03
#     src =0
#   #  python detect.py --weights runs/train/peace_results11/weights/best.pt --img 1920 --conf 0.2 --source 0
#     print(detect.result(wei,img,conf,src))
    
    
    # import web_peace.exam as Exam
    # from exam import Exam
    # ex = Exam()
    # print(ex.exam2())
    
    # from exam import Hello
    # h1 = Hello()
    # print(h1.hello())
    
    # import exam
    # print(exam.test())
    
    # import 
    # print(detect.result())
    
# for row in res:
#     print(row)
    
    
    

# with conn.cursor() as cur_ora:
#     getpw="123"
#     cur_ora.execute("select user_id from user1 where user_pw=:getpw")
#     res = cur_ora.fetchall()
#     print(res)
# for row in res:
#     print(res,row)
  

# for name in cursor:
#    print("테스트 이름 리스트 : ", name)


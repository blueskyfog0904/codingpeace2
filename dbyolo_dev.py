import time
import threading
import cx_Oracle
# import session
from flask import Flask, request,render_template,redirect,url_for,session
import pandas as pd
from http.client import HTTPResponse
import imp
from flask import Flask, request,render_template,redirect,url_for,session
import db
import dbyolo,dbyolo_dev
import matplotlib.pyplot as plt, mpld3
from flask import jsonify
import random

if __name__=="__main__":
    print('dbyolo_dev는 퇴치기에 대한 모듈입니다.')

# CAM에 SN 고유한값있음 여기닥
KICK_SN='kp748'
cnt = 0;

def start(): #영상기록중에만 작동
    conn = cx_Oracle.connect('final_ai4', 'smhrd4', 'project-db-stu.ddns.net:1524/xe', encoding="UTF-8", nencoding="UTF-8")

    KICK_SEQ=find_kick_seq(KICK_SN)
    KICK_IF_DATE=f"to_char(current_date,'yyyy-mm-dd hh24:mi:ss')"
    KICK_IF_IMG= ""
    KICK_IF_VID= ""
    cursor = conn.cursor()


    sql = f"insert into KICK_IF values({KICK_SEQ},'Y',{KICK_IF_DATE},'{KICK_IF_IMG}','{KICK_IF_VID}')"
    cursor.execute(sql)
    # print(cursor.fetchall())
    cursor.close()
    conn.commit()

    conn.close()




def finish(ipath): # db에서 실행시킴
    conn = cx_Oracle.connect('final_ai4', 'smhrd4', 'project-db-stu.ddns.net:1524/xe', encoding="UTF-8", nencoding="UTF-8")
    KICK_SEQ=find_kick_seq(KICK_SN)
    KICK_IF_DATE=f"to_char(current_date,'yyyy-mm-dd hh24:mi:ss')"
    KICK_IF_IMG = ipath.replace('\\', '/')[55:]
    KICK_IF_VID = KICK_IF_IMG.replace('jpg', 'mp4')
    cursor = conn.cursor()
    sql = f"insert into KICK_IF values({KICK_SEQ},'Y',{KICK_IF_DATE},'{KICK_IF_IMG}','{KICK_IF_VID}')"
    cursor.execute(sql)
    # print(cursor.fetchall())
    cursor.close()
    conn.commit()
    conn.close()






def find_kick_seq(KICK_SN):
    conn = cx_Oracle.connect('final_ai4', 'smhrd4', 'project-db-stu.ddns.net:1524/xe', encoding="UTF-8", nencoding="UTF-8")
    with conn.cursor() as cursor:
        cursor.execute(f"select KICK_SEQ from KICK where KICK_SN ='{KICK_SN}'")
        idval= cursor.fetchone()[0]
        return idval

def search(): # 아이디 넘겨줘야함
    id=session['user_id']
    result=[]
    conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8",  nencoding="UTF-8")
    cursor = conn.cursor()
    cursor.execute(f"select * from kick where user_id='{id}'")
    
    kick = cursor.fetchall()
    for k in kick:
        if k[1]:
            cursor.execute(f"select * from kick_if where kick_seq='{k[1]}' order by kick_if_date")
            data= cursor.fetchall()
            for i in data:
                result.append(
                    {
                        "kick_seq" : i[0],
                        "kick_if_run" : i[1],
                        "kick_if_date": i[2],
                        "kick_if_img": i[3],
                        "kick_if_vid": i[4]
                    }
                )
            print(f'{k} 번째실행결과',len(result))
    result.reverse()
    cursor.close()
    conn.close()
#     print(result)
    return result
  
  
 

def mycamera(): #영상기록중에만 작동
    conn = cx_Oracle.connect('final_ai4', 'smhrd4', 'project-db-stu.ddns.net:1524/xe', encoding="UTF-8", nencoding="UTF-8")

    id=session['user_id']
    result=[]
    cursor = conn.cursor()
    sql = f"select * from cam where user_id='{id}'"
    cursor.execute(sql)
    data=cursor.fetchall()
    for i in data:
                result.append(
                    {
                        "user_id":i[0],
                        "cam_conn": i[1],
                        "cam_seq":i[2],
                        "cam_model":i[3],
                        "cam_name":i[4],
                        "cam_ip":i[5],
                        "cam_sn" : i[6]
                    }
                )
           
    cursor.close()
    conn.commit()
    conn.close()  
    return result;

def saveImg(ipath):
    conn = cx_Oracle.connect('final_ai4', 'smhrd4', 'project-db-stu.ddns.net:1524/xe', encoding="UTF-8",
                             nencoding="UTF-8")

    CAM_SEQ = random.randint(1, 3)  # 카메라 3대등록된걸 가정하고 랜덤으로 지정
    IMG_PATH = ipath

    cursor = conn.cursor()
    sql = f"insert into savedata values({CAM_SEQ},'{IMG_PATH}')"
    cursor.execute(sql)
    # print(cursor.fetchall())
    cursor.close()
    conn.commit()

    conn.close()
# 시스템 한대당 카메라 3대 있다고 가정.
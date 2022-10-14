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


if __name__=="__main__":
    print('dbyolo_dev는 퇴치기에 대한 모듈입니다.')

# CAM에 SN 고유한값있음 여기닥
KICK_SN='kp123'
cnt = 0;

def start(): #영상기록중에만 작동
    conn = cx_Oracle.connect('final_ai4', 'smhrd4', 'project-db-stu.ddns.net:1524/xe', encoding="UTF-8", nencoding="UTF-8")

    KICK_SEQ=find_kick_seq(KICK_SN)
    KICK_IF_DATE=f"to_char(current_date,'yyyy-mm-dd hh24:mi:ss')"
    cursor = conn.cursor()
    sql = f"insert into KICK_IF values({KICK_SEQ},'Y',{KICK_IF_DATE})"
    cursor.execute(sql)
    # print(cursor.fetchall())
    cursor.close()
    conn.commit()

    conn.close()





def finish(): # db에서 실행시킴
    conn = cx_Oracle.connect('final_ai4', 'smhrd4', 'project-db-stu.ddns.net:1524/xe', encoding="UTF-8", nencoding="UTF-8")
    KICK_SEQ=find_kick_seq(KICK_SN)
    KICK_IF_DATE=f"to_char(current_date,'yyyy-mm-dd hh24:mi:ss')"
    cursor = conn.cursor()
    sql = f"insert into KICK_IF values({KICK_SEQ},'N',{KICK_IF_DATE})"
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
                        "kick_if_date": i[2]
                    }
                )
            print(f'{k} 번째실행결과',len(result))
    result.reverse()
    cursor.close()
    conn.close()
#     print(result)
    return result
            
  
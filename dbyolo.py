# from flask import Flask,session, request,render_template


import cx_Oracle
import pandas as pd

if __name__=="__main__":
    print('머지...')


# CAM에 SN 고유한값있음 여기닥
CAM_SN='op123'

def find_id(CAM_SN):
    conn = cx_Oracle.connect('final_ai4', 'smhrd4', 'project-db-stu.ddns.net:1524/xe', encoding="UTF-8", nencoding="UTF-8")
    with conn.cursor() as cursor:
        cursor.execute(f"select USER_ID from CAM where CAM_SN ='{CAM_SN}'")
        idval= cursor.fetchone()[0]
        print('find_id함수에서 id >>',idval)
    return idval



def write(result_name, result_conf,path):
    conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8",  nencoding="UTF-8")
    USER_ID = find_id(CAM_SN)
    print('유저아이디>>',USER_ID)
    CAM_SEQ=1
    ANI_DATE=f"to_char(current_date,'yyyy-mm-dd hh24:mi:ss')"
    IMG_PATH=path
    ANI_TYPE=result_name
    print('----성공하세요-----')
    print(result_name, result_conf)
    cursor = conn.cursor()
    sql = f"insert into ANI values('{USER_ID}',{CAM_SEQ},{ANI_DATE},'{ANI_TYPE}','{IMG_PATH}')"
    cursor.execute(sql)
    # print(cursor.fetchall())
    cursor.close()
    conn.commit()
    conn.close()
    

# def perday(whichday,ani):
#     conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8",  nencoding="UTF-8")
#     date =whichday
#     ani_type=ani
    
#     with conn.cursor() as cursor:
#         # cur_ora.execute("select * from N_ANI")
#         cursor.execute(f"select * from ANI where ANI_DATE like '{date}%' and ani_type='{ani_type}' order by ANI_DATE")
#         list = cursor.fetchall()
#         cursor.execute("select column_name from user_tab_columns where table_name = 'ANI'")
#         col=[]
#         colall= cursor.fetchall()
#         for i in colall:
#             for j in i:
#                 col.append(i[0])
                
#         df=pd.DataFrame(list)
#         df.columns=col
#     return df



def perday_total(whichday):
    conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8",  nencoding="UTF-8")
    date =whichday
    
    with conn.cursor() as cursor:
        # cur_ora.execute("select * from N_ANI")
        cursor.execute(f"select * from ANI where ANI_DATE like '{date}%' order by ANI_DATE")
        list = cursor.fetchall()
        cursor.execute("select column_name from user_tab_columns where table_name = 'ANI'")
        col=[]
        colall= cursor.fetchall()
        for i in colall:
            for j in i:
                col.append(i[0])
                
        df=pd.DataFrame(list)
        df.columns=col
    return df



# def perday(whichday,ani):
def perday(whichday):
    conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8",  nencoding="UTF-8")
    date =whichday
    # ani_type=ani
    
    with conn.cursor() as cursor:
        cursor.execute(f"select * from ANI where ANI_DATE like '{date}%' order by ANI_DATE")
        # cursor.execute(f"select * from ANI where ANI_DATE like '{date}%' and ani_type='{ani_type}' order by ANI_DATE")
        list = cursor.fetchall()
        if not list:
            print('====================================================================')
            print('데이터가 없습니다')
            print('====================================================================')
            return -1
        else:
            # print(list)
            cursor.execute("select column_name from user_tab_columns where table_name = 'ANI'")
            col=[]
            colall= cursor.fetchall()
            for i in colall:
                for j in i:
                    col.append(i[0])
            # print(col)        
            df=pd.DataFrame(list)
            df.columns=col
            return df
  







def permonth(whichmonth,ani):
    conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8",  nencoding="UTF-8")
    date =whichmonth
    ani_type=ani
    with conn.cursor() as cursor:
        # cur_ora.execute("select * from N_ANI")
        cursor.execute(f"select * from ANI where ANI_DATE like '{date}%' and ani_type='{ani_type}' order by ANI_DATE")
        list = cursor.fetchall()
        cursor.execute("select column_name from user_tab_columns where table_name = 'ANI'")
        col=[]
        colall= cursor.fetchall()
        for i in colall:
            for j in i:
                col.append(i[0])
                
        df=pd.DataFrame(list)
        df.columns=col
    return df


def during(whatday1,whatday2,ani):
    conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8",  nencoding="UTF-8")
    start =whatday1
    finish=whatday2
    ani_type=ani
    with conn.cursor() as cursor:
        cursor.execute(f"select * from ani where ani_date between '{start}' and '{finish}%'  and ani_type='{ani_type}' order by ANI_DATE ")
        duringlist = cursor.fetchall()
        # print(duringlist)
        cursor.execute("select column_name from user_tab_columns where table_name = 'ANI'")
        col=[]
        colall= cursor.fetchall()
        for i in colall:
            for j in i:
                col.append(i[0])
                
        df=pd.DataFrame(duringlist)
        df.columns=col
        return df


def frommark(mark,day):
    conn = cx_Oracle.connect('final_ai4','smhrd4','project-db-stu.ddns.net:1524/xe', encoding="UTF-8",  nencoding="UTF-8")
    how=day
    with conn.cursor() as cursor:
        sql=f"SELECT TO_DATE('{mark}', 'YYYY-MM-DD')+{how} FROM dual"
        cursor.execute(sql)
        marklist = cursor.fetchall()
        df=pd.DataFrame(marklist)
    return df



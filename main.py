from http.client import HTTPResponse
import imp
from flask import Flask, request,render_template,redirect,url_for,session
import db
import dbyolo
import matplotlib.pyplot as plt, mpld3
import dbyolo_dev

from matplotlib import font_manager, rc
import numpy as np
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

app = Flask(__name__, static_url_path="/static")
app.secret_key="My_key"

  
@app.route('/')
def mainpage():
    if 'user_id' in session:
        id=session['user_id']
        print(f'메인에서 세션아이디는>> {id}')
    return render_template('index.html')
    
        

@app.route('/login',methods=['POST','GET'])
def logincheck():
    pw, realpw, id='', '', ''
    isTrue=False
    if request.method == 'POST':
        id=request.form['user_id']
        pw=request.form['user_pw']
        isTrue = db.get_pw(id,pw)
        print(f'저장된값 id={id},pw={pw}')
        if isTrue:
            session['user_id']=id
            print(f"세션에 {session['user_id']}저장후 리턴")
            return redirect(url_for('mainpage'))
    return render_template('login.html')


@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('user_id',None)
    return redirect(url_for('mainpage'))
    


@app.route('/join',methods=['POST','GET'])
def join(): 
    return render_template('join.html')

@app.route('/e404',methods=['POST','GET'])
def e404(): 
    return render_template('404.html')

@app.route('/dashboard',methods=['POST','GET'])
def devtest():
    if request.method=='GET':
        result=dbyolo_dev.search()
        return render_template('dashboard.html',result = result)

@app.route('/Record_Check',methods=['POST','GET'])
def Record_Check(): 
    if request.method == 'GET':
        if 'user_id' in session:
            id=session['user_id']
        date1 = request.args.get('date1')
        date2 = request.args.get('date2')
        print(id, date1, date2)

        data_list1 = db.get_data(id, date1, date2)
        print(data_list1)        

    return render_template('Record_Check.html', name=id, data_list=data_list1)

@app.route('/Graph_LIst',methods=['POST','GET'])
def Graph_LIst(): 
    return render_template('Graph_LIst.html')

@app.route('/maps',methods=['POST','GET'])
def maps(): 
    return render_template('maps.html')

@app.route('/notifications',methods=['POST','GET'])
def notifications(): 
    return render_template('notifications.html')



@app.route('/result',methods=['POST','GET'])
def result():
    if request.method == 'POST':
        result = request.form
        db.test(result)
        db.insert_mem(request)
      #for i,v in enumerate(result):
       # print(i,v,v[i])
        return render_template("result.html",result = result)


@app.route('/perday',methods=['POST','GET']) # 예시 http://127.0.0.1:5000/perday?day=2022.10.11&ani=wBoar
def perday():
    if request.method == 'GET':
        par =request.args.get('day')
        # ani= request.args.get('ani')
        
        # df = dbyolo.perday(par,ani)
        df = dbyolo.perday(par)
        df_wBoar = df.loc[df['ANI_TYPE']=='wBoar']
        df_wDeer = df.loc[df['ANI_TYPE']=='wDeer']
        
        timeline=[]
        timelineWboar=[]
        timelineWdeer=[]

        
        for i in range(24):
            timeline.append(0)
            timelineWboar.append(0)
            timelineWdeer.append(0)
            
        for i in range(len(df)):
            index = df['ANI_DATE'][i][11:13] #12
            timeline[int(index)-1] +=1
        
        for i in df_wBoar['ANI_DATE']:
            index = i[11:13] #일자조회
            timelineWboar[int(index)-1] +=1

        for i in df_wDeer['ANI_DATE']:
            index = i[11:13] #일자조회
            timelineWdeer[int(index)-1] +=1     
        print(timeline)   
        print(timelineWboar)   
        print(timelineWdeer)   
        
        # mpld3.show()
        fig=plt.figure() 
        plt.subplot(2,1,1)
        plt.subplots_adjust(hspace=0.5)
        plt.plot(timeline, color='b', label='모든 야생동물', linestyle='solid', marker='v')
        plt.grid(True, color='gray', alpha=0.1)
        plt.xlabel('시     간', labelpad=5, fontsize=18)
        plt.ylabel('출 현 횟 수', labelpad=5, fontsize=18)
        plt.legend(fontsize=12)
        # plt.plot(timeline,'ks-', mec='w', mew=5, ms=20, color='b')
        
        plt.subplot(2,1,2)
        plt.plot(timelineWboar, color='r', label='멧돼지', linestyle='solid', marker='o')
        plt.plot(timelineWdeer, color='g', label='고라니', linestyle='solid', marker='X')
        plt.grid(True, color='gray', alpha=0.1)
        plt.xlabel('시     간', labelpad=5, fontsize=18)
        plt.ylabel('출 현 횟 수', labelpad=5, fontsize=18)
        
        plt.legend(fontsize=12)
        
        html_graph=mpld3.fig_to_html(fig)
        return html_graph #덮어쓰기
        return render_template('perday.html', result = html_graph) #html로 보내기
        
    

        
 
 
 
@app.route('/perday2',methods=['POST','GET']) # 예시 http://127.0.0.1:5000/perday?day=2022.10.11&ani=wBoar
def perday2():
    if request.method == 'GET':
        par =request.args.get('day')
        ani= request.args.get('ani')
        
        
        ##
        df = dbyolo.perday(par,ani)
        df_total=dbyolo.perday_total(par) #오버라이드안되넹..
        y1=[] #y축
        y2=[] #y축
        x=[] #x축

        for i in range(24):
            y1.append(0)
            y2.append(0)
            x.append(i)

        for i in range(len(df)):
            index = df['ANI_DATE'][i][11:13] #12
            index_total = df_total['ANI_DATE'][i][11:13] #12
            y1[int(index)-1] +=1 
            y2[int(index_total)-1] +=1 
            
            
        y1= np.array(y1)    
        y2= np.array(y2)    

        x= np.array(x)



        fig, ax1 =plt.subplots()
        # ax1.bar(x, y1, color='deeppink', label='Demand', alpha=0.7, width=0.7)

        ax1.set_xlabel('시간대 별')
        if ani =='고라니':
            axisname='고라니'
        else:
            axisname='멧돼지'
        ax1.bar(x, y1, color='deeppink', label=f'{axisname}', alpha=0.7, width=0.7)
            
        ax1.set_ylabel(f'{axisname}')
        ax1.tick_params(axis='both', direction='in')
        plt.legend()
        ax2 = ax1.twinx()
        ax2.plot(x, y2, '-s', color='blue', markersize=3, linewidth=2, alpha=0.7, label='통합')
        ax2.set_ylabel('고라니+멧돼지')
        ax2.tick_params(axis='y', direction='in')
        plt.legend(loc=(0.8,0.8))
        # plt.show()


        # fig=plt.figure() #plt.figure(figsize=(8,8))
        html_graph=mpld3.fig_to_html(fig)
        ##
        
        return html_graph #덮어쓰기
 
 
 
    
    



@app.route('/permonth',methods=['POST','GET']) #예시 http://127.0.0.1:5000/permonth?month=2022.10&ani=wBoar
def permonth():
    if request.method == 'GET':
        par =request.args.get('month')
        # ani= request.args.get('ani')
        df = dbyolo.permonth(par)
        df_wBoar = df.loc[df['ANI_TYPE']=='wBoar']
        df_wDeer = df.loc[df['ANI_TYPE']=='wDeer']
        # df = dbyolo.permonth(par,ani)
        timeline=[]
        timelineWboar=[]
        timelineWdeer=[]
        
        if int(par[5:7]) in [1,3,5,7,8,10,12]:
            howlong=31
        elif int(par[5:7]) ==2:
            if int(par[:4])%4==0:
                howlong=29
            else:
                howlong=28 
        else:
            howlong=30
        for i in range(howlong):
            timeline.append(0)
            timelineWboar.append(0)
            timelineWdeer.append(0)
            
        for i in range(len(df)):
            index = df['ANI_DATE'][i][8:10] #일자조회
            timeline[int(index)-1] +=1
        
        for i in df_wBoar['ANI_DATE']:
            index = i[8:10] #일자조회
            timelineWboar[int(index)-1] +=1

        for i in df_wDeer['ANI_DATE']:
            index = i[8:10] #일자조회
            timelineWdeer[int(index)-1] +=1
        

        fig=plt.figure() 
        plt.subplot(2,1,1)
        plt.subplots_adjust(hspace=0.5)
        plt.plot(timeline, color='b', label='모든 야생동물', linestyle='solid', marker='v')
        plt.grid(True, color='gray', alpha=0.1)
        plt.xlabel('날     짜', labelpad=5, fontsize=18)
        plt.ylabel('출 현 횟 수', labelpad=5, fontsize=18)
        plt.legend(fontsize=12)
        # plt.plot(timeline,'ks-', mec='w', mew=5, ms=20, color='b')
        
        plt.subplot(2,1,2)
        plt.plot(timelineWboar, color='r', label='멧돼지', linestyle='solid', marker='o')
        plt.plot(timelineWdeer, color='g', label='고라니', linestyle='solid', marker='X')
        plt.grid(True, color='gray', alpha=0.1)
        plt.xlabel('날     짜', labelpad=5, fontsize=18)
        plt.ylabel('출 현 횟 수', labelpad=5, fontsize=18)
        
        plt.legend(fontsize=12)
        
        # mpld3.show()
        html_graph=mpld3.fig_to_html(fig)
        # return render_template('permonth.html', result = html_graph)
        # return mpld3.fig_to_html(fig) #덮어쓰기
        return html_graph


    


@app.route('/perweek',methods=['POST','GET']) # 예시 http://127.0.0.1:5000/perweek?day1=2022.10.01&day2=2022.10.17&ani=wDeer
def perweek():
    if request.method == 'GET':
        whatday1 =request.args.get('day1')
        whatday2 =request.args.get('day2')
        # ani= request.args.get('ani')
        
        # df = dbyolo.during(whatday1,whatday2,ani)
        df = dbyolo.during(whatday1,whatday2)
        df_wBoar = df.loc[df['ANI_TYPE']=='wBoar']
        df_wDeer = df.loc[df['ANI_TYPE']=='wDeer']
        # df = dbyolo.permonth(par,ani)
        timeline=[]
        timelineWboar=[]
        timelineWdeer=[]
        
        xline=[]
        gap=int(whatday2[8:10])-int(whatday1[8:10])+1
        for i in range(gap):
            timeline.append(0)
            timelineWboar.append(0)
            timelineWdeer.append(0)
            xline.append(i+1)

        for i in range(len(df)):
            index = df['ANI_DATE'][i][8:10] #일자
            timeline[int(index)-1-int(whatday1[8:10])] +=1

        for i in df_wBoar['ANI_DATE']:
            index = i[8:10] #일자조회
            timelineWboar[int(index)-1-int(whatday1[8:10])] +=1

        for i in df_wDeer['ANI_DATE']:
            index = i[8:10] #일자조회
            timelineWdeer[int(index)-1-int(whatday1[8:10])] +=1


        # mpld3.show()

        fig=plt.figure() 
        plt.subplot(2,1,1)
        plt.subplots_adjust(hspace=0.5)
        plt.plot(xline, timeline, color='b', label='모든 야생동물', linestyle='solid', marker='v')
        plt.grid(True, color='gray', alpha=0.1)
        plt.xlabel('날     짜', labelpad=5, fontsize=18)
        plt.ylabel('출 현 횟 수', labelpad=5, fontsize=18)
        plt.legend(fontsize=12)
        # plt.plot(timeline,'ks-', mec='w', mew=5, ms=20, color='b')
        
        plt.subplot(2,1,2)
        plt.plot(xline, timelineWboar, color='r', label='멧돼지', linestyle='solid', marker='o')
        plt.plot(xline, timelineWdeer, color='g', label='고라니', linestyle='solid', marker='X')
        plt.grid(True, color='gray', alpha=0.1)
        plt.xlabel('날     짜', labelpad=5, fontsize=18)
        plt.ylabel('출 현 횟 수', labelpad=5, fontsize=18)
        
        plt.legend(fontsize=12)
    

        return mpld3.fig_to_html(fig)  #덮어쓰기













# @app.route('/result2',methods=['POST','GET'])
# def result2():
#       if request.method == 'POST':
#          result = request.form
#          return render_template("result.html",result = result)




if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)
    # app.run(debug = True)
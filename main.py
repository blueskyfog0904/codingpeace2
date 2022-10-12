from flask import Flask, request,render_template,redirect,url_for,session
import db
# import dbyolo
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
def dashboard(): 
    return render_template('dashboard.html')

@app.route('/Record_Check',methods=['POST','GET'])
def Record_Check(): 
    return render_template('Record_Check.html')

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


# @app.route('/result2',methods=['POST','GET'])
# def result2():
#       if request.method == 'POST':
#          result = request.form
#          return render_template("result.html",result = result)




if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)
    # app.run(debug = True)
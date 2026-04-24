import os
from flask import Flask, render_template, request, session, Response
import psycopg2
from dotenv import load_dotenv
from graph1 import transalanlysis, trans_analysis
from datetime import datetime, timedelta

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
    "sslmode": os.getenv("DB_SSLMODE", "require")
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key_for_development")

@app.route("/", methods =["GET"])
def login():
    return render_template("login.html")  

#***********************************************************************************************************#

@app.route("/login",methods = ["POST"])
def home():
    loginatmno = request.form.get("atmNo")
    loginpassword = request.form.get("loginpassword")
    conn = get_conn()
    try: 
        with conn.cursor() as cur: 
            cur.execute("select pass from bankdata where atmno = %s",(loginatmno,))
            loginresult = cur.fetchone()
            if loginresult is None:
                return render_template(
                    "login.html",message = "Account Not Found"
                )
            # Safe string comparison to avoid type mismatch or leading zero issues
            elif str(loginresult[0]) == str(loginpassword):
                session['atmno'] = loginatmno
                return render_template("index.html")
            else:
                return render_template(
                    "login.html",message = "Password is wrong!"
                )
    finally:
         conn.close()  
         
#************************************************************************************************************#

@app.route("/createaccount",methods= ["POST", "GET"])
def createaccount():
    if request.method == "GET":
        return render_template("createaccount.html")
    

    username = request.form.get("username")
    mobile = request.form.get("phonenumber")
    password = request.form.get("password")
    confirm = request.form.get("checkpassword")
    mobile = int(mobile)
    conn = get_conn()
    try: 
        with conn.cursor() as cur: 
            cur.execute("select name from bankdata where phoneno = %s",(mobile,))
            loginmobile = cur.fetchone()
            
            if loginmobile:
                return render_template("login.html",message = f"Account already created by {loginmobile[0]}")


        atmnumber = str(mobile%10000)+"91"+str(mobile//10000) 
        atmnumber = int(atmnumber)
    
        
        cur.execute("INSERT INTO bankdata (name, phoneno, atmno, pass, amt) VALUES (%s,%s,%s,%s,%s)",(username, mobile, atmnumber, password, 0.00))
        session['atmno'] = atmnumber
        
        conn.commit()
        return render_template(
        "index.html",message="Your account has been created successfully, your details are: ",
        username=username,
        mobile=mobile,
        password=password
        )
            
    except Exception:
        return render_template(
            "login.html",message="Not created due to any error"
        )
    finally:
        conn.close()

#*********************************************************************************************#

@app.route("/home",methods = ["POST"])
def mainhome():
    
    return render_template("index.html")

#***********************************************************************************************#

@app.route("/weekly-graph")

def weekly_graph():
    
    temp_atm =session.get('atmno')
    if not temp_atm:
        return "Login required", 401

    y = [0, 0, 0, 0, 0, 0, 0]  


    conn = get_conn()
    try:

        with conn.cursor() as newcur:

            newcur.execute("""
                SELECT EXTRACT(DOW FROM trans_time) AS day_no,
                    SUM(trans_amount) AS total_amount
                FROM trans
                WHERE trans_atm = %s
                AND trans_time >= NOW() - INTERVAL '7 days'
                GROUP BY day_no
                ORDER BY day_no;
            """, (temp_atm,))
            
        

            rows = newcur.fetchall()
    finally:
        conn.close()

    for day_no, total_amount in rows:
        y[int(day_no)] = float(total_amount)

    
        
    
    img = transalanlysis(y)
    return Response(img.getvalue(), mimetype="image/png")


#***********************************************************************************************************

@app.route("/transfermoney",methods = ["POST", "GET"])
def transfermoney():
     atmno = session.get('atmno')
     tatmno = request.form.get("tratmno")
     tamount = request.form.get("tramount")
     tpass = request.form.get("trPassword")
     
#*****credintial checking*******#
     if str(atmno) == str(tatmno):
         return render_template("index.html",transfer_error = "you can't transfer to yourself!",active_page="transferMoney")
     conn = get_conn()
     try:
        with conn.cursor() as cur:
            cur.execute("select pass from bankdata where atmno = %s",(tatmno,))
            chatmno = cur.fetchone()
            if chatmno is None:
                return render_template("index.html",transfer_error ="provide valid atm",active_page="transferMoney")
            
            cur.execute("select pass from bankdata where atmno = %s",(atmno,))
            chpass = cur.fetchone()
            if str(chpass[0]) != str(tpass):
                return render_template("index.html",transfer_error = "Wrong password, please try again",active_page="transferMoney")
            
             

            tamount  = float(tamount) 
       
            
            cur.execute("select amt from bankdata where atmno = %s",(atmno,))
            camount = cur.fetchone()
            if(tamount > camount[0]):
                return render_template("index.html",message = "transection failed,due to low balance")
            cur.execute("update bankdata set amt = amt + %s where atmno = %s",(tamount,tatmno))
            cur.execute("update bankdata set amt = amt -  %s where atmno = %s",(tamount,atmno))
            cur.execute("insert into trans(trans_atm,trans_atm2,trans_amount) values (%s,%s,%s)",(atmno,tatmno,tamount))
            conn.commit()
     
            return render_template("index.html",message = "Transaction successful!", )
     except Exception:
          conn.rollback() 
          return render_template(
        "login.html", message="Not created due to any error"
    )
     finally:
         conn.close()
#***************************************************************************************#

@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/dashboard")
def dashboard():
    return render_template("index.html", active_page="monthly-graph")


@app.route("/monthly-graph",methods = ["GET"])
def  monthly_graph():
    temp_atm =session.get('atmno')
    y = [0.0] * 31   

    conn = get_conn()
    try:
        with conn.cursor() as newcur:
            newcur.execute("""
                SELECT DATE(trans_time) AS day_date,
                    SUM(trans_amount) AS total_amount
                FROM trans
                WHERE trans_atm = %s
                AND trans_time >= NOW() - INTERVAL '31 days'
                GROUP BY day_date
                ORDER BY day_date;
            """, (temp_atm,))

            rows = newcur.fetchall()
    
        
            sql = """
            SELECT
            EXTRACT(DOW FROM trans_time) AS day_no,
            COALESCE(SUM(CASE WHEN trans_atm2 = %s THEN trans_amount END),0) AS deposit_total,
            COALESCE(SUM(CASE WHEN trans_atm = %s THEN trans_amount END),0) AS spend_total
            FROM trans
            WHERE (trans_atm = %s OR trans_atm2 = %s)
            AND trans_time >= NOW() - INTERVAL '7 days'
            GROUP BY day_no
            ORDER BY day_no;
            """

            

            newcur.execute(sql, (temp_atm, temp_atm, temp_atm, temp_atm))
            rows2 = newcur.fetchall()
    finally:
        conn.close()

    start_date = datetime.now().date() - timedelta(days=30)

    for day_date, total_amount in rows:
        idx = (day_date - start_date).days
        if 0 <= idx < 31:
            y[idx] = float(total_amount)
            #2
    deposit = [0]*7
    spend = [0]*7

    for day_no, dep, sp in rows2:
        deposit[int(day_no)] = float(dep)
        spend[int(day_no)] = float(sp)

    
    img = trans_analysis(y,deposit,spend)
    return Response(img.getvalue(), mimetype="image/png")
    


@app.route("/update",methods = ["GET"])
def update():
    return render_template("update.html")


@app.route("/update-data",methods = ['POST'])
def update_data():
    atm = session.get('atmno')
    
    name = request.form.get("newname")
    phoneno = request.form.get("newphoneno")
    password = request.form.get("newpassword")

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            if name:
                cur.execute("update bankdata set name = %s where atmno = %s" ,( name , atm))
            if phoneno:
                cur.execute("update bankdata set phoneno = %s where atmno = %s" , (phoneno , atm))
            if password:
                cur.execute("update bankdata set pass = %s where atmno = %s" , (password , atm))
            conn.commit()



        
    finally:
        conn.close()
    
    return render_template("index.html", message = "Updated ... ")




@app.route("/delete", methods = ["GET"])
def delete():
    return render_template("delete.html")

@app.route("/delete-account", methods = ["post"])
def delete_account():
    password = request.form.get("password")

    atmno = session.get("atmno")

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("select pass from bankdata where atmno = %s",(atmno,))
            user_pass = cur.fetchone()

            if not user_pass:
                return render_template("index.html", message="Account not found")

            if str(user_pass[0]) == str(password):
        
         
                cur.execute("delete from bankdata where atmno = %s" , (atmno,))
                conn.commit()
            else:
                return render_template("index.html",message = "password is wrong")
    finally:
        conn.close()
    


    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

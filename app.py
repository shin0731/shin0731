# Flaskからimportしてflaskを使えるようにする
from os import scandir
import re
import sqlite3, random
from flask import Flask,render_template ,request,redirect,session
from werkzeug.utils import redirect

# app っていう名前でFlaskアプリをつくっていくよ～みたいな
app = Flask(__name__)
app.secret_key = "sunabacokoza"

@app.route("/")
def top():
    return "はろーわーるど！ここはTOPページです！！"

# 新しいルートを作成。hello関数
@app.route("/hello/<name>")
def hello(name):
    return name + "さん、こんにちは！！"


@app.route("/") 
def helloWorld():
    return "Hello World."

# @app.route("/<name>") 
# def greet(name):
#     return name + "さん、はろー！！"

# 新しいルートを作成
@app.route("/test") 
def test():
    name = "羊仙人"
    age = 100
    return render_template("index.html",name = name ,age = age)


# @app.route("/template")
# def template():
#     py_name = "すなばこ"
#     return render_template("index.html", name = py_name)


# 新しい/wheatherというルートを作ってください
# 関数名はwheather()
# templatesフォルダの中にwheather.htmlを作成してください
# 戻り値でテンプレート(wheather.html)を表示させてください
# wheather.htmlには今日の天気は◯◯ですと表示するHTMLを書きましょう
# ◯◯には、python側作られたwheatherという変数の値を埋め込んで表示してください
# できた方はweather.htmlにFlask初日の感想を書いてTweetして
# コミットとプッシュをしてから、アンケート記入次第終了です！

@app.route("/wheather") 
def wheather():
    name = "晴れ"
    return render_template("wheather.html",name = name)


# 新しくブランチを作ってください git checkout -b suzu ←ブランチの作成と移動を同時に行えるよ！
# 新しい/colorというルートを作ってください
# 関数名はcolor()
# 戻り値でテンプレート(color.html)を表示させてください
# color.htmlには今日のラッキーカラーは◯◯ですと表示するHTMLを書きましょう
# ◯◯には、python側作られたpy_colorという変数の値をhtml_colorに埋め込んで表示してください

# @app.route("/color") 
# def color():
#     name = "青"
#     return render_template("color.html",name = name)
# データベースからデータを引っ張ってくる


@app.route("/color") 
def color():
    conn = sqlite3.connect("color.db")
    c = conn.cursor()
    c.execute("SELECT colors from colors ")
    
    py_color = c.fetchall()
    print(py_color)
    py_color = random.choice(py_color)[0]
    c.close()
    return render_template("color.html",html_color = py_color)


# 新しいブランチsuzuを作成して移動する
# 新しいルート/addを作る
# /addでは関数add_getを実行するように指定する
# add関数では戻り値としてadd.htmlというファイルを表示する
#add.htmlにはh1タグで新規追加とかいておいてください！ 




@app.route("/add" ,methods=["GET"]) 
def add_get():
    if "user_id" in session :    #ログインしてからの処理
        return render_template("add.html")
    else:
        return redirect("/login")







@app.route("/add" ,methods=["POST"]) 
def add_post():
    if "user_id" in session :
        #変数に今ログインしていてセッションに保存されてるidを代入
        user_id = session["user_id"]
        #フォームからtaskと名前のついたデータを取得して変数taskに代入
        task = request.form.get("task")
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("INSERT INTO tasks VALUES(null,?,?)",(task,user_id))
        print(task)
        conn.commit() #データベースの変更を保存
        c.close()  #データベースと接続解除。操作を終了

        return redirect("/list")
    else:
        return redirect("/login") 


#     一覧ページを表示しよう！
# 1）/listというルートの作成(メソッドはGET)
# 2）ルート内でtask_listという関数の作成
# 3）戻り値でlist.htmlを表示する
# 4）list.htmlはbaseと紐づける
# 5）h1タグでタスク一覧と表示
# 6）/listにアクセスしてページが表示されたらOK

@app.route("/list" ,methods=["GET"]) 
def task_list():
    if "user_id" in session :             # ログインしている投稿のみ表示
        user_id = session["user_id"]      # ログインしている人のid
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("select id,task from tasks where user_id = ?",(user_id,))
        task_list = []
        for row in c.fetchall(): #検索結果、全件とってくる
            task_list.append({"id":row[0],"task":row[1]})
        c.close()  #データベースと接続解除。操作を終了
        return render_template("list.html", task_list = task_list)
    else:
        return redirect("/login")   # ログインに戻す

# 新しくルートを作ってください名前はdel/<id>
# 関数名はdel_task()引数でURLからidを受け取る
# 処理はデータベースに接続して
# データを操作できるようにして
# sql文で投稿idを用いて投稿を削除するコードをかいて
# データを変更したのでデータベースの変更を保存するコードを書く
# データベースと接続を解除する
# 戻り値として/listに戻る

@app.route("/edit/<id>" ,methods=["GET"]) 
def edit(id):
    if "user_id" in session :
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("select task from tasks WHERE id = ?",(id,))
        task = c.fetchone()[0]
        c.close()
        item = {"id":id,"task":task}
        return render_template("edit.html", item = item)
    else:
        return redirect("/login")



@app.route("/edit" ,methods=["post"]) 
def edit_post():
    if "user_id" in session :
        task = request.form.get("task")
        id = request.form.get("task_id")
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("UPDATE tasks SET task = ? WHERE id = ?",(task,id))
        conn.commit() #データベースの変更を保存
        c.close()  #データベースと接続解除。操作を終了
        return redirect("/list")
    else:
        return redirect("/login")



# 新しくルートを作ってください名前はdel/<id>
# 関数名はdel_task()引数でURLからidを受け取る
# 処理はデータベースに接続して
# データを操作できるようにして
# sql文で投稿idを用いて投稿を削除するコードをかいて
# データを変更したのでデータベースの変更を保存するコードを書く
# データベースと接続を解除する
# 戻り値として/listに戻る

@app.route("/del/<id>" ) 
def del_task(id):
    if "user_id" in session :
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("DELETE from tasks WHERE id = ?",(id,))
        conn.commit() #データベースの変更を保存
        c.close()  #データベースと接続解除。操作を終了
        return redirect("/list")
    else:
        return redirect("/login")


# 入力フォームを作ってみよう！
# regist.htmlに会員登録用のフォームを作成してください。
# 1）/registというルートの作成(メソッドはGET)
# 2）ルート内でregist_getという関数の作成
# 3）戻り値でregist.htmlを表示する
# 4）regist.htmlはbaseと紐づける
# 5）h1タグで新規会員登録と表示
# 6）/registにアクセスしてページが表示されたらOK
# ※/add の GETメソッドの処理を参考にするよいいよ！

@app.route("/regist" ,methods=["GET"]) 
def regist_get():
    if "user_id" in session :
        return redirect("/list")   # 登録後すぐの方にはリスト表示
    else:
        return render_template("regist.html")


# 会員登録をしよう！
# 1）/registのPOSTメソッドのルートをつくる
# 2）関数はregist_post()
# 3)フォームからusernameの値を取得し変数nameに代入
# 4）フォームからpasswordの値を取得し変数passwordに代入
# 5）データベースに接続＆操作
# 6）SQL文を実行（users テーブルにユーザー情報を追加する）
# 7）データベースの保存
# 8）データベースと接続解除
# 9）戻り値で 「会員登録できました」という文字を表示
# ※/addのPOSTメソッドが少し参考になるかも？

@app.route("/regist" ,methods=["POST"]) 
def regist_post():
    name = request.form.get("username")
    password = request.form.get("password")
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (null,?,?)",(name,password))
    conn.commit() #データベースの変更を保存
    c.close()  #データベースと接続解除。操作を終了
    return redirect("/login")



# ログインぺーじを作ろう！
# loginページを表示するルートを作ろう
# 1）/login のGETメソッドで動くルートを作ろう
# 2）関数はlogin_get
# 3)戻り値としてlogin.htmlを表示する
# 4）login.htmlはbaseと紐づく
# 5）login.htmlにh1タグでログインしてくださいと表示
# 6）ボタンはログインと表示
# ※/registとかregist.htmlをコピーするとはやいよ！

@app.route("/login" ,methods=["GET"]) 
def login_get():
    if "user_id" in session :
        return redirect("/list") # 登録済みなのですぐにリスト表示
    else:
        return render_template("login.html")



# ログイン処理をしよう！
# ログインボタンが押されたらユーザーをログインさせる機能作ろう
# 1）/login のPOSTメソッドで動くルートを作ろう
# 2）関数はlogin_post
# 3)フォームからusernameの値を取得し変数nameに代入
# 4）フォームからpasswordの値を取得し変数passwordに代入
# 5）データベースに接続＆操作できるようにする
# 6）SQL文を実行
# （入力されたnameとpasswordの情報を元にusers テーブルにある
# userのidを取得）
# 7）データベースと接続解除
# 8)戻り値として/listを表示する
# ※/registのpostめそっどを参考にするといいよ！

@app.route("/login" ,methods=["POST"]) 
def login_post():
    name = request.form.get("username")
    password = request.form.get("password")
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE name =? and pass = ?",(name,password))
    user_id =c.fetchone()
    c.close()  
    if user_id is None :
        return render_template("login.html")
    else:
        session["user_id"] = user_id[0]
    return redirect("/list")


@app.route("/logout" ,methods=["GET"]) 
def logout():
    session.pop("user_id",None)
    return redirect("/login")






@app.errorhandler(404)
def notfound(code):
    return "404エラー"




if __name__ == "__main__":
# Flask が持っている開発用サーバーを、実行します。必ず最後に！
    app.run(debug=True)

# Flaskからimportしてflaskを使えるようにする
from os import scandir
import sqlite3, random
from flask import Flask,render_template ,request,redirect
from werkzeug.utils import redirect

# app っていう名前でFlaskアプリをつくっていくよ～みたいな
app = Flask(__name__)

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
    return render_template("add.html")


@app.route("/add" ,methods=["POST"]) 
def add_post():
    #フォームからtaskと名前のついたデータを取得して変数taskに代入
    task = request.form.get("task")
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks VALUES(null,?)",(task,))
    print(task)
    conn.commit() #データベースの変更を保存
    c.close()  #データベースと接続解除。操作を終了

    return redirect("/list")


#     一覧ページを表示しよう！
# 1）/listというルートの作成(メソッドはGET)
# 2）ルート内でtask_listという関数の作成
# 3）戻り値でlist.htmlを表示する
# 4）list.htmlはbaseと紐づける
# 5）h1タグでタスク一覧と表示
# 6）/listにアクセスしてページが表示されたらOK

@app.route("/list" ,methods=["GET"]) 
def task_list():
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("select id,task from tasks ")
    task_list = []
    for row in c.fetchall(): #検索結果、全件とってくる
        task_list.append({"id":row[0],"task":row[1]})
    c.close()  #データベースと接続解除。操作を終了
    return render_template("list.html", task_list = task_list)

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
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("select task from tasks WHERE id = ?",(id,))
    task = c.fetchone()[0]
    c.close()
    item = {"id":id,"task":task}
    return render_template("edit.html", item = item)

@app.route("/edit" ,methods=["post"]) 
def edit_post():
    task = request.form.get("task")
    id = request.form.get("task_id")
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET task = ? WHERE id = ?",(task,id))
    conn.commit() #データベースの変更を保存
    c.close()  #データベースと接続解除。操作を終了

    return redirect("/list")



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
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("DELETE from tasks WHERE id = ?",(id,))
    conn.commit() #データベースの変更を保存
    c.close()  #データベースと接続解除。操作を終了
    return redirect("/list")


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
    return render_template("regist.html")


@app.errorhandler(404)
def notfound(code):
    return "404エラー"




if __name__ == "__main__":
# Flask が持っている開発用サーバーを、実行します。必ず最後に！
    app.run(debug=True)

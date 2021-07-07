# Flaskからimportしてflaskを使えるようにする
from flask import Flask,render_template
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

@app.route("/<name>") 
def greet(name):
    return name + "さん、はろー！！"

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




if __name__ == "__main__":
# Flask が持っている開発用サーバーを、実行します。必ず最後に！
    app.run(debug=True)

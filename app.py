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


@app.route("/wheather") 
def wheather():
    name = "晴れ"
    return render_template("wheather.html",name = name)

# 新しい/wheatherというルートを作ってください
# 関数名はwheather()
# templatesフォルダの中にwheather.htmlを作成してください
# 戻り値でテンプレート(wheather.html)を表示させてください
# wheather.htmlには今日の天気は◯◯ですと表示するHTMLを書きましょう
# ◯◯には、python側作られたwheatherという変数の値を埋め込んで表示してください
# できた方はweather.htmlにFlask初日の感想を書いてTweetして
# コミットとプッシュをしてから、アンケート記入次第終了です！




if __name__ == "__main__":
# Flask が持っている開発用サーバーを、実行します。必ず最後に！
    app.run(debug=True)

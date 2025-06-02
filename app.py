from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import csv

app = Flask(__name__)
app.secret_key = "your_secret_key"  # セッションに必要（適当な文字列でOK）

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")
        now = datetime.now()
        jst = now.strftime("%Y-%m-%d %H:%M:%S")

        with open("record.csv", mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([jst, task])

        # メッセージの切り替え（セッションで管理）
        if session.get("message_flag") == "alt":
            session["message"] = "自信をもて！肯定感UP!"
            session["message_flag"] = "main"
        else:
            session["message"] = "上げてけ、いい流れだ！"
            session["message_flag"] = "alt"

        return redirect("/")

    # 記録を読み込む（最新20件、新しい順に並べ替え）
    records = []
    try:
        with open("record.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            records = list(reader)[-20:][::-1]
    except FileNotFoundError:
        pass

    now = datetime.now()
    jst = now.strftime("%Y-%m-%d %H:%M:%S")

    # 表示用メッセージ（初回はデフォルト）
    message = session.get("message", "自信をもて！肯定感UP!")

    return render_template("index.html", current_time=jst, records=records, message=message)

if __name__ == "__main__":
    app.run(debug=True)

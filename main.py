from flask import Flask, render_template, request, redirect, send_file
from so import get_jobs as so_get_jobs
from indeed import get_jobs as indeed_get_jobs
from exporter import save_to_file
app = Flask("JobScrapper")  # 이름

db = {}  # 딕셔너리


@app.route("/")
def home():
    return render_template("home.html")  # html 불러오기


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:  # word가 없을때 대비
        word = word.lower()  # 소문자로
        existingJobs = db.get(word)  # value
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = indeed_get_jobs(word) + so_get_jobs(word)
            db[word] = jobs  # db에 넣기
    else:
        return redirect("/")
    return render_template("report.html",
                           searchingBy=word,
                           resultsNumber=len(jobs),
                           jobs=jobs)  # 정보 전달


@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:  # word가 없을때 대비
            raise Exception()
        word = word.lower()  # 소문자로
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")  # jobs.csv파일 보내기
    except:  # 예외(error) 발생시
        return redirect("/")


app.run(host="0.0.0.0", port="8000")

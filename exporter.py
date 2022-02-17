import csv


def save_to_file(jobs):
    file = open("jobs.csv", mode="w")  # 쓰기모드로 파일열기
    writer = csv.writer(file)  # 쓸 파일 지정
    writer.writerow(["Title", "Company", "Location", "Link"])
    for job in jobs:
        writer.writerow(list(job.values()))  # 딕셔너리 값을 리스트로 가져오기
    return

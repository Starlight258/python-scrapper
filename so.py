import requests
from bs4 import BeautifulSoup


def get_last_page(URL):  # load last page
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)  # Next다음 마지막 페이지수, 공백 없애기
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find("h3", {"class": "mb4"}).find_all(
        "span", recursive=False)  # 한단계만, 두 요소 각각 대응
    company = company.get_text(strip=True)  # 띄어쓰기 없애기
    location = location.get_text(strip=True)
    job_id = html['data-jobid']
    return {'title': title, 'company': company, 'location': location,
            'link': f"https://stackoverflow.com/jobs/{job_id}"}


def extract_jobs(last_page, URL):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page:{page}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):  # 단어 받아오기
    URL = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(URL)  # URL 넘겨주기
    jobs = extract_jobs(last_page, URL)
    return jobs

import requests
from bs4 import BeautifulSoup
LIMIT = 50


def get_last_page(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")  # text 가져오기, 형식은 html

    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')

    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))  # 텍스트만 가져오기
    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "jobTitle"}).find(
        "span", title=True).string
    company = html.find("span", {"class": "companyName"}).string
    # string은 내부 태그있으면 None
    location = html.find("div", {"class": "companyLocation"}).text
    job_id = html["data-jk"]
    return {'title': title, 'company': company, 'location': location,
            'link': f"https://www.indeed.com/viewjob?jk={job_id}&from=serp&vjs=3"}


def extract_jobs(last_page, URL):
    jobs = []
    for page in range(last_page):  # 0~4, 나중에 last page를 20으로 바꾸자
        print(f"Scrapping Indeed: Page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("a", {"class": "fs-unmask"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    URL = f"https://www.indeed.com/jobs?q={word}&limit={LIMIT}&from=web&vjs=3 "
    last_page = get_last_page(URL)
    jobs = extract_jobs(last_page, URL)
    return jobs

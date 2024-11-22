import time
import pyperclip
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import chromedriver_autoinstaller
from bs4 import BeautifulSoup

# ====== 설정 ======
LOGIN_URL = "https://www.jobkorea.co.kr/Login/Login_Tot.asp?rDBName=GG&re_url=/"
TARGET_URL = "https://www.jobkorea.co.kr/starter/PassAssay"  # 예시 크롤링 대상 URL
USER_ID = ""  # 여기에 잡코리아 아이디 입력
USER_PW = ""  # 여기에 잡코리아 비밀번호 입력
OUTPUT_CSV = "jobkorea_data.csv"  # 저장할 파일명

# 크롬 옵션 설정
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 크롬 드라이버 버전 확인 및 설치
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
chromedriver_path = f'./{chrome_ver}/chromedriver.exe'
chromedriver_autoinstaller.install(True)

# Service 객체를 생성하여 드라이버 초기화
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.implicitly_wait(10)

def login_to_jobkorea():
    driver.get("https://www.jobkorea.co.kr/Login/Login_Tot.asp")
    time.sleep(2)

    # ID 입력
    id_input = driver.find_element("id", "M_ID")
    id_input.click()
    pyperclip.copy(USER_ID)  # 여기서 "your_id"를 실제 ID로 변경하세요
    id_input.send_keys(Keys.CONTROL, 'v')

    # PW 입력
    pw_input = driver.find_element("id", "M_PWD")
    pw_input.click()
    pyperclip.copy(USER_PW)  # 여기서 "your_password"를 실제 비밀번호로 변경하세요
    pw_input.send_keys(Keys.CONTROL, 'v')

    # 로그인 버튼 클릭
    login_btn = driver.find_element("class name", "login-button")
    login_btn.click()
    time.sleep(3)

def remove_query_string(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

# ====== 데이터 크롤링 ======
def scrape_data():
    page = 1
    data_rows = []

    while True:
        # 현재 페이지 URL 설정
        page_url = f"https://www.jobkorea.co.kr/Search/?stext=IT%EA%B0%9C%EB%B0%9C%EC%9E%90&tabType=recruit&Page_No={page}"
        driver.get(page_url)
        time.sleep(3)

        # HTML 가져오기
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 채용공고 리스트 추출
        job_listings = soup.select("section.content-recruit article.list-item")
        # if soup.select_one("article.list-empty"):  # 더 이상 공고가 없으면 종료
        if page == 3:
            print("모든 페이지 크롤링 완료")
            break

        for job in job_listings:
            # 제목
            title = job.select_one(".information-title-link").get_text(strip=True) if job.select_one(".information-title-link") else ""

            # 회사명
            company = job.select_one(".corp-name-link").get_text(strip=True) if job.select_one(".corp-name-link") else ""
            keywords = ["중소기업", "중견기업", "대기업", "벤처기업"]
            if any(keyword in company for keyword in keywords):
                company = "헤드헌터"

            # 지원 URL
            job_url = "https://www.jobkorea.co.kr" + job.select_one(".information-title-link")["href"] if job.select_one(".information-title-link") else ""
            job_url = remove_query_string(job_url)

            # 경력
            career_info = job.select_one(".chip-information-item:nth-child(1)").get_text(strip=True) if job.select_one(".chip-information-item:nth-child(1)") else ""

            # 학력
            education_info = job.select_one(".chip-information-item:nth-child(2)").get_text(strip=True) if job.select_one(".chip-information-item:nth-child(2)") else ""

            # 고용 형태
            employment_type = job.select_one(".chip-information-item:nth-child(3)").get_text(strip=True) if job.select_one(".chip-information-item:nth-child(3)") else ""
            if employment_type == "연수생/교육생":
                continue

            # 지역
            location = job.select_one(".chip-information-item:nth-child(4)").get_text(strip=True) if job.select_one(".chip-information-item:nth-child(4)") else ""

            # 마감 기한
            deadline = job.select_one(".chip-information-item:nth-child(5)").get_text(strip=True) if job.select_one(".chip-information-item:nth-child(5)") else ""

            # 데이터 저장
            data_rows.append([title, company, job_url, career_info, education_info, employment_type, location, deadline])

        print(f"{page}번 페이지 데이터 크롤링 완료")
        page += 1  # 다음 페이지로 이동

    # CSV 저장
    with open("jobkorea_jobs.csv", mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Job URL", "Career", "Education", "Employment Type", "Location", "Deadline"])
        writer.writerows(data_rows)

    print("데이터가 jobkorea_jobs.csv 파일에 저장되었습니다.")


# ====== 메인 실행 ======
try:
    login_to_jobkorea()
    scrape_data()
finally:
    driver.quit()
    print("크롬 드라이버가 종료되었습니다.")

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from custom_function import RemoveAlphabate
from selenium import webdriver
from datetime import date
from tabulate import tabulate

ChromeDriver = "C:\project_data\chromedriver\chromedriver.exe"
url = "https://www.ccsuforms.in/scriet_registration_2021/login.php"

SubjectCode = {"[BT-507]": "Transducer", "[BT-508]": "Signal processing", "[BT-509]": "Itcs",
               "[BT-502]": "Microprocessor", "[BT-506]": "Inst and measurement", "[BT-501]": "Integrated circuits"}


def Check_subjectCode(code):
    try:
        return SubjectCode[code]
    except:
        return "Not defined"


Frm_no = input('Enter your form number')
pswd = input('Enter your form pswd')

ser = Service(ChromeDriver)
op = webdriver.ChromeOptions()
op.add_argument("--headless")
op.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=ser, options=op)

driver.get(url)
formno = driver.find_element(By.XPATH, '//*[@id="formno"]')
userpass = driver.find_element(By.XPATH, '//*[@id="userpass"]')
question = driver.find_element(By.XPATH, '//*[@id="ebcaptchatext"]').text
solution = driver.find_element(By.XPATH, '//*[@id="ebcaptchainput"]')
submit = driver.find_element(By.XPATH, '//*[@id="submit"]')


answer = eval(RemoveAlphabate(question))
From = "01/01/2000"
To = date.today().strftime("%d/%m/%Y")

status1 = formno.is_displayed()
status2 = userpass.is_displayed()

if status1 and status2:
    formno.send_keys(Frm_no)
    userpass.send_keys(pswd)
    solution.send_keys(answer)
if submit.is_enabled():
    submit.click()
ViewAttendance = driver.find_element(
    By.XPATH, '/html/body/section/div/div[2]/div[4]/a').click()
driver.switch_to.window(driver.window_handles[1])
DateFrom = driver.find_element(By.NAME, "datefrom")
DateTo = driver.find_element(By.XPATH, '//*[@id="dateto"]')
SubjectWise = Select(driver.find_element(By.XPATH, '//*[@id="subjectwise"]'))
Submit = driver.find_element(By.NAME, "submit")
if DateFrom.is_displayed() and DateTo.is_displayed():
    DateFrom.click()
    DateFrom.send_keys(From)
    DateTo.send_keys(To)
    SubjectWise.select_by_visible_text("Yes")
    Submit.click()
    title = driver.find_element(
        By.XPATH, '//*[@id="dtHorizontalVerticalExample"]/thead[1]/tr')
    total = driver.find_element(
        By.XPATH, '//*[@id="dtHorizontalVerticalExample"]/tfoot/tr')
    title = f"{title.text}"
    title = title.split()
    title = title[2:len(title)-1]
    total = f"{total.text}"
    total = total.split(" T")[1:]
    total = [f"T{x}".split(" : ") for x in total]
    Total = []
    Present = []
    Absent = []
    Percentage = []
    for y in total:
        for i, x in enumerate(y):
            value = int(x[2:].strip("]"))
            if i == 0:
                Total.append(value)

            if i == 1:
                Present.append(value)
            if i == 2:
                Absent.append(value)
    name = [Check_subjectCode(x) for x in title]
    for T, P in zip(Total, Present):
        if T == 0:
            Percentage.append(f"No Class")
        else:
            percent = P*100/T
            Percentage.append(f"{format(percent,'.2f')} %")

    print(tabulate(tuple(zip(name, title, Total, Present, Absent, Percentage)), headers=[
          "Subject", "Code", "Total(T)", "Present(P)", " Absent(A)", "Percentage(%)"], tablefmt="pretty"))

driver.close()
driver.quit()

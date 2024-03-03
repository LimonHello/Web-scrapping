import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'


def gen_headers():
    browser = ["chrome"][0]
    os = ["win"][0]
    headers = Headers(browser=browser, os=os)
    return headers.generate()



def search():
    response = requests.get(url, headers=gen_headers())
    soup = BeautifulSoup(response.text, 'lxml')
    vacancies = soup.findAll('div', class_='vacancy-serp-item-body')
    data = []

    for vacancy in vacancies:
        link = vacancy.find('a', class_='bloko-link').get('href')
        position = vacancy.find('a', class_='bloko-link').text
        try:
            salary = vacancy.find('span', class_='bloko-header-section-2').text.replace("\u202f", " ").replace("\xa0",
                                                                                                               " ")
        except:
            salary = 'не указана'
        company_name = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace("\xa0", " ")
        location = vacancy.findAll('div', class_='bloko-text')[1].text.replace("\xa0", " ")

        data.append([link, position, salary, company_name, location])

    return data

def convert_to_dict(data):
    return [dict(zip(['link', 'position', 'salary', 'company_name', 'location'], row)) for row in data]


def write_json(data):
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    search()
    write_json(convert_to_dict(search()))



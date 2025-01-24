import requests
import csv
from bs4 import BeautifulSoup
from numbers import Numbers

class DataLoader:
    def __init__(self):
        self.dataSet = []


    def load(self):
        self.dataSet = self.__loadAllDataFromCsv()

    
    def info(self):
        print(f"> No. {len(self.dataSet)}")
        print(f"> Date. {self.dataSet[-1].getDate()}")


    def getData(self):
        return self.dataSet
    
    
    def __loadFromWeb(self, num):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={num}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return {
                'n' : data['drwNo'],
                'date': data['drwNoDate'], 
                'numbers': [str(data[f"drwtNo{i}"]) for i in range(1, 7)], 
            }
        except requests.exceptions.RequestException as e:
            print(f"exception: {e}")


    def __maxRound(self):
        url = "https://dhlottery.co.kr/common.do?method=main"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        max_numb = soup.find(name="strong", attrs={"id": "lottoDrwNo"}).text
        return int(max_numb)
    

    # very slow api (please waiting...)
    def __saveAllDataToCsv(self):
        with open('data_set.csv', 'w', newline='') as csvfile:
            # CSV 파일 쓰기
            writer = csv.writer(csvfile, delimiter=',')

            start = 1
            end = self.__maxRound() + 1
            for i in range(start, end):
                res = self.__loadFromWeb(i)
                writer.writerow([res.get('n'), res.get('date')] + res.get('numbers'))

    
    def __loadAllDataFromCsv(self):
        with open('data_set.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            arr = []
            for row in reader:
                arr.append(Numbers(row))
            return arr
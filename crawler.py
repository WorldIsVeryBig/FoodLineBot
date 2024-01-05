import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class Food(ABC):

    def __init__(self, area, food_type):
        self.area = area  # 地區
        self.food_type = food_type # 食物種類

    @abstractmethod
    def scrape(self):
        pass


class IFoodie(Food):

    def scrape(self):
        content = ""
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        area = self.area
        if "臺" in self.area:
            area = area.replace("臺", "台")
        if len(area) > 3:
            country = area[:3]
            region = area[3:]
            response = requests.get("http://ifoodie.tw/explore/" + country + "/" + region + "/list/" + self.food_type + "?sortby=popular&opening=true", headers=headers)
        else:
            response = requests.get("http://ifoodie.tw/explore/" + area + "/list/" + self.food_type + "?sortby=popular&opening=true", headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            # 爬取前五筆餐廳卡片資料
            cards = soup.find_all(
                'div', {'class': 'jsx-1309326380 restaurant-info'}, limit=5)
            if cards:
                for card in cards:
                    # 餐廳名稱
                    title = card.find("a", {"class": "jsx-1309326380 title-text"}).getText()
                    # 營業時間
                    business_hour = card.find("div", {"class": "jsx-1309326380 info"}).getText().split(': ')[1]
                    # 餐廳評價
                    stars = card.find("div", {"class": "jsx-2373119553 text"}).getText()
                    # 餐廳地址
                    address = card.find("div", {"class": "jsx-1309326380 address-row"}).getText()
                    #餐廳網址
                    restaurant_url = card.find("a", {"class": "jsx-1309326380"}).get('href')

                    restaurant_response = requests.get("https://ifoodie.tw" + restaurant_url)
                    if restaurant_response.status_code == 200:
                        re_soups = BeautifulSoup(restaurant_response.content, "html.parser")
                        restaurant_cards = re_soups.find_all("div", {"class": "jsx-2591663717 restaurant-info"})
                        for restaurant_card in restaurant_cards:
                            #聯絡電話
                            phone_data = restaurant_card.find("div", {"class": "jsx-2591663717 phone-wrapper wrap"})
                            phone = phone_data.getText()[5:] if phone_data else "無電話資訊"
                        content += f"{title} \n營業時間:{business_hour} \n{stars}顆星 \n{address}\n聯絡電話: {phone}\n餐廳網址： https://ifoodie.tw{restaurant_url} \n\n"
            else:
                content = False
        else: 
            content = "未成功連線至目標網站！"
        return content

from email import message
import requests
from flask import Flask, request, abort
from bs4 import BeautifulSoup
import json,requests
city_dict = {'基隆市':'2306188','嘉義市':'2296315','臺北市':'2306179','水上鄉':'12517927',
             '新北市':'90717580','臺南市':'2306182','桃園市':'91982232','高雄市':'2306180',
             '屏東縣':'91290319','新竹市':'2306185','臺東市':'91290354','苗栗市':'2301128',
             '臺中市':'2306181','宜蘭市':'91290369','彰化市':'91290191','七美鄉':'28760739',
             '南投市':'2306204','金湖鎮':'12517930','花蓮市':'91290403'}

def aday(city):
    city = city.replace('花蓮市','花蓮縣')
    current_city = city
    current_city = current_city.replace('嘉義縣','水上鄉')
    current_city = current_city.replace('金門縣','金湖鎮')
    current_city = current_city.replace('澎湖縣','七美鄉')
    current_city = current_city.replace('花蓮縣','花蓮市')
    token = 'CWB-E143136A-110E-4A69-8D66-E2176E9CAE23'  #剛剛生成的Token
    reply_message = "" 
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + str(city)
    Data = requests.get(url)
    Data = (json.loads(Data.text))
    weather_elements = Data["records"]["location"][0]["weatherElement"]
    current_url = "https://tw.news.yahoo.com/weather/台灣/{city}/{city}-" + city_dict[current_city]
    current_response = requests.get(current_url)
    soup = BeautifulSoup(current_response.text, 'lxml')
    info_items = soup.find_all('div', 'weather TW zh-Hant-TW')
    detail = soup.find_all('li', 'item BdB Cf Py(8px) Fz(1.1em) Bds(d) Bdbc(t)')
    for item in info_items:
        tem = item.find('span', 'Va(t)').getText()
        current_weather = item.find('span', 'description Va(m) Px(2px) Fz(1.3em)--sm Fz(1.6em)').getText()
        for item in detail:
            uv = item.find('div', 'Fl(end)').getText()
    # # weather
    weather = weather_elements[0]["time"][0]["parameter"]["parameterName"]
    reply_message += f"今天{city}的天氣: {weather}\n"
    reply_message += f"現在天氣狀況: {current_weather}\n"
    # # temperature
    min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
    max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]
    temperature = "溫度界於: {}°C ~ {}°C\n".format(min_tem, max_tem)
    reply_message += temperature
    current_tem = "目前溫度: {}°C\n".format(tem)
    reply_message += current_tem
    # # rain
    rain = weather_elements[1]["time"][0]["parameter"]["parameterName"]
    reply_message += f"降雨機率: " + rain + "%\n"
    reply_message += "紫外線指數: " + uv + "\n"
    # # comfort
    comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
    reply_message += "舒適度: " + comfort + "\n"
    if int(rain) or "雨" in current_weather> 50:
        reply_message += "提醒您，今天很有可能會下雨，出門記得帶把傘哦!"
    elif int(max_tem) > 33:
        reply_message += "提醒您，今天很熱，外出要小心中暑哦~"
    elif int(min_tem) < 10:
        reply_message += "提醒您，今天很冷，記得穿暖一點再出門哦~"
    elif uv[3] == '高' :
        reply_message += "提醒您，今天紫外線強烈, 注意防曬"
    # print(reply_message)
    return reply_message

def future(city):
    city_dict = {'基隆市':'2306188','嘉義市':'2296315','臺北市':'2306179','水上鄉':'12517927',
        '新北市':'90717580','臺南市':'2306182','桃園市':'91982232','高雄市':'2306180',
        '屏東縣':'91290319','新竹市':'2306185','臺東市':'91290354','苗栗市':'2301128',
        '臺中市':'2306181','宜蘭市':'91290369','彰化市':'91290191','七美鄉':'28760739',
        '南投市':'2306204','金湖鎮':'12517930','花蓮縣':'91290403'}
    city = city.replace('嘉義縣','水上鄉')
    city = city.replace('金門縣','金湖鎮')
    city = city.replace('澎湖縣','七美鄉')
    url = "https://tw.news.yahoo.com/weather/台灣/{city}/{city}-" + city_dict[city]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    reply_message = ""
    reply_message += f"未來五天{city}的天氣:\n"
    section = soup.find('section', 'weather-card C(#fff) P(10px) Bgc(#000.54) M(10px)')
    data = section.getText().split("星期")
    for i in range(1,6):
        # reply_message += "星期" + data[i].split("%")[0][0] + "   " + data[i].split("%")[0][1:] + "%    " + data[i].split("%")[1] + "\n"
        date = data[i].split("%")[0][0]
        rain = data[i].split("%")[0][1:]
        temp = data[i].split("%")[1] + "\n"
        reply_message += "星期{} 降雨機率: {}%    溫度: {}".format(date, rain, temp)
    return reply_message

# def news(city):
#     url = https://www.google.com/search?q=%E6%B0%A3%E8%B1%A1%E6%96%B0%E8%81%9E&hl=zh-TW&tbm=nws&ei=T3fqYeenO4nv-QaM4JngDA&start=0&sa=N&ved=2ahUKEwini8DYvsL1AhWJd94KHQxwBsw4HhDy0wN6BAgBED0&biw=618&bih=712&dpr=2.5
    
    
    
    
    
    
    
    
    
    
#  def current(city):
    # city_dict = {'基隆市':'2306188','嘉義市':'2296315','臺北市':'2306179','水上鄉':'12517927',
    #          '新北市':'90717580','臺南市':'2306182','桃園市':'91982232','高雄市':'2306180',
    #          '屏東縣':'91290319','新竹市':'2306185','臺東市':'91290354','苗栗市':'2301128',
    #          '臺中市':'2306181','宜蘭市':'91290369','彰化市':'91290191','七美鄉':'28760739',
    #          '南投市':'2306204','金湖鎮':'12517930','花蓮縣':'91290403'}
    # city = city.replace('嘉義縣','水上鄉')
    # city = city.replace('金門縣','金湖鎮')
    # city = city.replace('澎湖縣','七美鄉')
    # current_url = "https://tw.news.yahoo.com/weather/台灣/{city}/{city}-" + city_dict[city]
    # current_response = requests.get(current_url)
    # soup = BeautifulSoup(current_response.text, 'lxml')
    # info_items = soup.find_all('div', 'weather TW zh-Hant-TW')
    # detail = soup.find_all('li', 'item BdB Cf Py(8px) Fz(1.1em) Bds(d) Bdbc(t)')
    # reply_message = ""
    # for item in info_items:
    #     tem = item.find('span', 'Va(t)').getText()
    #     weather = item.find('span', 'description Va(m) Px(2px) Fz(1.3em)--sm Fz(1.6em)').getText()
    #     for item in detail:
    #         uv = item.find('div', 'Fl(end)').getText()
    #     temperature = "溫度: {}°C\n".format(tem)
    #     reply_message += f"目前{city}的天氣: {weather}\n"
    #     reply_message += temperature
    #     reply_message += "紫外線指數: " + uv
    # if uv[3] == '高' :
    #     reply_message += "紫外線強烈, 注意防曬"
    # elif "雨" in weather:
    #     reply_message += "\n提醒您，現在可能在下雨，出門記得帶把傘哦!"
        
    # return reply_message

    
    
    
    
future('高雄市')
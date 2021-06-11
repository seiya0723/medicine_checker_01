#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests,bs4,uuid,json,datetime,time

URL     = "https://www.qlife.jp/meds/newsmed_1/rx_list_1.html"
TIMEOUT = 10 
HEADER  = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"}
MODEL   = "medicine.medicine"


def page_urls():

    try:
        result  = requests.get(URL,timeout=TIMEOUT,headers=HEADER)
        time.sleep(1)
    except Exception as e:
        print(e)

        return []
    else:
        #全ページのリンクを抜き取る
        soup    = bs4.BeautifulSoup(result.content,"html.parser")
        links   = soup.select(".pager > .cl > li > a")
        
        urls    = [ "https://www.qlife.jp/meds/newsmed_1/rx_list_1.html" ]

        for link in links:
            print(link.get("href"))
            urls.append("https://www.qlife.jp"+link.get("href"))

        return urls

def medicine_urls(page_url):

    try:
        result  = requests.get(page_url,timeout=TIMEOUT,headers=HEADER)
        time.sleep(1)
    except Exception as e:
        print(e)
        return []
    else:
        #全ページのリンクを抜き取る
        soup    = bs4.BeautifulSoup(result.content,"html.parser")
        links   = soup.select(".drugs_list > .cl > li > a")
        
        urls    = []

        for link in links:
            print(link.get("href"))
            urls.append("https://www.qlife.jp"+link.get("href"))

        return urls


def medicine_datails(medicine_url):

    try:
        result  = requests.get(medicine_url,timeout=TIMEOUT,headers=HEADER)
        time.sleep(1)
    except Exception as e:
        print(e)
        return []
    else:
        soup    = bs4.BeautifulSoup(result.content,"html.parser")

        row     = { "name":"",
                    "effect":"",
                    "caution":"",
                    "dosage":"",
                    "side_effect":"",
                }

        #HACK:そのうちここ直す

        name                = soup.select("h1.page_title")
        effect              = soup.select("#dp01")
        caution             = soup.select("#dp02")
        dosage              = soup.select("#dp03")
        side_effect         = soup.select("#dp04")

        try:
            name                    = name[0].text
            row["name"]             = name.replace("の基本情報","")
        except:
            row["name"]             = ""
        try:
            row["effect"]           = effect[0].text
        except:
            row["effect"]           = ""
        try:
            row["caution"]          = caution[0].text
        except:
            row["caution"]          = ""
        try:
            row["dosage"]           = dosage[0].text
        except:
            row["dosage"]           = ""
        try:
            row["side_effect"]      = side_effect[0].text
        except:
            row["side_effect"]      = ""

        return row


page_urls   = page_urls()
medicines   = []

#メイン処理
for page_url in page_urls:
    urls        = medicine_urls(page_url)

    for url in urls:

        #fieldsの受け取りとdtの追加
        row             = medicine_datails(url)
        dt              = datetime.datetime.now()
        row["dt"]       = dt.strftime("%Y-%m-%dT%H:%M:%SZ")


        dic = {}
        dic["model"]    = MODEL
        dic["pk"]       = str(uuid.uuid4())
        dic["fields"]   = row 

        print(dic)
        medicines.append(dic)


    json_data   = json.dumps(medicines, ensure_ascii=False,)
    print(json_data)

    #書き込み処理をループごとに実行するので負荷がかかるが、あくまでも動作確認のため
    with open("test.json",mode="w") as f:
        f.write(json_data)


#TODO:抜き取ったデータにPKを割り当て、jsonファイルを生成する。←ただ、問題は常に主キーが不定になる点。新しいデータを入れるには、一旦DBを削除した後、jsonをloaddataで入れる必要があると思われる。

#TODO:この方法では終わるまでに約12時間かかるのでAPIが使えるか調査するか、並列でリクエストを飛ばすなどの対策が必要と思われる。





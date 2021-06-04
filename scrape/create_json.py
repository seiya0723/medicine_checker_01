#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,json,uuid,datetime

MODEL   = "medicine.medicine"



def main():

    medicines   = []
    dic         = {}

    dic["model"]    = MODEL
    dic["pk"]       = str(uuid.uuid4())

    row             = { "name": "ロキソニン",
                        "effect": "qweqew",
                        "caution": "qewewqewqwe",
                        "dosage": "eqw",
                        "side_effect": "ewqewqewq"
                        }

    #2021-05-29T09:38:59Z
    dt              = datetime.datetime.now()
    row["dt"]       = dt.strftime("%Y-%m-%dT%H:%M:%SZ")


    #ここで抜き取ったデータの辞書型を代入
    dic["fields"]   = row


    medicines.append(dic)
    print(dic)


    json_data   = json.dumps(medicines, ensure_ascii=False,)
    print(json_data)

    with open("test.json",mode="w") as f:
        f.write(json_data)
        #f.write(json_data.encode("utf-8"))





if __name__ == "__main__":
    try:
        print("Hello world")
        main()

    except KeyboardInterrupt:
        print("\nprogram was ended.\n")
        sys.exit()


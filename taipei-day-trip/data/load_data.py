# import json
# import os
# from dotenv import load_dotenv

# import mysql.connector
# load_dotenv()
# PASSWORD = os.getenv("PASSWORD")
# USER = os.getenv("USER")
# HOST = os.getenv("HOST")
# DB_NAME = os.getenv("DB_NAME")
# user_config = {
#     "user": USER,
#     "password": PASSWORD,
#     "host": HOST,
#     "database": DB_NAME,
# }
# cnx = mysql.connector.connect(**user_config)

# with open(file="data/taipei-attractions.json", mode="r", encoding="utf-8") as file:
#     data = json.load(file)
#     attraction_info = data["result"]["results"]
#    print(attraction_info)
# with cnx.cursor() as cursor:

# for attraction in attraction_info:

#     cursor.execute(
#         "INSERT INTO attractions(att_id, name, category, description, address, transport, mrt, lat, lng) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#         (attraction.get("_id"), attraction.get("name"), attraction.get('CAT'), attraction.get('description'), "".join(attraction.get(
#             'address').split(" ")), attraction.get('direction'), attraction.get('MRT'), attraction.get('latitude'), attraction.get('longitude'))
#     )

#     urls = attraction.get("file").split("https")
#     for i, url in enumerate(urls):
#         if i == 0:
#             continue
#         elif (url.endswith((".JPG", ".jpg", ".PNG", ".png"))):
#             full_url = "https" + url
#             cursor.execute("INSERT INTO img_urls(attraction_id, url) values(%s, %s)",
#                            (attraction.get("_id"), full_url))

# cnx.commit()
# cnx.close()

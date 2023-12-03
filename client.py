"""Клиент для отправки запросов к серверу main.py"""
import requests
 
response = requests.post("http://127.0.0.1:5000/advertisements", 
                        json={"name": "adv_5", 
                        "description": "post method 5",
                        "author": "user_1"})

response = requests.get("http://127.0.0.1:5000/advertisements/11")


# print(response.status_code)
# print(response.json())

# response = requests.delete("http://127.0.0.1:5000/advertisements/9")

# print(response.status_code)
# print(response.json())

#response = requests.get("http://127.0.0.1:5000/advertisements/2")


print(response.status_code)
print(response.json())

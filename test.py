import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "student", {"first_name":"Charles","last_name":"Tochukwu","dob":'1995-10-06',"amount_due":100})
print(response)

response = requests.get(BASE + "student/f56d8de7b6c741c68ba4aea6fe4242f6")
print(response)

response = requests.patch(BASE + "student/f56d8de7b6c741c68ba4aea6fe4242f6", {"first_name":"Henry"})
print(response)

response = requests.delete(BASE + "student/f56d8de7b6c741c68ba4aea6fe4242f6")
print(response)
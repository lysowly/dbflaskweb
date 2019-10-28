
import json

with open('movielist.txt','r',encoding='utf8') as f:
	movies = f.read()
for movie in json.loads(movies):
	print(movie)
	print('*'*50)
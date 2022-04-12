import json
import os, sys
import random
from random import randint

import requests


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialNetwork.settings')

try:
	from django.core.management import execute_from_command_line
except ImportError as exc:
	raise ImportError(
		"Couldn't import Django. Are you sure it's installed and "
		"available on your PYTHONPATH environment variable? Did you "
		"forget to activate a virtual environment?"
	) from exc
execute_from_command_line(sys.argv)

import django
django.setup()

from network_app.models import Post, CustomUser


def create_posts(server, access, max_posts):
	posts_user = randint(1, max_posts)
	for posts in range(posts_user):
		title = "Title for post"
		text = "Text for post"
		r = requests.post(server +"api/posts/", data={'title': title, 'text': text},
						  headers={'Authorization': "Bearer " + access})
		r = r.json()
		print(r)


def sign_up(server, number_of_users, max_posts):
	for x in range(number_of_users):
		user = "user" + str(x)
		email = user + "@gmail.com"
		password = user + "password"

		register = requests.post(server + "api/sign_up/",
								 data={'username': user, 'email': email, 'password': password}).json()

		login = requests.post(server + "api/login/", data={'username': user, 'password': password}).json()
		access = login["access"]

		create_posts(server, access, max_posts)


def like_posts(server, max_likes):
	users = CustomUser.objects.all()
	posts = Post.objects.all()
	list_id = []

	for id in posts:
		list_id.append(id.id)

	for user in users:
		count_like = randint(1, max_likes)
		post_to_like = random.sample(list_id, count_like)

		for id in post_to_like:
			login = requests.post(server + "api/login/",
							  data={'username': user.username, 'password': user.username + 'password'}).json()
			like = requests.post(server + f"api/posts/{id}/like/",
							 headers={'Authorization': "Bearer " + login["access"]})
			print(like.json())


def bot_configuration():
	print("\nNow, you will be asked to setup configuration for bot activities. \n")

	server = input("Write Django development server address. Leave blank if it is: http://127.0.0.1:8000/ ")

	if server == "":
		server = "http://127.0.0.1:8000/"

	number_of_users = input("How many users you wish to create: ")
	max_posts = input("Maximum number of posts per user: ")
	max_likes = input("Maximum number of likes per user: ")

	with open("bot.config", "r+") as f:
		data = json.load(f)

		data["host"] = server
		data["number_of_users"] = number_of_users
		data["max_posts"] = max_posts
		data["max_likes"] = max_likes

		f.seek(0,0)
		json.dump(data, f)

	print("\nbot.config updated!")


def first_bot_activity():
	with open("bot.config", "r+") as f:
		data = json.load(f)
		server = data["host"]
		number_of_users = int(data["number_of_users"])
		max_posts = int(data["max_posts"])

	sign_up(server, number_of_users, max_posts)

def second_bot_activity():
	with open("bot.config", "r+") as f:

		data = json.load(f)
		server = data["host"]
		max_likes = int(data["max_likes"])

	like_posts(server, max_likes)






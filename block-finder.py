# -*- coding: utf-8 -*-
import tweepy
from tweepy import OAuthHandler

auth = tweepy.OAuthHandler("Consumer Key (API Key)", "Consumer Secret (API Secret)") #YOU MUST FIX HERE
auth.set_access_token("Access Token", "Access Token Secret") #YOU MUST FIX HERE

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)

blockcount = 0
depthlimit = 3 #resize as you want
checked = []

def findblock(id, depth):
	if id in checked:
		return 0
	else:
		checked.append(id)
	count = 0
	try:
		user = api.get_user(id)
	except tweepy.TweepError as e:
		print(str(e))
		time.sleep(10)
		return 0
	except TypeError:
		return 0
	except Exception as e:
		print(str(e))
		return 0
	if user.protected == True: #protected
		return 0
	elif user.statuses_count == 0: #No tweets
		return 0
	elif not hasattr(user,"status"): #blocked
		try:
			print("Try to block:", user.screen_name, "(ID:", id, ")")
			api.create_block(id)
		except Exception:
			print("Failed:", user.screen_name, "(ID:", id, ")")
			return 0
	else: #normal
		nextlist = api.friends_ids(id)
		for next in nextlist:
			if depth<depthlimit:
				res = findblock(next, depth+1)
				count = count + res
		return count

if __name__ == "__main__": 
	me = api.me()
	followings = api.friends_ids(me.screen_name)
	for friend in followings:
		list = api.friends_ids(friend)
		for user in list:
			res = findblock(user, 1)
			blockcount = blockcount + res
	print("Block ", blockcount, " accounts")

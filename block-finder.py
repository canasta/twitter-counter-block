# -*- coding: utf-8 -*-
import tweepy
from tweepy import OAuthHandler

auth = tweepy.OAuthHandler("Consumer Key (API Key)", "Consumer Secret (API Secret)")
auth.set_access_token("Access Token", "Access Token Secret")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)

blockcount = 0
depthlimit = 4 #resize as you want
checked = []
try:
	with open("./checked.list","r+") as list:
		checked = list.read().split()
except:
	with open("./checked.list","w") as list:
		checked = []
	
		
def findblock(id, depth):
	if id in checked:
		return 0
			
	count = 0
	try:
		user = api.get_user(id)
	except tweepy.TweepError as e:
		print(str(e))
		return 0
	except TypeError:
		return 0
	except Exception as e:
		print(str(e))
		return 0
		
	if user.protected == True: #protected
		return 0
	elif user.statuses_count == 0: #No tweets(Dummy account)
		return 0
	elif not hasattr(user,"status"): #blocked
		try:
			api.create_block(id)
			blockcount = blockcount + 1
			print("(",blockcount,")Block:", user.screen_name, "(ID:", id, ")")
			with open("./blocked.list", "a") as list:
				list.write("%s %s\n"%(user.screen_name,id))
		except Exception:
			print("Failed:", user.screen_name, "(ID:", id, ")")
			return -1
	else: #normal
		if depth<depthlimit:
			nextlist = api.friends_ids(id)
			if len(nextlist)>20 and len(nextlist)<500:
				for next in nextlist:
					findblock(next, depth+1)
			else:
				with open("./skipped.list","a") as list:
					list.write("%s %s\n"%(user.screen_name,id))
				print("- Skipped:", user.screen_name, "(ID:", id, ")")
				
	checked.append(id)
	with open("./checked.list", "a") as list:
		list.write("%s %s\n"%(user.screen_name,id))
		
	return 0

if __name__ == "__main__": 
	me = api.me()
	followings = api.friends_ids(me.screen_name)
	for friend in followings:
		list = api.friends_ids(friend)
		for user in list:
			findblock(user, 1)
	print("Block ", blockcount, " accounts")

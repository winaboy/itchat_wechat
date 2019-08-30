#!/usr/bin/python
# -*-coding:utf-8 -*-

import itchat
from itchat.content import TEXT
from itchat.content import *
import sys
import re
import os
import json
import collections

group_id = '西雅图股票分享探讨总群'
data= {}
chatrooms= {}

@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def receive_msg(msg):
	if 'ActualNickName' in msg:
		group_id = msg['ToUserName']
		group_name = chatrooms[group_id]
		from_user_name = msg['ActualNickName']  # 谁发的
		if group_name in data:
			data[group_name]['Members'][from_user_name] += 1
			print("来自", group_name, "成员", from_user_name, "计数", data[group_name]['Members'][from_user_name])

			f=open('wechat.json', 'w')
			f.write(json.dumps(data,indent=4, ensure_ascii=False))
			f.close

if __name__ == '__main__':
	with open('wechat.json', 'r') as json_file:
	  data = json.load(json_file)

	itchat.auto_login(hotReload=True,enableCmdQR=False)
	raw_chatrooms = itchat.search_chatrooms(name=group_id)
	for chatroom in raw_chatrooms:
		itchat.update_chatroom(chatroom['UserName'])
		chatrooms[chatroom['UserName']] = chatroom['NickName']

		if chatroom.get('NickName') not in data:
			members = collections.defaultdict(int)
			for member in map(lambda members: members.get('NickName'), chatroom.get('MemberList')):
				members[member] = 0
			data[chatroom.get('NickName')] = {'Members': members}

		print(chatroom['UserName'],chatroom['NickName'],chatroom['MemberCount'])

	itchat.run()


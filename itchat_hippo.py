#!/usr/bin/python
# -*-coding:utf-8 -*-

import itchat
from itchat.content import TEXT
from itchat.content import *
import sys
import re
import os
import json

group_name = '西雅图股票分享探讨总群'
chatroom_list={}

def myupdate_chatroom_mem(cr_list,UserName,MemberList):
	if UserName not in cr_list:
		print("群信息不存在")
		return False
	for mem in MemberList:
		if  mem['UserName'] not in cr_list[UserName]['MemberList']:
			cr_list[UserName]['MemberList'][mem['UserName']] = {'NickName':mem['NickName'],"count":0}
	return True

@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def receive_msg(msg):
	global chatroom_list
	if 'ActualNickName' in msg:
		ToUserName = msg['FromUserName']  # 来自哪个群聊
		if ToUserName[1] != '@':
			print("来自自己的消息")
			ToUserName = msg['ToUserName']  # 来自哪个群聊
		FromUserName = msg['ActualUserName']  # 谁发的
		if ToUserName in chatroom_list:
			if FromUserName in chatroom_list[ToUserName]['MemberList']:
				chatroom_list[ToUserName]['MemberList'][FromUserName]['count']+=1
				print("来自",chatroom_list[ToUserName]['NickName'],"成员",chatroom_list[ToUserName]['MemberList'][FromUserName]['NickName'],"计数",chatroom_list[ToUserName]['MemberList'][FromUserName]['count'])
			else:
				print("未找到用户信息，更新")
				myupdate_chatroom_mem(chatroom_list,msg['User']['UserName'],msg['User']['MemberList'])
				if FromUserName in chatroom_list[ToUserName]['MemberList']:
					chatroom_list[ToUserName]['MemberList'][FromUserName]['count']+=1
					print("来自",chatroom_list[ToUserName]['NickName'],"成员",chatroom_list[ToUserName]['MemberList'][FromUserName]['NickName'],"计数",chatroom_list[ToUserName]['MemberList'][FromUserName]['count'])
				else:
					json_dicts=json.dumps(chatroom_list,indent=4, ensure_ascii=False)
					json_dicts=json.dumps(msg,indent=4, ensure_ascii=False)
					print("未找到用户信息，放弃更新计数")
	f=open('wechat.json', 'w')
	f.write(json.dumps(chatroom_list,indent=4, ensure_ascii=False))
	f.close

	summary=[]
	for key in chatroom_list:
		summary_x={}
		summary_x['qunmingcheng'] = chatroom_list[key]['NickName']
		summary_x['qunrenshu'] = chatroom_list[key]['MemberCount']
		mem_l=[]
		for mem in chatroom_list[key]['MemberList']:
			if chatroom_list[key]['MemberList'][mem]['count'] != 0:
				mem_l.append(chatroom_list[key]['MemberList'][mem]['NickName'])
		summary_x['huoyuwrenshu'] = len(mem_l)
		if summary_x['huoyuwrenshu'] != 0:
			summary_x['huoyuedu'] = summary_x['huoyuwrenshu']/float(summary_x['qunrenshu'])
		summary_x['yonghu'] = mem_l
		summary.append(summary_x)
	f=open('data.json', 'w')
	f.write(json.dumps(summary, indent=4, ensure_ascii=False))
	f.close

if __name__ == '__main__':
	with open('wechat.json', 'r') as json_file:
	  chatroom_list = json.load(json_file)

	itchat.auto_login(hotReload=True,enableCmdQR=False)
	chatrooms = itchat.search_chatrooms(name=group_name)
	for i in range(0, len(chatrooms)):
		itchat.update_chatroom(chatrooms[i]['UserName'], detailedMember=True)
		print(chatrooms[i]['UserName'],chatrooms[i]['NickName'],chatrooms[i]['MemberCount'])

	itchat.run()


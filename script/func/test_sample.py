
#			wSubRes = cls.OBJ_TwitterMain.TestRun()
###			wTime = CLS_OSIF.sGetTimeformat_Twitter( "2021-10-06T12:23:44.000Z" )
###			print( str(wTime['TimeDate']) )
#
###			wSubRes = cls.OBJ_TwitterMain.CircleWeekend()
#
#			wSubRes = gVal.OBJ_Tw_IF.GetTweetLookup( "1473387112351559680" )
#			print( str(wSubRes) )
##			wTwitterRes = gVal.OBJ_Tw_IF.GetTweetLookup( "1516980757394190337" )
##			if wTwitterRes['Result']!=True :
##				wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
##				gVal.OBJ_L.Log( "B", wRes )
##				return wRes
###			print( wTwitterRes['Responce'] )
###
###			print( "zzz: " + str(wTwitterRes['Responce']) )
##
##			d = {'k1': 1, 'k2': 2, 'k3': 3}
##			print( str(d) )
##			removed_value = d.pop('k1')
##			print( str(d) )
###			wSubRes = gVal.OBJ_DB_IF.GetRecordNum( "tbl_favouser_data" )
###			print( str(wSubRes) )

##			wSubRes = self.OBJ_Twitter.GetListMember( gVal.STR_UserInfo['ListName'] )
##			if wSubRes['Result']!=True :
##				wRes['Reason'] = "xxxx: " + wSubRes['Reason']
##				gVal.OBJ_L.Log( "B", wRes )
##				return wRes

##			wARR_Dict = {}
##			wARR_Dict.update({ "test1" : 1 })
##			wARR_Dict.update({ "test2" : 2 })
##			wARR_Dict.update({ "test3" : 3 })
##			wARR_Dict.update({ "test4" : 4 })
##			if "test2" in wARR_Dict :
##				print("OK")
##			else:
##				print("NG")
##			
##			if "test5" in wARR_Dict :
##				print("OK")
##			else:
##				print("NG")

###			wSubRes = gVal.OBJ_Tw_IF.ViewList_User( "korei_comm" )

######		
#			wTweetRes = gVal.OBJ_Tw_IF.Tweet( "てすとついーと２" )
#			wTweetRes = gVal.OBJ_Tw_IF.GetSearch( inQuery="てすとついーと２" )
#			print(str( wTweetRes ))
######		
#			wSubRes = gVal.OBJ_Tw_IF.GetLists( "korei_xlix" )
#			print(str( wSubRes ))
######		
#			wTweetRes = gVal.OBJ_Tw_IF.GetSearch( "togenohito " + '\n' + "お願い リスト vtuber をフォローするには当アカウント korei_xlix もフォローしてください。" )
#			print(str( wTweetRes ))
######		
			wGetListsRes = gVal.OBJ_Tw_IF.GetLists( "account" )
			print(str( wGetListsRes['Responce'] ))
######		

#####################################################
# TEST
#####################################################
	def TestRun(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "TestRun"
		
#		#############################
#		# リアクションチェック
#		wSubRes = self.OBJ_TwitterFollower.ReactionCheck()
#		if wSubRes['Result']!=True :
#			wRes['Reason'] = "ReactionCheck"
#			gVal.OBJ_L.Log( "B", wRes )
#			return wRes
#		
#		#############################
#		# いいね情報送信
#		wSubRes = self.OBJ_TwitterFollower.SendFavoDate()
#		if wSubRes['Result']!=True :
#			wRes['Reason'] = "SendFavoDate"
#			gVal.OBJ_L.Log( "B", wRes )
#			return wRes
		
###		#############################
###		# ふぁぼ一覧 取得
###		wFavoRes = gVal.OBJ_Tw_IF.GetFavo()
###		if wFavoRes['Result']!=True :
###			wRes['Reason'] = "GetFavoData is failed"
###			gVal.OBJ_L.Log( "C", wRes )
###			return wRes
###		
		#############################
		# リストいいね
		wSubRes = self.OBJ_TwitterFavo.ListFavo()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "ListFavo"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes




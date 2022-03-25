#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : トラヒック
#####################################################

from osif import CLS_OSIF
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_Traffic():

#####################################################
# トラヒック情報の取得
#####################################################
	@classmethod
	def sGet(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Traffic"
		wRes['Func']  = "Get"
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "PC時間の取得に失敗しました"
			return wRes
		### wTD['TimeDate']
		wARR_TD = wTD['TimeDate'].split(" ")
		
		#############################
		# DBの今日のトラヒック情報取得
		wQuery = "select * from tbl_traffic_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' " + \
					" and day = '" + wARR_TD[0] + "';"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_RateTraffic = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 今日の記録がなければ
		#   =空行を作成する
		if len(wARR_RateTraffic)==0 :
			#############################
			# DBに空行を挿入
			wResIns = cls.__insert_Traffic( wTD['TimeDate'] )
			if wResIns['Result']!=True :
				##失敗
				wRes['Reason'] = "__insert_Traffic is failed: " + CLS_OSIF.sCatErr( wResIns )
				return wRes
		
		#############################
		# 今日の記録があれば
		# [0]を今日とする
		else:
			wARR_RateTraffic = wARR_RateTraffic[0]
			
			wKeylist = list( gVal.STR_TrafficInfo.keys() )
			for wKey in wKeylist :
				if wKey=="update" :
					gVal.STR_TrafficInfo[wKey] = wTD['TimeDate']
				else:
					if wKey in wARR_RateTraffic :
						gVal.STR_TrafficInfo[wKey] = wARR_RateTraffic[wKey]
					else:
						gVal.STR_TrafficInfo[wKey] = 0
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes

	#####################################################
	@classmethod
	def __insert_Traffic( cls, inTimeDate ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Traffic"
		wRes['Func']  = "__insert_Traffic"
		
		#############################
		# 日時だけ取り出し
		wARR_TD = inTimeDate.split(" ")
		
		#############################
		# 空行を挿入
		wQuery = "insert into tbl_traffic_data values (" + \
					"'" + gVal.STR_UserInfo['Account'] + "'," + \
					"'" + str( inTimeDate ) + "'," + \
					"'" + str( inTimeDate ) + "'," + \
					"'" + str( wARR_TD[0] ) + "'," + \
					"false," + \
					"0," + \
					"0, 0," + \
					"0, 0, 0, 0, 0, 0," + \
					"0, 0," + \
					"0, 0, 0, 0," + \
					"0, 0, 0," + \
					"0, 0, 0," + \
					"0, 0," + \
					"0, 0, 0, 0 " + \
					") ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 初期化
		wKeylist = list( gVal.STR_TrafficInfo.keys() )
		for wKey in wKeylist :
			if wKey=="update" :
				gVal.STR_TrafficInfo[wKey] = inTimeDate
			else :
				gVal.STR_TrafficInfo[wKey] = 0
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# トラヒック情報の記録
#####################################################
	@classmethod
	def sSet(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Traffic"
		wRes['Func']  = "Set"
		
		wRes['Responce'] = False
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "PC時間の取得に失敗しました"
			return wRes
		### wTD['TimeDate']
		wARR_NowTD = wTD['TimeDate'].split(" ")
		wARR_NowTD = wARR_NowTD[0].split("-")
		wARR_NowTD = wARR_NowTD[0] + wARR_NowTD[1]
		
		#############################
		# 更新
		wQuery = "update tbl_traffic_data set " + \
					"timeline = " + str( gVal.STR_TrafficInfo['timeline'] ) + "," + \
					"runbot = "   + str( gVal.STR_TrafficInfo['runbot'] ) + "," + \
					"runapi = "   + str( gVal.STR_TrafficInfo['runapi'] ) + "," + \
					"now_myfollow = " + str( gVal.STR_TrafficInfo['now_myfollow'] ) + "," + \
					"now_follower = " + str( gVal.STR_TrafficInfo['now_follower'] ) + "," + \
					"get_myfollow = " + str( gVal.STR_TrafficInfo['get_myfollow'] ) + "," + \
					"get_follower = " + str( gVal.STR_TrafficInfo['get_follower'] ) + "," + \
					"rem_myfollow = " + str( gVal.STR_TrafficInfo['rem_myfollow'] ) + "," + \
					"rem_follower = " + str( gVal.STR_TrafficInfo['rem_follower'] ) + "," + \
					"now_unfollow = "    + str( gVal.STR_TrafficInfo['now_unfollow'] ) + "," + \
					"now_remove = "      + str( gVal.STR_TrafficInfo['now_remove'] ) + "," + \
					"run_unfollow = "      + str( gVal.STR_TrafficInfo['run_unfollow'] ) + "," + \
					"run_unfollowrem = "   + str( gVal.STR_TrafficInfo['run_unfollowrem'] ) + "," + \
					"run_autoremove = "    + str( gVal.STR_TrafficInfo['run_autoremove'] ) + "," + \
					"run_muteremove = "    + str( gVal.STR_TrafficInfo['run_muteremove'] ) + "," + \
					"now_agent = "    + str( gVal.STR_TrafficInfo['now_agent'] ) + "," + \
					"now_vipuser = "  + str( gVal.STR_TrafficInfo['now_vipuser'] ) + "," + \
					"get_reaction = " + str( gVal.STR_TrafficInfo['get_reaction'] ) + "," + \
					"now_favo = " + str( gVal.STR_TrafficInfo['now_favo'] ) + "," + \
					"get_favo = " + str( gVal.STR_TrafficInfo['get_favo'] ) + "," + \
					"rem_favo = " + str( gVal.STR_TrafficInfo['rem_favo'] ) + "," + \
					"send_tweet = "   + str( gVal.STR_TrafficInfo['send_tweet'] ) + "," + \
					"send_retweet = " + str( gVal.STR_TrafficInfo['send_retweet'] ) + "," + \
					"db_req = " + str( gVal.STR_TrafficInfo['db_req'] ) + "," + \
					"db_ins = " + str( gVal.STR_TrafficInfo['db_ins'] ) + "," + \
					"db_up = "  + str( gVal.STR_TrafficInfo['db_up'] ) + "," + \
					"db_del = " + str( gVal.STR_TrafficInfo['db_del'] ) + "," + \
					"update = '" + str( gVal.STR_TrafficInfo['update'] ) + "' " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and day = '" + str( wARR_NowTD[0] ) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 月が変わったか
		wARR_TD = gVal.STR_TrafficInfo['update'].split(" ")
		wARR_TD = wARR_TD[0].split("-")
		wARR_TD = wARR_TD[0] + wARR_TD[1]
		
		if wARR_NowTD!=wARR_TD :
			### 月=変わった
			###   DBに空行を挿入
			wResIns = cls.__insert_Traffic( wTD['TimeDate'] )
			if wResIns['Result']!=True :
				##失敗
				wRes['Reason'] = "__insert_Traffic is failed: " + CLS_OSIF.sCatErr( wResIns )
				return wRes
			wRes['Responce'] = True	#トラヒックが変更したことを知らせる
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 未報告のトラヒック情報を報告する
#####################################################
	@classmethod
	def sReport( cls, inToday=False, inAll=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Traffic"
		wRes['Func']  = "sReport"
		
		wRes['Responce'] = False
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "PC時間の取得に失敗しました"
			return wRes
		### wTD['TimeDate']
		wARR_TD = wTD['TimeDate'].split(" ")
		
		#############################
		# DBの未報告のトラヒック情報取得
		wQuery = "select * from tbl_traffic_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' " + \
					" and reported = False" + \
					" and day = '" + wARR_TD[0] + "'" + \
					" order by day desc ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_RateTraffic = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wReportNum = len( wARR_RateTraffic )
		#############################
		# 未報告の記録がなければ終わり
		if wReportNum==0 :
			wRes['Result'] = True
			return wRes
		
		wReported = 0	#報告した数
		wIndex = 0
		while True :
			#############################
			# 全て報告した
			if wReportNum<=wIndex :
				break
			
			#############################
			# 今日分はスキップする
			if wARR_RateTraffic[wIndex]['day']==wARR_TD[0] and inToday==False :
				wIndex += 1
				continue
			
			#############################
			# 表示する
			cls.__view_Traffic( wARR_RateTraffic[wIndex] )
			
			#############################
			# 報告済みにする
			wQuery = "update tbl_traffic_data set " + \
						"reported = True " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and day = '" + str( wARR_TD[0] ) + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery, False )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			wReported += 1
			wIndex += 1
			
			#############################
			# Twitterに送信する
			wResTwitter = cls.__send_Twitter( wARR_RateTraffic[wIndex] )
			if wResTwitter['Result']!=True :
				##失敗
				wResTwitter['Reason'] = "__send_Twitter is failed(Traffic=True): " + CLS_OSIF.sCatErr( wResTwitter )
				gVal.OBJ_L.Log( "B", wResTwitter )
			
			#############################
			# 1回だけならループ終了
			if inAll==False :
				break
			
		
		#############################
		# 1件以上報告した
		if wReportNum>=1 :
			wRes['Responce'] = True
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes

	#####################################################
	@classmethod
	def __view_Traffic( cls, inTraffic, inConfirm=True ):
		#############################
		# ヘッダ表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "トラヒック情報 報告", False )
		wStr = str( inTraffic['update'] ) + '\n'
		
		#############################
		# 情報の作成
		wStr = wStr + '\n'
		wStr = wStr + "フォロワー情報" + '\n'
		wStr = wStr + "--------------------" + '\n'
		wStr = wStr + "現フォロー者数       : " + str( inTraffic['now_myfollow'] ) + '\n'
		wStr = wStr + "現フォロワー数       : " + str( inTraffic['now_follower'] ) + '\n'
		wStr = wStr + '\n'
		wStr = wStr + "フォロー者獲得数     : " + str( inTraffic['get_myfollow'] ) + '\n'
		wStr = wStr + "フォロワー獲得数     : " + str( inTraffic['get_follower'] ) + '\n'
		wStr = wStr + "リムーブフォロー者数 : " + str( inTraffic['rem_myfollow'] ) + '\n'
		wStr = wStr + "リムーブフォロワー数 : " + str( inTraffic['rem_follower'] ) + '\n'

		wStr = wStr + '\n'
		wStr = wStr + "内部監視情報" + '\n'
		wStr = wStr + "--------------------" + '\n'
		wStr = wStr + "現非フォロワー数     : " + str( inTraffic['now_unfollow'] ) + '\n'
		wStr = wStr + "現疑似リムーブ数     : " + str( inTraffic['now_remove'] ) + '\n'
		wStr = wStr + "現監視ユーザ数       : " + str( inTraffic['now_agent'] ) + '\n'
		wStr = wStr + "現VIPユーザ数数      : " + str( inTraffic['now_vipuser'] ) + '\n'
		wStr = wStr + '\n'
		wStr = wStr + "非フォロー化実行数   : " + str( inTraffic['run_unfollow'] ) + '\n'
		wStr = wStr + "非フォロー化解除数   : " + str( inTraffic['run_unfollowrem'] ) + '\n'
		wStr = wStr + "自動リムーブ実行数   : " + str( inTraffic['run_autoremove'] ) + '\n'
		wStr = wStr + "ミュート解除数       : " + str( inTraffic['run_muteremove'] ) + '\n'
		wStr = wStr + "リアクション獲得数   : " + str( inTraffic['get_reaction'] ) + '\n'
		
		wStr = wStr + '\n'
		wStr = wStr + "いいね情報" + '\n'
		wStr = wStr + "--------------------" + '\n'
		wStr = wStr + "現いいね数           : " + str( inTraffic['now_favo'] ) + '\n'
		wStr = wStr + "いいね実施数         : " + str( inTraffic['get_favo'] ) + '\n'
		wStr = wStr + "いいね解除数         : " + str( inTraffic['rem_favo'] ) + '\n'
		
		wStr = wStr + '\n'
		wStr = wStr + "ツイート情報" + '\n'
		wStr = wStr + "--------------------" + '\n'
		wStr = wStr + "ツイート送信数       : " + str( inTraffic['send_tweet'] ) + '\n'
		wStr = wStr + "リツイート実施数     : " + str( inTraffic['send_retweet'] ) + '\n'
		
		wStr = wStr + '\n'
		wStr = wStr + "データベース情報" + '\n'
		wStr = wStr + "--------------------" + '\n'
		wStr = wStr + "クエリ要求回数       : " + str( inTraffic['db_req'] ) + '\n'
		wStr = wStr + "DB挿入回数           : " + str( inTraffic['db_ins'] ) + '\n'
		wStr = wStr + "DB更新回数           : " + str( inTraffic['db_up'] ) + '\n'
		wStr = wStr + "DB削除回数           : " + str( inTraffic['db_del'] ) + '\n'
		
		wStr = wStr + '\n'
		wStr = wStr + "取得タイムライン数   : " + str( inTraffic['timeline'] ) + '\n'
		wStr = wStr + "Bot実行回数          : " + str( inTraffic['runbot'] ) + '\n'
		wStr = wStr + "Twitter API実行回数  : " + str( inTraffic['runapi'] ) + '\n'
		
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 確認しなくていいなら終了
		if inConfirm==False :
			return
		
		CLS_OSIF.sInp( "確認したらリターンキーを押してください。[RT]" )
		return

	#####################################################
	@classmethod
	def __send_Twitter( cls, inTraffic ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Traffic"
		wRes['Func']  = "__send_Twitter"
		
		#############################
		# 文の組み立て
		wTweet = "Traffic: " + str(gVal.STR_TrafficInfo['update']) + '\n'
		wTweet = "get follower " + str(gVal.STR_TrafficInfo['get_follower']) + '\n'
		wTweet = "rem follower " + str(gVal.STR_TrafficInfo['rem_follower']) + '\n'
		wTweet = "reaction " + str(gVal.STR_TrafficInfo['get_reaction']) + '\n'
		wTweet = "runapi "   + str(gVal.STR_TrafficInfo['runapi']) + '\n'
		
		#############################
		# Twitterに送信
		wTwitterRes = gVal.OBJ_Tw_IF.SendDM( gVal.STR_UserInfo['id'], wTweet )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "SendDM is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# トラヒック情報を表示する
#####################################################
	@classmethod
	def sView(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Traffic"
		wRes['Func']  = "sView"
		
		#############################
		# DBの未報告のトラヒック情報取得
		wQuery = "select * from tbl_traffic_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' " + \
					" order by day desc ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_RateTraffic = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wReportNum = len( wARR_RateTraffic )
		#############################
		# トラヒックがなければ終わり
		if wReportNum==0 :
			wRes['Result'] = True
			return wRes
		
		wIndex = 0
		while True :
			#############################
			# 表示する
			cls.__view_Traffic( wARR_RateTraffic[wIndex], False )
			wIndex += 1
			
			#############################
			# 全て報告した
			if wReportNum<=wIndex :
				break
			
			#############################
			# 停止するか
			wResNext = CLS_OSIF.sInp( '\n' + "次のトラヒック情報を表示しますか？(q=中止 / other=表示する)=> " )
			if wResNext=="y" :
				break
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes




#####################################################
# 現トラヒック表示
#####################################################
	@classmethod
	def sNowView(cls):
		#############################
		# 現トラヒック表示(コンソール)
		cls.__view_Traffic( gVal.STR_TrafficInfo, inConfirm=False )
		
		return




#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 いいね監視系
#####################################################

from ktime import CLS_TIME
from osif import CLS_OSIF
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterFavo():
#####################################################
	OBJ_Parent = ""				#親クラス実体
	
	ARR_FavoUserID = {}
	ARR_OverFavoUserID = {}
	

										###自動いいね 処理モード
	DEF_AUTOFAVO_RETURN_FAVO = 1		#    お返しいいね
	DEF_AUTOFAVO_FOLLOWER_FAVO = 19		#    フォロワー支援



#####################################################
# Init
#####################################################
	def __init__( self, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__init__"
		
		if parentObj==None :
			###親クラス実体の未設定
			wRes['Reason'] = "You have not set the parent class entity for parentObj"
			gVal.OBJ_L.Log( "A", wRes )
			return
		
		self.OBJ_Parent = parentObj
		return



#####################################################
# いいね解除
#####################################################
###	def RemFavo( self, inFLG_FirstDisp=True ):
	def RemFavo( self, inFLG_FirstDisp=True, inFLG_All=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "RemFavo"
		
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "いいね解除中" )
		
		#############################
		# ふぁぼ一覧 取得
		wFavoRes = gVal.OBJ_Tw_IF.GetFavo()
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "GetFavoData is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ふぁぼ一覧 取得
		wARR_TwData = gVal.OBJ_Tw_IF.GetFavoData()
		
		#############################
		# いいねがない場合、処理を終わる
		if len(wARR_TwData)==0 :
			wStr = "いいねがないため、処理を終わります。"
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True	#正常終了
			return wRes
		
		wARR_Tw_ID = list( wARR_TwData.keys() )
		wARR_Tw_ID.reverse()	#逆ソート
		
		#############################
		# 最古のいいねIDを算出
		wARR_Tw_ID_LastKey = wARR_Tw_ID[-1]
		
###		###ウェイト初期化
###		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_Tw_ID ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
###		
		wARR_RemoveID = []
		wRemTweet = 0
		wCancelNum = 0
		#############################
		# 期間を過ぎたいいねを選出する
		for wID in wARR_Tw_ID :
###			###ウェイトカウントダウン
###			if self.OBJ_Parent.Wait_Next()==False :
###				break	###ウェイト中止
###			
			wID = str( wID )
			
			###日時の変換
###			wTime = CLS_OSIF.sGetTimeformat_Twitter( wARR_TwData[wID]['created_at'] )
###			if wTime['Result']!=True :
###				wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wARR_TwData[wID]['created_at'])
###				gVal.OBJ_L.Log( "B", wRes )
###				continue
			if inFLG_All==False :
				wTime = CLS_TIME.sTTchg( wRes, "(1)", wARR_TwData[wID]['created_at'] )
				if wTime['Result']!=True :
					continue
				wARR_TwData[wID]['created_at'] = wTime['TimeDate']
				
				###期間を過ぎているか
				wGetLag = CLS_OSIF.sTimeLag( str(wARR_TwData[wID]['created_at']), inThreshold=gVal.DEF_STR_TLNUM['forRemFavoSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==False :
					###期間内
					###  次へ
					wStr = "○解除対象外: " + str(wARR_TwData[wID]['created_at']) + " : " + str(wARR_TwData[wID]['user']['screen_name'])
					CLS_OSIF.sPrn( wStr )
					wCancelNum += 1
					if gVal.DEF_STR_TLNUM['favoCancelNum']<=wCancelNum :
						### 規定回数のスキップなので処理停止
						break
					continue
				
				wCancelNum = 0
			
###			###  いいねを外す
###			wRemoveRes = gVal.OBJ_Tw_IF.FavoRemove( wID )
###			if wRemoveRes['Result']!=True :
###				wRes['Reason'] = "Twitter Error"
###				gVal.OBJ_L.Log( "B", wRes )
###			
###			if wRemoveRes['Responce']['Run']==True :
###				wTextReason = "●解除いいね日時: id=" + str(wID) + ": " + str(wRemoveRes['Responce']['Data']['created_at']) + " : " + str(wRemoveRes['Responce']['Data']['user']['screen_name'])
###				gVal.OBJ_L.Log( "T", wRes, wTextReason )
###				
###				wRemTweet += 1
###			else:
###				wRes['Reason'] = "FavoRemove failed: id=" + str(wID)
###				gVal.OBJ_L.Log( "D", wRes )
###				return wRes
			#############################
			# 対象なのでIDを詰める
			wARR_RemoveID.append( wID )
			
			#############################
			# 正常
			continue	#次へ
		
		#############################
		# 処理数の表示
		wStr = "いいね解除対象数= " + str(len( wARR_Tw_ID )) + " 個" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_RemoveID ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		wRemTweet = 0
		#############################
		# 選出したいいねを解除していく
		for wID in wARR_RemoveID :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			wID = str( wID )
			
			#############################
			# いいねを外す
			wRemoveRes = gVal.OBJ_Tw_IF.FavoRemove( wID )
			if wRemoveRes['Result']!=True :
				wRes['Reason'] = "Twitter Error"
				gVal.OBJ_L.Log( "B", wRes )
			
			if wRemoveRes['Responce']['Run']==True :
				wTextReason = "いいね解除: id=" + str(wID) + ": " + str(wRemoveRes['Responce']['Data']['created_at']) + " : " + str(wRemoveRes['Responce']['Data']['user']['screen_name'])
				gVal.OBJ_L.Log( "T", wRes, wTextReason )
				
				wRemTweet += 1
			else:
				wRes['Reason'] = "FavoRemove failed: id=" + str(wID)
				gVal.OBJ_L.Log( "D", wRes )
		
		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "Twitterいいね数  : " + str( len(wARR_Tw_ID) )+ '\n'
		wStr = wStr + "いいね解除対象数 : " + str( len( wARR_Tw_ID ) )+ '\n'
		wStr = wStr + "いいね解除実施数 : " + str( wRemTweet )+ '\n'
		wStr = wStr + "最古いいね日時   : " + str( str( wARR_TwData[wARR_Tw_ID_LastKey]['created_at'] ) )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# いいね全解除
#####################################################
###	def AllFavoRemove( self, inFLG_FirstDisp=True ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterFavo"
###		wRes['Func']  = "AllFavoRemove"
###		
###		#############################
###		# 取得開始の表示
###		if inFLG_FirstDisp==True :
###			wResDisp = CLS_MyDisp.sViewHeaderDisp( "全てのいいね解除中" )
###		
###		#############################
###		# ふぁぼ一覧 取得
###		wFavoRes = gVal.OBJ_Tw_IF.GetFavo()
###		if wFavoRes['Result']!=True :
###			wRes['Reason'] = "GetFavoData is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# ふぁぼ一覧 取得
###		wARR_TwData = gVal.OBJ_Tw_IF.GetFavoData()
###		
###		#############################
###		# いいねがない場合、処理を終わる
###		if len(wARR_TwData)==0 :
###			wStr = "いいねがないため、処理を終わります。"
###			CLS_OSIF.sPrn( wStr )
###			wRes['Result'] = True	#正常終了
###			return wRes
###		
###		wARR_Tw_ID = list( wARR_TwData.keys() )
###		
###		#############################
###		# 処理数の表示
###		wStr = "いいね数= " + str(len( wARR_Tw_ID )) + " 個" + '\n'
###		CLS_OSIF.sPrn( wStr )
###		
###		###ウェイト初期化
###		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_Tw_ID ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
###		
###		wRemTweet = 0
###		#############################
###		# 期間を過ぎたいいねを解除していく
###		for wID in wARR_Tw_ID :
###			###ウェイトカウントダウン
###			if self.OBJ_Parent.Wait_Next()==False :
###				break	###ウェイト中止
###			
###			wID = str( wID )
###			
###			###  いいねを外す
###			wRemoveRes = gVal.OBJ_Tw_IF.FavoRemove( wID )
###			if wRemoveRes['Result']!=True :
###				wRes['Reason'] = "Twitter Error"
###				gVal.OBJ_L.Log( "B", wRes )
###			
###			if wRemoveRes['Responce']['Run']==True :
###				wTextReason = "●解除いいね日時: id=" + str(wID) + ": " + str(wRemoveRes['Responce']['Data']['created_at']) + " : " + str(wRemoveRes['Responce']['Data']['user']['screen_name'])
###				gVal.OBJ_L.Log( "T", wRes, wTextReason )
###				
###				wRemTweet += 1
###			else:
###				wRes['Reason'] = "FavoRemove failed: id=" + str(wID)
###				gVal.OBJ_L.Log( "D", wRes )
###				return wRes
###			
###			#############################
###			# 正常
###			continue	#次へ
###		
###		#############################
###		# 取得結果の表示
###		wStr = ""
###		if inFLG_FirstDisp==False :
###			wStr = "------------------------------" + '\n'
###		wStr = wStr + "Twitterいいね数  : " + str( len(wARR_Tw_ID) )+ '\n'
###		wStr = wStr + "いいね解除数     : " + str( wRemTweet )+ '\n'
###		CLS_OSIF.sPrn( wStr )
###		
###		#############################
###		# 正常終了
###		wRes['Result'] = True
###		return wRes
###
###

#####################################################
# リストいいね
#####################################################
	def ListFavo( self, inFLG_FirstDisp=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "ListFavo"
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['mffavo'] ), inThreshold=gVal.DEF_STR_TLNUM['forListFavoSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			### 規定以内は除外
			wStr = "●リストいいね期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		self.ARR_FavoUserID = {}
		self.ARR_OverFavoUserID = {}
		wResult = {
			"Over_TweetNum"	: 0,
			"Over_RunFavo"	: 0,
		}
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リストいいね実行中" )
		
		#############################
		# リストいいね指定の処理
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		for wKey in wKeylist :
			### 無効ならスキップ
			if gVal.ARR_ListFavo[wKey]['valid']!=True :
				continue
			
			#############################
			# リストの表示
			wStr = "******************************" + '\n'
			wStr = wStr + "処理中リスト: @" + gVal.ARR_ListFavo[wKey]['screen_name'] + "/ " + gVal.ARR_ListFavo[wKey]['list_name'] + '\n'
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# ユーザIDの取得
			wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=gVal.ARR_ListFavo[wKey]['screen_name'] )
			if wUserInfoRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: @" + gVal.ARR_ListFavo[wKey]['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			### IDの取得
			wUserID = str( wUserInfoRes['Responce']['id'] )
			
			#############################
			# リストIDの取得
			wListsRes = gVal.OBJ_Tw_IF.GetListID(
			   inListName=gVal.ARR_ListFavo[wKey]['list_name'],
			   inScreenName=gVal.ARR_ListFavo[wKey]['screen_name'] )
			
			if wListsRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: GetListID"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			### List IDの取得
			wListID = str( wListsRes['Responce'] )
			
			#############################
			# タイムラインを取得する
			wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="list", inFLG_Rep=True, inFLG_Rts=True,
				 inID=wUserID, inListID=wListID,
				 inCount=gVal.DEF_STR_TLNUM['getUserTimeLine'] )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: GetTL"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if len(wTweetRes['Responce'])==0 :
				### ツイートが取得できないのでスキップ
				continue
			wResult['Over_TweetNum'] += len( wTweetRes['Responce'] )
			
			###ウェイト初期化
			self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
			
			wFLG_ZanCountSkip = False
			for wTweet in wTweetRes['Responce'] :
				###ウェイトカウントダウン
				if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
					break	###ウェイト中止
				wFLG_ZanCountSkip = False
				
				wUserID = str(wTweet['user']['id'])
				#############################
				# 自動いいね
				wResFavo = self.OverAutoFavo( wTweet, gVal.ARR_ListFavo[wKey] )
				if wResFavo['Result']!=True :
					wRes['Reason'] = "Twitter Error"
					gVal.OBJ_L.Log( "B", wRes )
					continue
				
				if wResFavo['Responce']['flg_favo_run']==True :
					### いいね実施数をカウント
					wResult['Over_RunFavo'] += 1
				else:
					### いいねを実実行しなければループ待機スキップする
					wFLG_ZanCountSkip = True
				
				if wResFavo['Responce']['flg_favo']==True :
					### いいね済み扱いはスキップ
					wFLG_ZanCountSkip = True
		
 		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "外部 ツイート総数  : " + str( wResult['Over_TweetNum'] )+ '\n'
		wStr = wStr + "外部 いいね実施数  : " + str( wResult['Over_RunFavo'] )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "mffavo", gVal.STR_Time['TimeDate'] )
		if wListRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['mffavo']
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes

	#####################################################
	def ListFavo_single( self, inIndex, inFLG_FirstDisp=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "ListFavo_single"
		
#		self.ARR_FavoUserID = {}
#		self.ARR_OverFavoUserID = {}
		wResult = {
			"Over_TweetNum"	: 0,
			"Over_RunFavo"	: 0,
		}
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リストいいね実行中" )
		
		#############################
		# リストの表示
		wStr = "******************************" + '\n'
		wStr = wStr + "処理中リスト: @" + gVal.ARR_ListFavo[inIndex]['screen_name'] + "/ " + gVal.ARR_ListFavo[inIndex]['list_name'] + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# ユーザIDの取得
		wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=gVal.ARR_ListFavo[inIndex]['screen_name'] )
		if wUserInfoRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: @" + gVal.ARR_ListFavo[inIndex]['screen_name']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		### IDの取得
		wUserID = str( wUserInfoRes['Responce']['id'] )
		
		#############################
		# リストIDの取得
		wListsRes = gVal.OBJ_Tw_IF.GetListID(
		   inListName=gVal.ARR_ListFavo[inIndex]['list_name'],
		   inScreenName=gVal.ARR_ListFavo[inIndex]['screen_name'] )
		
		if wListsRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetListID"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		### List IDの取得
		wListID = str( wListsRes['Responce'] )
		
		#############################
		# タイムラインを取得する
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="list", inFLG_Rep=True, inFLG_Rts=True,
			 inID=wUserID, inListID=wListID,
			 inCount=gVal.DEF_STR_TLNUM['getUserTimeLine'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetTL"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if len(wTweetRes['Responce'])==0 :
			### ツイートが取得できないのでスキップ
			return wRes
		wResult['Over_TweetNum'] += len( wTweetRes['Responce'] )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		wFLG_ZanCountSkip = False
		for wTweet in wTweetRes['Responce'] :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
				break	###ウェイト中止
			wFLG_ZanCountSkip = False
			
			wUserID = str(wTweet['user']['id'])
			#############################
			# 自動いいね
			wResFavo = self.OverAutoFavo( wTweet, gVal.ARR_ListFavo[inIndex] )
			if wResFavo['Result']!=True :
				wRes['Reason'] = "Twitter Error"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			if wResFavo['Responce']['flg_favo_run']==True :
				### いいね実施数をカウント
				wResult['Over_RunFavo'] += 1
			else:
				### いいねを実実行しなければループ待機スキップする
				wFLG_ZanCountSkip = True
			
			if wResFavo['Responce']['flg_favo']==True :
				### いいね済み扱いはスキップ
				wFLG_ZanCountSkip = True
		
		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "外部 ツイート総数  : " + str( wResult['Over_TweetNum'] )+ '\n'
		wStr = wStr + "外部 いいね実施数  : " + str( wResult['Over_RunFavo'] )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# フォロワーいいね
#####################################################
	def FollowerFavo( self, inFLG_FirstDisp=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "FollowerFavo"
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['flfavo'] ), inThreshold=gVal.DEF_STR_TLNUM['forListFavoFollowerSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			### 規定以内は除外
			wStr = "●フォロワー支援いいね期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		wResult = {
			"UserNum"	: 0,
			"RunFavo"	: 0
		}
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "フォロワー支援いいね実行中" )
		
		#############################
		# フォロー情報取得
		wARR_FollowData = gVal.OBJ_Tw_IF.GetFollowerData()
		wResult['UserNum'] = len( wARR_FollowData )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_FollowData ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		#############################
		# フォロー、フォロワー含まないリストへの
		# フォロワーへのいいね支援
		wFLG_ZanCountSkip = False
		wKeylist = list( wARR_FollowData.keys() )
		for wUserID in wKeylist :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
				break	###ウェイト中止
			wFLG_ZanCountSkip = False
			
			wUserID = str(wUserID)
			
			### フォロワーでなければ スキップ
			if wARR_FollowData[wUserID]['follower']!=True :
				wFLG_ZanCountSkip = True
				continue
			
			#############################
			# DBからいいね情報を取得する(1個)
###			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( wARR_FollowData[wUserID] )
			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( wARR_FollowData[wUserID], inFLG_New=False )
			if wDBRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB未登録ならスキップ
			if wDBRes['Responce']['Data']==None :
				continue
			wARR_DBData = wDBRes['Responce']['Data']
			
			#############################
			# 自動いいね
			wResFavo = self.AutoFavo( wARR_FollowData[wUserID], wARR_DBData, inMode=self.DEF_AUTOFAVO_FOLLOWER_FAVO )
			if wResFavo['Result']!=True :
				wRes['Reason'] = "Twitter Error"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			if wResFavo['Responce']['flg_favo_run']==True :
				### いいね実施数をカウント
				wResult['RunFavo'] += 1
			else:
				### いいねを実実行しなければループ待機スキップする
				wFLG_ZanCountSkip = True
			
			if wResFavo['Responce']['flg_favo']==True :
				### いいね済み扱いはスキップ
				wFLG_ZanCountSkip = True
		
 		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "支援 対象ユーザ数  : " + str( wResult['UserNum'] )+ '\n'
		wStr = wStr + "支援 いいね実施数  : " + str( wResult['RunFavo'] )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "flfavo", gVal.STR_Time['TimeDate'] )
		if wListRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['flfavo']
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 自動いいね
#####################################################
	def AutoFavo( self, inUser, inData, inMode=DEF_AUTOFAVO_RETURN_FAVO ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "AutoFavo"
		
		#############################
		# 自動いいね基本動作
		# ユーザのタイムラインのうち以下をいいねする
		# ・期間内のツイート
		# ・フォロワー支援いいねの場合、相互はスパン短い、フォロワーはスパンが長い
		# ・おかえしいいねは、スパン短い
		# ・リプライ、リツイート、引用リツイート、センシティブツイート、禁止ユーザは除外
		# ・いいね一覧にあった場合は除外
		# ・禁止文字含めは除外
		wRes['Responce'] = {
			"flg_favo"			: False,
			"flg_favo_run"		: False
		}
		
		wUserID = str( inData['id'] )
		#############################
		# いいね一覧にあるユーザへは
		# おかえししない
		wTweetRes = gVal.OBJ_Tw_IF.CheckFavoUser( wUserID )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: CheckFavoUser"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wTweetRes['Responce']==True :
			### いいね済み
			wStr = "●自動いいね中止(いいね済ユーザ): " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# 禁止ユーザは除外
		wUserRes = self.OBJ_Parent.CheckExtUser( inData, "自動いいね中止" )
		if wUserRes['Result']!=True :
			wRes['Reason'] = "CheckExtUser failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wUserRes['Responce']==False :
			### 禁止あり=除外
			wRes['Result'] = True
			return wRes
		
		#############################
		# リストいいね期間外
		if inMode==self.DEF_AUTOFAVO_FOLLOWER_FAVO :
			### フォロワー支援いいね
			if gVal.OBJ_Tw_IF.CheckMyFollow( wUserID)==True :
				### 相互フォロー者へ
				wLFavoDateLen = gVal.DEF_STR_TLNUM['forListFavoMyFollowFavoSec']
			else:
				### 片フォロワーへ
				wLFavoDateLen = gVal.DEF_STR_TLNUM['forListFavoFollowerFavoSec']
		else:
			### お返しいいね
			wLFavoDateLen = gVal.DEF_STR_TLNUM['forListFavoReturnFavoSec']
		
###		if inData['lfavo_date']!=None and inData['lfavo_date']!="" :
###			wGetLag = CLS_OSIF.sTimeLag( str( inData['lfavo_date'] ), inThreshold=wLFavoDateLen )
		if inData['pfavo_date']==gVal.DEF_NOTEXT :
			wGetLag = CLS_OSIF.sTimeLag( str( inData['pfavo_date'] ), inThreshold=wLFavoDateLen )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				### 規定内は処理しない
				wStr = "●自動いいね中止(いいね期間内): " + inData['screen_name'] + " timedate=" + str(inData['lfavo_date']) + '\n' ;
				CLS_OSIF.sPrn( wStr )
				
				wRes['Result'] = True
				return wRes
		
		#############################
		# タイムラインを取得する
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
			 inID=wUserID, inCount=gVal.DEF_STR_TLNUM['getUserTimeLine'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetTL"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if len(wTweetRes['Responce'])==0 :
			### ツイートが取得できないのでスキップ
			wStr = "●自動いいね中止(ツイートなし): " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		wFavoID = None
		#############################
		# ツイートチェック
		# 以下は除外
		# ・リプライ
		# ・リツイート
		# ・引用リツイート
		# ・規定期間外のツイート
		# 該当なしは いいねしない
		for wTweet in wTweetRes['Responce'] :
			###日時の変換
			wTime = CLS_TIME.sTTchg( wRes, "(2)", wTweet['created_at'] )
			if wTime['Result']!=True :
				continue
			wTweet['created_at'] = wTime['TimeDate']
			
			wTweetID = str( wTweet['id'] )
			### リツイートは除外
			if "retweeted_status" in wTweet :
				continue
			### 引用リツイートは除外
			if "quoted_status" in wTweet :
				continue
			### リプライは除外
			if wTweet['text'].find("@")>=0 :
				continue
			### センシティブなツイートは除外
			if "possibly_sensitive" in wTweet :
				if str(wTweet['possibly_sensitive'])=="true" :
					continue
			
			### 範囲時間内のツイートか
			wGetLag = CLS_OSIF.sTimeLag( str( wTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forListFavoAutoFavoTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				### 規定外 =古いツイートなので除外
				continue
			
			### discriptionチェック
			wWordRes = self.OBJ_Parent.CheckExtWord( inData, inUser['description'] )
			if wWordRes['Result']!=True :
				wRes['Reason'] = "CheckExtWord failed(description)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wWordRes['Responce']==False :
				### 除外
				continue
			
			### ツイートチェック
			wWordRes = self.OBJ_Parent.CheckExtWord( inData, wTweet['text'] )
			if wWordRes['Result']!=True :
				wRes['Reason'] = "CheckExtWord failed(word)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wWordRes['Responce']==False :
				### 除外
				continue
			
			### ※いいねツイート確定
			wFavoID = wTweetID
			break
		
		#############################
		# いいねツイートなしはおわり
		if wFavoID==None :
			wStr = "●自動いいね中止(対象なし): " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# いいねする
		wSubRes = gVal.OBJ_Tw_IF.Favo( wFavoID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(Favo): user=" + inData['screen_name'] + " id=" + str(wFavoID)
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wStr = "--------------------" + '\n' ;
		if wSubRes['Responce']['Run']==True :
			if inMode==self.DEF_AUTOFAVO_FOLLOWER_FAVO :
				### フォロワー支援いいね
				wTextReason = "自動いいね（フォロワー支援） 実施: user=" + inData['screen_name'] + " id=" + str(wFavoID)
			else:
				### お返しいいね
				wTextReason = "自動いいね（お返し） 実施: user=" + inData['screen_name'] + " id=" + str(wFavoID)
			gVal.OBJ_L.Log( "T", wRes, wTextReason )
			
			wRes['Responce']['flg_favo_run'] = True		#いいね済み
		else :
			wStr = wStr + "●自動いいね中止(いいね被り): " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# 1個取り出す
###		wResDBData = gVal.OBJ_DB_IF.GetFavoDataOne( inData )
		wResDBData = gVal.OBJ_DB_IF.GetFavoDataOne( inData, inFLG_New=False )
		if wResDBData['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB登録なし
		if wResDBData['Responce']['Data']==None :
			### 正常
			wRes['Result'] = True
			return wRes
		
		wARR_DBData = wResDBData['Responce']['Data']
		
		#############################
		# いいね情報：いいね送信更新
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Put( inData, wFavoID, wARR_DBData )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "UpdateFavoData_Put is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Responce']['flg_favo'] = True		#いいね済み
		wRes['Result'] = True
		return wRes



#####################################################
# 外部自動いいね
#####################################################
	def OverAutoFavo( self, inData, inListFavoData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "OverAutoFavo"
		
		#############################
		# 外部いいね基本動作
		# 設定リストのタイムラインのうち以下をいいねする
		# ・期間内のツイート
		# ・前回のいいね期間内（相互はスパン短い、フォロワーはスパンが長い）
		# ・今処理では1回のみ
		# ・処理規定回数以内
		# ・リプライ、センシティブツイート、禁止ユーザは除外
		# ・フォロー者・フォロワーは除外（オプションで含め化）
		# ・いいね一覧にあった場合は除外
		# ・禁止文字含めは除外
		wRes['Responce'] = {
			"flg_favo"			: False,
			"flg_favo_run"		: False,
			"data"				: None
		}
		
		#############################
		# ツイートj情報を丸めこむ
		wFavoID = str( inData['id'] )
		wSTR_User = {
			"id"				: None,
			"name"				: None,
			"screen_name"		: None,
			"description"		: None
		}
		wSTR_SrcUser = {
			"id"				: None,
			"name"				: None,
			"screen_name"		: None,
			"description"		: None
		}
		wSTR_Tweet = {
			"kind"				: None,
			"id"				: wFavoID,
			"text"				: inData['text'],
			"created_at"		: None,
			"user"				: wSTR_User,
			"src_user"			: wSTR_SrcUser
		}
		
		### リツイート
		if "retweeted_status" in inData :
			wSTR_Tweet['kind'] = "retweet"
			wUserID = str( inData['retweeted_status']['user']['id'] )
			wName   = inData['retweeted_status']['user']['name'].replace( "'", "''" )
			wSN     = inData['retweeted_status']['user']['screen_name']
			wDisk   = inData['retweeted_status']['user']['description']
			wCrAt   = str(inData['retweeted_status']['created_at'])
			
			wSTR_Tweet['src_user']['id'] = str( inData['user']['id'] )
			wSTR_Tweet['src_user']['name']        = inData['user']['name'].replace( "'", "''" )
			wSTR_Tweet['src_user']['screen_name'] = inData['user']['screen_name']
			wSTR_Tweet['src_user']['description'] = inData['user']['description']
		
		### 引用リツイート
		elif "quoted_status" in inData :
			wSTR_Tweet['kind'] = "quoted"
			wUserID = str( inData['quoted_status']['user']['id'] )
			wName   = inData['quoted_status']['user']['name'].replace( "'", "''" )
			wSN     = inData['quoted_status']['user']['screen_name']
			wDisk   = inData['quoted_status']['user']['description']
			wCrAt   = str(inData['quoted_status']['created_at'])
			
			wSTR_Tweet['src_user']['id'] = str( inData['user']['id'] )
			wSTR_Tweet['src_user']['name']        = inData['user']['name'].replace( "'", "''" )
			wSTR_Tweet['src_user']['screen_name'] = inData['user']['screen_name']
			wSTR_Tweet['src_user']['description'] = inData['user']['description']
		
		### リプライ
		elif wSTR_Tweet['text'].find("@")>=0 :
			wSTR_Tweet['kind'] = "reply"
			wUserID = str( inData['user']['id'] )
			wName   = inData['user']['name'].replace( "'", "''" )
			wSN     = inData['user']['screen_name']
			wDisk   = inData['user']['description']
			wCrAt   = str(inData['created_at'])
		
		### 通常ツイート
		else:
			wSTR_Tweet['kind'] = "normal"
			wUserID = str( inData['user']['id'] )
			wName   = inData['user']['name'].replace( "'", "''" )
			wSN     = inData['user']['screen_name']
			wDisk   = inData['user']['description']
			wCrAt   = str(inData['created_at'])
		
		#############################
		# 今処理で同一ユーザへの処理は除外
		if wUserID in self.ARR_FavoUserID :
#			wStr = "●外部いいね中止(同一ユーザ): " + wName + '\n' ;
#			CLS_OSIF.sPrn( wStr )
			### 同一ユーザ検出 =終了
			self.ARR_FavoUserID[wUserID] += 1
			wRes['Result'] = True
			return wRes
		else:
			### ユーザをメモする
			self.ARR_FavoUserID.update({ wUserID : 1 })
		
		#############################
		# 規定以上の外部ユーザへの処理は除外
		if wSTR_Tweet['kind']=="retweet" or wSTR_Tweet['kind']=="quoted" :
			wOverUserID = wSTR_Tweet['src_user']['id']
			
			if wOverUserID in self.ARR_OverFavoUserID :
				if self.ARR_OverFavoUserID[wOverUserID]>=gVal.DEF_STR_TLNUM['forOverListFavoCount'] :
					### 規定回数超え
#					wStr = "●外部いいね中止(外部ユーザ規定数): " + wName + '\n' ;
#					CLS_OSIF.sPrn( wStr )
					wRes['Result'] = True
					return wRes
				else:
					self.ARR_OverFavoUserID[wOverUserID] += 1
			else:
				### ユーザをメモする
				self.ARR_OverFavoUserID.update({ wOverUserID : 1 })
		
		### ユーザ情報のセット
		wSTR_Tweet['user']['id'] = wUserID
		wSTR_Tweet['user']['name']        = wName
		wSTR_Tweet['user']['screen_name'] = wSN
		wSTR_Tweet['user']['description'] = wDisk
		wSTR_Tweet['created_at'] = wCrAt
		wRes['Responce']['data']     = wSTR_Tweet
		
		#############################
		# リプライの場合は除外
		if wSTR_Tweet['kind']=="reply" :
			wStr = "●外部いいね中止(リプライ): " + wSTR_Tweet['user']['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# センシティブなツイートは除外
		if inListFavoData['sensitive']==False :
			if "possibly_sensitive" in inData :
				if str(inData['possibly_sensitive'])=="true" :
					wStr = "●外部いいね中止(センシティブ): " + wSTR_Tweet['user']['screen_name'] + '\n' ;
					CLS_OSIF.sPrn( wStr )
					
					wRes['Responce']['flg_favo'] = True		#いいね済み扱い
					wRes['Result'] = True
					return wRes
		
		#############################
		# 禁止ユーザは除外
		wFLG_ExtUser = False
		### 禁止ユーザか
		wUserRes = self.OBJ_Parent.CheckExtUser( wSTR_Tweet['user'], "外部いいね中止" )
		if wUserRes['Result']!=True :
			wRes['Reason'] = "CheckExtUser failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wUserRes['Responce']==False :
			### 禁止あり=除外
			wFLG_ExtUser = True
		
		### リツイート、引用リツイートの場合、ソースが禁止ユーザか
		if wSTR_Tweet['kind']=="retweet" or wSTR_Tweet['kind']=="quoted" :
			wUserRes = self.OBJ_Parent.CheckExtUser( wSTR_Tweet['src_user'], "外部いいね中止（リツイ元ユーザ）" )
			if wUserRes['Result']!=True :
				wRes['Reason'] = "CheckExtUser failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wUserRes['Responce']==False :
				### 禁止あり=除外
				wFLG_ExtUser = True
		
		if wFLG_ExtUser!=False :
			### 禁止あり=除外
			wRes['Responce']['flg_favo'] = True		#いいね済み扱い
			wRes['Result'] = True
			return wRes
		
		#############################
		# フォロー者、フォロワーを含めない場合
		#   フォロー者、フォロワーを除外
		wFLG_MyFollow = gVal.OBJ_Tw_IF.CheckMyFollow( wUserID)
		if inListFavoData['follow']!=True :
			if wFLG_MyFollow==True :
#				wStr = "●外部いいね中止(フォロー者): " + wSTR_Tweet['user']['screen_name'] + '\n' ;
#				CLS_OSIF.sPrn( wStr )
#				
				wRes['Result'] = True
				return wRes
			
			if gVal.OBJ_Tw_IF.CheckFollower( wUserID)==True :
#				wStr = "●外部いいね中止(フォロワー): " + wSTR_Tweet['user']['screen_name'] + '\n' ;
#				CLS_OSIF.sPrn( wStr )
#				
				wRes['Result'] = True
				return wRes
		
		#############################
		# 期間を過ぎたツイートは除外
		wTime = CLS_TIME.sTTchg( wRes, "(3)", wSTR_Tweet['created_at'] )
		if wTime['Result']!=True :
			return wRes
		###wTweet['created_at'] = wTime['TimeDate']
		
		wGetLag = CLS_OSIF.sTimeLag( str( wTime['TimeDate'] ), inThreshold=gVal.DEF_STR_TLNUM['forListFavoOverTweetSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==True :
			### 規定外 =古いツイートなので除外
			wStr = "●外部いいね中止(期間外のツイート): " + wSTR_Tweet['user']['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Responce']['flg_favo'] = True		#いいね済み扱い
			wRes['Result'] = True
			return wRes
		
		#############################
		# いいね一覧にあるユーザは除外
		wTweetRes = gVal.OBJ_Tw_IF.CheckFavoUser( wUserID )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: CheckFavoUser"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wTweetRes['Responce']==True :
			wStr = "●外部いいね中止(いいね済ユーザ): " + wSTR_Tweet['user']['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Responce']['flg_favo'] = True		#いいね済み扱い
			wRes['Result'] = True
			return wRes
		
		#############################
		# 禁止文字を含む場合は除外
		wWordRes = self.OBJ_Parent.CheckExtWord( wSTR_Tweet['user'], wSTR_Tweet['user']['description'] )
		if wWordRes['Result']!=True :
			wRes['Reason'] = "CheckExtWord failed(description)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wWordRes['Responce']==False :
			wStr = "●外部いいね中止(プロフ禁止文字): " + wSTR_Tweet['user']['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		wWordRes = self.OBJ_Parent.CheckExtWord( wSTR_Tweet['user'], wSTR_Tweet['text'] )
		if wWordRes['Result']!=True :
			wRes['Reason'] = "CheckExtWord failed(word)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wWordRes['Responce']==False :
			wStr = "●外部いいね中止(ツイート禁止文字): " + wSTR_Tweet['user']['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		wNewUser = False
		#############################
		# DBからいいね情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( inData )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録（ありえない）
		if wSubRes['Responce']['Data']==None :
###			wRes['Reason'] = "GetFavoDataOne(3) is failed"
			wRes['Reason'] = "GetFavoDataOne is no data"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']['FLG_New']==True :
			wNewUser = True	#新規登録
			#############################
			# 新規情報の設定
			wSubRes = self.OBJ_Parent.SetNewFavoData( inUser, wSubRes['Responce']['Data'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "SetNewFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wARR_DBData = wSubRes['Responce']['Data']
		
		#############################
		# 前回からのいいね期間内は除外
		if wFLG_MyFollow==True :
			wListFavoSec = gVal.DEF_STR_TLNUM['forListFavoOverMyFollowSec']
		else:
			wListFavoSec = gVal.DEF_STR_TLNUM['forListFavoOverNoFollowSec']
		
		if wARR_DBData['pfavo_date']==gVal.DEF_NOTEXT :
			wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['pfavo_date'] ), inThreshold=wListFavoSec )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				### 規定内は処理しない
				wStr = "●外部いいね中止(前回から期間内): " + wSTR_Tweet['user']['screen_name'] + '\n' ;
				CLS_OSIF.sPrn( wStr )
				
				wRes['Responce']['flg_favo'] = True		#いいね済み扱い
				wRes['Result'] = True
				return wRes
		
		#############################
		# いいねする
		wSubRes = gVal.OBJ_Tw_IF.Favo( wFavoID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(Favo): user=" + wSTR_Tweet['user']['screen_name'] + " id=" + str(wFavoID)
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		if wSubRes['Responce']['Run']==True :
			if wSTR_Tweet['kind']=="retweet" or wSTR_Tweet['kind']=="quoted" :
				wTextReason = "外部いいね 実施: user=" + wSTR_Tweet['user']['screen_name'] + " id=" + str(wFavoID)
				wTextReason = wTextReason + " src_user=" + wSTR_Tweet['src_user']['screen_name']
			else:
				wTextReason = "外部いいね 実施: user=" + wSTR_Tweet['user']['screen_name'] + " id=" + str(wFavoID)
			gVal.OBJ_L.Log( "T", wRes, wTextReason )
			
			wRes['Responce']['flg_favo_run'] = True		#いいね済み
		else :
			wStr = "●外部いいね中止(いいね被り): " + wSTR_Tweet['user']['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# いいね情報：いいね送信更新
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Put( wSTR_Tweet['user'], wFavoID, wARR_DBData )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "UpdateListFavoData is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Responce']['flg_favo'] = True		#いいね済み
		wRes['Result'] = True
		return wRes



#####################################################
# リストいいね設定
#####################################################
	def SetListFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "SetListFavo"
		
		#############################
		# コンソールを表示
		while True :
			
			#############################
			# データ表示
			self.__view_ListFavo()
			
			#############################
			# 実行の確認
			wListNumber = CLS_OSIF.sInp( "コマンド？(\\q=中止)=> " )
			if wListNumber=="\\q" :
				###  設定をセーブして終わる
				wSubRes = gVal.OBJ_DB_IF.SaveListFavo()
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SaveListFavo is failed"
					gVal.OBJ_L.Log( "B", wRes )

				wRes['Result'] = True
				return wRes
			
			#############################
			# コマンド処理
			wCommRes = self.__run_ListFavo( wListNumber )
			if wCommRes['Result']!=True :
				wRes['Reason'] = "__run_ListFavo is failed: " + wCommRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# 画面表示
	#####################################################
	def __view_ListFavo(self):
		
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		wListNum = 1
		wStr = ""
		for wI in wKeylist :
			wStr = wStr + "   : "
			
			### リスト番号
###			wListData = wI + 1
			wListData = str(gVal.ARR_ListFavo[wI]['list_number'])
###			wListData = str(wListData)
			wListNumSpace = 4 - len( wListData )
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + "  "
			
			### 有効/無効
			if gVal.ARR_ListFavo[wI]['valid']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### フォロー者、フォロワーを含める
			if gVal.ARR_ListFavo[wI]['follow']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### 警告の有無
			if gVal.ARR_ListFavo[wI]['caution']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### センシティブツイートを含める
			if gVal.ARR_ListFavo[wI]['sensitive']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### 自動リムーブ
			if gVal.ARR_ListFavo[wI]['auto_rem']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "    "
			
			### ユーザ名（screen_name）
			wListData = gVal.ARR_ListFavo[wI]['screen_name']
			wListNumSpace = gVal.DEF_SCREEN_NAME_SIZE - len(wListData)
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + ": "
			
			### リスト名
			wListData = gVal.ARR_ListFavo[wI]['list_name']
			wStr = wStr + wListData
			
			wStr = wStr + '\n'
		
		wResDisp = CLS_MyDisp.sViewDisp( inDisp="ListFavoConsole", inIndex=-1, inData=wStr )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "D", wResDisp )
		
		return

	#####################################################
	# コマンド処理
	#####################################################
	def __run_ListFavo( self, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__run_ListFavo"
		
		#############################
		# f: フォロー者反応
		if inWord=="\\f" :
			self.__view_ListFollower()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# g: フォロワー支援
		elif inWord=="\\g" :
			wSubRes = self.FollowerFavo()
			if wSubRes['Result']!=True :
				wRes['Reason'] = "FollowerFavo"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# チェック
		
		wARR_Comm = str(inWord).split("-")
		wCom = None
		if len(wARR_Comm)==1 :
			wNum = wARR_Comm[0]
			wCom = None
		elif len(wARR_Comm)==2 :
			wNum = wARR_Comm[0]
			wCom = wARR_Comm[1]
		else:
			CLS_OSIF.sPrn( "コマンドの書式が違います" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		### 整数か
		try:
			wNum = int(wNum)
		except ValueError:
			CLS_OSIF.sPrn( "LIST番号が整数ではありません" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		wNum = wNum - 1
		if wNum<0 or len(gVal.ARR_ListFavo)<=wNum :
			CLS_OSIF.sPrn( "LIST番号が範囲外です" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# コマンドの分岐
		
		#############################
		# コマンドなし: 指定の番号のリストの設定変更をする
		if wCom==None :
			if gVal.ARR_ListFavo[wNum]['valid']==True :
				gVal.ARR_ListFavo[wNum]['valid'] = False
			else:
				gVal.ARR_ListFavo[wNum]['valid'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# f: フォロー者、フォロワーを含める ON/OFF
		elif wCom=="f" :
			if gVal.ARR_ListFavo[wNum]['follow']==True :
				gVal.ARR_ListFavo[wNum]['follow'] = False
			else:
				gVal.ARR_ListFavo[wNum]['follow'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# c: 警告 ON/OFF
		elif wCom=="c" :
			if gVal.ARR_ListFavo[wNum]['caution']==True :
				gVal.ARR_ListFavo[wNum]['caution'] = False
			else:
				gVal.ARR_ListFavo[wNum]['caution'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# n: センシティブツイートを含める
		elif wCom=="n" :
			if gVal.ARR_ListFavo[wNum]['sensitive']==True :
				gVal.ARR_ListFavo[wNum]['sensitive'] = False
			else:
				gVal.ARR_ListFavo[wNum]['sensitive'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# r: 自動リムーブ
		elif wCom=="r" :
			if gVal.ARR_ListFavo[wNum]['auto_rem']==True :
				gVal.ARR_ListFavo[wNum]['auto_rem'] = False
			else:
				gVal.ARR_ListFavo[wNum]['auto_rem'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# v: リストユーザ表示
		elif wCom=="v" :
			self.__view_ListFavoUser( gVal.ARR_ListFavo[wNum]['list_name'] )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# g: リストいいね実行
		elif wCom=="g" :
			wSubRes = self.ListFavo_single( wNum )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "ListFavo_single is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# 範囲外のコマンド
		else:
			CLS_OSIF.sPrn( "コマンドが違います" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# リストユーザ表示
	#####################################################
	def __view_ListFavoUser( self, inListName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__view_ListFavoUser"
		
		#############################
		# Twitterからリストのユーザ一覧を取得
		wSubRes = gVal.OBJ_Tw_IF.GetListMember( inListName=inListName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 画面表示
		wSubRes = self.__view_ListFavoUser_Disp( wSubRes['Responce'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "__view_ListFavoUser_Disp is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# フォロー者反応表示
	#####################################################
	def __view_ListFollower(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__view_ListFollower"
		
		#############################
		# Twitterからリストのユーザ一覧を取得
		wARR_FollowerData = gVal.OBJ_Tw_IF.GetFollowerData()
		if len(wARR_FollowerData)==0 :
			wRes['Reason'] = "FollowerData is zero"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 表示するユーザ情報の作成
		#   フォロー者 かつ FAVO送信ありユーザをセット
		wARR_ListUser = {}
		wKeylist = list( wARR_FollowerData.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			if wARR_FollowerData[wID]['myfollow']==False :
				### フォロー者じゃないので除外
				continue
			
			#############################
			# DBからいいね情報を取得する(1個)
			#   
			#   
###			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( wID )
###			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( wARR_FollowerData[wID] )
			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( wARR_FollowerData[wID], inFLG_New=False )
			if wDBRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB登録なし
###			if wDBRes['Responce']==None :
			if wDBRes['Responce']['Data']==None :
				### 除外
				continue
			
###			if str(wDBRes['Responce']['lfavo_date'])==gVal.DEF_TIMEDATE or \
###			   wDBRes['Responce']['lfavo_date']==None :
			if str(wDBRes['Responce']['Data']['lfavo_date'])==gVal.DEF_TIMEDATE or \
			   wDBRes['Responce']['Data']['lfavo_date']==None :
				### リストいいねしてないなら除外
				continue
			
###			if wARR_FollowerData[wID]['follower']==False and \
###			   wDBRes['Responce']['favo_cnt']==0 :
			if wARR_FollowerData[wID]['follower']==False and \
			   wDBRes['Responce']['Data']['favo_cnt']==0 :
				### フォロワーではない かつ いいね受信=0 は除外
				continue
			
			#############################
			# 対象なのでセット
			wCell = {
				"id"			: wARR_FollowerData[wID]['id'],
				"screen_name"	: wARR_FollowerData[wID]['screen_name']
			}
			wARR_ListUser.update({ wID : wCell })
		
		#############################
		# 対象ユーザなし
		if len(wARR_ListUser)==0 :
			CLS_OSIF.sPrn( "対象ユーザがありません" + '\n' )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 画面表示
		wSubRes = self.__view_ListFavoUser_Disp( wARR_ListUser )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "__view_ListFavoUser_Disp is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# リスト画面表示
	#####################################################
	def __view_ListFavoUser_Disp( self, inARR_Data ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__view_ListFavoUser_Disp"
		
		#############################
		# ユーザなし
		if len( inARR_Data )==0 :
			CLS_OSIF.sPrn( "リスト登録のユーザはありません" )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# ヘッダの表示
###		wStr = "USER NAME         FW者  FW受  FAVO受信(回数/日)   FAVO送信日   最終活動日" + '\n'
		wStr = "USER NAME         LEVEL   FW者  FW受  FAVO受信(回数/日)   FAVO送信日(回数)   最終活動日" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# いいねユーザデータを作成する
		wKeylist = list( inARR_Data.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			wARR_DBData = {
###				"favo_cnt"		: 0,
###				"now_favo_cnt"	: 0,
###				"favo_date"		: gVal.DEF_TIMEDATE,
###				"lfavo_date"	: gVal.DEF_TIMEDATE,
				"level_tag"		: None,
				"rfavo_cnt"		: 0,
				"rfavo_n_cnt"	: 0,
				"rfavo_date"	: gVal.DEF_TIMEDATE,
				"pfavo_date"	: gVal.DEF_TIMEDATE,
				"pfavo_cnt"		: 0,
				
				"update_date"	: gVal.DEF_TIMEDATE,
				"my_tweet"		: False
			}
			
			#############################
			# タイムラインを取得する
			#   最初の1ツイートの日時を最新の活動日とする
			wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=True,
				 inID=wID, inCount=gVal.DEF_STR_TLNUM['getUserTimeLine'] )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: GetTL"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wTweetRes['Responce'])>=1 :
				### 最新の活動日時
				
				wTweetIndex = 0
				for wTweet in wTweetRes['Responce'] :
					wTweetIndex += 1
					if wTweetIndex==1 :
						### 1行目の日付を活動日にする
						###日時の変換をして、設定
###						wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
###						if wTime['Result']!=True :
###							wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweet['created_at'])
###							gVal.OBJ_L.Log( "B", wRes )
###							return wRes
						wTime = CLS_TIME.sTTchg( wRes, "(4)", wTweet['created_at'] )
						if wTime['Result']!=True :
							return wRes
						wARR_DBData['update_date'] = wTime['TimeDate']
						
						if ("retweeted_status" not in wTweet) and ("quoted_status" not in wTweet) :
							### リツイート もしくは 引用でなければ自分
							wARR_DBData['my_tweet'] = True

						continue
					
					### 2行目以降
					### リツイート もしくは 引用でなければ活動日にする(自分のツイート)
					if ("retweeted_status" not in wTweet) and ("quoted_status" not in wTweet) :
###						wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
###						if wTime['Result']!=True :
###							wRes['Reason'] = "sGetTimeformat_Twitter is failed(2): " + str(wTweet['created_at'])
###							gVal.OBJ_L.Log( "B", wRes )
###							return wRes
						wTime = CLS_TIME.sTTchg( wRes, "(5)", wTweet['created_at'] )
						if wTime['Result']!=True :
							return wRes
						wARR_DBData['update_date'] = wTime['TimeDate']
						wARR_DBData['my_tweet'] = True
						break	#おわり
			
			#############################
			# DBからいいね情報を取得する(1個)
			#   
			#   
###			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( wID )
			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( inARR_Data[wID] )
			if wDBRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB登録
###			if wDBRes['Responce']!=None :
###				wARR_DBData['favo_cnt']     = wDBRes['Responce']['favo_cnt']
###				wARR_DBData['now_favo_cnt'] = wDBRes['Responce']['now_favo_cnt']
###				wARR_DBData['favo_date']  = wDBRes['Responce']['favo_date']
###				wARR_DBData['lfavo_date'] = wDBRes['Responce']['lfavo_date']
###			if wDBRes['Responce']['Data']!=None :
			if wDBRes['Responce']['Data']==None :
				wRes['Reason'] = "GetFavoDataOne is no data"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wDBRes['Responce']['FLG_New']==None :
				wNewUser = True	#新規登録
				#############################
				# 新規情報の設定
				wDBRes = self.OBJ_Parent.SetNewFavoData( inUser, wDBRes['Responce']['Data'] )
				if wDBRes['Result']!=True :
					###失敗
					wRes['Reason'] = "SetNewFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			wARR_DBData['level_tag']   = self.OBJ_Parent.LevelTagSttring( wDBRes['Responce']['Data']['level_tag'] )
			wARR_DBData['rfavo_cnt']   = wDBRes['Responce']['Data']['rfavo_cnt']
			wARR_DBData['rfavo_n_cnt'] = wDBRes['Responce']['Data']['rfavo_n_cnt']
			wARR_DBData['rfavo_date']  = wDBRes['Responce']['Data']['rfavo_date']
			wARR_DBData['pfavo_date']  = wDBRes['Responce']['Data']['pfavo_date']
			wARR_DBData['pfavo_cnt']   = wDBRes['Responce']['Data']['pfavo_cnt']
			
			#############################
			# 表示するデータ組み立て
			wStr = ""
			
			### 名前
			wListNumSpace = gVal.DEF_SCREEN_NAME_SIZE - len(inARR_Data[wID]['screen_name'])
			if wListNumSpace>0 :
				wListData = inARR_Data[wID]['screen_name'] + " " * wListNumSpace
			wStr = wStr + wListData + "  "
			
			### レベル
			wStr = wStr + wARR_DBData['level_tag'] + "  "
			
			### フォロー者
			if gVal.OBJ_Tw_IF.CheckMyFollow( wID )==True :
				wListData = "〇"
			else:
				wListData = "--"
			wStr = wStr + wListData + "    "
			
			### フォロワー
			if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
				wListData = "〇"
			else:
				wListData = "--"
			wStr = wStr + wListData + "    "
			
			### いいね回数
###			wListNumSpace = 5 - len( str(wARR_DBData['favo_cnt']) )
			wListNumSpace = 5 - len( str(wARR_DBData['rfavo_cnt']) )
			if wListNumSpace>0 :
###				wListData = str(wARR_DBData['favo_cnt']) + " " * wListNumSpace
				wListData = str(wARR_DBData['rfavo_cnt']) + " " * wListNumSpace
			wStr = wStr + wListData + ": "
			
			### いいね受信日
###			if str(wARR_DBData['favo_date'])==gVal.DEF_TIMEDATE or \
###			   str(wARR_DBData['favo_date'])==None :
			if str(wARR_DBData['rfavo_date'])==gVal.DEF_TIMEDATE :
				wListData = "----/--/--"
			else:
###				wListData = str(wARR_DBData['favo_date']).split(" ")
				wListData = str(wARR_DBData['rfavo_date']).split(" ")
				wListData = wListData[0]
			wStr = wStr + wListData + "   "
			
			### いいね実施回数
			wListNumSpace = 5 - len( str(wARR_DBData['pfavo_cnt']) )
			if wListNumSpace>0 :
				wListData = str(wARR_DBData['pfavo_cnt']) + " " * wListNumSpace
			wStr = wStr + wListData + ": "
			
			### いいね送信日
###			if str(wARR_DBData['lfavo_date'])==gVal.DEF_TIMEDATE or \
###			   str(wARR_DBData['lfavo_date'])==None :
			if str(wARR_DBData['pfavo_date'])==gVal.DEF_TIMEDATE :
				wListData = "----/--/--"
			else:
###				wListData = str(wARR_DBData['lfavo_date']).split(" ")
				wListData = str(wARR_DBData['pfavo_date']).split(" ")
				wListData = wListData[0]
			wStr = wStr + wListData + "   "
			
			### 最終活動日
			if str(wARR_DBData['update_date'])==gVal.DEF_TIMEDATE :
				wListData = "----/--/--"
			else:
				if wARR_DBData['my_tweet']==True :
					###自分のツイート
					wListData = str(wARR_DBData['update_date']).split(" ")
					wListData = " " + wListData[0]
				else:
					###引用リツイート
					wListData = str(wARR_DBData['update_date']).split(" ")
					wListData = "(" + wListData[0] + ")"
			wStr = wStr + wListData
			
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes




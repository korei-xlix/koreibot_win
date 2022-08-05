#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 メインモジュール
#####################################################
from twitter_follower import CLS_TwitterFollower
from twitter_favo import CLS_TwitterFavo
from twitter_keyword import CLS_TwitterKeyword
from twitter_admin import CLS_TwitterAdmin
from test_sample import CLS_Test

from ktime import CLS_TIME
from osif import CLS_OSIF
from traffic import CLS_Traffic
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterMain():
#####################################################
	OBJ_TwitterFollower = None
	OBJ_TwitterFavo     = None
	OBJ_TwitterKeyword  = None
	OBJ_TwitterAdmin    = None
	OBJ_Test            = None

###	CHR_GetReactionDate = None
###	CHR_GetListFavoDate = None
###	CHR_RunFollowerFavoDate = None
	ARR_ReacrionUserID = []

	CHR_AutoRemoveDate = None



#####################################################
# テスト用
#####################################################
	def Test(self):
		self.OBJ_Test.Test()
		return



#####################################################
# Init
#####################################################
	def __init__(self):
		self.OBJ_TwitterFollower = CLS_TwitterFollower( parentObj=self )
		self.OBJ_TwitterFavo     = CLS_TwitterFavo( parentObj=self )
		self.OBJ_TwitterKeyword  = CLS_TwitterKeyword( parentObj=self )
		self.OBJ_TwitterAdmin    = CLS_TwitterAdmin( parentObj=self )
		self.OBJ_Test            = CLS_Test( parentObj=self )
		return



#####################################################
# 初期化
#####################################################
	def Init(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "Init"
		
###		#############################
###		# 時間を取得
###		wSubRes = self.TimeUpdate( inInit=True )
###		if wSubRes['Result']!=True :
###			###時間取得失敗  時計壊れた？
###			wRes['Reason'] = "TimeUpdate is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
		#############################
		# Twitterから自ユーザ情報を取得する
		wUserinfoRes = gVal.OBJ_Tw_IF.GetMyUserinfo()
		if wUserinfoRes['Result']!=True :
			wRes['Reason'] = "Twitter Error"
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		gVal.STR_UserInfo['id'] = wUserinfoRes['Responce']['id']
		
		#############################
		# トラヒック情報読み込み
		wResSub = CLS_Traffic.sGet()
		if wResSub['Result']!=True :
			wRes['Reason'] = "Get Traffic failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 除外文字読み込み
		wResSub = gVal.OBJ_DB_IF.GetExeWord()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetExcWord failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 禁止ユーザ読み込み
		wResSub = gVal.OBJ_DB_IF.GetExeUser()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetExeUser failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 警告ツイート読み込み
		wResSub = gVal.OBJ_DB_IF.GetCautionTweet()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetCautionTweet failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 検索ワード読み込み
		wResSub = gVal.OBJ_DB_IF.GetSearchWord()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetSearchWord failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リストいいね指定読み込み
		wResSub = gVal.OBJ_DB_IF.GetListFavo()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetListFavo failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# グローバル時間更新
#####################################################
###	def TimeUpdate( self, inInit=False ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterMain"
###		wRes['Func']  = "TimeUpdate"
###		
###		#############################
###		# 時間を取得
###		wTD = CLS_OSIF.sGetTime()
###		if wTD['Result']!=True :
###			###時間取得失敗  時計壊れた？
###			wRes['Reason'] = "sGetTime is faied"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		### wTD['TimeDate']
###		wTD = CLS_TIME.sGet( wRes, "(1)" )
###		if wTD['Result']!=True :
###			return wRes
###		
###		#############################
###		# 時間を設定
###		### 初回起動で時刻が入ってなければ、ロック時間を設定する
###		if inInit==False :
###			if gVal.STR_SystemInfo['RateTimeDate']==None :
###				gVal.STR_SystemInfo['RateTimeDate'] = str(gVal.STR_SystemInfo['RateLockTD'])
###			else :
###				gVal.STR_SystemInfo['RateTimeDate'] = gVal.STR_Time['TimeDate']
###		
###		gVal.STR_Time['TimeDate'] = wTD['TimeDate']
###		
###		#############################
###		# 完了
###		wRes['Result'] = True
###		return wRes
###
###

#####################################################
# 周期15分処理
#####################################################
	def Circle15min(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "Circle15min"
		
		#############################
		# 時間を取得
		wSubRes = CLS_TIME.sTimeUpdate()
		if wSubRes['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "TimeUpdate is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 前回チェックから15分経っているか
###		wGetLag = CLS_OSIF.sTimeLag( gVal.STR_SystemInfo['APIrect'], inThreshold=gVal.DEF_STR_TLNUM['resetAPISec'] )
		wGetLag = CLS_OSIF.sTimeLag( gVal.STR_Time['run'], inThreshold=gVal.DEF_STR_TLNUM['resetAPISec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		if wGetLag['Beyond']==False :
			###前回から15分経ってない
			wRes['Result'] = True
			return wRes
		
		### ※前回から15分経ったので処理実行
###		#############################
###		# 時間を取得
###		wSubRes = CLS_TIME.sTimeUpdate()
###		if wSubRes['Result']!=True :
###			###時間取得失敗  時計壊れた？
###			wRes['Reason'] = "TimeUpdate is failed"
###			gVal.OBJ_L.Log( "C", wRes )
###			return wRes
###		
		#############################
		# Twitter再接続
		wTwitterRes = gVal.OBJ_Tw_IF.ReConnect()
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitterの再接続失敗"
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		
###		#############################
###		# カウント時刻を更新
###		gVal.STR_SystemInfo['APIrect'] = str(wGetLag['NowTime'])
		#############################
		# コマンド実行時間を更新
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "run", wGetLag['NowTime'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック情報の記録と報告
		wResTraffic = CLS_Traffic.sSet()
		if wResTraffic['Result']!=True :
			wRes['Reason'] = "Set Traffic failed: reason=" + CLS_OSIF.sCatErr( wResTraffic )
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ウェイト処理
#####################################################
	def Wait_Init( self, inZanNum=0, inWaitSec=gVal.DEF_STR_TLNUM['defWaitSec'], inZanCount=gVal.DEF_STR_TLNUM['defWaitCount'] ):
		gVal.STR_WaitInfo['zanNum']   = inZanNum
		gVal.STR_WaitInfo['zanCount'] = inZanCount
		gVal.STR_WaitInfo['setZanCount'] = inZanCount
		gVal.STR_WaitInfo['waitSec']  = inWaitSec
		gVal.STR_WaitInfo['Skip']     = False
		return True

	#####################################################
	def Wait_Next( self, inZanCountSkip=False ):
		#############################
		# カウントダウン
		gVal.STR_WaitInfo['zanNum']   -= 1
		if inZanCountSkip==False :
			gVal.STR_WaitInfo['zanCount'] -= 1
		
		###処理全て終わり
		if gVal.STR_WaitInfo['zanNum']<0 :
			return False	###全処理完了
		
		#############################
		# カウントチェック
		if gVal.STR_WaitInfo['zanCount']<0 :
			###カウントリセット
			gVal.STR_WaitInfo['zanCount'] = gVal.STR_WaitInfo['setZanCount']
			gVal.STR_WaitInfo['Skip']     = False	#ノーマル待機するので無効化
			
			#############################
			# 処理ウェイト(ノーマル)
			CLS_OSIF.sPrn( "CTRL+Cで中止することもできます。残り処理数= " + str( gVal.STR_WaitInfo['zanNum'] ) + " 個" + '\n' )
			wResStop = CLS_OSIF.sPrnWAIT( gVal.STR_WaitInfo['waitSec'] )
			if wResStop==False :
				CLS_OSIF.sPrn( "処理を中止しました。" + '\n' )
				return False	#ウェイト中止
			
			#############################
			# ついでに、15分周期処理
			w15Res = self.Circle15min()
			if w15Res['Result']!=True :
				###関数側でエラーを吐くので
				return False
		
		else:
			#############################
			# スキップ待機が設定されているか
			if gVal.STR_WaitInfo['Skip']==True :
				gVal.STR_WaitInfo['Skip'] = False
				#############################
				# 処理ウェイト(スキップ)
				CLS_OSIF.sPrn( "CTRL+Cで中止することもできます。残り処理数= " + str( gVal.STR_WaitInfo['zanNum'] ) + " 個" + '\n' )
				wResStop = CLS_OSIF.sPrnWAIT( gVal.DEF_STR_TLNUM['defWaitSkip'] )
				if wResStop==False :
					CLS_OSIF.sPrn( "処理を中止しました。" + '\n' )
					return False	#ウェイト中止
			else:
				if inZanCountSkip==False :
					CLS_OSIF.sSleep( gVal.DEF_STR_TLNUM['defWaitSkip'] )	#スリープ
		
		return True

	#####################################################
	def Wait_Skip(self):
		gVal.STR_WaitInfo['Skip'] = True	#次のNext起動時、スキップ待機をおこなう
		return True



#####################################################
# Twittter情報取得
#####################################################
	def GetTwitterInfo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "GetTwitterInfo"
		
		wRes['Responce'] = False
		
		#############################
		# リスト登録ユーザ取得
		wSubRes = gVal.OBJ_Tw_IF.GetFollowListUser()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetFollowListUser is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 自動リストユーザ取得
		wSubRes = gVal.OBJ_Tw_IF.GetAutoListUser()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetAutoListUser is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ふぁぼ一覧 取得
		wFavoRes = gVal.OBJ_Tw_IF.GetFavo()
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "GetFavo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# フォロー情報取得
###		CLS_MyDisp.sViewHeaderDisp( "フォロー情報取得" )
###		
		wFavoRes = gVal.OBJ_Tw_IF.GetFollow()
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "GetFollow is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
###		wStr = "〇フォロー一覧を取得しました" + '\n'
###		CLS_OSIF.sPrn( wStr )
###		
		### フォロー情報 取得
		wFollowerData = gVal.OBJ_Tw_IF.GetFollowerData()
		
		#############################
		# フォロー状態をDBに反映する
###		wStr = "フォロー状態をDBに記録中..." + '\n'
###		CLS_OSIF.sPrn( wStr )
		CLS_MyDisp.sViewHeaderDisp( "フォロー情報の記録中" )
		
		wKeylist = list( wFollowerData.keys() )
		for wID in wKeylist :
###			wUserID = str(wID)
			wID = str(wID)
			
			#############################
			# DBからいいね情報を取得する(1個)
###			wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wUserID )
###			wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wFollowerData[wUserID] )
			wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wFollowerData[wID] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB未登録
			if wSubRes['Responce']['Data']==None :
###			if wSubRes['Responce']==None :
###				###DBに登録する
###				wSetRes = gVal.OBJ_DB_IF.InsertFavoData( wFollowerData[wID] )
###				if wSetRes['Result']!=True :
###					###失敗
###					wRes['Reason'] = "InsertFavoData is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###				wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wUserID )
###				if wSubRes['Result']!=True :
###					###失敗
###					wRes['Reason'] = "GetFavoDataOne(2) is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###				### DB未登録（ありえない）
###				if wSubRes['Responce']==None :
###					wRes['Reason'] = "GetFavoDataOne(3) is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
				wRes['Reason'] = "GetFavoDataOne(3) is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Responce']['FLG_New']==None :
				#############################
				# 新規情報の設定
				wSubRes = self.SetNewFavoData( inUser, wSubRes['Responce']['Data'] )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "SetNewFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
###			wARR_DBData = wSubRes['Responce']
			wARR_DBData = wSubRes['Responce']['Data']
			
			wMyFollow = None
			wFollower = None
###			wFavoUpdate = False
###			wDetectRemove = False
			wUserLevel = None
			#############################
			# レベルDの修正→レベルAへ
			if ( wARR_DBData['myfollow']=="D" and wARR_DBData['myfollow']=="C+" ) and \
			   wFollowerData[wID]['myfollow']==True and \
			   gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==True :
				if self.CheckMutualListUser( wID )==False and \
				   self.CheckFollowListUser( wID )==False :
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "A" )
			
			#############################
			# フォロー者チェック
			if wARR_DBData['myfollow']!=wFollowerData[wID]['myfollow'] :
				#############################
				# 〇フォロー者検出
				if wFollowerData[wID]['myfollow']==True :
					if str(wARR_DBData['myfollow_date'])==gVal.DEF_TIMEDATE :
						wStr = "〇新規フォロー者"
###						wFavoUpdate = True
					else:
						wStr = "△再フォロー者"
###						wFavoUpdate = True
					
					if wARR_DBData['level_tag']!="A+" and \
					   self.CheckVIPUser( wFollowerData[wID] )==True :
						### VIPのフォロー
						wUserLevel = "A+"
###					if gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==True :
					elif gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==True :
						### 公式垢などのフォロー
						wUserLevel = "A"
					else:
						if wFollowerData[wID]['follower']==True :
							### フォローして相互フォローになった
							wUserLevel = "C+"
						else:
							### 自発的フォロー者（まだ相互じゃない）
							wUserLevel = "D"
						
						### 相互フォローリストに追加
###						wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wID )
						wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wFollowerData[wID] )
					
					### ユーザレベル変更
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
					
					### トラヒック記録（フォロー者獲得）
					CLS_Traffic.sP( "p_myfollow" )
					
					### ユーザ記録
					gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'] )
				
				else:
				#############################
				# 〇リムーブ者検出
					wStr = "●リムーブ者"
###					### 関係性チェック
###					wFollowInfoRes = gVal.OBJ_Tw_IF.GetFollowInfo( wID )
###					if wSubRes['Result']!=True :
###						wRes['Reason'] = "GetFollowInfo is failed"
###						gVal.OBJ_L.Log( "B", wRes )
###						return wRes
###					if wFollowInfoRes['Responce']['blocked_by']==True :
###						### 被ブロック検知
###						wStr = "●被ブロック検知"
###						wUserLevel = "G"
###					else:
					if wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" :
						### 公式垢以外
						if wFollowerData[wID]['follower']==True :
							### フォロワー（フォロー者OFF・フォロワーになった）
							wUserLevel = "E"
							
							### 片フォロワーリストに追加
###							wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( wID )
							wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( wFollowerData[wID] )
						
						else:
							### 自発的リムーブ扱い（フォロー者・フォロワーともにOFF）
###							wStr = "●リムーブ者"
							wUserLevel = "D-"
							
							### リストリムーブ
###							wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wID )
							wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wFollowerData[wID] )
						
						### ユーザレベル変更
						wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
					
					### トラヒック記録（フォロー者減少）
					CLS_Traffic.sP( "d_myfollow" )
					
					### ユーザ記録
					gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'] )
				
###				### ユーザ記録
				wMyFollow = wFollowerData[wID]['myfollow']
###				gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'] )
			
			#############################
			# フォロワーチェック
			if wARR_DBData['follower']!=wFollowerData[wID]['follower'] :
				#############################
				# 〇フォロワー検出
				if wFollowerData[wID]['follower']==True :
					#############################
					# ユーザ情報の確認
					# 次のユーザはブロック→リムーブする
					# ・ユーザレベル=A or A+以外
					# ・片フォロワー（フォロー者OFF）
					# ・ツイート数=0 もしくは 鍵アカウント
					# ・最終ツイートが一定期間過ぎてるか
					wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=wFollowerData[wID]['screen_name'] )
					if wUserInfoRes['Result']!=True :
						wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wUserInfoRes['Reason'] + " screen_name=" + wFollowerData[wID]['screen_name']
						gVal.OBJ_L.Log( "B", wRes )
						continue
					
					wFLG_RemDetect = False
###					if wFollowerData[wID]['myfollow']==False and \
###					   wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel=="A" and \
###					   ( wUserInfoRes['Responce']['statuses_count']==0 or \
###					     wUserInfoRes['Responce']['protected']==True ) :
###					if wFollowerData[wID]['myfollow']==False and \
###					   wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel=="A" and \
					if wARR_DBData['level_tag']=="A" or wARR_DBData['level_tag']=="A+" or wUserLevel=="A" or wUserLevel=="A+" :
						wFLG_RemDetect = False
					
###					if wFollowerData[wID]['myfollow']==False and \
###					   wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel!="A" and \
###					   ( wUserInfoRes['Responce']['statuses_count']==0 or \
###					     wUserInfoRes['Responce']['protected']==True ) :
					elif wFollowerData[wID]['myfollow']==False and \
					   wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel!="A" and \
					   ( wUserInfoRes['Responce']['statuses_count']==0 or \
					     wUserInfoRes['Responce']['protected']==True ) :
						###対象
						wFLG_RemDetect = True
					
					else:
						###最終ツイート日時が規定日を超えているか
						wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=True,
							 inID=wID, inCount=1 )
						if wTweetRes['Result']!=True :
							wRes['Reason'] = "Twitter Error: GetTL"
							gVal.OBJ_L.Log( "B", wRes )
							continue
						
						###日時の変換をして、設定
						wTime = CLS_TIME.sTTchg( wRes, "(1)", wTweetRes['Responce'][0]['created_at'] )
						if wTime['Result']!=True :
							continue
						
						wGetLag = CLS_OSIF.sTimeLag( str( wTime['TimeDate'] ), inThreshold=gVal.DEF_STR_TLNUM['forAutoUserRemoveSec'] )
						if wGetLag['Result']!=True :
							wRes['Reason'] = "sTimeLag failed"
							gVal.OBJ_L.Log( "B", wRes )
							continue
						if wGetLag['Beyond']==True :
							### 規定外 =許容外の日数なので対象
							wFLG_RemDetect = True
					
					if wFLG_RemDetect==True :
						#############################
						# ブロック→リムーブする
						wBlockRes = gVal.OBJ_Tw_IF.BlockRemove( wID )
						if wBlockRes['Result']!=True :
							wRes['Reason'] = "Twitter API Error(BlockRemove): " + wBlockRes['Reason'] + " screen_name=" +wFollowerData[wID]['screen_name']
							gVal.OBJ_L.Log( "B", wRes )
							continue
						
###						wStr = "●追い出し"
###						
						### ユーザレベル変更
						wUserLevel = "G-"
						wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
						
						### トラヒック記録（フォロワー減少）
						CLS_Traffic.sP( "d_follower" )
						
						### ユーザ記録
						wStr = "●追い出し"
						gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'] )
					
					else:
						wFollower = True
						if str(wARR_DBData['follower_date'])==gVal.DEF_TIMEDATE :
							wStr = "〇新規フォロワー"
						else:
							wStr = "△再フォローされた"
						
						if wARR_DBData['level_tag']!="A+" and wUserLevel!="A+" and \
						   self.CheckVIPUser( wFollowerData[wID] )==True :
							### VIPのフォロワー
							wUserLevel = "A+"
						
###						if wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel=="A" :
###						if wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel!="A" :
						elif wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel!="A" and wUserLevel!="A+" :
							if wFollowerData[wID]['myfollow']==True :
								### フォローされて相互フォローになった
								wUserLevel = "C+"
							else:
								### フォロワー
								wUserLevel = "E"
								
								### 片フォロワーリストに追加
###								wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( wID )
								wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( wFollowerData[wID] )
							
							### ユーザレベル変更
							wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
						
						### トラヒック記録（フォロワー獲得）
						CLS_Traffic.sP( "p_follower" )
						
						### ユーザ記録
						gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'] )
				
				else:
				#############################
				# 〇被リムーブ検出
###					wStr = "●リムーブされた"
###					### 関係性チェック
###					wFollowInfoRes = gVal.OBJ_Tw_IF.GetFollowInfo( wID )
###					if wSubRes['Result']!=True :
###						wRes['Reason'] = "GetFollowInfo is failed"
###						gVal.OBJ_L.Log( "B", wRes )
###						return wRes
###					if wFollowInfoRes['Responce']['blocked_by']==True :
###						### 被ブロック検知
###						wStr = "●被ブロック検知"
###						wUserLevel = "G"
###					else:
					wFollower = False
###					if wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel=="A" :
					if wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel!="A" :
						if wFollowerData[wID]['myfollow']==True :
							### フォロー者（相互フォロー中、フォロー者ON・フォロワーOFFになった）
###							wStr = "●リムーブされた"
###							
###							### ユーザレベル変更
###							wUserLevel = "C-"
###							wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
###							
###							#############################
###							# 即自動リムーブする
###							wTwitterRes = gVal.OBJ_Tw_IF.AutoRemove( inUser )
###							if wTwitterRes['Result']!=True :
###								wRes['Reason'] = "AutoRemove is failed"
###								gVal.OBJ_L.Log( "B", wRes )
###								return wRes
###							if wTwitterRes['Responce']==True :
###								### 自動リムーブした場合
###								wUserLevel = "E-"
###								wMyFollow = False
###							else:
###								wUserLevel = "C-"
							#############################
							# 即自動リムーブする
							wSubRes = self.OBJ_TwitterFollower.AutoRemove( wFollowerData[wID] )
							if wSubRes['Result']!=True :
								wRes['Reason'] = "AutoRemove is failed"
								gVal.OBJ_L.Log( "B", wRes )
								return wRes
							if wSubRes['Responce']==False :
								### 自動リムーブしてない（フォロー者ON・フォロワーOFF）
								
								### ユーザレベル変更
								wUserLevel = "C-"
								wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
								
								### ユーザ記録
								wStr = "●リムーブされた"
								gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'] )
						
						else:
							### 自発的リムーブ扱い（フォロー者・フォロワーともにOFF）
###							wStr = "●リムーブされた"
###							wUserLevel = "E-"
###							
							### リストリムーブ
###							wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wID )
							wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wFollowerData[wID] )
							
							### ユーザレベル変更
							wUserLevel = "E-"
							wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
							
							### ユーザ記録
							wStr = "●リムーブされた"
							gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'] )
					
					### トラヒック記録（フォロワー減少）
					CLS_Traffic.sP( "d_follower" )
					
###					### ユーザ記録
###					gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'] )
###					
###					wDetectRemove = True
###					#############################
###					# フォロー中かつ、リムーブされたら自動リムーブする
###					if wARR_DBData['myfollow']==True and \
###					   wFollowerData[wID]['myfollow']==True :
###						wSubRes = self.OBJ_TwitterFollower.AutoRemove( wID )
###						if wSubRes['Result']!=True :
###							wRes['Reason'] = "AutoRemove is failed(1)"
###							gVal.OBJ_L.Log( "B", wRes )
###							return wRes
###					### ※リムーブ状況は既にDBに反映済
###				
###				### ユーザ記録
###				wFollower = wFollowerData[wID]['follower']
###				gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'] )
			
			#############################
			# 変更ありの場合
			#   DBへ反映
			if wMyFollow!=None or wFollower!=None :
###				wSubRes = gVal.OBJ_DB_IF.UpdateFavoDataFollower( wID, wMyFollow, wFollower, wFavoUpdate )
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wID, wMyFollow, wFollower )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				wRes['Responce'] = True
			
###			#############################
###			# リムーブされたら自動リムーブする
###			if wDetectRemove==True :
###				wSubRes = self.OBJ_TwitterFollower.AutoRemove( wID )
###				if wSubRes['Result']!=True :
###					wRes['Reason'] = "AutoRemove is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###		
###		#############################
###		# リムーブ もしくは ブロックでTwitterから完全リムーブされたか
###		#   DB上フォロー者 もしくは フォロワーを抽出
###		wQuery = "select * from tbl_favouser_data where " + \
###					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
###					"myfollow = True or " + \
###					"follower = True " + \
###					";"
###		
###		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
###		if wResDB['Result']!=True :
###			wRes['Reason'] = "Run Query is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# 辞書型に整形
###		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
###		
###		#############################
###		# 添え字をIDに差し替える
###		wARR_RateFavoDate = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		#############################
		# リムーブ もしくは ブロックでTwitterから完全リムーブされたか
		#   DB上フォロー者 もしくは フォロワーを抽出
		wARR_RateFavoDate = {}
		wSubRes = gVal.OBJ_DB_IF.GetFavoData()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoData is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_RateFavoDate = wSubRes['Responce']
		
		wKeylist = list( wARR_RateFavoDate.keys() )
		for wID in wKeylist :
			wUserID = str(wID)
			
			#############################
			# Twitterでフォロー者 もしくは フォロワーの場合
			# スキップ
			if wID in wFollowerData :
				continue
			
			# ※Twitterでリムーブした リムーブされた ブロックされた
			#   でTwitterからアンフォロー（=情報がなくなった）
			#   かつ DBではフォロー者 フォロワーの場合
			
			wMyFollow = None
			wFollower = None
			wBlockBy  = False
			#############################
			# ブロックチェック
			wFollowInfoRes = gVal.OBJ_Tw_IF.GetFollowInfo( wID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "GetFollowInfo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wFollowInfoRes['Responce']['blocked_by']==True :
				### 被ブロック検知
				wBlockBy = True
				
				### 通信記録
				wStr = "●被ブロック検知"
				gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wARR_RateFavoDate[wID]['screen_name'] )

				### ユーザレベル変更
				wUserLevel = "G"
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
				
				### トラヒック記録
				if wARR_RateFavoDate[wID]['myfollow']==True :
					wMyFollow = True
					CLS_Traffic.sP( "d_myfollow" )
				
				if wARR_RateFavoDate[wID]['myfollow']==True :
					wFollower = True
					CLS_Traffic.sP( "follower" )
			
###			wMyFollow = None
###			wFollower = None
			#############################
			# 〇リムーブ者検出
			if wARR_RateFavoDate[wID]['myfollow']==True and wBlockBy==False :
				wMyFollow = False
				
				#############################
				# 〇リムーブ者＆被リムーブ検出
				if wARR_RateFavoDate[wID]['follower']==True :
					wFollower = False
					
					### 通信記録（フォロー者ON・フォロワーONから、フォロー者・フォロワーOFFへ）
					wStr = "●リムーブ者・リムーブされた（同時検出）"
					
					### トラヒック記録
					CLS_Traffic.sP( "d_follower" )
				
				else:
					### 通信記録（片フォロー者・フォロワーOFFから、フォロー者・フォロワーOFFへ）
					wStr = "●リムーブ者"
				
				### リストリムーブ
###				wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wID )
				wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wARR_RateFavoDate[wID] )
				
				### ユーザレベル変更
				wUserLevel = "E-"
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
				
				### 通信記録
				gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wARR_RateFavoDate[wID]['screen_name'] )
				
				### トラヒック記録
				CLS_Traffic.sP( "d_myfollow" )
				
			
			#############################
			# 〇被リムーブ検出
			if wARR_RateFavoDate[wID]['follower']==True and wBlockBy==False and \
			   wARR_RateFavoDate[wID]['myfollow']==False :
				wFollower = False
				
				### リストリムーブ
###				wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wID )
				wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wARR_RateFavoDate[wID] )
				
				### ユーザレベル変更
				wUserLevel = "E"
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
				
				### 通信記録（フォロー者OFF・フォロワーから、フォロー者・フォロワーOFFへ）
				wStr = "●リムーブされた"
				gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wARR_RateFavoDate[wID]['screen_name'] )
				
				### トラヒック記録
				CLS_Traffic.sP( "d_follower" )
			
			#############################
			# 変更ありの場合
###			#   DBへ反映して自動リムーブする
			#   DBへ反映する
			if wMyFollow!=None or wFollower!=None :
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wID, wMyFollow, wFollower )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
###				#############################
###				# 自動リムーブする
###				if wARR_DBData['myfollow']==True and \
###				   wFollowerData[wID]['myfollow']==True :
###					wSubRes = self.OBJ_TwitterFollower.AutoRemove( wARR_RateFavoDate[wID] )
###					if wSubRes['Result']!=True :
###						wRes['Reason'] = "AutoRemove is failed(2)"
###						gVal.OBJ_L.Log( "B", wRes )
###						return wRes
###				
###				wRes['Responce'] = True
###		
###		#############################
###		# ふぁぼ一覧 取得
###		wFavoRes = gVal.OBJ_Tw_IF.GetFavo()
###		if wFavoRes['Result']!=True :
###			wRes['Reason'] = "GetFavo is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		wStr = "〇いいね一覧を取得しました" + '\n'
###		CLS_OSIF.sPrn( wStr )
###		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 自動監視
#####################################################
###	def AllRun( self, inFLG_Short=False ):
	def AllRun(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "AllRun"
		
		wFLG_Short = False
		#############################
		# フル自動監視 期間内か
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['autorun'] ), inThreshold=gVal.DEF_STR_TLNUM['forAutoAllRunSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			### 規定以内= ショート処理
			wFLG_Short = True
		
		#############################
		# Twitter情報取得
		wFavoRes = self.GetTwitterInfo()
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "GetTwitterInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 禁止ユーザ自動削除（●フル自動監視）
		if wFLG_Short==False :
			wSubRes = self.OBJ_TwitterAdmin.ExcuteUser_AutoDelete()
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "ExcuteUser_AutoDelete is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# ユーザ自動削除（●フル自動監視）
		if wFLG_Short==False :
			wSubRes = self.OBJ_TwitterAdmin.RunAutoUserRemove()
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "RunAutoUserRemove is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# いいね解除（●フル自動監視）
		if wFLG_Short==False :
			wSubRes = self.OBJ_TwitterFavo.RemFavo()
			if wSubRes['Result']!=True :
				wRes['Reason'] = "RemFavo"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# リスト通知 リストとユーザの更新
		wSubRes = self.UpdateListIndUser()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateListIndUser error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リスト登録ユーザチェック
		wSubRes = self.CheckListUsers()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "CheckListUsers error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 自動リムーブチェック
		wSubRes = self.CheckAutoRemove()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "CheckAutoRemove error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リアクションチェック
		wSubRes = self.OBJ_TwitterFollower.ReactionCheck( inFLG_Short=wFLG_Short )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "ReactionCheck"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# VIPリアクション監視チェック
		wSubRes = self.OBJ_TwitterFollower.VIP_ReactionCheck()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "VIP_ReactionCheck is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リストいいね（●フル自動監視）
		if wFLG_Short==False :
			wSubRes = self.OBJ_TwitterFavo.ListFavo()
			if wSubRes['Result']!=True :
				wRes['Reason'] = "ListFavo"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# フォロワー支援
		wSubRes = self.OBJ_TwitterFavo.FollowerFavo()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "FollowerFavo"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# いいね情報送信
		wSubRes = self.OBJ_TwitterFollower.SendFavoDate()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SendFavoDate"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 検索ワード実行（●フル自動監視）
		if wFLG_Short==False :
			wSubRes = self.OBJ_TwitterKeyword.RunKeywordSearchFavo()
			if wSubRes['Result']!=True :
				wRes['Reason'] = "RunKeywordSearchFavo"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 警告ツイートの削除（●フル自動監視）
		if wFLG_Short==False :
			wSubRes = self.OBJ_TwitterAdmin.RemoveCautionTweet()
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "RemoveCautionTweet is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 古いいいね情報の削除（●フル自動監視）
		if wFLG_Short==False :
			wSubRes = gVal.OBJ_DB_IF.DeleteFavoData()
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "DeleteFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 自動監視時間に 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "autorun", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['autorun']
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ管理
#####################################################
	def UserAdmin(self):
		wRes = self.OBJ_TwitterAdmin.UserAdmin()
		return wRes



#####################################################
# 警告ユーザ管理
#####################################################
	def AdminCautionUser(self):
		wRes = self.OBJ_TwitterAdmin.AdminCautionUser()
		return wRes



#####################################################
# トレンドタグ設定
#####################################################
	def SetTrendTag(self):
		wRes = self.OBJ_TwitterAdmin.SetTrendTag()
		return wRes



#####################################################
# リスト通知設定
#####################################################
	def SetListName(self):
		wRes = self.OBJ_TwitterAdmin.SetListName()
		return wRes



#####################################################
# 自動リムーブ設定
#####################################################
	def SetAutoRemove(self):
		wRes = self.OBJ_TwitterAdmin.SetAutoRemove()
		return wRes



#####################################################
# フォローリスト設定
#####################################################
###	def SetAutoList(self):
###		wRes = self.OBJ_TwitterAdmin.SetAutoList()
###		return wRes
###
###

#####################################################
# 禁止ユーザ
#####################################################
	def ExcuteUser(self):
		wRes = self.OBJ_TwitterAdmin.ExcuteUser()
		return wRes



#####################################################
# いいね全解除
#####################################################
	def AllFavoRemove(self):
###		wRes = self.OBJ_TwitterFavo.AllFavoRemove()
		wRes = self.OBJ_TwitterFavo.RemFavo( inFLG_All=True )
		return wRes



#####################################################
# トレンドツイート
#####################################################
###	def TrendTweet(self):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterMain"
###		wRes['Func']  = "TrendTweet"
###		
###		#############################
###		# リスト通知 リストとユーザの更新
###		wSubRes = self.UpdateListIndUser()
###		if wSubRes['Result']!=True :
###			wRes['Reason'] = "UpdateListIndUser error"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		wRes = self.OBJ_TwitterKeyword.TrendTweet()
###		
###		#############################
###		# 完了
###		wRes['Result'] = True
###		return wRes
###
###

#####################################################
# キーワードいいね
#####################################################
	def KeywordFavo(self):
		#############################
		# Twitter情報取得
		wFavoRes = self.GetTwitterInfo()
		if wFavoRes['Result']!=True :
			return wFavoRes
		
		wRes = self.OBJ_TwitterKeyword.KeywordFavo()
		return wRes



#####################################################
# リストいいね設定
#####################################################
	def SetListFavo(self):
		#############################
		# Twitter情報取得
		wFavoRes = self.GetTwitterInfo()
		if wFavoRes['Result']!=True :
			return wFavoRes
		
		wRes = self.OBJ_TwitterFavo.SetListFavo()
		return wRes



#####################################################
# リアクションツイートチェック
#####################################################
###	def ReactionTweetCheck( self, inTweet ):
	def ReactionTweetCheck( self, inMyUserID, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "ReactionTweetCheck"
		
		wTweet = inTweet
		
		wUserID = str( wTweet['user']['id'] )
		#############################
		# 自分のツイート以外は処理を抜ける
###		if str(gVal.STR_UserInfo['id'])!=wUserID :
		if inMyUserID!=wUserID :
			### 自分のツイートではない＝正常終了
			wRes['Result'] = True
			return wRes
		
		#############################
		# 自分かのフラグ
		wFLG_MyUser = False
		if str(gVal.STR_UserInfo['id'])==wUserID :
			wFLG_MyUser = True
		
		wTweet['id'] = str(wTweet['id'])
		wTweetID = wTweet['id']
		
		#############################
		# チェック対象のツイート表示
		wStr = '\n' + "--------------------" + '\n' ;
		wStr = wStr + "チェック中: " + str(wTweet['created_at']) + '\n' ;
		wStr = wStr + wTweet['text'] + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# いいねチェック
		wSubRes = gVal.OBJ_Tw_IF.GetLikesLookup( wTweetID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetLikesLookup): Tweet ID: " + wTweetID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wKeylist = list( wSubRes['Responce'].keys() )
		for wID in wKeylist :
			wID = str(wID)
			###ユーザ単位のリアクションチェック
###			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet )
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet, wFLG_MyUser )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wReactionRes['Responce']==True :
				wStr = "〇いいね検出: " + wSubRes['Responce'][wID]['screen_name'] + '\n'
				CLS_OSIF.sPrn( wStr )
				
				### トラヒック記録
				if wFLG_MyUser==True :
					CLS_Traffic.sP( "r_reaction" )
					CLS_Traffic.sP( "r_favo" )
					if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
						CLS_Traffic.sP( "r_in" )
					else:
						CLS_Traffic.sP( "r_out" )
				else:
					CLS_Traffic.sP( "r_vip" )
		
		#############################
		# リツイートチェック
		wSubRes = gVal.OBJ_Tw_IF.GetRetweetLookup( wTweetID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetRetweetLookup): Tweet ID: " + wTweetID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wKeylist = list( wSubRes['Responce'].keys() )
		for wID in wKeylist :
			wID = str(wID)
			###ユーザ単位のリアクションチェック
###			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet )
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet, wFLG_MyUser )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 2): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wReactionRes['Responce']==True :
				wStr = "〇リツイート検出: " + wSubRes['Responce'][wID]['screen_name'] ;
				CLS_OSIF.sPrn( wStr )
				
				### トラヒック記録
				if wFLG_MyUser==True :
					CLS_Traffic.sP( "r_reaction" )
					CLS_Traffic.sP( "r_favo" )
					if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
						CLS_Traffic.sP( "r_in" )
					else:
						CLS_Traffic.sP( "r_out" )
				else:
					CLS_Traffic.sP( "r_vip" )
		
		#############################
		# 引用リツイートチェック
		wSubRes = gVal.OBJ_Tw_IF.GetRefRetweetLookup( wTweetID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetRefRetweetLookup): Tweet ID: " + wTweetID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wKeylist = list( wSubRes['Responce'].keys() )
		for wID in wKeylist :
			wID = str(wID)
			###ユーザ単位のリアクションチェック
###			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet )
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet, wFLG_MyUser )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 3): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wReactionRes['Responce']==True :
				wStr = "〇引用リツイート検出: " + wSubRes['Responce'][wID]['screen_name'] ;
				CLS_OSIF.sPrn( wStr )
				
				### トラヒック記録
				if wFLG_MyUser==True :
					CLS_Traffic.sP( "r_reaction" )
					CLS_Traffic.sP( "r_favo" )
					if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
						CLS_Traffic.sP( "r_in" )
					else:
						CLS_Traffic.sP( "r_out" )
				else:
					CLS_Traffic.sP( "r_vip" )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# リアクションユーザチェック
#####################################################
###	def ReactionUserCheck( self, inUser, inTweet ):
	def ReactionUserCheck( self, inUser, inTweet, inFLG_MyUser=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "ReactionUserCheck"
		
		wRes['Responce'] = False
		
		wUserID = str(inUser['id'])
		
		wFLG_Action = True
		#############################
		# リアクション済みのユーザは除外
		if wUserID in self.ARR_ReacrionUserID :
			wFLG_Action = False	#除外
		
		wNewUser = False
		#############################
		# DBからいいね情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( inUser )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録
		if wSubRes['Responce']['Data']==None :
			wRes['Reason'] = "GetFavoDataOne is no data"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']['FLG_New']==None :
			wNewUser = True	#新規登録
			#############################
			# 新規情報の設定
			wSubRes = self.SetNewFavoData( inUser, wSubRes['Responce']['Data'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "SetNewFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wARR_DBData = wSubRes['Responce']['Data']
		
		wTweetID = str( inTweet['id'] )
		#############################
		# 同じアクションはノーリアクション
		if wARR_DBData['favo_id']==wTweetID :
			wFLG_Action = False	#除外
		
		#############################
		# 前のリアクションより最新なら新アクション
		if wFLG_Action==True :
###			wSubRes = CLS_OSIF.sCmpTime( inTweet['created_at'], inDstTD=wARR_DBData['favo_date'] )
			wSubRes = CLS_OSIF.sCmpTime( inTweet['created_at'], inDstTD=wARR_DBData['rfavo_date'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "sCmpTime is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Future']==False :
				wFLG_Action = False	#除外
		
		#############################
		# リアクション禁止ユーザか
		wUserRes = self.CheckExtUser( wARR_DBData, "リアクション検出" )
		if wUserRes['Result']!=True :
			wRes['Reason'] = "CheckExtUser failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wUserRes['Responce']==False :
			### 禁止あり=除外
			
			if wFLG_Action==True :
				### 除外してない場合
				
				### いいね情報を更新する
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, False )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				wStr = "●リアクション禁止: " + wARR_DBData['screen_name'] + '\n'
				CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# アクションが有効なら、リアクション済みにする
		if wFLG_Action==True :
			#############################
			# いいね情報を更新する
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			#############################
			# リアクション済みID
			self.ARR_ReacrionUserID.append( inUser['id'] )
			
			#############################
			# リアクションへのリアクション
###			wSubRes = self.__ReactionUserCheck_PutReaction( inUser, wARR_DBData, inTweet, wNewUser )
			wSubRes = self.__ReactionUserCheck_PutReaction( inUser, wARR_DBData, inTweet, inFLG_MyUser, wNewUser )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "__ReactionUserCheck_ListInd is failed"
				gVal.OBJ_L.Log( "B", wRes )
			
			#############################
			# リアクション済み
			wRes['Responce'] = True
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# リアクションユーザへのリアクション
	#####################################################
###	def __ReactionUserCheck_PutReaction( self, inUser, inData, inTweet, inNewUser=False ):
	def __ReactionUserCheck_PutReaction( self, inUser, inData, inTweet, inFLG_MyUser=True, inNewUser=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "__ReactionUserCheck_PutReaction"
		
		if inFLG_MyUser==True :
			#############################
			# 期間外のTweetで 新規ユーザに対しては
			# リアクションを返さない(仕様)
			if inNewUser==True :
				wGetLag = CLS_OSIF.sTimeLag( str( inTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外= とりま通知しない
					wStr = "●新規ユーザのため非通知: " + inData['screen_name'] + '\n' ;
					CLS_OSIF.sPrn( wStr )
					
					wRes['Result'] = True
					return wRes
			
			#############################
			# 自動おかえしいいねする
			if gVal.DEF_STR_TLNUM['autoRepFavo']==True :
###				wSubRes = self.OBJ_TwitterFavo.AutoFavo( inUser, inData )
				wSubRes = self.OBJ_TwitterFavo.AutoFavo( inUser, gVal.DEF_STR_TLNUM['forReturnFavoSec'] )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "AutoFavo is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# リスト通知をおこなう
		if gVal.STR_UserInfo['ListName']!=gVal.DEF_NOTEXT :
			wSubRes = self.__ReactionUserCheck_ListInd( inData )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "__ReactionUserCheck_ListInd is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# リスト通知をおこなう
	#####################################################
	def __ReactionUserCheck_ListInd( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "__ReactionUserCheck_ListInd"
		
		#############################
		# 前回が今日以外なら通知する
		wNowDate = str(gVal.STR_Time['TimeDate'])
		wNowDate = wNowDate.split(" ")
		wNowDate = wNowDate[0]
		wRateDate = str(inData['list_ind_date'])
		wRateDate = wRateDate.split(" ")
		wRateDate = wRateDate[0]
		if wNowDate==wRateDate :
			### 今日なので通知しない
			wStr = "●今日は通知済み: " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# リストがTwitterにあるか確認
		wSubRes = gVal.OBJ_Tw_IF.ListInd_AddUser( inData )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(InserttListIndUser): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
			### 既に登録済み
			wStr = "●リスト通知済み: " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# DBに登録する
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_ListIndData( inData )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateFavoData_ListIndData Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
###		wTextReason = "○リスト通知の発行: " + inData['screen_name']
###		gVal.OBJ_L.Log( "T", wRes, wTextReason )
		wTextReason = "リスト通知: " + inData['screen_name']
		gVal.OBJ_L.Log( "RR", wRes, wTextReason )
		
		wRes['Result'] = True
		return wRes



#####################################################
# リスト通知ユーザ更新
#####################################################
	def UpdateListIndUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "UpdateListIndUser"
		
###		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['list_clear'] ), inThreshold=gVal.DEF_VAL_DAY )
###		if wGetLag['Result']!=True :
###			wRes['Reason'] = "sTimeLag failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		if wGetLag['Beyond']==False :
###			### 規定以内= 処理しない
###			wRes['Result'] = True
###			return wRes
		wGetLag = CLS_OSIF.sCheckNextDay( str( gVal.STR_Time['list_clear'] ), str( gVal.STR_Time['TimeDate'] ) )
		if wGetLag['Result']!=True :
###			wRes['Reason'] = "sCheckNextDay failed"
###			wRes['Reason'] = "sCheckNextDay failed: list_clear=" + str(gVal.STR_Time['list_clear'])
			wRes['Reason'] = "sCheckNextDay failed: reason=" + wGetLag['Reason'] + " list_clear=" + str(gVal.STR_Time['list_clear'])
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Next']==False :
			### 翌日ではない= スキップ
			wRes['Result'] = True
			return wRes
		
###		#############################
###		# 処理時間の更新
###		wSubRes = gVal.OBJ_DB_IF.UpdateListIndDate()
###		if wSubRes['Result']!=True :
###			wRes['Reason'] = "UpdateListIndDate Error"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		wFLG_NextDay = wSubRes['Responce']
###		
		#############################
		# 翌日の場合
		#   リスト通知をクリアする
###		if wFLG_NextDay==True :
###		if gVal.STR_SystemInfo['Day']==True :
		wSubRes = gVal.OBJ_Tw_IF.ListInd_Clear()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "AllClearListInd error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==True :
			gVal.OBJ_L.Log( "SC", wRes, "リスト通知クリア" )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "list_clear", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['list_clear']
		
		wRes['Result'] = True
		return wRes



#####################################################
# リスト登録ユーザチェック
#####################################################
	def CheckListUsers(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckListUsers"
		
###		wStr = "リスト登録ユーザチェック中..."
###		CLS_OSIF.sPrn( wStr )
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "リスト登録ユーザチェック" )
		
		#############################
		# 通知リストのチェック
		# 自動リムーブが有効なら、相互フォローリスト、片フォロワーリストのチェック
		wARR_IndListName = []
###		if gVal.STR_UserInfo['ListID']==gVal.DEF_NOTEXT :
		if gVal.STR_UserInfo['ListID']!=gVal.DEF_NOTEXT :
			wARR_IndListName.append( gVal.STR_UserInfo['ListName'] )
		
		if gVal.STR_UserInfo['AutoRemove']==True and \
		   ( gVal.STR_UserInfo['mListID']!=gVal.DEF_NOTEXT or \
		     gVal.STR_UserInfo['fListID']!=gVal.DEF_NOTEXT ) :
			wARR_IndListName.append( gVal.STR_UserInfo['mListName'] )
			wARR_IndListName.append( gVal.STR_UserInfo['fListName'] )
		
###		wKeylist = list( wARR_IndList.keys() )
###		wKeylist = list( wARR_IndListName.keys() )
###		for wKey in wKeylist :
		for wListName in wARR_IndListName :
###			wStr = "〇チェック中リスト: " + wARR_IndListName[wKey]
			wStr = "〇チェック中リスト: " + wListName
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# Twitterからリストの登録ユーザ一覧を取得
###			wListRes = gVal.OBJ_Tw_IF.GetListSubscribers(
###			   inListName=wARR_IndListName[wKey],
###			   inScreenName=gVal.STR_UserInfo['Account'] )
			wListRes = gVal.OBJ_Tw_IF.GetListSubscribers(
			   inListName=wListName,
			   inScreenName=gVal.STR_UserInfo['Account'] )
			
			if wListRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetListSubscribers:List): " + wListRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wListRes['Responce'])>=1 :
				### 登録者あり
				wKeylistUser = list( wListRes['Responce'].keys() )
				for wID in wKeylistUser :
					wID = str(wID)
					
					### 警告済はスキップ
					if wID in gVal.ARR_CautionTweet :
						continue
					### 自分には警告しない
					if str(gVal.STR_UserInfo['id'])==wID  :
						continue
					
###					wSubRes = self.SendTweet_Caution( wListRes['Responce'][wID], gVal.STR_UserInfo['Account'], wARR_IndListName[wKey], inFLG_ListCaution=True )
###					if wSubRes['Result']!=True :
###						wRes['Reason'] = "SendTweet_Caution is failed(1): user=" + wListRes['Responce'][wID]['screen_name'] + " list=" + wARR_IndListName[wKey]
					wSubRes = self.SendTweet_Caution( wListRes['Responce'][wID], gVal.STR_UserInfo['Account'], wListName, inFLG_ListCaution=True )
					if wSubRes['Result']!=True :
						wRes['Reason'] = "SendTweet_Caution is failed(1): user=" + wListRes['Responce'][wID]['screen_name'] + " list=" + wListName
						gVal.OBJ_L.Log( "B", wRes )
						continue
		
		#############################
		# ListFavo一覧のうち
		# 警告ありのリストをチェックする
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		for wKey in wKeylist :
			if gVal.ARR_ListFavo[wKey]['caution']!=True :
				### 警告なしはスキップ
				continue
			
			wStr = "〇チェック中リスト: " + gVal.ARR_ListFavo[wKey]['list_name']
			CLS_OSIF.sPrn( wStr )
			#############################
			# Twitterからリストの登録ユーザ一覧を取得
			wListRes = gVal.OBJ_Tw_IF.GetListSubscribers(
			   inListName=gVal.ARR_ListFavo[wKey]['list_name'],
			   inScreenName=gVal.ARR_ListFavo[wKey]['screen_name'] )
			
			if wListRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetListSubscribers): " + wListRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wListRes['Responce'])==0 :
				### 登録者なしはスキップ
				continue
			
			wKeylistUser = list( wListRes['Responce'].keys() )
			for wID in wKeylistUser :
				wID = str(wID)
				
				### 警告済はスキップ
				if wID in gVal.ARR_CautionTweet :
					continue
				### 自分には警告しない
				if str(gVal.STR_UserInfo['id'])==wID  :
					continue
				
				# ※警告確定
###				#############################
###				# 警告ツイートを作成
###				wTweet = "@" + wListRes['Responce'][wID]['screen_name'] + '\n'
###				wTweet = wTweet + "[ご注意] ユーザ " + gVal.ARR_ListFavo[wKey]['screen_name'] + " のリスト " + gVal.ARR_ListFavo[wKey]['list_name'] + " はフォロー禁止です。" + '\n'
###				wTweet = wTweet + "[Caution] Excuse me. The list " + gVal.ARR_ListFavo[wKey]['list_name'] + " for user " + gVal.ARR_ListFavo[wKey]['screen_name'] + " is unfollowable."
###				
###				wTweetID = "(none)"
###				if gVal.DEF_STR_TLNUM['sendListUsersCaution']==True :
###					#############################
###					# ツイート送信
###					wTweetRes = gVal.OBJ_Tw_IF.Tweet( wTweet )
###					if wTweetRes['Result']!=True :
###						wRes['Reason'] = "Twitter API Error(3): " + wTweetRes['Reason']
###						gVal.OBJ_L.Log( "B", wRes )
###						continue
###					else:
###						### Tweet完了まで10秒遅延待機
###						CLS_OSIF.sSleep(10)
###						
###						### ツイートIDを取得する
###						wTweetRes = gVal.GetSearch( wTweet )
###						if wTweetRes['Result']!=True :
###							wRes['Reason'] = "Twitter API Error(4): " + wTweetRes['Reason']
###							gVal.OBJ_L.Log( "B", wRes )
###							continue
###						if len(wTweetRes['Responce'])!=1 :
###							wRes['Reason'] = "Twitter is not one screen_name=" + wListRes['Responce'][wID]['screen_name']
###							gVal.OBJ_L.Log( "B", wRes )
###							continue
###						wTweetID = str( wTweetRes['Responce'][0]['id'] )
###						
###						### ログに記録
###						gVal.OBJ_L.Log( "U", wRes, "●リスト登録への警告: " + wListRes['Responce'][wID]['screen_name'] )
###				else:
###					### ログに記録
###					gVal.OBJ_L.Log( "U", wRes, "●リスト登録への警告(Twitter未送信): " + wListRes['Responce'][wID]['screen_name'] )
###				
###				### IDを警告済に追加
###				wSubRes = gVal.OBJ_DB_IF.SetCautionTweet( wListRes['Responce'][wID], wTweetID )
###				if wSubRes['Result']!=True :
###					wRes['Reason'] = "SetCautionTweet is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###					continue
				wSubRes = self.SendTweet_Caution( wListRes['Responce'][wID], gVal.ARR_ListFavo[wKey]['screen_name'], gVal.ARR_ListFavo[wKey]['list_name'], inFLG_ListCaution=True )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SendTweet_Caution is failed(1): user=" + wListRes['Responce'][wID]['screen_name'] + " list=" + gVal.ARR_ListFavo[wKey]['list_name']
					gVal.OBJ_L.Log( "B", wRes )
					continue
		
		wStr = "チェック終了" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 所有リストの登録者のうち、フォロワーじゃない人にフォローを促す
###		wStr = "全リストの登録ユーザチェック中..."
###		CLS_OSIF.sPrn( wStr )
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "全リストの登録ユーザチェック" )
		
		#############################
		# リストの取得
		wGetListsRes = gVal.OBJ_Tw_IF.GetLists( gVal.STR_UserInfo['Account'] )
		if wGetListsRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(31): " + wGetListsRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_Lists = wGetListsRes['Responce']
		
		wListFavo_Keylist = list( gVal.ARR_ListFavo.keys() )
		wKeylist = list( wARR_Lists.keys() )
		for wKey in wKeylist :
			### 自分のリスト以外はスキップ
			if wARR_Lists[wKey]['me']==False :
				continue
			
			### リストいいね登録中
			###   警告ありのものはスキップ(上で処理済)
			wFLG_ListFavo_Caution = False
			for wListFavoKey in wListFavo_Keylist :
				if wARR_Lists[wKey]['user']['screen_name']==gVal.ARR_ListFavo[wListFavoKey]['screen_name'] and \
				   wARR_Lists[wKey]['name']==gVal.ARR_ListFavo[wListFavoKey]['list_name'] :
					if gVal.ARR_ListFavo[wListFavoKey]['caution']==True :
						wFLG_ListFavo_Caution = True
					break
			
			if wFLG_ListFavo_Caution==True :
				### リストいいねで警告対象のリストはスキップ
				continue
			
			wStr = "〇チェック中リスト: " + wARR_Lists[wKey]['name']
			CLS_OSIF.sPrn( wStr )
			#############################
			# Twitterからリストの登録ユーザ一覧を取得
			wListRes = gVal.OBJ_Tw_IF.GetListSubscribers(
			   inListName=wARR_Lists[wKey]['name'],
			   inScreenName=wARR_Lists[wKey]['user']['screen_name'] )
			
			if wListRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetListSubscribers(2)): " + wListRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wListRes['Responce'])==0 :
				### 登録者なしはスキップ
				continue
			
			wARR_ListUsers = wListRes['Responce']
			
			wKeylistUser = list( wARR_ListUsers.keys() )
			for wID in wKeylistUser :
				wID = str(wID)
				
				### 警告済はスキップ
				if wID in gVal.ARR_CautionTweet :
					continue
				### 自分には警告しない
				if str(gVal.STR_UserInfo['id'])==wID  :
					continue
				### フォロワーはスキップ
				if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
					continue
				### 禁止ユーザはスキップ
###				wUserRes = self.CheckExtUser( wARR_ListUsers[wID], "フォロワー以外のリスト登録者", inFLG_Log=False )
				wUserRes = self.CheckExtUser( wARR_ListUsers[wID], "全リストチェック中の検出", inFLG_Log=False )
				if wUserRes['Result']!=True :
					wRes['Reason'] = "CheckExtUser failed"
					gVal.OBJ_L.Log( "B", wRes )
					continue
				if wUserRes['Responce']==False :
					### 禁止あり=除外
					continue
				
				# ※警告確定
				#############################
				# Twitterからユーザ情報を取得する
				wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=wARR_ListUsers[wID]['screen_name'] )
				if wUserInfoRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wUserInfoRes['Reason'] + " screen_name=" + wARR_ListUsers[wID]['screen_name']
					gVal.OBJ_L.Log( "B", wRes )
					continue
				
				#############################
				# 次のユーザはブロック→リムーブする(リスト強制解除)
				# ・非フォロワー
				# ・ツイート数=0
				# ・鍵アカウント
				if wUserInfoRes['Responce']['statuses_count']==0 or \
				   wUserInfoRes['Responce']['protected']==True :
					wBlockRes = gVal.OBJ_Tw_IF.BlockRemove( wID )
					if wBlockRes['Result']!=True :
						wRes['Reason'] = "Twitter API Error(BlockRemove): " + wBlockRes['Reason'] + " screen_name=" + wARR_ListUsers[wID]['screen_name']
						gVal.OBJ_L.Log( "B", wRes )
						continue
					
					### ユーザレベル変更
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "G-" )
					
					### トラヒック記録（フォロワー減少）
					CLS_Traffic.sP( "d_follower" )
					
					### ログに記録
					gVal.OBJ_L.Log( "R", wRes, "追い出し: screen_name=" + wARR_ListUsers[wID]['screen_name'] )
				
				#############################
				# 通常アカウントへは警告ツイートを送信
				else:
###					wTweetID = "(none)"
###					#############################
###					# 警告の送信が有効の場合
###					if gVal.DEF_STR_TLNUM['sendListUsersCaution']==True :
###						#############################
###						# 警告ツイートを作成
###						wTweet = "@" + wARR_ListUsers[wID]['screen_name'] + '\n'
###						wTweet = wTweet + "[お願い] リスト " + wARR_Lists[wKey]['name'] + " をフォローするには当アカウント " + gVal.STR_UserInfo['Account'] + " もフォローしてください。" + '\n'
###						wTweet = wTweet + "[Request] To follow the list " + wARR_Lists[wKey]['name'] + ", please also follow this account " + gVal.STR_UserInfo['Account'] + "."
###						
###						#############################
###						# ツイート送信
###						wTweetRes = gVal.OBJ_Tw_IF.Tweet( wTweet )
###						if wTweetRes['Result']!=True :
###						###	if wTweetRes['StatusCode']=="403" :
###							wRes['Reason'] = "Twitter API Error(38): " + wTweetRes['Reason']
###							gVal.OBJ_L.Log( "B", wRes )
###							continue
###						else:
###							### Tweet完了→Twitter再取得可能になるまで約10秒遅延待機
###							CLS_OSIF.sSleep(10)
###							
###							#############################
###							# 送信したツイートのパターン生成
###							wNoRet_Tweet = wTweet.replace( "@", "" )
###							wNoRet_Tweet = wNoRet_Tweet.replace( "[", "" )
###							wNoRet_Tweet = wNoRet_Tweet.replace( "]", "" )
###							
###							wTweetRes = gVal.OBJ_Tw_IF.GetSearch( wNoRet_Tweet )
###							if wTweetRes['Result']!=True :
###								wRes['Reason'] = "Twitter API Error(48): " + wTweetRes['Reason']
###								gVal.OBJ_L.Log( "B", wRes )
###								continue
###							
###							#############################
###							# 送信したツイートのツイートIDを取得する
###							if len(wTweetRes['Responce'])==1 :
###								wTweetID = str( wTweetRes['Responce'][0]['id'] )
###							else:
###								### 1ツイート以外はありえない？
###								wRes['Reason'] = "Twitter is dual ttweet, or not one screen_name=" + wARR_ListUsers[wID]['screen_name']
###								gVal.OBJ_L.Log( "D", wRes )
###							
###							### ログに記録
###							gVal.OBJ_L.Log( "U", wRes, "●非フォロワーのリスト登録者: screen_name=" + wARR_ListUsers[wID]['screen_name'] + " tweetid=" + wTweetID )
###					
###					#############################
###					# 警告の送信が有効の場合
###					else:
###						### ログに記録
###						gVal.OBJ_L.Log( "U", wRes, "●非フォロワーのリスト登録者(Twitter未送信): screen_name=" + wARR_ListUsers[wID]['screen_name'] )
###					
###					### IDを警告済に追加
###					wSubRes = gVal.OBJ_DB_IF.SetCautionTweet( wARR_ListUsers[wID], wTweetID )
###					if wSubRes['Result']!=True :
###						wRes['Reason'] = "SetCautionTweet is failed"
###						gVal.OBJ_L.Log( "B", wRes )
###						continue
					wSubRes = self.SendTweet_Caution( wARR_ListUsers[wID], gVal.STR_UserInfo['Account'], wARR_Lists[wKey]['name'], inFLG_ListCaution=False )
					if wSubRes['Result']!=True :
						wRes['Reason'] = "SendTweet_Caution is failed(2): user=" + wARR_ListUsers[wID]['screen_name'] + " list=" + wARR_Lists[wKey]['name']
						gVal.OBJ_L.Log( "B", wRes )
						continue
		
		wStr = "チェック終了" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes

	#####################################################
	# 警告ツイート送信
	#####################################################
	def SendTweet_Caution( self, inUser, inOwnerName, inListName, inFLG_ListCaution=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SendTweet_Caution"
		
		wRes['Responce'] = False
		
###		wUserID     = str(inUser['id'])
		wScreenName = inUser['screen_name']
		
		wTweetID = gVal.DEF_NOTEXT
		#############################
		# 警告ツイートを作成
		if inFLG_ListCaution==True :
			### 警告リスト登録者への警告
			wTweet = "@" + wScreenName + '\n'
			wTweet = wTweet + "[ご注意] ユーザ " + str(inOwnerName) + " のリスト " + str(inListName) + " はフォロー禁止です。" + '\n'
			wTweet = wTweet + "[Caution] Excuse me. The list " + str(inListName) + " for user " + str(inOwnerName) + " is unfollowable."
		
		else:
			### 非フォロワーのリスト登録者への警告
			wTweet = "@" + wScreenName + '\n'
			wTweet = wTweet + "[お願い] リスト " + str(inListName) + " をフォローするには当アカウント " + str(inOwnerName) + " もフォローしてください。" + '\n'
			wTweet = wTweet + "[Request] To follow the list " + str(inListName) + ", please also follow this account " + str(inOwnerName) + "."
		
		#############################
		# 送信したツイートのパターン生成
		wNoRet_Tweet = wTweet.replace( "@", "" )
		wNoRet_Tweet = wNoRet_Tweet.replace( "[", "" )
		wNoRet_Tweet = wNoRet_Tweet.replace( "]", "" )
		
		#############################
		# Twitterへの送信が有効の場合
		if gVal.DEF_STR_TLNUM['sendListUsersCaution']==True :
			#############################
			# ツイート送信
			wTweetRes = gVal.OBJ_Tw_IF.Tweet( wTweet )
			if wTweetRes['Result']!=True :
			###	if wTweetRes['StatusCode']=="403" :
				wRes['Reason'] = "Twitter API Error(Tweet): " + wTweetRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			else:
				### Tweet完了→Twitter再取得可能になるまで約10秒遅延待機
				CLS_OSIF.sSleep(10)
				
				wTweetRes = gVal.OBJ_Tw_IF.GetSearch( wNoRet_Tweet )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error(GetSearch): " + wTweetRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				#############################
				# 送信したツイートのツイートIDを取得する
				if len(wTweetRes['Responce'])==1 :
					wTweetID = str( wTweetRes['Responce'][0]['id'] )
				else:
					### 1ツイート以外はありえない？
					wRes['Reason'] = "Twitter is dual ttweet, or not one screen_name=" + wScreenName
					gVal.OBJ_L.Log( "D", wRes )
					return wRes
				
				### ログに記録
				wStr = "リスト登録者へ警告(規定外ユーザ): screen_name=" + wScreenName + " tweetid=" + wTweetID + " list=" + str(inListName)
				gVal.OBJ_L.Log( "RR", wRes, wStr )
			
			wRes['Responce'] = True	#Twitterへ送信済
		
		#############################
		# Twitterへの送信が無効の場合
		else:
			### ログに記録
			wStr = "リスト登録者へ警告(規定外ユーザ・Twitter未送信): screen_name=" + wScreenName + " tweetid=" + wTweetID + " list=" + str(inListName)
			gVal.OBJ_L.Log( "RR", wRes, wStr )
		
		#############################
		# IDを警告済に追加
		wSubRes = gVal.OBJ_DB_IF.SetCautionTweet( inUser, wTweetID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetCautionTweet is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# 自動リムーブチェック
#####################################################
###	def CheckAutoRemove( self, inData, inWord ):
	def CheckAutoRemove(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckAutoRemove"
		
		wRes['Responce'] = False
		#############################
		# 自動リムーブが無効ならここで終わる
		if gVal.STR_UserInfo['AutoRemove']==False :
			wRes['Result'] = True
			return wRes
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['auto_remove'] ), inThreshold=gVal.DEF_STR_TLNUM['forCheckAutoRemoveSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			### 規定以内は除外
			wStr = "●自動リムーブチェック期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
###		wStr = "自動リムーブチェック中..."
###		CLS_OSIF.sPrn( wStr )
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "自動リムーブチェック" )
		
		#############################
		# ListFavo一覧のうち
		# 自動リムーブ有効のリストをチェックする
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		for wKey in wKeylist :
			if gVal.ARR_ListFavo[wKey]['auto_rem']!=True :
				### 自動リムーブ無効はスキップ
				continue
			
			wStr = "〇チェック中リスト: " + gVal.ARR_ListFavo[wKey]['list_name']
			CLS_OSIF.sPrn( wStr )
			#############################
			# Twitterからリストの登録ユーザ一覧を取得
			wListRes = gVal.OBJ_Tw_IF.GetListMember(
			   inListName=gVal.ARR_ListFavo[wKey]['list_name'],
			   inScreenName=gVal.ARR_ListFavo[wKey]['screen_name'] )
			
			if wListRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetListMember): " + wListRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wListRes['Responce'])==0 :
				### 登録者なしはスキップ
				continue
			
			wKeylistUser = list( wListRes['Responce'].keys() )
			for wID in wKeylistUser :
				wID = str(wID)
				
				###自分は除外する
				if str(gVal.STR_UserInfo['id'])==wID :
					continue
				
				#############################
				# 自動リムーブ
				wSubRes = self.OBJ_TwitterFollower.AutoRemove( wListRes['Responce'][wID] )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "AutoRemove is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "auto_remove", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['auto_remove']
		
		wStr = "チェック終了" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 除外文字チェック
#####################################################
	def CheckExtWord( self, inData, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckExtWord"
		
		wRes['Responce'] = False
		#############################
		# 除外文字があるかチェック
		for wExeWord in gVal.ARR_ExeWordKeys :
			if inWord.find( wExeWord )>=0 :
				if gVal.ARR_ExeWord[wExeWord]['report']==True :
					### 報告対象の表示と、ログに記録(テストログ)
					gVal.OBJ_L.Log( "N", wRes, "●報告対象の文字除外: id=" + inData['screen_name'] + " word=" + inWord )
				else:
					### 報告対象の表示と、ログに記録(テストログ)
					gVal.OBJ_L.Log( "N", wRes, "文字除外: id=" + inData['screen_name'] + " word=" + inWord )
				
				### 除外
				wRes['Result'] = True
				return wRes
		
		#############################
		# 正常終了
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes



#####################################################
# 禁止ユーザチェック
#####################################################
###	def CheckExtUser( self, inName, inReason ):
###	def CheckExtUser( self, inName, inReason, inFLG_Log=True ):
	def CheckExtUser( self, inData, inReason, inFLG_Log=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckExtUser"
		
		wUserID = str(inData['id'])
		
		wRes['Responce'] = False
		#############################
		# 禁止ユーザかチェック
###		if inName in gVal.ARR_NotReactionUser :
		if wUserID in gVal.ARR_NotReactionUser :
###			if gVal.ARR_NotReactionUser[inName]['vip']==True :
			if gVal.ARR_NotReactionUser[wUserID]['vip']==True :
				### VIPは除外する
				wRes['Result'] = True
				return wRes
			
###			if gVal.ARR_NotReactionUser[inName]['report']==True and inFLG_Log==True :
			if gVal.ARR_NotReactionUser[wUserID]['report']==True and inFLG_Log==True :
				### 報告対象の表示と、ログに記録(テストログ)
###				gVal.OBJ_L.Log( "N", wRes, "●禁止ユーザ: user=" + inName + " reason=" + inReason )
				gVal.OBJ_L.Log( "N", wRes, "●禁止ユーザ: screen_name=" + inData['screen_name'] + " reason=" + inReason )
			
			### 除外
			wRes['Result'] = True
			return wRes
		
		#############################
		# 正常終了
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes



#####################################################
# VIPユーザチェック
#####################################################
	def CheckVIPUser( self, inData ):
		
		wUserID = str(inData['id'])
		
		#############################
		# 禁止ユーザかチェック
		if wUserID in gVal.ARR_NotReactionUser :
			if gVal.ARR_NotReactionUser[wUserID]['vip']==True :
				### VIP
				return True
		
		return False



#####################################################
# VIP監視ユーザリスト取得
#####################################################
	def GetVIPUser(self):
		
		wARR_List = []
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			### 自分は監視しない
			if wID==str(gVal.STR_UserInfo['id']) :
				continue
			
			if gVal.ARR_NotReactionUser[wID]['ope']==True :
				wARR_List.append( wID )
		
		return wARR_List



#####################################################
# 新規いいね情報の設定
#####################################################
	def SetNewFavoData( self, inUser, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetNewFavoData"
		
		if inData['level_tag']!=gVal.DEF_NOTEXT :
			### 既にレベルが設定されてたら終わる
			wRes['Result'] = True
			return wRes
		
		wID = str(inData['id'])
		
		wMyFollow = None
		wFollower = None
		wUserLevel = "F"
		#############################
		# 関係性チェック
		wFollowInfoRes = gVal.OBJ_Tw_IF.GetFollowInfo( wID )
		if wFollowInfoRes['Result']!=True :
			wRes['Reason'] = "GetFollowInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wFollowInfoRes['Responce']['blocked_by']==True :
			### 被ブロック検知
			wUserLevel = "G"
			
			wStr = "●被ブロック検知"
			gVal.OBJ_L.Log( "R", wRes, wStr + ": " + inData['screen_name'] )
		
		### 片フォロー者の場合
		elif wFollowInfoRes['Responce']['following']==True and \
		     wFollowInfoRes['Responce']['followed_by']==False :
			wMyFollow = True
			wUserLevel = "D"
			
			### 相互フォローリストに追加
###			wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wID )
			wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( inData )
		
		### フォロワーの場合
		elif wFollowInfoRes['Responce']['following']==False and \
		     wFollowInfoRes['Responce']['followed_by']==True :
			wFollower = True
			wUserLevel = "E"
			
			### 片フォロワーリストに追加
###			wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( wID )
			wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( inData )
		
		### 相互フォローの場合
		elif wFollowInfoRes['Responce']['following']==True and \
		     wFollowInfoRes['Responce']['followed_by']==True :
			wMyFollow = True
			wFollower = True
			wUserLevel = "C+"
			
			### 相互フォローリストに追加
###			wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wID )
			wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( inData )
		
		#############################
		# ユーザレベル変更
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
		
		#############################
		# フォロー情報をDBへ反映する
		if wMyFollow!=None or wFollower!=None :
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wID, wMyFollow, wFollower )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateFavoData_Follower is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 更新によりデータリロード
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( inUser, inFLG_New=False )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Responce'] = wSubRes['Responce']
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# レベルタグ出力
#####################################################
	def LevelTagSttring( self, inLevelTag ):
		wLevelTag = str(inLevelTag)
		if len(inLevelTag)<2 :
			wLevelTag = wLevelTag + " "
		return wLevelTag



#####################################################
# システム情報の表示
#####################################################
	def View_Sysinfo(self):
		#############################
		# Twitter情報取得
		wFavoRes = self.GetTwitterInfo()
		if wFavoRes['Result']!=True :
			return wFavoRes
		
		wRes = self.OBJ_TwitterAdmin.View_Sysinfo()
		return wRes




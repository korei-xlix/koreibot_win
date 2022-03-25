#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 メインモジュール
#####################################################
from twitter_favo import CLS_TwitterFavo
from twitter_follower import CLS_TwitterFollower
from twitter_keyword import CLS_TwitterKeyword
from twitter_admin import CLS_TwitterAdmin

from osif import CLS_OSIF
from traffic import CLS_Traffic
from gval import gVal
#####################################################
class CLS_TwitterMain():
#####################################################
	OBJ_TwitterFavo     = None
	OBJ_TwitterFollower = None
	OBJ_TwitterKeyword  = None
	OBJ_TwitterAdmin    = None



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
		
		#############################
		# いいね情報の取得
		wResSub = self.OBJ_TwitterFavo.Get()
		if wResSub['Result']!=True :
			wRes['Reason'] = "OBJ_TwitterFavo.Get failed: " + CLS_OSIF.sCatErr( wResSub )
			return wRes
		
		#############################
		# いいね監視の実行
		wResSub = self.OBJ_TwitterFavo.Run()
		if wResSub['Result']!=True :
			wRes['Reason'] = "OBJ_TwitterFavo.Run failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# Init
#####################################################
	def __init__(self):
		self.OBJ_TwitterFavo     = CLS_TwitterFavo( parentObj=self )
		self.OBJ_TwitterFollower = CLS_TwitterFollower( parentObj=self )
		self.OBJ_TwitterKeyword  = CLS_TwitterKeyword( parentObj=self )
		self.OBJ_TwitterAdmin    = CLS_TwitterAdmin( parentObj=self )
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
		
		#############################
		# 時間を取得
		wSubRes = self.TimeUpdate( inInit=True )
		if wSubRes['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "TimeUpdate is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# Twitterから自ユーザ情報を取得する
		wUserinfoRes = gVal.OBJ_Tw_IF.GetMyUserinfo()
		if wUserinfoRes['Result']!=True :
			wRes['Reason'] = "Twitter Error"
			gVal.OBJ_L.Log( "B", wRes )
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
		# 除外ユーザ名読み込み
		wResSub = gVal.OBJ_DB_IF.GetExeUser()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetExeUser failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 除外文字読み込み
		wResSub = gVal.OBJ_DB_IF.GetExeWord()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetExcWord failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# アクションリツイート文字読み込み
		wResSub = gVal.OBJ_DB_IF.GetActionRetweet()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetActionRetweet failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 定期時刻のチェック
		gVal.STR_SystemInfo['NextDay'] = False
		gVal.STR_SystemInfo['Weekend'] = False
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# グローバル時間更新
#####################################################
	def TimeUpdate( self, inInit=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "TimeUpdate"
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "sGetTime is faied"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### wTD['TimeDate']
		
		#############################
		# 時間を設定
		### 初回起動で時刻が入ってなければ、ロック時間を設定する
		if inInit==False :
			if gVal.STR_SystemInfo['RateTimeDate']==None :
				gVal.STR_SystemInfo['RateTimeDate'] = str(gVal.STR_SystemInfo['RateLockTD'])
			else :
				gVal.STR_SystemInfo['RateTimeDate'] = gVal.STR_SystemInfo['TimeDate']
		
		gVal.STR_SystemInfo['TimeDate'] = wTD['TimeDate']
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



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
		# 前回チェックから15分経っているか
		wGetLag = CLS_OSIF.sTimeLag( gVal.STR_SystemInfo['APIrect'], inThreshold=gVal.DEF_STR_TLNUM['resetAPISec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		if wGetLag['Beyond']==False :
			###前回から15分経ってない
			wRes['Result'] = True
			return wRes
		
		### ※前回から15分経ったので処理実行
		
		#############################
		# Twitter再接続
		wTwitterRes = gVal.OBJ_Tw_IF.ReConnect()
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitterの再接続失敗"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# カウント時刻を更新
		gVal.STR_SystemInfo['APIrect'] = str(wGetLag['NowTime'])
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 周期1日ごと処理
#####################################################
	def Circle1Day(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "Circle1Day"
		
		#############################
		# DB記録リセット
		wQuery = "update tbl_follower_data set " + \
					"get_agent = False, " + \
					"favo_f_cnt = 0, " + \
					"r_favo_f_cnt = 0, " + \
					"rt_cnt = 0 " + \
					" ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 候補ユーザ消去
		gVal.ARR_FollowKouho = {}
		
		gVal.STR_SystemInfo['NextDay'] = False
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 周期 週末ごと処理
#####################################################
	def CircleWeekend( self, inWeekend ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CircleWeekend"
		
		wRes['Responce'] = False
		
		# inWeekend
		# wRes = {
		# 	"Result"	: False,
		# 	"RateTD"	: "",
		# 	"NextTD"	: "",
		# 	"Weekday"	: False,
		# 	"Weekend"	: False
		# }
		
		#############################
		# 週末日時ログ
		wStr = "週末情報：Rate=" + inWeekend['RateTD'] + " Next=" + inWeekend['NextTD'] + " Day=" + str(inWeekend['Weekday'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# トロフィー獲得者
		wSubRes = self.OBJ_TwitterFollower.TorpyGetter()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "TorpyGetter is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wRes['Responce'] = wSubRes['Responce']
		
		gVal.STR_SystemInfo['Weekend'] = False
		
		#############################
		# フォロー者候補 クリア
		wResSub = gVal.OBJ_DB_IF.ClearFollowAgent()
		if wResSub['Result']!=True :
			wRes['Reason'] = "ClearFollowAgent failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 自動リツイート クリア
		wResSub = gVal.OBJ_DB_IF.ClearAutoRetweet()
		if wResSub['Result']!=True :
			wRes['Reason'] = "ClearAutoRetweet failed"
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
# 除外チェック系
#####################################################
#####################################################
# 除外ユーザ名 チェック
#   ユーザ名とプロフィールのチェックに使う
#####################################################
	def CheckExcUser( self, inWord ):
		for wLine in gVal.STR_ExeUser :
			if inWord.find( wLine )>=0 :
				return False
		return True



#####################################################
# 除外文字 チェック
#####################################################
	def CheckExcWord( self, inWord ):
		for wLine in gVal.STR_ExeWord :
			if inWord.find( wLine )>=0 :
				return False
		return True



#####################################################
# 全自動監視の実行
#####################################################
	def AllRun(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "AllRun"
		
		#############################
		# ユーザ一覧取得
		wTwitterRes = self.GetUser()
		if wTwitterRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetUser is failed: " + CLS_OSIF.sCatErr( wTwitterRes )
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# いいね情報の取得
		wResSub = self.OBJ_TwitterFavo.Get()
		if wResSub['Result']!=True :
			wRes['Reason'] = "OBJ_TwitterFavo.Get failed: " + CLS_OSIF.sCatErr( wResSub )
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リアクションチェック
		wResSub = self.OBJ_TwitterFollower.ReactionCheck_new()
		if wResSub['Result']!=True :
			wRes['Reason'] = "OBJ_TwitterFollower.ReactionCheck_new failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# フォロワー情報の実行
		wResSub = self.OBJ_TwitterFollower.Run()
		if wResSub['Result']!=True :
			wRes['Reason'] = "OBJ_TwitterFollower.Run failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# いいね監視の実行
		wResSub = self.OBJ_TwitterFavo.Run()
		if wResSub['Result']!=True :
			wRes['Reason'] = "OBJ_TwitterFavo.Run failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 通常いいねの実行
		wResSub = self.OBJ_TwitterFavo.NormalFavo()
		if wResSub['Result']!=True :
			wRes['Reason'] = "OBJ_TwitterFavo.NormalFavo failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes


#####################################################
# ユーザ取得
#####################################################
	def GetUser(self):
		wRes = self.OBJ_TwitterFollower.Get()
		return wRes



#####################################################
# いいね取得
#####################################################
	def GetFavo(self):
		wRes = self.OBJ_TwitterFavo.Get()
		return wRes



#####################################################
# フォロワー情報表示
#####################################################
	def ViewFollower( self, inFLGall=False ):
		wRes = self.OBJ_TwitterFollower.View( inFLGall )
		return wRes



#####################################################
# トレンドツイート
#####################################################
	def TrendTweet(self):
		wRes = self.OBJ_TwitterKeyword.TrendTweet()
		return wRes



#####################################################
# VIPいいね
#####################################################
	def VIPFavo(self):
		wRes = self.OBJ_TwitterFavo.VIPFavo()
		return wRes



#####################################################
# ちょっかいいいね
#####################################################
	def ChoFavo(self):
		wRes = self.OBJ_TwitterFavo.ChoFavo()
		return wRes



#####################################################
# フォローサーチ
#####################################################
	def FollowSearch(self):
		wRes = self.OBJ_TwitterFollower.FollowSearch()
		return wRes



#####################################################
# フォロー候補表示
#####################################################
	def ViewFollowAgent(self):
		wRes = self.OBJ_TwitterFollower.AutoNewFollow( inViewNum=gVal.DEF_STR_TLNUM['manualNewFollowNum'] )
		return wRes



#####################################################
# ユーザ管理
#####################################################
	def UserAdmin(self):
		wRes = self.OBJ_TwitterAdmin.UserAdmin()
		return wRes



#####################################################
# ブロックチェック
#####################################################
	def BlockCheck(self):
		wRes = self.OBJ_TwitterFollower.BlockCheck()
		return wRes



#####################################################
# 自動リツイート判定
#####################################################
	def DetectAutoRetweet( self, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "DetectAutoRetweet"
		
		wRes['Responce'] = False
		#############################
		# ツイートを改行ごとに分割する
		wARR_Tweet = inTweet.split('\n')
		
		#############################
		# 判定
		for wTweet in wARR_Tweet :
			for wAutoRetweet in gVal.STR_ActionRetweet :
				if wTweet.find( wAutoRetweet )>=0 :
					# 自動リツイート文字あり
					wRes['Responce'] = True
					break
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes




#####################################################
# 自動リツイート実行
#####################################################
	def GoAutoRetweet( self, inARR_Users ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "GoAutoRetweet"
		
		#############################
		# ユーザごとに処理する
		for wObjUserID in inARR_Users :
			wObjUserID = str(wObjUserID)
			
			#############################
			# 対象の直近のツイートを取得
			wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
				 inID=wObjUserID, inCount=gVal.DEF_STR_TLNUM['reactionRetweetLine'] )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: GetTL"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wTweetRes['Responce'])==0 :
				wRes['Reason'] = "Tweet is not get: me"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wTweetLen = len(wTweetRes['Responce'])
			
			#############################
			# 取得ツイートからリツイートするIDを選定する(最新1個だけ)
			#   アクションリツイートで設定されたもののうち、
			#   最新でヒットした1ツイートだけが処理される
			#   その最新が既にリツイート済みなら、リツイートは済んだとして処理しない
			wScreenName = None
			wRetweetID  = None
			for wTweet in wTweetRes['Responce'] :
				wUserID = str(wTweet['user']['id'])
				wScreenName = wTweet['user']['screen_name']
				
				###対象以外はスキップ
				if wObjUserID!=wUserID :
					continue
				
				###自動リツイート対象のツイートでなければスキップ
				wFLG_Retweet = False
				### ツイートを改行ごとに分割する
				wARR_Tweet = wTweet['text'].split('\n')
				
				for wObjTweet in wARR_Tweet :
					for wRetweet in gVal.STR_ActionRetweet :
						if wObjTweet.find( wRetweet )>=0 :
							# 自動リツイート文字あり
							wFLG_Retweet = True
							break
				if wFLG_Retweet==False :
					continue
				
				###リツイート候補のツイートID
				wTweetID = str( wTweet['id'] )
				
				### 既にリツイート済みツイートか
				wSubRes = gVal.OBJ_DB_IF.CheckAutoRetweet( wTweetID )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "GetActionRetweet failed"
					gVal.OBJ_L.Log( "C", wRes )
					continue
				if wSubRes['Responce']!=True :
					continue
				
				###リツイートのなかに自分のIDが入っているかチェック
				wSubRes = gVal.OBJ_Tw_IF.GetRetweetLookup( wTweetID )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "Twitter Error(GetRetweetLookup): Tweet ID: " + wTweetID
					gVal.OBJ_L.Log( "B", wRes )
					continue
				wFLG_Retweet = False
				wKeylist = list( wSubRes['Responce'] )
				for wID in wKeylist :
					wID = str(wID)
					if str(gVal.STR_UserInfo['id'])==wID :
						# リツイ済
						wFLG_Retweet = True
						break
				if wFLG_Retweet==True :
					# 最新がリツイ済みなら処理停止
					break
				
				# ※リツイート確定
				wRetweetID = wTweetID
				break
			
			#############################
			# リツイートする
			#   未決定ならエラー表示だけ
			if wFLG_Retweet==True :
				wStr = "●既に自動リツイート済: " + str( wScreenName ) ;
				CLS_OSIF.sPrn( wStr )
			elif wRetweetID==None :
				wStr = "●自動リツイート対象なし: " + str( wScreenName ) ;
				CLS_OSIF.sPrn( wStr )
			else :
				wSubRes = gVal.OBJ_Tw_IF.Retweet( wRetweetID )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "Twitter Error(Retweet): Tweet ID: " + wRetweetID
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				wStr = "〇自動リツイート完了: " + str( wScreenName )
				CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ制御：フォロー
#####################################################
	def SetMyFollow( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetMyFollow"
		
		wID = str( inData['id'] )
		wName = str( inData['name'].replace( "'", "''" ) )
		wScreenName = str( inData['screen_name'] )
		wLastCount = 0
		if "lastcount" in inData :
			wLastCount = inData['lastcount']		#DBのツイート数
		elif "statuses_count" in inData :
			wLastCount = inData['statuses_count']	#Twitterのツイート数
		
		#############################
		# 状況表示
		wStr = "フォロー処理中......: @" + wScreenName
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# フォローする
		wTwitterRes = gVal.OBJ_Tw_IF.Follow( wID, True )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# DB未登録なら枠を作る
		if gVal.OBJ_DB_IF.CheckFollowerData(wID)==False :
			wSubRes = gVal.OBJ_DB_IF.InsertFollowerData( inData )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "InsertFollowerData is failed: " + CLS_OSIF.sCatErr( wSubRes )
				return wRes
			
			###※DB登録
			wText = "DBに登録したユーザ: @" + wScreenName
			gVal.OBJ_L.Log( "U", wRes, wText )
		
		#############################
		# DB更新
		wQuery = "update tbl_follower_data set " + \
					"r_myfollow = True, " + \
					"rc_myfollow = True, " + \
					"un_follower = False, " + \
					"removed = False, " + \
					"adm_agent = True, " + \
					"foldate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "', " + \
					"name = '" + str( wName ) + "', " + \
					"screen_name = '" + str( wScreenName ) + "', " + \
					"lastcount = " + str( wLastCount ) + ", " + \
					"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + wID + "' ;"
		
		###実行
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		###※フォロー
		gVal.OBJ_L.Log( "U", wRes, "フォローしたユーザ: @" + wScreenName )
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ制御：非フォロー化解除
#####################################################
	def SetActiveFollow( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetActiveFollow"
		
		wID = str( inData['id'] )
		wScreenName = str( inData['screen_name'] )
		
		#############################
		# 状況表示
		wStr = "非フォロー化解除処理中......: @" + wScreenName
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 非フォローをOFFにする
		wQuery = "update tbl_follower_data set " + \
					"un_follower = False " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + wID + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		gVal.OBJ_L.Log( "U", wRes, "非フォロー化解除: @" + wScreenName )
		
		#############################
		# トラヒック計測：非フォロー化解除数
		gVal.STR_TrafficInfo['run_unfollowrem'] += 1
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ制御：非フォロー化
#####################################################
	def SetUnfollow( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetUnfollow"
		
		wID = str( inData['id'] )
		wScreenName = str( inData['screen_name'] )
		
		#############################
		# 状況表示
		wStr = "非フォロー化処理中......: @" + wScreenName
		CLS_OSIF.sPrn( wStr )
		
		inData['un_fol_cnt'] += 1
		wUnfolLock = False
		if gVal.DEF_STR_TLNUM['forUnfollowLockCount']<=inData['un_fol_cnt'] :
			# 非フォロー化ロック
			wUnfolLock = True
		
		#############################
		# 非フォローをONにする
		wQuery = "update tbl_follower_data set " + \
					"un_follower = True, " + \
					"un_fol_lock = " + str(wUnfolLock) + ", " + \
					"un_fol_cnt = " + str(inData['un_fol_cnt']) + ", " + \
					"limited = False " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + wID + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		gVal.OBJ_L.Log( "U", wRes, "非フォロー化: @" + wScreenName )
		if wUnfolLock== True :
			gVal.OBJ_L.Log( "U", wRes, "非フォロー化ロック(自動解除不能): @" + wScreenName )
		
		#############################
		# トラヒック計測：非フォロー化実行数
		gVal.STR_TrafficInfo['run_unfollow'] += 1
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ制御：非フォローロックOFF
#####################################################
	def SetUnfollowLockoff( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetUnfollowLockoff"
		
		wID = str( inData['id'] )
		wScreenName = str( inData['screen_name'] )
		
		#############################
		# 状況表示
		wStr = "非フォローロックOFF中......: @" + wScreenName
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 非フォローをONにする
		wQuery = "update tbl_follower_data set " + \
					"un_fol_lock = False, " + \
					"un_fol_cnt = 0, " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + wID + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		gVal.OBJ_L.Log( "U", wRes, "非フォローロックOFF: @" + wScreenName )
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ制御：リムーブ
#####################################################
	def RelRemove( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "RelRemove"
		
		wID = str( inData['id'] )
		wScreenName = str( inData['screen_name'] )
		
		#############################
		# 状況表示
		wStr = "リムーブ処理中......: @" + wScreenName
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# リムーブする
		wRemoveRes = gVal.OBJ_Tw_IF.Remove( wID )
		if wRemoveRes['Result']!=True :
			wRes['Reason'] = "Twitter Error"
			gVal.OBJ_L.Log( "B", wRes )
			if wRemoveRes['StatusCode']==404 :
				###存在しないのでDBから抹消する
				self.RelElase( inData, inDBonly=True )
			return wRes
		
		#############################
		# limited をOFF、removed をONにする
		wQuery = "update tbl_follower_data set " + \
					"rc_myfollow = False, " + \
					"limited = False " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + wID + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.OBJ_L.Log( "U", wRes, "リムーブ処理: @" + wScreenName )
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ制御：ブロック→リムーブ
#####################################################
	def BlockRemove( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "BlockRemove"
		
		wID = str( inData['id'] )
		wScreenName = str( inData['screen_name'] )
		
		#############################
		# 状況表示
		wStr = "ブロックリムーブ処理中......: @" + wScreenName
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# ブロック→ブロック解除する
		wRemoveRes = gVal.OBJ_Tw_IF.BlockRemove( wID )
		if wRemoveRes['Result']!=True :
			wRes['Reason'] = "Twitter Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# limited をOFF、removed をONにする
		wQuery = "update tbl_follower_data set " + \
					"rc_myfollow = False, " + \
					"rc_follower = False, " + \
					"limited = False " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + wID + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		gVal.OBJ_L.Log( "U", wRes, "ブロックリムーブ処理: @" + wScreenName )
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ制御：疑似リムーブ
#####################################################
	def SoftRemove( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SoftRemove"
		
		wID = str( inData['id'] )
		wScreenName = str( inData['screen_name'] )
		
		#############################
		# 状況表示
		wStr = "疑似リムーブ処理中......: @" + wScreenName
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# limited をOFF、removed をONにする
		wQuery = "update tbl_follower_data set " + \
					"limited = False, " + \
					"removed = True " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + wID + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.OBJ_L.Log( "U", wRes, "疑似リムーブ処理: @" + wScreenName )
		
		#############################
		# トラヒック計測：自動リムーブ実行数
		gVal.STR_TrafficInfo['run_autoremove'] += 1
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ制御：ユーザ抹消
#####################################################
	def RelElase( self, inData, inDBonly=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "RelElase"
		
		wID = str( inData['id'] )
		wScreenName = str( inData['screen_name'] )
		
		#############################
		# 状況表示
		wStr = "未活動のユーザ情報消去 処理中......: @" + wScreenName
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# リムーブする
		if inDBonly==False :
			wRemoveRes = gVal.OBJ_Tw_IF.Remove( wID )
			if wRemoveRes['Result']!=True :
				wRes['Reason'] = "Twitter Error"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# DB削除
		wQuery = "delete from tbl_follower_data " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + wID + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		gVal.OBJ_L.Log( "U", wRes, "ユーザ情報消去: @" + wScreenName )
		wRes['Result'] = True
		return wRes



#####################################################
# DBフォロワー取得
#####################################################
	def GetDBFollower(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "GetDBFollower"
		
		#############################
		# DBのフォロワー一覧取得
		wQuery = "select * from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_RateFollowers = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 添え字をIDに差し替える
		wARR_RateFollowers = gVal.OBJ_DB_IF.ChgDataID( wARR_RateFollowers )
		
		wRes['Responce'] = wARR_RateFollowers
		wRes['Result']   = True
		return wRes



#####################################################
# DBフォロワー登録
#####################################################
	def InsertNewFollower( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "InsertNewFollower"
		
		#############################
		# ユーザ情報を取得する
		wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=inID )
		if wUserInfoRes['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# DBに登録
		wSubRes = gVal.OBJ_DB_IF.InsertFollowerData( wUserInfoRes['Responce'] )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "InsertFollowerData is failed: " + CLS_OSIF.sCatErr( wSubRes )
			return wRes
		
		gVal.OBJ_L.Log( "U", wRes, "DBに登録したユーザ: @" + str( wUserInfoRes['Responce']['screen_name'] ) )
		
		wRes['Result']   = True
		return wRes



#####################################################
# ユーザ活動チェック
#####################################################
	def CheckUserAlive( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckUserAlive"
		
		wRes['Responce'] = {
			"Alive"		: False,
			"Retweet"	: False
		}
		#############################
		# ユーザツイートを取得
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=True, inFLG_Rts=True,
			 inID=inID, inCount=gVal.DEF_STR_TLNUM['UserAliveLine'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		###自分のツイートがない
		if len(wTweetRes['Responce'])==0 :
			wRes['Reason'] = "My Tweet is none"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 連続リツイートの状態
		wRetweet = 0
		wAlive = False
		for wTweet in wTweetRes['Responce'] :
			### リツイートは除外
			if "retweeted_status" in wTweet :
				wRetweet += 1
			else:
			### 通常ツイート、引用リツイート、もしくはリプライ
				if wAlive==False :
					# 先頭一回だけ実施
					wAlive = True
					
					###日時の変換
					wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
					if wTime['Result']!=True :
						wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweet['created_at'])
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
					wTweet['created_at'] = wTime['TimeDate']
					
					### 範囲時間内のツイートか
					wGetLag = CLS_OSIF.sTimeLag( str(wTweet['created_at']), inThreshold=gVal.DEF_STR_TLNUM['UserAliveSec'] )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
					if wGetLag['Beyond']==False :
						### 期間内
						wRes['Responce']['Alive'] = True
		
		wRetweetRange = gVal.DEF_STR_TLNUM['UserAliveLine'] * gVal.DEF_STR_TLNUM['UserAliveRetweetRange']
		if wRetweetRange<=wRetweet :
			# リツイート割合が許容超え
			wRes['Responce']['Retweet'] = True
		
		wRes['Result'] = True
		return wRes




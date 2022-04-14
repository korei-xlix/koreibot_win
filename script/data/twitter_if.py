#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter I/F
#####################################################
from twitter_use import CLS_Twitter_Use

from osif import CLS_OSIF
from gval import gVal
#####################################################
###class CLS_Config() :
class CLS_Twitter_IF() :
#####################################################
	OBJ_Twitter = ""		#Twitterオブジェクト
	
							#Twitter情報
	ARR_MyFollowID = []		#  フォロー者ID	
	ARR_FollowerID = []		#  フォロワーID
	
	CHR_GetFollowDate = None
	ARR_FollowData = []		#退避用

	DEF_VAL_SLEEP = 10			#Twitter処理遅延（秒）

	ARR_Lists = {}			#リスト一覧
###	ARR_ListIndUserID = []	#リスト通知のユーザID(screen_name
	ARR_ListIndUser = {}	#リスト通知のユーザ

#####################################################
# Init
#####################################################
	def __init__(self):
		return



#####################################################
# フォロー取得
#####################################################
	def GetFollow(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetFollow"
		
		wRes['Responce'] = {
			"Update"	: False,
			"Data"		: []
		}
		#############################
		# 取得可能時間か？
		if self.CHR_GetFollowDate!=None :
			### 範囲時間内のツイートか
			wGetLag = CLS_OSIF.sTimeLag( str( self.CHR_GetFollowDate ), inThreshold=gVal.DEF_STR_TLNUM['forGetUserSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				### 規定以内は除外
				wRes['Responce']['Date'] = self.ARR_FollowData	#退避した古いデータを返す
				wRes['Result'] = True
				return wRes
		
		self.CHR_GetFollowDate = None	#一度クリアしておく(異常時再取得するため)
		#############################
		# フォロー一覧 取得
		wMyFollowRes = self.OBJ_Twitter.GetMyFollowList()
		gVal.STR_TrafficInfo['runapi'] += wMyFollowRes['RunAPI']
		if wMyFollowRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetMyFollowList): " + wMyFollowRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# フォロワー一覧 取得
		wFollowerRes = self.OBJ_Twitter.GetFollowerList()
		gVal.STR_TrafficInfo['runapi'] += wFollowerRes['RunAPI']
		if wFollowerRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetFollowerList): " + wFollowerRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		self.ARR_MyFollowID = []	#  フォロー者ID	
		self.ARR_FollowerID = []	#  フォロワーID
		wARR_FollowData = {}
		#############################
		# フォローデータの加工
		wARR_MyFollowData = {}
		for wROW in wMyFollowRes['Responce'] :
			
			wID = str( wROW['id'] )
			wName = str(wROW['name']).replace( "'", "''" )
			###情報の詰め込み
			wCell = {
				"id"			: wID,
				"name"			: wName,
				"screen_name"	: str( wROW['screen_name'] ),
				"statuses_count"	: wROW['statuses_count'],
				"myfollow"		: True,
				"follower"		: False
			}
			wARR_FollowData.update({ wID : wCell })
			self.ARR_MyFollowID.append( wID )
		
		#############################
		# フォロワーデータの加工
		for wROW in wFollowerRes['Responce'] :
			
			wID = str( wROW['id'] )
			wName = str(wROW['name']).replace( "'", "''" )
			###情報の詰め込み
			if wID in self.ARR_MyFollowID :
				###相互
				wARR_FollowData[wID]['follower'] = True
			else :
				###片フォロワー
				wCell = {
					"id"			: wID,
					"name"			: wName,
					"screen_name"	: str( wROW['screen_name'] ),
					"statuses_count"	: wROW['statuses_count'],
					"myfollow"		: False,
					"follower"		: True
				}
				wARR_FollowData.update({ wID : wCell })
			
			self.ARR_FollowerID.append( wID )
		
		#############################
		# トラヒック計測：フォロワー監視情報
		gVal.STR_TrafficInfo['now_myfollow'] = len( self.ARR_MyFollowID )
		gVal.STR_TrafficInfo['now_follower'] = len( self.ARR_FollowerID )
		
		#############################
		# 正常
		
		###現時刻をメモる
		self.CHR_GetFollowDate = str(gVal.STR_SystemInfo['TimeDate'])
		self.ARR_FollowData    = wARR_FollowData
		
		wRes['Responce']['Update'] = True
		wRes['Responce']['Date']   = wARR_FollowData
		wRes['Result'] = True
		return wRes



#####################################################
# ふぁぼ取得
#####################################################
	def GetFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetFavo"
		
		#############################
		# フォロー一覧 取得
		wTwitterRes = self.OBJ_Twitter.GetFavolist()
		gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wARR_TwitterData = {}
		for wROW in wTwitterRes['Responce'] :
			###時間の変換
			wTime = CLS_OSIF.sGetTimeformat_Twitter( wROW['created_at'] )
			if wTime['Result']!=True :
				wRes['Reason'] = "sGetTimeformat_Twitter is Failed: " + str(wROW['created_at'])
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			###wTime['TimeDate']
			
			wID = str( wROW['id'] )
			wText = str(wROW['text']).replace( "'", "''" )
			###情報の詰め込み
			wCell = {
				"id"			: wID,
				"user_id"		: str( wROW['user']['id'] ),
				"text"			: wText,
				"created_at"	: wTime['TimeDate']
			}
			wARR_TwitterData.update({ wID : wCell })
		
		#############################
		# トラヒック計測：いいね情報
		gVal.STR_TrafficInfo['now_favo'] = len( wARR_TwitterData )
		
		#############################
		# 正常
		wRes['Responce'] = wARR_TwitterData
		wRes['Result'] = True
		return wRes



#####################################################
# Twitter接続設定
#####################################################
	def SetTwitter( self, inTwitterAccount ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "SetTwitter"
		
		#############################
		# Twitterオブジェクトの作成
		self.OBJ_Twitter = CLS_Twitter_Use()
		
		wRes['Responce'] = {}
		wRes['Responce'].update({
			"Account"   : inTwitterAccount,
			"APIkey"    : "(none)",
			"APIsecret" : "(none)",
			"ACCtoken"  : "(none)",
			"ACCsecret" : "(none)",
			"Bearer"    : "(none)"
		})
		
		#############################
		# Twitterキーの入力
		CLS_OSIF.sPrn( "Twitter APIキーの設定をおこないます。" )
		CLS_OSIF.sPrn( "---------------------------------------" )
		while True :
			###初期化
			wRes['Responce']['APIkey']    = "(none)"
			wRes['Responce']['APIsecret'] = "(none)"
			wRes['Responce']['ACCtoken']  = "(none)"
			wRes['Responce']['ACCsecret'] = "(none)"
			wRes['Responce']['Bearer']    = "(none)"
			
			#############################
			# 実行の確認
			wSelect = CLS_OSIF.sInp( "キャンセルしますか？(y)=> " )
			if wSelect=="y" :
				# 完了
				wRes['Result'] = True
				return wRes
			
			#############################
			# 入力
			wStr = "Twitter Devで取得した API key を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sGpp( "API key？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "キーが未入力です" + '\n' )
				continue
			wRes['Responce']['APIkey'] = wKey
			
			wStr = "Twitter Devで取得した API secret key を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sGpp( "API secret key？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "キーが未入力です" + '\n' )
				continue
			wRes['Responce']['APIsecret'] = wKey
			
			wStr = "Twitter Devで取得した Access token を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sGpp( "Access token？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "キーが未入力です" + '\n' )
				continue
			wRes['Responce']['ACCtoken'] = wKey
			
			wStr = "Twitter Devで取得した Access token secret を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sGpp( "Access token secret？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "キーが未入力です" + '\n' )
				continue
			wRes['Responce']['ACCsecret'] = wKey
			
			wStr = "Twitter Devで取得した Bearer token secret を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sGpp( "Bearer token secret？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "キーが未入力です" + '\n' )
				continue
			wRes['Responce']['Bearer'] = wKey
			
			###ここまでで入力は完了した
			break
		
		#############################
		# Twitter接続テスト
		wResTwitter_Create = self.OBJ_Twitter.Create(
					wRes['Responce']['Account'],
					wRes['Responce']['APIkey'],
					wRes['Responce']['APIsecret'],
					wRes['Responce']['ACCtoken'],
					wRes['Responce']['ACCsecret'],
					wRes['Responce']['Bearer']
				)
		wResTwitter = self.OBJ_Twitter.GetTwStatus()
		if wResTwitter_Create!=True :
			wRes['Reason'] = "Twitterの接続に失敗しました: reason=" + wResTwitter['Reason']
			return wRes
		
		###結果の確認
		if wResTwitter['Init']!=True :
			wRes['Reason'] = "Twitterが初期化できてません"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wStr = "Twitterへ正常に接続しました。" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# Twitter接続
#####################################################
	def Connect( self, inAPIkey, inAPIsecret, inACCtoken, inACCsecret, inBearer ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Connect"
		
		#############################
		# Twitter生成→接続
		self.OBJ_Twitter = CLS_Twitter_Use()
		wResTwitter_Create = self.OBJ_Twitter.Create( gVal.STR_UserInfo['Account'], inAPIkey, inAPIsecret, inACCtoken, inACCsecret, inBearer )
		
		#############################
		# Twitter状態の取得
		wResTwitter = self.OBJ_Twitter.GetTwStatus()
		if wResTwitter_Create!=True :
			wRes['Reason'] = "Twitterの接続失敗: reason=" + wResTwitter['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			
			self.__connectFailView()
			return False
		
		###結果の確認
		if wResTwitter['Init']!=True :
			wRes['Reason'] = "Twitter初期化失敗"
			gVal.OBJ_L.Log( "B", wRes )
			
			self.__connectFailView()
			return False
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	def __connectFailView(self):
		if gVal.FLG_Test_Mode==False :
			return	#テストモードでなければ終わる
		
		#############################
		# DB接続情報を表示
		wStr =        "******************************" + '\n'
		wStr = wStr + "API Key    : " + inAPIkey + '\n'
		wStr = wStr + "API Secret : " + inAPIsecret + '\n'
		wStr = wStr + "ACC Token  : " + inACCtoken + '\n'
		wStr = wStr + "ACC Secret : " + inACCsecret + '\n'
		wStr = wStr + "Bearer     : " + inBearer + '\n'
		wStr = wStr + "******************************" + '\n'
		CLS_OSIF.sPrn( wStr )
		return



#####################################################
# Twitter再接続
#####################################################
	def ReConnect(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "ReConnect"
		
		#############################
		# APIカウントリセット
		self.OBJ_Twitter.ResetAPI()
		
		#############################
		# Twitter再接続
		wTwitterRes = self.OBJ_Twitter.Connect()
		
		#############################
		# Twitter状態の取得
		if wTwitterRes!=True :
			wTwitterStatus = self.OBJ_Twitter.GetTwStatus()
			wRes['Reason'] = "Twitterの再接続失敗: reason=" + wTwitterStatus['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ログ
		gVal.OBJ_L.Log( "R", wRes, "Twitter規制解除＆再接続" )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# タイムライン読み込み処理
#####################################################
	def GetTL( self, inTLmode="home", inFLG_Rep=True, inFLG_Rts=False, inCount=CLS_Twitter_Use.VAL_TwitNum, inID=None, inListID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetTL"
		
		#############################
		# ユーザツイートを取得
		wTweetRes = self.OBJ_Twitter.GetTL( inTLmode=inTLmode, inFLG_Rep=inFLG_Rep, inFLG_Rts=inFLG_Rts, inCount=inCount, inID=inID, inListID=inListID )
		gVal.STR_TrafficInfo['runapi'] += wTweetRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：取得タイムライン数
		gVal.STR_TrafficInfo['timeline'] += len( wTweetRes['Responce'] )
		
		#############################
		# 完了
		wRes['Responce'] = wTweetRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# タイムライン検索
#####################################################
	def GetSearch( self, inQuery, inMaxResult=40 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetSearch"
		
		#############################
		# 検索を利用する
		wTweetRes = self.OBJ_Twitter.GetTweetSearch_v2( inQuery=inQuery, inMaxResult=inMaxResult )
		gVal.STR_TrafficInfo['runapi'] += wTweetRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason'] + " query=" + str(inQuery)
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：取得タイムライン数
		gVal.STR_TrafficInfo['timeline'] += len( wTweetRes['Responce'] )
		
		#############################
		# 完了
		wRes['Responce'] = wTweetRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet Tweet Lookup取得
#####################################################
	def GetTweetLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetTweetLookup"
		
		#############################
		# ユーザツイートを取得
		wTweetRes = self.OBJ_Twitter.GetTweetLookup( inID=inID )
		gVal.STR_TrafficInfo['runapi'] += wTweetRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：取得タイムライン数
		gVal.STR_TrafficInfo['timeline'] += len( wTweetRes['Responce'] )
		
		#############################
		# 完了
		wRes['Responce'] = wTweetRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet Mention Lookup取得
# 自分に対するメンション情報を取得する
#####################################################
	def GetMyMentionLookup(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetMyMentionLookup"
		
		#############################
		# 自分へのメンション情報を取得
		wTweetRes = self.OBJ_Twitter.GetMentionLookup( inID=gVal.STR_UserInfo['id'] )
		gVal.STR_TrafficInfo['runapi'] += wTweetRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# データ加工
		#   メンション情報がない場合はセットなし
		wMentions = {}
		if wTweetRes['Responce']['meta']['result_count']>0 and \
		   "data" in wTweetRes['Responce'] :
			
			for wTweet in wTweetRes['Responce']['data'] :
				wReplyID     = str( wTweet['id'] )
				wReplyUserID = str( wTweet['author_id'] )
				wReplyText   = str( wTweet['text'] )
				wTimeDate   = str( wTweet['created_at'] )
				
				if "referenced_tweets" not in wTweet :
					continue
				wTweetID = str( wTweet['referenced_tweets'][0]['id'] )
				
				wSTR_Cell = {}
				wSTR_Cell.update({ "id" : wReplyUserID })	#ユーザID
				wSTR_Cell.update({ "created_at"    : wTimeDate })
				wSTR_Cell.update({ "reply_id"    : wReplyID })
				wSTR_Cell.update({ "reply_text"  : wReplyText })
				wSTR_Cell.update({ "tweet_id"    : wTweetID })
				wMentions.update({ wReplyID : wSTR_Cell })
		
		#############################
		# トラヒック計測：取得タイムライン数
		gVal.STR_TrafficInfo['timeline'] += len( wMentions )
		
		#############################
		# 完了
		wRes['Responce'] = wMentions
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet Likes Lookup取得
#   いいねした人のユーザ情報を取得する
#####################################################
	def GetLikesLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetLikesLookup"
		
		#############################
		# ユーザツイートを取得
		wTweetRes = self.OBJ_Twitter.GetLikesLookup( inID=inID )
		gVal.STR_TrafficInfo['runapi'] += wTweetRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# データ加工
		#   いいねがない場合はセットなし
		wUsers = {}
		if wTweetRes['Responce']['meta']['result_count']>0 and \
		   "data" in wTweetRes['Responce'] :
			for wUser in wTweetRes['Responce']['data'] :
				wID = str(wUser['id'])
				wName = wUser['name'].replace( "'", "''" )
				
				wSTR_Cell = {}
				wSTR_Cell.update({ "id"          : wID })
				wSTR_Cell.update({ "name"        : wName })
				wSTR_Cell.update({ "screen_name" : wUser['username'] })
				wUsers.update({ wID : wSTR_Cell })
		
		#############################
		# 完了
		wRes['Responce'] = wUsers
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet retweeted by 取得
#   リツイートした人のユーザ情報を取得する
#####################################################
	def GetRetweetLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetRetweetLookup"
		
		#############################
		# ユーザツイートを取得
		wTweetRes = self.OBJ_Twitter.GetRetweetLookup( inID=inID )
		gVal.STR_TrafficInfo['runapi'] += wTweetRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# データ加工
		#   いいねがない場合はセットなし
		wUsers = {}
		if wTweetRes['Responce']['meta']['result_count']>0 and \
		   "data" in wTweetRes['Responce'] :
			for wUser in wTweetRes['Responce']['data'] :
				wID = str(wUser['id'])
				wName = wUser['name'].replace( "'", "''" )
				
				wSTR_Cell = {}
				wSTR_Cell.update({ "id"          : wID })
				wSTR_Cell.update({ "name"        : wName })
				wSTR_Cell.update({ "screen_name" : wUser['username'] })
				wUsers.update({ wID : wSTR_Cell })
		
		#############################
		# 完了
		wRes['Responce'] = wUsers
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet reference retweeted 取得
#   引用リツイートした人のユーザ情報を取得する
#####################################################
	def GetRefRetweetLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetRefRetweetLookup"
		
		#############################
		# 検索を利用する
		wQuery = "{id} -is:retweet"
		wQuery = wQuery.format( id=inID )
		wTweetRes = self.OBJ_Twitter.GetTweetSearch_v2( inQuery=wQuery )
		gVal.STR_TrafficInfo['runapi'] += wTweetRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# データ加工
		#   いいねがない場合はセットなし
		wUsers = {}
		if wTweetRes['Responce']['meta']['result_count']>0 and \
		   "includes" in wTweetRes['Responce'] and \
		   "data" in wTweetRes['Responce'] :
			
			### Tweetデータから対象引用リツイートを抽出
			for wTweet in wTweetRes['Responce']['data'] :
				if "referenced_tweets" not in wTweet :
					continue
				for wTweetCont in wTweet['referenced_tweets'] :
					wSTR_Cell = {}
					if "id" not in wTweetCont :
						continue
					wID = str(wTweetCont['id'])
					if wID!=inID :
						continue
					
					wUserID = str( wTweet['author_id'] )
					wSTR_Cell.update({ "id"     : wUserID })					#引用したユーザID
					wSTR_Cell.update({ "name"        : None })
					wSTR_Cell.update({ "screen_name" : None })
					wSTR_Cell.update({ "tweet_id"    : str( wTweet['id'] ) })	#引用リツイートID
					wSTR_Cell.update({ "text"        : wTweet['text'] })
					wSTR_Cell.update({ "set_data"    : True })
					break
				if "set_data" in wSTR_Cell :
					wUsers.update({ wUserID : wSTR_Cell })
			
			### Tweetデータから関連ユーザ情報を抜き出す
			for wUser in wTweetRes['Responce']['includes']['users'] :
				wUserID = str( wUser['id'] )
				if wUserID not in wUsers :
					continue
				wUsers[wUserID]['name'] = wUser['name'].replace( "'", "''" )
				wUsers[wUserID]['screen_name'] = wUser['username']
		
		#############################
		# 完了
		wRes['Responce'] = wUsers
		wRes['Result'] = True
		return wRes



#####################################################
# ついーと処理
#####################################################
	def Tweet( self, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Tweet"
		
		#############################
		# ツイート
		wTweetRes = self.OBJ_Twitter.Tweet( inTweet )
		gVal.STR_TrafficInfo['runapi'] += wTweetRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：ツイート送信数
		gVal.STR_TrafficInfo['send_tweet'] += 1
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ついーと削除処理
#####################################################
	def DelTweet( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "DelTweet"
		
		#############################
		# ツイート
		wTweetRes = self.OBJ_Twitter.DelTweet( inID )
		gVal.STR_TrafficInfo['runapi'] += wTweetRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# DM処理
#####################################################
	def SendDM( self, inID, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Tweet"
		
		#############################
		# DM送信
		wTwitterRes = self.OBJ_Twitter.SendDM( inID, inTweet )
		gVal.STR_TrafficInfo['runapi'] += wTweetRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：ツイート送信数
		gVal.STR_TrafficInfo['send_tweet'] += 1
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# フォロー
#####################################################
	def Follow( self, inID, inMute=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Follow"

		#############################
		# フォローする
		wTwitterRes = self.OBJ_Twitter.CreateFollow( inID )
		gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(CreateFollow): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# フォローに追加
		if self.CheckMyFollow( inID )==False :
			self.ARR_MyFollowID.append( inID )
			#############################
			# トラヒック情報：フォロー者獲得数
			gVal.STR_TrafficInfo['get_myfollow'] += 1
		
		#############################
		# 完了
		wRes['Result'] = True
		
		#############################
		# ミュートする
		if inMute==True :
			wTwitterRes = self.OBJ_Twitter.CreateMute( inID )
			gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
			if wTwitterRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(CreateMute): " + wTwitterRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
		
		return wRes

	#####################################################
	def CheckMyFollow( self, inID ):
		if str( inID ) not in self.ARR_MyFollowID :
			return False
		return True

	#####################################################
	def CheckFollower( self, inID ):
		if str( inID ) not in self.ARR_FollowerID :
			return False
		return True



#####################################################
# リムーブ
#####################################################
	def Remove( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Remove"

		#############################
		# リムーブする
		wTwitterRes = self.OBJ_Twitter.RemoveFollow( inID )
		gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
		
		wRes['StatusCode'] = wTwitterRes['StatusCode']
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(RemoveFollow): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# フォローから削除
		if self.CheckMyFollow( inID )==True :
			self.ARR_MyFollowID.remove( inID )
			#############################
			# トラヒック情報：リムーブフォロー者数
			gVal.STR_TrafficInfo['rem_myfollow'] += 1
			gVal.STR_TrafficInfo['run_autoremove'] += 1
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ブロックリムーブ
#####################################################
	def BlockRemove( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "BlockRemove"
		
		#############################
		# ブロックする
		wTwitterRes = self.OBJ_Twitter.CreateBlock( inID )
		gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(CreateBlock): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# ブロック解除する
		wTwitterRes = self.OBJ_Twitter.RemoveBlock( inID )
		gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(RemoveBlock): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# フォロー、フォロワーから削除
		if self.CheckMyFollow( inID )==True :
			self.ARR_MyFollowID.remove( inID )
			#############################
			# トラヒック情報：リムーブフォロー者数
			gVal.STR_TrafficInfo['rem_myfollow'] += 1
			gVal.STR_TrafficInfo['run_autoremove'] += 1
		
		if self.CheckFollower( inID )==True :
			self.ARR_FollowerID.remove( inID )
			#############################
			# トラヒック情報：リムーブフォロワー数
			gVal.STR_TrafficInfo['rem_follower'] += 1
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 当該ユーザのいいね一覧 取得
#####################################################
	def GetUserFavolist( self, inID, inCount=2 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetUserFavolist"
		
		#############################
		# いいね一覧を取得
		wTwitterRes = self.OBJ_Twitter.GetUserFavolist( inID, inCount )
		gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wTwitterRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# いいね
#####################################################
	def Favo( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Favo"
		
		#############################
		# いいねする
		wTwitterRes = self.OBJ_Twitter.CreateFavo( inID )
		gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：いいね実施数
		gVal.STR_TrafficInfo['get_favo'] += 1
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# いいね解除
#####################################################
	def FavoRemove( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "FavoRemove"
		
		#############################
		# いいね解除する
		wTwitterRes = self.OBJ_Twitter.RemoveFavo( inID )
		gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：いいね解除数
		gVal.STR_TrafficInfo['rem_favo'] += 1
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# リツイート
#####################################################
	def Retweet( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Retweet"
		
		#############################
		# リツイートする
		wTwitterRes = self.OBJ_Twitter.CreateRetweet( inID )
		gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：リツイート実施数
		gVal.STR_TrafficInfo['send_retweet'] += 1
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ミュート
#####################################################
	def Mute( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Mute"

		#############################
		# ミュートする
		wTwitterRes = self.OBJ_Twitter.CreateMute( inID )
		gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(CreateMute): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ミュート解除(できるだけ)
#####################################################
	def AllMuteRemove(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "AllMuteRemove"
		
		wRes['Responce'] = False
		#############################
		# ミュート一覧 取得
		wMuteRes = self.OBJ_Twitter.GetMuteIDs()
		gVal.STR_TrafficInfo['runapi'] += wMuteRes['RunAPI']
		if wMuteRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetMuteIDs): " + wMuteRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ミュート解除ID一覧の作成
		wARR_MuteRemoveID = []
		if len(wMuteRes['Responce'])>=1 :
			for wID in wMuteRes['Responce']:
				wID = str( wID )
				
				###フォロー者は対象外
				if self.CheckMyFollow( wID )==True :
					continue
				
				wARR_MuteRemoveID.append( wID )
		
		###対象者なし
		if len( wARR_MuteRemoveID )==0 :
			wRes['Result'] = True
			return wRes
		
		#############################
		# 解除実行
		else:
			#############################
			# ミュート解除していく
			wStr = "ミュート解除対象数: " + str(len( wARR_MuteRemoveID )) + '\n'
			wStr = wStr + "ミュート解除中......." + '\n'
			CLS_OSIF.sPrn( wStr )
			
			for wID in wARR_MuteRemoveID :
				###  ミュート解除する
				wRemoveRes = self.OBJ_Twitter.RemoveMute( wID )
				if wRemoveRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error(RemoveMute): " + wRemoveRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				### Twitter Wait
				CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
				
				###  ミュート一覧にないID=ミュート解除してない 場合は待機スキップ
				if wRemoveRes['Responce']==False :
					continue
		
		#############################
		# トラヒック計測：ミュート解除数
		gVal.STR_TrafficInfo['run_muteremove'] += len( wTweetRes['Responce'] )
		
		#############################
		# 完了
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes



#####################################################
# 自ユーザ情報 取得
#####################################################
	def GetMyUserinfo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetMyUserinfo"
		
		#############################
		# Twitterから自ユーザ情報を取得する
		wUserinfoRes = self.OBJ_Twitter.GetMyUserinfo()
		gVal.STR_TrafficInfo['runapi'] += wUserinfoRes['RunAPI']
		
		#############################
		# 結果チェック
		if wUserinfoRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: " + wUserinfoRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wUserinfoRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ情報 取得
#####################################################
	def GetUserinfo( self, inID=-1, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetUserinfo"
		
		#############################
		# Twitterからユーザ情報を取得する
		wUserinfoRes = self.OBJ_Twitter.GetUserinfo( inID=inID, inScreenName=inScreenName )
		gVal.STR_TrafficInfo['runapi'] += wUserinfoRes['RunAPI']
		
		wRes['StatusCode'] = wUserinfoRes['StatusCode']
		#############################
		# 結果チェック
		if wUserinfoRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: " + wUserinfoRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wUserinfoRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# フォロー者ID一覧 取得
#####################################################
	def GetFollowIDList( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetFollowIDList"

		#############################
		# フォロー者ID一覧 取得
		wTwitterRes = self.OBJ_Twitter.GetFollowIDList( inID )
		gVal.STR_TrafficInfo['runapi'] += wTweetRes['RunAPI']
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wTwitterRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# 関係チェック
#####################################################
	def GetFollowInfo( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetFollowInfo"
		
		#############################
		# Twitterから関係情報を取得
		wUserinfoRes = self.OBJ_Twitter.GetFollowInfo( gVal.STR_UserInfo['id'], inID )
		gVal.STR_TrafficInfo['runapi'] += wUserinfoRes['RunAPI']
		
		#############################
		# 結果チェック
		if wUserinfoRes['Result']!=True :
			wRes['Reason'] = "GetFollowInfo API Error: " + wUserinfoRes['Reason']
			wRes['Responce'] = wUserinfoRes['StatusCode']
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wUserinfoRes['Responce']['relationship']['source']
		wRes['Result'] = True
		return wRes



#####################################################
# トレンド取得
#####################################################
	def GetTrends(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetTrends"
		
		#############################
		# Twitterからトレンドを取得
		wSubRes = self.OBJ_Twitter.GetTrends()
		gVal.STR_TrafficInfo['runapi'] += wSubRes['RunAPI']
		
		wRes['Responce'] = {
			"trends"		: [],
			"as_of"			: None,		#リストが作られた日時
			"created_at"	: None		#最も古いトレンド日時
		}
		#############################
		# Twitter処理結果
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetTrends API Error: " + wSubRes['Reason']
			return wRes
		if len(wSubRes['Responce'])<=0 :
			wRes['Reason'] = "Trend Data error: not 0"
			return wRes
		if "trends" not in wSubRes['Responce'][0] :
			wRes['Reason'] = "Trend Data error: not trends"
			return wRes
		wTrendRes = wSubRes['Responce'][0]['trends']
		
		#############################
		# トレンド情報の詰め込み
		wARR_Trends = {}
		wIndex = 0
		for wROW in wTrendRes :
			wCell = {
				"name"				: str( wROW['name'] ),
				"promoted_content"	: wROW['promoted_content'],
				"tweet_volume"		: wROW['tweet_volume'],
				"hit"				: 0
			}
			wARR_Trends.update({ wIndex : wCell })
			wIndex += 1
		
		if len(wARR_Trends)==0 :
			wRes['Reason'] = "Trend Data error: set trend=0"
			return wRes
		
		#############################
		# データの設定
		wTime = CLS_OSIF.sGetTimeformat_Twitter( wSubRes['Responce'][0]['as_of'] )
		if wTime['Result']!=True :
			wRes['Reason'] = "sGetTimeformat_Twitter is Failed(1): " + str(wSubRes['Responce'][0]['as_of'])
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wRes['Responce']['as_of'] = wTime['TimeDate']
		
		wTime = CLS_OSIF.sGetTimeformat_Twitter( wSubRes['Responce'][0]['created_at'] )
		if wTime['Result']!=True :
			wRes['Reason'] = "sGetTimeformat_Twitter is Failed(2): " + str(wSubRes['Responce'][0]['created_at'])
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wRes['Responce']['created_at'] = wTime['TimeDate']
		
		wRes['Responce']['trends'] = wARR_Trends
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# リスト通知
#####################################################

#####################################################
# リスト通知 取得
#####################################################
	def GetListInd( self, inUpdate=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetListInd"
		
		wRes['Responce'] = False
###		#############################
###		# リスト通知が未設定の場合は
###		#   処理を抜ける
###		if gVal.STR_UserInfo['ListName']=="" :
###			wStr = "リスト通知は未設定です" + '\n' ;
###			CLS_OSIF.sPrn( wStr )
###			
###			wRes['Result'] = True
###			return wRes
###		
		#############################
		# リスト一覧が空なら
		#   Twitterリスト一覧を取得する
		if len(self.ARR_Lists)==0 or inUpdate==True :
			### Twitterリスト一覧を取得
			self.ARR_Lists = {}
			
			wSubRes = self.OBJ_Twitter.GetLists()
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			self.ARR_Lists = wSubRes['Responce']
		
		#############################
		# リストがTwitterにあるか確認
		wSubRes = self.CheckListInd( gVal.STR_UserInfo['ListName'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
###			wStr = "Twitterに存在しないリストです: " + gVal.STR_UserInfo['ListName'] + '\n' ;
###			CLS_OSIF.sPrn( wStr )
###			
			gVal.STR_UserInfo['ListName'] = ""
			wRes['Result'] = True
			return wRes
		
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes

#####################################################
# リスト通知 ユーザ取得
#####################################################
	def GetListIndUser( self, inUpdate=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetListIndUser"
		
		#############################
		# リストがTwitterにあるか確認
		wSubRes = self.CheckListInd( gVal.STR_UserInfo['ListName'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
			wRes['Reason'] = "Twitter List not found: " + gVal.STR_UserInfo['ListName']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リスト通知のユーザIDが空なら
		#   ユーザ一覧を取得する
###		if len(self.ARR_ListIndUserID)==0 or inUpdate==True :
###			self.ARR_ListIndUserID = []
		if len(self.ARR_ListIndUser)==0 or inUpdate==True :
			self.ARR_ListIndUser = {}
			
			wSubRes = self.OBJ_Twitter.GetListMember( gVal.STR_UserInfo['ListName'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
###			wIndex = 0
			for wLine in wSubRes['Responce'] :
###				self.ARR_ListIndUserID.append( str( wLine['id'] ) )
###				self.ARR_ListIndUserID.append( str( wLine['screen_name'] ) )
				wCell = {
					"id"          : str( wLine['id'] ),
					"screen_name" : wLine['screen_name']
				}
				self.ARR_ListIndUser.update({ str(wLine['id']) : wCell })
###				wIndex += 1
			
###			wStr = "リスト通知ユーザIDを取得しました: " + str( len(self.ARR_ListIndUserID) ) + ".件" + '\n' ;
			wStr = "リスト通知ユーザIDを取得しました: " + str( len(self.ARR_ListIndUser) ) + ".件" + '\n' ;
			CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes

#####################################################
# リスト通知 チェック
#####################################################
	def CheckListInd( self, inListName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "CheckListInd"
		
		wFLG_Detect = False
		#############################
		# リストがTwitterにあるか確認
		wKeylist = list( self.ARR_Lists )
		for wIndex in wKeylist :
###			if self.ARR_Lists[wIndex]['name']==gVal.STR_UserInfo['ListName'] :
			if self.ARR_Lists[wIndex]['name']==inListName :
				wFLG_Detect = True
				break
		
		wRes['Responce'] = wFLG_Detect
		wRes['Result'] = True
		return wRes

#####################################################
# リスト通知 ユーザチェック
#####################################################
	def CheckListIndUser( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "CheckListIndUser"
		
		wFLG_Detect = False
		#############################
		# リスト通知ユーザがTwitterにあるか確認
		if inID in self.ARR_ListIndUser :
			wFLG_Detect = True
		
		wRes['Responce'] = wFLG_Detect
		wRes['Result'] = True
		return wRes

#####################################################
# リスト通知 追加
#####################################################
###	def InserttListIndUser( self, inID ):
	def InserttListIndUser( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "InserttListIndUser"
		
###		wID = str( inID )
		wID = str( inUser['id'] )
###		wScreenName = str( inUser['screen_name'] )
		
		wRes['Responce'] = False
		#############################
		# リストがTwitterにあるか確認
		wSubRes = self.CheckListInd( gVal.STR_UserInfo['ListName'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
			wRes['Reason'] = "Twitter List not found: " + gVal.STR_UserInfo['ListName']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リスト通知に存在するか？
###		if wID in self.ARR_ListIndUserID :
###			wRes['Reason'] = "ARR_ListIndUserID in exist User ID: " + wID
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		wKeylist = list( self.ARR_ListIndUser )
###		if wID in wKeylist :
###			wRes['Reason'] = "ARR_ListIndUser in exist User ID: " + inUser['screen_name']
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
		wSubRes = self.CheckListIndUser( inID=wID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
###			wStr = "●リスト通知登録済み: " + self.ARR_ListIndUser[wID]['screen_name'] + '\n' ;
###			CLS_OSIF.sPrn( wStr )
###			
			### リスト通知済み
			wRes['Result'] = True
			return wRes
		
		#############################
		# リスト通知にID追加
		wSubRes = self.OBJ_Twitter.AddUserList( gVal.STR_UserInfo['ListName'], wID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(AddUserList): " + wSubRes['Reason'] + " : List Name=" + gVal.STR_UserInfo['ListName'] + " id=" + wID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		### 追加
###		self.ARR_ListIndUserID.append( wID )
		wCell = {
			"id"          : wID,
			"screen_name" : inUser['screen_name']
		}
		self.ARR_ListIndUser.update({ wID : wCell })
		
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes

#####################################################
# リスト通知 クリア
#####################################################
	def AllClearListInd(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "ClearListInd"
		
		#############################
		# リスト通知 ユーザの更新
		wSubRes = self.GetListIndUser( inUpdate=True )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetListIndUser error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 全クリア
###		for wID in self.ARR_ListIndUserID :
		wKeylist = list( self.ARR_ListIndUser )
		for wID in wKeylist :
			wSubRes = self.OBJ_Twitter.RemoveUserList( gVal.STR_UserInfo['ListName'], wID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(RemoveUserList): " + wSubRes['Reason'] + " : List Name=" + gVal.STR_UserInfo['ListName'] + " user id=" + self.ARR_ListIndUser[wID]['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				continue
		
		wStr = "リスト通知を全クリアしました" + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
###		self.ARR_ListIndUserID = []
		self.ARR_ListIndUser = {}
		wRes['Result'] = True
		return wRes

#####################################################
# リスト通知 表示
#####################################################
	def ViewListIndUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "ViewListIndUser"
		
		#############################
		# リスト通知が未設定の場合は
		#   処理を抜ける
		if gVal.STR_UserInfo['ListName']=="" :
			wStr = "リスト通知は未設定です" + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# リスト一覧
		wStr = '\n' + "--------------------" + '\n' ;
		wStr = wStr + "Twitterリスト一覧" + '\n' + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
		wKeylist = list( self.ARR_Lists )
		wStr = ""
		for wIndex in wKeylist :
			wStr = wStr + str(self.ARR_Lists[wIndex]['id']) + " : "
			wStr = wStr + str(self.ARR_Lists[wIndex]['name']) + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# ユーザ一覧
		wStr = '\n' + "--------------------" + '\n' ;
		wStr = wStr + "リスト通知ユーザ一覧" + '\n' + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
		wStr = ""
###		for wID in self.ARR_ListIndUserID :
		wKeylist = list( self.ARR_ListIndUser )
		for wID in wKeylist :
###			wStr = wStr + wID + '\n'
			wStr = wStr + self.ARR_ListIndUser[wID]['screen_name'] + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



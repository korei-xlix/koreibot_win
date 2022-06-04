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
class CLS_Twitter_IF() :
#####################################################
	OBJ_Twitter = ""		#Twitterオブジェクト
	
							#Twitter情報
	ARR_MyFollowID = []		#  フォロー者ID	
	ARR_FollowerID = []		#  フォロワーID
	
	CHR_GetFollowDate = None
	ARR_FollowData = []		#退避用
	
	ARR_Favo       = {}		#  いいね一覧
###	ARR_FavoUserID = []		#  いいね一覧のユーザID
	ARR_FavoUser = {}		#  いいね一覧のユーザ
	
	DEF_VAL_SLEEP = 10				#Twitter処理遅延（秒）
	DEF_VAL_FAVO_1DAYSEC = 86400	#いいね1日経過時間  1日 (60x60x24)x1

	ARR_Lists = {}			#リスト一覧
	ARR_ListIndUser = {}	#リスト通知のユーザ
###	ARR_FavoUser = {}		#いいねユーザ
###	ARR_ListFavoUser = {}	#リストいいねユーザ

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
		
###		wRes['Responce'] = {
###			"Update"	: False,
###			"Data"		: []
###		}
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
###				wRes['Responce']['Date'] = self.ARR_FollowData	#退避した古いデータを返す
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
		
###		wRes['Responce']['Update'] = True
###		wRes['Responce']['Date']   = wARR_FollowData
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
		
###		self.ARR_FavoUserID = []
		self.ARR_FavoUser = {}
		#############################
		# フォロー一覧 取得
		wTwitterRes = self.OBJ_Twitter.GetFavolist()
		gVal.STR_TrafficInfo['runapi'] += wTwitterRes['RunAPI']
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		self.ARR_Favo = {}
		for wROW in wTwitterRes['Responce'] :
			wResSub =self.AddFavoUserID( wROW )
			if wResSub['Result']!=True :
				wRes['Reason'] = "AddFavoUserID failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# トラヒック計測：いいね情報
		gVal.STR_TrafficInfo['now_favo'] = len( self.ARR_Favo )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# 排他ユーザ追加
	#####################################################
	def AddFavoUserID( self, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "AddFavoUserID"
		
		wID = str( inTweet['id'] )
		wText = str(inTweet['text']).replace( "'", "''" )
		wUserID = str( inTweet['user']['id'] )
		#############################
		# 時間の変換
		wTime = CLS_OSIF.sGetTimeformat_Twitter( inTweet['created_at'] )
		if wTime['Result']!=True :
			wRes['Reason'] = "sGetTimeformat_Twitter is Failed: " + str(inTweet['created_at'])
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###wTime['TimeDate']
		
		#############################
		# 重複があるか
		if wID in self.ARR_Favo :
			wRes['Reason'] = "ID is exist : id=" + str( wID )
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# いいね情報の詰め込み
###		wID = str( inTweet['id'] )
###		wText = str(inTweet['text']).replace( "'", "''" )
###		wUserID = str( inTweet['user']['id'] )
		
		wCellUser = {
			"id"			: wUserID,
			"screen_name"	: inTweet['user']['screen_name']
		}
		
		wCell = {
			"id"			: wID,
			"text"			: wText,
			"created_at"	: str(wTime['TimeDate']),
			"user"			: wCellUser
		}
		self.ARR_Favo.update({ wID : wCell })
		
		#############################
		# ユーザの重複があるか
		
		#############################
		# 重複なし
		#   新規追加
		if wUserID not in self.ARR_FavoUser :
			wCellUser = {
				"id"			: wUserID,
				"screen_name"	: inTweet['user']['screen_name']
			}
			wCell = {
				"id"			: wID,
				"created_at"	: str(wTime['TimeDate']),
				"user"			: wCellUser
			}
			self.ARR_FavoUser.update({ wUserID : wCell })

		#############################
		# 重複あり
		else:
			#############################
			# 前の日付より新しければ新アクション
			wSubRes = CLS_OSIF.sCmpTime( str(wTime['TimeDate']), self.ARR_FavoUser[wUserID]['created_at'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "sCmpTime is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Future']==True :
				### 最新
				self.ARR_FavoUser[wUserID]['id']         = wID
				self.ARR_FavoUser[wUserID]['created_at'] = str(wTime['TimeDate'])
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいねデータ取得
	#####################################################
	def GetFavoData(self):
		return self.ARR_Favo



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
		# データ加工
		#   いいねがない場合はセットなし
		wARR_Tweets = {}
		if wTweetRes['Responce']['meta']['result_count']>0 and \
		   "includes" in wTweetRes['Responce'] and \
		   "data" in wTweetRes['Responce'] :
			
			### Tweetデータから対象引用リツイートを抽出
			for wTweet in wTweetRes['Responce']['data'] :
				### 枠の作成
				wSTR_CellUser = {}
				wSTR_CellUser.update({ "id"				: None })
				wSTR_CellUser.update({ "name"			: None })
				wSTR_CellUser.update({ "screen_name"	: None })
				wSTR_Cell = {}
				wSTR_Cell.update({ "type"			: None })
				wSTR_Cell.update({ "reply_settings"	: None })
				wSTR_Cell.update({ "id"				: None })
				wSTR_Cell.update({ "text"			: None })
				wSTR_Cell.update({ "created_at"		: None })
				wSTR_Cell.update({ "referenced_id"	: None })
				wSTR_Cell.update({ "user"	: wSTR_CellUser })
				
				### リプライの抜き取り
				if "referenced_tweets" not in wTweet :
					### 通常ツイート
					wID = str( wTweet['id'] )
					wSTR_Cell['type'] = "normal"
					wSTR_Cell['reply_settings'] = str( wTweet['reply_settings'] )
					wSTR_Cell['id']             = wID
					wSTR_Cell['text']           = str( wTweet['text'] )
					wSTR_Cell['created_at']     = str( wTweet['created_at'] )
					wSTR_Cell['user']['id']     = str( wTweet['author_id'] )
					wSTR_Cell.update({ "set_data" : False })
					wARR_Tweets.update({ wID : wSTR_Cell })
				
				else :
					for wTweetCont in wTweet['referenced_tweets'] :
						if "id" not in wTweetCont :
							continue
						if wTweetCont['type']!="replied_to" and \
						   wTweetCont['type']!="quoted" and \
						   wTweetCont['type']!="retweeted" :
							continue
						
						### 値の抜き取り
						wID = str( wTweet['id'] )
						wSTR_Cell['type']           = str( wTweetCont['type'] )
						wSTR_Cell['referenced_id']  = str( wTweetCont['id'] )
						
						wSTR_Cell['reply_settings'] = str( wTweet['reply_settings'] )
						wSTR_Cell['id']             = wID
						wSTR_Cell['text']           = str( wTweet['text'] )
						wSTR_Cell['created_at']     = str( wTweet['created_at'] )
						wSTR_Cell['user']['id']     = str( wTweet['author_id'] )
						wSTR_Cell.update({ "set_data" : False })
						wARR_Tweets.update({ wID : wSTR_Cell })
			
			### Tweetデータから関連ユーザ情報を抜き出す
			wARR_Users = {}
			for wUser in wTweetRes['Responce']['includes']['users'] :
				wID = str( wUser['id'] )
				if wID in wARR_Users :
					continue
				wName = wUser['name'].replace( "'", "''" )
				
				wSTR_Cell = {}
				wSTR_Cell.update({ "id"				: wID })
				wSTR_Cell.update({ "name"			: wName })
				wSTR_Cell.update({ "screen_name"	: wUser['username'] })
				wARR_Users.update({ wID : wSTR_Cell })
			
			### ユーザ情報を反映する
			wKeylist  = list( wARR_Tweets.keys() )
			for wID in wKeylist :
				wUserID = wARR_Tweets[wID]['user']['id']
				if wUserID not in wARR_Users :
					### ユーザ情報がない
					continue
				
				###日時の変換
				wTime = CLS_OSIF.sGetTimeformat_Twitter( wARR_Tweets[wID]['created_at'] )
				if wTime['Result']!=True :
					continue
				wARR_Tweets[wID]['created_at'] = wTime['TimeDate']
				
				wARR_Tweets[wID]['user']['name']        = wARR_Users[wUserID]['name']
				wARR_Tweets[wID]['user']['screen_name'] = wARR_Users[wUserID]['screen_name']
				wARR_Tweets[wID]['set_data'] = True
		
		###返すデータを設定する
		wResTweet = []
		for wID in wKeylist :
			if wARR_Tweets[wID]['set_data']==True :
				wResTweet.append( wARR_Tweets[wID] )
		
		#############################
		# トラヒック計測：取得タイムライン数
		gVal.STR_TrafficInfo['timeline'] += len( wTweetRes['Responce'] )
		
		#############################
		# 完了
		wRes['Responce'] = wResTweet
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
		# データ加工
		wTweets = {}
		if "data" in wTweetRes['Responce'] :
			
			wSTR_Cell = {}
			wSTR_CellUser = {}
			wID     = str( wTweetRes['Responce']['data']['id'] )
			wUserID = str( wTweetRes['Responce']['data']['author_id'] )
			
			### screen_nameの取り出し
			wScreenName = ""
			for wUsers in wTweetRes['Responce']['includes']['users'] :
				if str(wUsers['id'])==wUserID :
					wScreenName = wUsers['username']
			
			###日時の変換
			wTimeDate = wTweetRes['Responce']['data']['created_at']
			wTimeRes = CLS_OSIF.sGetTimeformat_Twitter( wTimeDate )
			if wTimeRes['Result']!=True :
				wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str( wTimeDate )
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			wTimeDate = str( wTimeRes['TimeDate'] )
		 	
			wSTR_CellUser.update({ "id" 			: wUserID })
			wSTR_CellUser.update({ "screen_name"	: wScreenName })
			
			wSTR_Cell.update({ "created_at"		: wTimeDate })
			wSTR_Cell.update({ "id"				: wID })
			wSTR_Cell.update({ "text"			: wTweetRes['Responce']['data']['text'] })
			wSTR_Cell.update({ "user"			: wSTR_CellUser })
			
			wSTR_Cell.update({ "data" : wTweetRes['Responce'] })
			wTweets = wSTR_Cell
		
		#############################
		# トラヒック計測：取得タイムライン数
		gVal.STR_TrafficInfo['timeline'] += len( wTweetRes['Responce'] )
		
		#############################
		# 完了
		wRes['Responce'] = wTweets
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
	def GetFollowerID(self):
		wSTR_Follower = {
			"MyFollowID" : self.ARR_MyFollowID,
			"FollowerID" : self.ARR_FollowerID
		}
		return wSTR_Follower

	#####################################################
	def GetFollowerData(self):
		return self.ARR_FollowData



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
		
		wRes['Responce'] = {
			"Run"	: False,
			"Data"	: None
		}
		#############################
		# いいね済みなら抜ける
		wID = str( inID )
		if wID in self.ARR_Favo :
			### いいね済み
			wRes['Result'] = True
			return wRes
		
		#############################
		# ツイートの情報を取得する
		wTweetInfoRes = self.GetTweetLookup( inID )
		if wTweetInfoRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetInfoRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		

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
		# いいね情報を登録する
		wResSub =self.AddFavoUserID( wTweetInfoRes['Responce'] )
		if wResSub['Result']!=True :
			wRes['Reason'] = "sTimeLag failed(1)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wRes['Responce']['Data'] = self.ARR_Favo[wID]
		
		#############################
		# トラヒック計測：いいね実施数
		gVal.STR_TrafficInfo['get_favo'] += 1
		
		#############################
		# 完了
		wRes['Responce']['Run']  = True
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
		
		wRes['Responce'] = {
			"Run"	: False,
			"Data"	: None
		}
		#############################
		# いいねがないなら抜ける
		wID = str( inID )
		if wID not in self.ARR_Favo :
			### いいね済み
			wRes['Result'] = True
			return wRes
		
		wRes['Responce']['Data'] = self.ARR_Favo[wID]
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
		# いいね情報を削除する
		self.ARR_Favo.pop( wID )
		
		#############################
		# トラヒック計測：いいね解除数
		gVal.STR_TrafficInfo['rem_favo'] += 1
		
		#############################
		# 完了
		wRes['Responce']['Run']  = True
		wRes['Result'] = True
		return wRes



#####################################################
# いいねユーザチェック
#####################################################
	def CheckFavoUser( self, inUserID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "CheckFavoUser"
		
###		wRes['Responce'] = False
		wRes['Responce'] = True
		### False = 重複いいねなし判定（現いいね有効）
		### True  = 重複いいねあり判定（現いいね無効）
###		#############################
###		# いいね済みユーザか
###		wID = str( inUserID )
###		if wID in self.ARR_FavoUserID :
###			wRes['Responce'] = True
###		
		#############################
		# ユーザがない場合
		if inUserID not in self.ARR_FavoUser :
			wRes['Responce'] = False	# 重複いいねなし
			wRes['Result'] = True
			return wRes
		
		#############################
		# 1日超経過してるか？
		wGetLag = CLS_OSIF.sTimeLag( self.ARR_FavoUser[inUserID]['created_at'] , inThreshold=self.DEF_VAL_FAVO_1DAYSEC )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed(1)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==True :
			###期間外= 1日超経過
			wRes['Responce'] = False	# 重複いいねなし
		
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
# リスト取得
#####################################################
	def GetList( self, inListName=None, inUpdate=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetList"
		
		wRes['Responce'] = False
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
		# リスト名が設定されてなければ抜ける
		# ※リストを取るだけ
		if inListName==None :
			wRes['Result'] = True
			return wRes
		
		#############################
		# リストがTwitterにあるか確認
		wSubRes = self.CheckList( inListName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==True :
			wRes['Responce'] = True
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# リストチェック
	#####################################################
	def CheckList( self, inListName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "CheckList"
		
		wFLG_Detect = False
		#############################
		# リストがTwitterにあるか確認
		wKeylist = list( self.ARR_Lists.keys() )
		for wIndex in wKeylist :
			if self.ARR_Lists[wIndex]['name']==inListName :
				wFLG_Detect = True
				break
		
		wRes['Responce'] = wFLG_Detect
		wRes['Result'] = True
		return wRes



#####################################################
# リストユーザ取得
#####################################################
	def GetListMember( self, inListName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetListMember"
		
		wRes['Responce'] = {}
		#############################
		# リストがTwitterにあるか確認
		wSubRes = self.CheckList( inListName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
			wRes['Reason'] = "Twitter List not found: " + inListName
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ユーザ一覧を取得する
		wARR_ListUser = {}
		
		wSubRes = self.OBJ_Twitter.GetListMember( inListName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		for wLine in wSubRes['Responce'] :
			wID = str( wLine['id'] )
			wCell = {
				"id"          : wID,
				"screen_name" : wLine['screen_name']
			}
			wARR_ListUser.update({ wID : wCell })
		
		wRes['Responce'] = wARR_ListUser
		wRes['Result'] = True
		return wRes



#####################################################
# リスト通知
#####################################################

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
		
		wRes['Responce'] = {
			"Num"		: 0,
			"Update"	: False
		}
		
		#############################
		# リストがTwitterにあるか確認
		wSubRes = self.CheckList( gVal.STR_UserInfo['ListName'] )
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
		if len(self.ARR_ListIndUser)==0 or inUpdate==True :
			self.ARR_ListIndUser = {}
			
			wSubRes = self.OBJ_Twitter.GetListMember( gVal.STR_UserInfo['ListName'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			for wLine in wSubRes['Responce'] :
				wCell = {
					"id"          : str( wLine['id'] ),
					"screen_name" : wLine['screen_name']
				}
				self.ARR_ListIndUser.update({ str(wLine['id']) : wCell })
			
			wRes['Responce']['Update'] = True
		
		wRes['Responce']['Num'] = len( self.ARR_ListIndUser )	#数を返す
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
	def InserttListIndUser( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "InserttListIndUser"
		
		wID = str( inUser['id'] )
		
		wRes['Responce'] = False	#通知済み
		#############################
		# リストがTwitterにあるか確認
		wSubRes = self.CheckList( gVal.STR_UserInfo['ListName'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
			wRes['Reason'] = "Twitter List not found: " + gVal.STR_UserInfo['ListName']
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# リスト通知に存在するか？
		wSubRes = self.CheckListIndUser( inID=wID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==True :
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
		wCell = {
			"id"          : wID,
			"screen_name" : inUser['screen_name']
		}
		self.ARR_ListIndUser.update({ wID : wCell })
		
		wRes['Responce'] = True		#新規通知
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
		wKeylist = list( self.ARR_ListIndUser.keys() )
		for wID in wKeylist :
			wSubRes = self.OBJ_Twitter.RemoveUserList( gVal.STR_UserInfo['ListName'], wID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(RemoveUserList): " + wSubRes['Reason'] + " : List Name=" + gVal.STR_UserInfo['ListName'] + " user id=" + self.ARR_ListIndUser[wID]['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				continue
		
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
		
		wKeylist = list( self.ARR_Lists.keys() )
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
		wKeylist = list( self.ARR_ListIndUser.keys() )
		for wID in wKeylist :
			wStr = wStr + self.ARR_ListIndUser[wID]['screen_name'] + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# リストいいね
#####################################################

#####################################################
# リストいいねデータ取得
#####################################################
###	def GetFavoUser(self):
###		return self.ARR_FavoUser
###		return self.ARR_ListFavoUser
###
###

#####################################################
# リストいいね ユーザ取得
#####################################################
###	def GetFavoUserData( self, inUpdate=False ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_Twitter_IF"
###		wRes['Func']  = "GetFavoUserData"
###		
###		wRes['Responce'] = {
###			"Num"		: 0,
###			"Update"	: False
###		}
###		
###		#############################
###		# リストがTwitterにあるか確認
###		wSubRes = self.CheckList( gVal.STR_UserInfo['LFavoName'] )
###		if wSubRes['Result']!=True :
###			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		if wSubRes['Responce']==False :
###			wRes['Reason'] = "Twitter List not found: " + gVal.STR_UserInfo['LFavoName']
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# リスト通知のユーザIDが空なら
###		# リストのクリア
###		if len(self.ARR_ListFavoUser)==0 or inUpdate==True :
###			self.ARR_ListFavoUser = {}
###		
###		#############################
###		# Twitterからリストのユーザ一覧を取得
###		wSubRes = self.OBJ_Twitter.GetListMember( gVal.STR_UserInfo['LFavoName'] )
###		if wSubRes['Result']!=True :
###			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		wKeylist = list( self.ARR_Favo.keys() )
###		wUpdate = False
###		#############################
###		# いいねユーザデータを作成する
###		for wLine in wSubRes['Responce'] :
###			wID = str( wLine['id'] )
###			
###			#############################
###			# 枠がなければ作成する
###			if wID not in self.ARR_ListFavoUser :
###				wCell = {
###					"id"				: wID,
###					"screen_name"		: wLine['screen_name'],
###					"flg_favo"			: False,
###					"lastTweetDate"		: None
###				}
###				self.ARR_ListFavoUser.update({ wID : wCell })
###				wUpdate = True
###			
###			#############################
###			# 既にいいね済みか
###			# いいね済みがあれば、メモする
###			#   いいね一覧: ARR_Favo
###			for wTweetID in wKeylist :
###				if self.ARR_Favo[wTweetID]['user']['id']==wID :
###					### 既にいいね あり
###					self.ARR_ListFavoUser[wID]['flg_favo'] = True
###					self.ARR_ListFavoUser[wID]['lastTweetDate'] = str( self.ARR_Favo[wTweetID]['created_at'] )
###					
###					#############################
###					# リストいいね情報の更新
###					wSubRes = gVal.OBJ_DB_IF.UpdateListFavoData( self.ARR_Favo[wTweetID]['user'], wTweetID, str(self.ARR_Favo[wTweetID]['created_at']) )
###					if wSubRes['Result']!=True :
###						###失敗
###						wRes['Reason'] = "UpdateListFavoData is failed"
###						gVal.OBJ_L.Log( "B", wRes )
###						break
###					
###					wUpdate = True
###					break
###			
###			#############################
###			# 最終活動日がなければ
###			# 1ツイート目の日付を入れる
###			if self.ARR_ListFavoUser[wID]['lastTweetDate']==None :
###				wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=True,
###					 inID=wID, inCount=1 )
###				if wTweetRes['Result']!=True :
###					wRes['Reason'] = "Twitter Error: GetTL"
###					gVal.OBJ_L.Log( "B", wRes )
###					continue
###				for wTweet in wTweetRes['Responce'] :
###					###日時の変換
###					wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
###					if wTime['Result']!=True :
###						wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweet['created_at'])
###						gVal.OBJ_L.Log( "B", wRes )
###						break
###					### wTime['TimeDate']
###					self.ARR_ListFavoUser[wID]['lastTweetDate'] = str( wTime['TimeDate'] )
###					break
###		
###		wRes['Responce']['Update'] = wUpdate
###		wRes['Responce']['Num'] = len( self.ARR_ListFavoUser )	#数を返す
###		wRes['Result'] = True
###		return wRes
###
###

#####################################################
# リストいいね チェック
#####################################################
###	def CheckFavoUserData( self, inID ):
###		#############################
###		# リストいいねユーザがあるか確認
###		if inID not in self.ARR_ListFavoUser :
###			return False
###		
###		return True
###
###

#####################################################
# リストいいね 更新
#####################################################
###	def UpdateFavoUserData( self, inID, inFLG_Favo=None, inLastTweetDate=None ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_Twitter_IF"
###		wRes['Func']  = "UpdateFavoUserData"
###		
###		wRes['Responce'] = False
###		#############################
###		# リストいいねユーザがあるか確認
###		if self.CheckFavoUserData( inID )!=True :
###			wRes['Result'] = True
###			return wRes
###		
###		#############################
###		# リストいいねの更新
###		if inFLG_Favo!=None :
###			self.ARR_ListFavoUser[inID]['flg_favo'] = inFLG_Favo
###		if inLastTweetDate!=None :
###			self.ARR_ListFavoUser[inID]['lastTweetDate'] = str(inLastTweetDate)
###		
###		wRes['Responce'] = True	#更新あり
###		wRes['Result'] = True
###		return wRes
###
###

#####################################################
# リストいいね クリア
#####################################################
###	def ClearFavoUserData(self):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_Twitter_IF"
###		wRes['Func']  = "ClearFavoUserData"
###		
###		wKeylist = list( self.ARR_ListFavoUser.keys() )
###		for wID in wKeylist :
###			self.ARR_ListFavoUser[wID]['flg_favo'] = False
###		
###		wRes['Result'] = True
###		return wRes
###
###

#####################################################
# リストいいね 表示
#####################################################
###	def ViewFavoUserData(self):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_Twitter_IF"
###		wRes['Func']  = "ViewFavoUserData"
###		
###		#############################
###		# リストいいねが未設定の場合は
###		#   処理を抜ける
###		if gVal.STR_UserInfo['LFavoName']=="" :
###			wStr = "リストいいねは未設定です" + '\n' ;
###			CLS_OSIF.sPrn( wStr )
###			
###			wRes['Result'] = True
###			return wRes
###		
###		#############################
###		# フォロー情報未取得なら
###		# 取得する
###		if len(self.ARR_MyFollowID)==0 :
###			wSubRes = self.GetFollow()
###			if wSubRes['Result']!=True :
###				###失敗
###				wRes['Reason'] = "GetFollow is error"
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###		
###		#############################
###		# ユーザ一覧
###		wStr = '\n' + "--------------------" + '\n' ;
###		wStr = wStr + "リストいいねユーザ一覧" + '\n'
###		wStr = wStr + '\n'
###		wStr = wStr + "FL FV 最終活動日  反応受信日  自動いいね  ユーザ名"
###		CLS_OSIF.sPrn( wStr )
###		
###		wKeylist = list( self.ARR_ListFavoUser.keys() )
###		for wID in wKeylist :
###			#############################
###			# DBからいいね日を取得する
###			wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wID )
###			if wSubRes['Result']!=True :
###				###失敗
###				wRes['Reason'] = "GetFavoDataOne is failed"
###				gVal.OBJ_L.Log( "B", wRes )
###				continue
###			wResFavoDate  = "----------"
###			wListFavoDate = "----------"
###			if wSubRes['Responce']!=None :
###				if wSubRes['Responce']['favo_date']!=None and wSubRes['Responce']['favo_date']!="" and \
###				   wSubRes['Responce']['favo_id']!="(none)" :
###					wResFavoDate  = str(wSubRes['Responce']['favo_date']).split(" ")
###					wResFavoDate  = wResFavoDate[0]
###				
###				if wSubRes['Responce']['lfavo_date']!=None and wSubRes['Responce']['lfavo_date']!="" and \
###				   wSubRes['Responce']['lfavo_id']!="(none)" :
###					wListFavoDate = str(wSubRes['Responce']['lfavo_date']).split(" ")
###					wListFavoDate = wListFavoDate[0]
###			
###			wStr = ""
###			### フォロー者
###			if wID in self.ARR_MyFollowID :
###				wStr = wStr + "〇 "
###			else:
###				wStr = wStr + "－ "
###			
###			### いいね済み
###			if self.ARR_ListFavoUser[wID]['flg_favo']==True :
###				wStr = wStr + "〇 "
###			else:
###				wStr = wStr + "－ "
###			
###			### 最終ツイート日
###			wLastTweetDate = "----------"
###			if self.ARR_ListFavoUser[wID]['lastTweetDate']!=None :
###				wLastTweetDate = self.ARR_ListFavoUser[wID]['lastTweetDate'].split(" ")
###				wLastTweetDate = wLastTweetDate[0]
###			wStr = wStr + wLastTweetDate + ": "
###			
###			### アクション日
###			wStr = wStr + wResFavoDate + ": "
###			
###			### いいね日
###			wStr = wStr + wListFavoDate + ": "
###			
###			### screen_name
###			wStr = wStr + self.ARR_ListFavoUser[wID]['screen_name']
###			CLS_OSIF.sPrn( wStr )
###		
###		wRes['Result'] = True
###		return wRes
###
###
###


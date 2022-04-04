#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 フォロワー監視系
#####################################################
###from htmlif import CLS_HTMLIF
from osif import CLS_OSIF
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterFollower():
#####################################################
	OBJ_Parent = ""				#親クラス実体
	
	CHR_GetReactionDate = None
	ARR_ReacrionUserID = []

#####################################################
# Init
#####################################################
	def __init__( self, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "__init__"
		
		if parentObj==None :
			###親クラス実体の未設定
			wRes['Reason'] = "You have not set the parent class entity for parentObj"
			gVal.OBJ_L.Log( "A", wRes )
			return
		
		self.OBJ_Parent = parentObj
		return



#####################################################
# リアクションチェック
#####################################################
	def ReactionCheck(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "ReactionCheck"
		
		#############################
		# 取得可能時間か？
		if self.CHR_GetReactionDate!=None :
			### 範囲時間内のツイートか
			wGetLag = CLS_OSIF.sTimeLag( str( self.CHR_GetReactionDate ), inThreshold=gVal.DEF_STR_TLNUM['forReactionSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				### 規定以内は除外
				wRes['Result'] = True
				return wRes
		
		self.CHR_GetReactionDate = None	#一度クリアしておく(異常時再取得するため)
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中" )
		
		#############################
		# 自分の直近のツイートを取得
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
			 inID=gVal.STR_UserInfo['id'], inCount=gVal.DEF_STR_TLNUM['reactionTweetLine'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetTL"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if len(wTweetRes['Responce'])==0 :
			wRes['Reason'] = "Tweet is not get: me"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# チェック
		# いいね、リツイート、引用リツイートしたユーザ
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		self.ARR_ReacrionUserID = []
		wARR_AutoRetUsers = []
		wFLG_AutoRetweet = False
		for wTweet in wTweetRes['Responce'] :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			wTweet['id'] = str(wTweet['id'])
			wTweetID = wTweet['id']
			
			###日時の変換
			wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
			if wTime['Result']!=True :
				wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweet['created_at'])
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wTweet['created_at'] = wTime['TimeDate']
			
			#############################
			# チェック対象のツイート表示
			wStr = '\n' + "--------------------" + '\n' ;
			wStr = wStr + "チェック中: " + str(wTime['TimeDate']) + '\n' ;
			wStr = wStr + wTweet['text'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# いいねチェック
			wSubRes = gVal.OBJ_Tw_IF.GetLikesLookup( wTweetID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetLikesLookup): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			wKeylist = list( wSubRes['Responce'] )
			for wID in wKeylist :
				wID = str(wID)
				###ユーザ単位のリアクションチェック
###				wReactionRes = self.ReactionUserCheck( wID, wTweet )
				wReactionRes = self.ReactionUserCheck( wTweet )
				if wReactionRes['Result']!=True :
					wRes['Reason'] = "Twitter Error(ReactionUserCheck): Tweet ID: " + wTweetID
					gVal.OBJ_L.Log( "B", wRes )
					continue
				if wReactionRes['Responce']['Reaction']==True :
					wStr = "〇いいね検出: " + wSubRes['Responce'][wID]['screen_name'] ;
					CLS_OSIF.sPrn( wStr )
			
			#############################
			# リツイートチェック
			wSubRes = gVal.OBJ_Tw_IF.GetRetweetLookup( wTweetID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetRetweetLookup): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			wKeylist = list( wSubRes['Responce'] )
			for wID in wKeylist :
				wID = str(wID)
				###ユーザ単位のリアクションチェック
###				wReactionRes = self.ReactionUserCheck( wID, wTweet, wFLG_AutoRetweet, wARR_AutoRetUsers )
				wReactionRes = self.ReactionUserCheck( wTweet )
				if wReactionRes['Result']!=True :
					wRes['Reason'] = "Twitter Error(ReactionUserCheck 2): Tweet ID: " + wTweetID
					gVal.OBJ_L.Log( "B", wRes )
					continue
				if wReactionRes['Responce']['Reaction']==True :
					wStr = "〇リツイート検出: " + wSubRes['Responce'][wID]['screen_name'] ;
					CLS_OSIF.sPrn( wStr )
			
			#############################
			# 引用リツイートチェック
			wSubRes = gVal.OBJ_Tw_IF.GetRefRetweetLookup( wTweetID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetRefRetweetLookup): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			wKeylist = list( wSubRes['Responce'] )
			for wID in wKeylist :
				wID = str(wID)
				###ユーザ単位のリアクションチェック
###				wReactionRes = self.ReactionUserCheck( wID, wTweet )
				wReactionRes = self.ReactionUserCheck( wTweet )
				if wReactionRes['Result']!=True :
					wRes['Reason'] = "Twitter Error(ReactionUserCheck 3): Tweet ID: " + wTweetID
					gVal.OBJ_L.Log( "B", wRes )
					continue
				if wReactionRes['Responce']['Reaction']==True :
					wStr = "〇引用リツイート検出: " + wSubRes['Responce'][wID]['screen_name'] ;
					CLS_OSIF.sPrn( wStr )
		
		#############################
		# チェック
		# メンションしたユーザ
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中：メンション" )
		
		wSubRes = gVal.OBJ_Tw_IF.GetMyMentionLookup()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetRefRetweetLookup): Tweet ID: " + wTweetID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wSubRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		wKeylist = list( wSubRes['Responce'] )
		for wReplyID in wKeylist :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			#############################
			# チェック対象のツイート表示
			wStr = '\n' + "--------------------" + '\n' ;
			wStr = wStr + "チェック中: " + '\n' ;
			wStr = wStr + wSubRes['Responce'][wReplyID]['reply_text'] ;
			CLS_OSIF.sPrn( wStr )
			
			wID = str(wSubRes['Responce'][wReplyID]['id'])
			
			###日時の変換
			wTime = CLS_OSIF.sGetTimeformat_Twitter( wSubRes['Responce'][wReplyID]['created_at'] )
			if wTime['Result']!=True :
				wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wSubRes['Responce'][wReplyID]['created_at'])
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wSubRes['Responce'][wReplyID]['created_at'] = wTime['TimeDate']
			
			###ユーザ単位のリアクションチェック
###			wReactionRes = self.ReactionUserCheck( wID, wSubRes['Responce'][wReplyID] )
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wReplyID] )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 4): Tweet ID: " + wSubRes['Responce'][wReplyID]['tweet_id']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wReactionRes['Responce']['Reaction']==True :
				#############################
				# ユーザ情報を取得する
				wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=wID )
				if wUserInfoRes['Result']!=True :
					wRes['Reason'] = "Twitter Error: @" + wUserInfoRes['Responce']['screen_name']
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				wStr = "〇リプライ検出: " + wUserInfoRes['Responce']['screen_name']
				CLS_OSIF.sPrn( wStr )
		
		#############################
		# 現時刻をメモる
		self.CHR_GetReactionDate = str(gVal.STR_SystemInfo['TimeDate'])
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# リアクションユーザチェック
#####################################################
###	def ReactionUserCheck( self, inID, inTweet, inFLG_AutoRetweet=False, outARR_AutoUsers=[] ):
	def ReactionUserCheck( self, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "ReactionUserCheck"
		
###		wRes['Responce'] = {
###			"Reaction" : False,		#リアクション更新済
###			"Removed"  : False		#疑似リムーブユーザのアクション
###		}
		wRes['Responce'] = False
		
		wUserID = str(inTweet['user']['id'])
		
###		### 自動リツイート対象ユーザリスト(ポインタ)
###		pARR_AutoUsers = outARR_AutoUsers
###		
		wFLG_Action = True
		#############################
		# リアクション済みのユーザは除外
###		if inID in self.ARR_ReacrionUserID :
		if wUserID in self.ARR_ReacrionUserID :
			wFLG_Action = False	#除外
		
		#############################
		# DBからいいね情報を取得する(1個)
###		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( inID )
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wUserID )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録
		if wSubRes['Responce']==None :
			###DBに登録する
			wSetRes = gVal.OBJ_DB_IF.InsertFavoData( inTweet )
			if wSetRes['Result']!=True :
				###失敗
				wRes['Reason'] = "InsertFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
###			wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( inID )
			wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wUserID )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne(2) is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB未登録（ありえない）
			if wSubRes['Responce']==None :
				wRes['Reason'] = "GetFavoDataOne(3) is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wARR_DBData = wSubRes['Responce']
		
		wTweetID = str( inTweet['id'] )
		#############################
		# 同じアクションはノーリアクション
		if wARR_DBData['favo_id']==wTweetID :
			wFLG_Action = False	#除外
		
		#############################
		# 前のリアクションより最新なら新アクション
		wSubRes = CLS_OSIF.sCmpTime( inTweet['created_at'], inDstTD=wARR_DBData['favo_date'] )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "sCmpTime is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		if wSubRes['Future']==False :
			wFLG_Action = False	#除外
		
		#############################
		# アクションが有効なら、リアクション済みにする
		if wFLG_Action==True :
			#############################
			# いいね情報を更新する
			wSubRes = gVal.OBJ_DB_IF.CountupFavoData( inTweet, wARR_DBData )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "CountupFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			#############################
			# リアクション済みID
###			self.ARR_ReacrionUserID.append( inID )
			self.ARR_ReacrionUserID.append( wUserID )
			
			#############################
			# トラヒック計測：リアクション獲得数
			gVal.STR_TrafficInfo['get_reaction'] += 1
			
			#############################
			# リアクション済み
###			wRes['Responce']['Reaction'] = True
			wRes['Responce'] = True
		
		wRes['Result'] = True
		return wRes



#####################################################
# いいね情報送信
#####################################################
	def SendFavoDate(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "SendFavoDate"
		
		#############################
		# いいね情報を送信する日時か
		wGetLag = CLS_OSIF.sTimeLag( str(gVal.STR_UserInfo['FavoDate']), inThreshold=gVal.DEF_STR_TLNUM['favoSendsSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed(1)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			###期間内
			###  次へ
			wStr = "●いいね送信期間外 処理スキップ" + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		wRes['Responce'] = False
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "いいね情報を送信します" )
		
		#############################
		# DBのいいね情報取得
		# ・送信済 False=送信対象
		wQuery = "select * from tbl_favouser_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"sended = False " + \
					"order by now_favo_cnt desc " + \
					";"
###					"order by week_cnt desc, r_favo_date desc " + \
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 添え字をIDに差し替える
		wARR_RateFavoDate = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		if len( wARR_RateFavoDate )==0 :
			wStr = "●いいね情報 送信者はいませんでした" + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		wSendUserNum = 0
		wSendTweet = []
		wSendTweet.append( wTrendHeader + '\n' )
		wSendTweetIndex = 0
		
		#############################
		# ヘッダの設定
		wTrendHeader = "いいね情報送信"
		
		#############################
		# タグの設定
		wTrendTag = ""
		if gVal.STR_UserInfo['TrendTag']!="" and \
		   gVal.STR_UserInfo['TrendTag']!=None :
			wTrendTag = '\n' + "#" + gVal.STR_UserInfo['TrendTag']
		
		wKeylist = list( wARR_DBData )
		for wID in wKeylist :
			wID = sttr( wID )
			
			#############################
			# リアクション 2回以上は送信
			if wARR_DBData[wID]['now_favo_cnt']>=2 :
				#############################
				# 1行設定
				wLine = "@" + wARR_DBData[wID]['screen_name'] + " : " + \
				        str(wARR_DBData[wID]['now_favo_cnt']) + \
				        "(" + str(wARR_DBData[wID]['now_favo_cnt']) + ")" + '\n'
				
				if ( len( wSendTweet[wSendTweetIndex] ) + len( wLine ) + len( wTrendTag ) )<140 :
					wSendTweet[wSendTweetIndex] = wSendTweet[wSendTweetIndex] + wLine
				else:
					### ヘッダの再設定
					wSendTweet.append( wTrendHeader + '\n' + wLine )
					wSendTweetIndex += 1
			
			#############################
			# リアクション 1回以下
			else:
				wSubRes = gVal.OBJ_DB_IF.SendedFavoData( wID, -1 )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "CountupFavoData(1) is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# 前のトレンドツイートを消す
		
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
			 inID=gVal.STR_UserInfo['id'], inCount=gVal.DEF_STR_TLNUM['favoTweetLine'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetTL"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if len(wTweetRes['Responce'])>0 :
			for wTweet in wTweetRes['Responce'] :
				wID = str(wTweet['id'])
				
				if wTweet['text'].find( wTrendHeader )==0 :
					wTweetRes = gVal.OBJ_Tw_IF.DelTweet( wID )
					if wTweetRes['Result']!=True :
						wRes['Reason'] = "Twitter API Error(2): " + wTweetRes['Reason'] + " id=" + str(wID)
						gVal.OBJ_L.Log( "B", wRes )
					else:
						wStr = "いいね情報ツイートを削除しました。" + '\n'
						wStr = wStr + "------------------------" + '\n'
						wStr = wStr + wTweet['text'] + '\n'
						CLS_OSIF.sPrn( wStr )
		
		#############################
		# ツイートする
		for wLine in wSendTweet :
#			wTweetRes = gVal.OBJ_Tw_IF.Tweet( wLine )
#			if wTweetRes['Result']!=True :
#				wRes['Reason'] = "Twitter API Error(3): " + wTweetRes['Reason']
#				gVal.OBJ_L.Log( "B", wRes )
#				return wRes
#			
			#############################
			# 送信完了
			wStr = "いいね情報を送信しました。" + '\n'
			wStr = wStr + "------------------------" + '\n'
			wStr = wStr + wTrendTweet + '\n'
			CLS_OSIF.sPrn( wStr )
			
		
		#############################
		# 送信済 いいね情報を更新する
		#   リアクション 2回以上
		for wID in wKeylist :
			wID = sttr( wID )
			
			if wARR_DBData[wID]['now_favo_cnt']>=2 :
				wSubRes = gVal.OBJ_DB_IF.SendedFavoData( wID, wARR_DBData[wID]['favo_cnt'] )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "CountupFavoData(1) is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# いいね者送信日時を更新する
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoDate( str( gVal.STR_SystemInfo['TimeDate'] ) )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "UpdateFavoDate is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Result'] = True
		return wRes




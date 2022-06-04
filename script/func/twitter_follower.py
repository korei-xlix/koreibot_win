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
###	def ReactionCheck(self):
	def ReactionCheck( self, inFLG_Short=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "ReactionCheck"
		
		#############################
		# 取得可能時間か？
		if self.OBJ_Parent.CHR_GetReactionDate!=None :
			### 範囲時間内のツイートか
			wGetLag = CLS_OSIF.sTimeLag( str( self.OBJ_Parent.CHR_GetReactionDate ), inThreshold=gVal.DEF_STR_TLNUM['forReactionSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				### 規定以内は除外
				wStr = "●リアクション期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
				CLS_OSIF.sPrn( wStr )
				wRes['Result'] = True
				return wRes
		
		self.OBJ_Parent.CHR_GetReactionDate = None	#一度クリアしておく(異常時再取得するため)
		#############################
		# 取得開始の表示
###		wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中" )
		if inFLG_Short==False :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中（通常）" )
			wCount = gVal.DEF_STR_TLNUM['reactionTweetLine']
		else :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中（ショート）" )
			wCount = gVal.DEF_STR_TLNUM['reactionTweetLine_Short']
		
		#############################
		# 自分の直近のツイートを取得
###		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
###			 inID=gVal.STR_UserInfo['id'], inCount=gVal.DEF_STR_TLNUM['reactionTweetLine'] )
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
			 inID=gVal.STR_UserInfo['id'], inCount=wCount )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetTL"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if len(wTweetRes['Responce'])==0 :
			wRes['Reason'] = "Tweet is not get: me"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# チェック
		# いいね、リツイート、引用リツイートしたユーザ
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		self.OBJ_Parent.ARR_ReacrionUserID = []
		for wTweet in wTweetRes['Responce'] :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			###日時の変換
			wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
			if wTime['Result']!=True :
				wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweet['created_at'])
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wTweet['created_at'] = wTime['TimeDate']
			
			#############################
			# ツイートチェック
			wSubRes = self.OBJ_Parent.ReactionTweetCheck( wTweet )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "ReactionTweetCheck"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
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
		
###		wKeylist = list( wSubRes['Responce'] )
		wKeylist = list( wSubRes['Responce'].keys() )
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
			
			#############################
			# 期間内のTweetか
			wGetLag = CLS_OSIF.sTimeLag( str( wSubRes['Responce'][wReplyID]['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed(1)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				###期間外= 古いツイートなので処理しない
				wStr = "●古いリプライのためスキップします"
				CLS_OSIF.sPrn( wStr )
				continue
			
			#############################
			# ユーザ情報を取得する
			wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=wID )
			if wUserInfoRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: @" + wUserInfoRes['Responce']['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			###ユーザ単位のリアクションチェック
			wReactionRes = self.OBJ_Parent.ReactionUserCheck( wUserInfoRes['Responce'], wSubRes['Responce'][wReplyID] )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 4): Tweet ID: " + str(wSubRes['Responce'][wReplyID]['id'])
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wReactionRes['Responce']==True :
				wStr = "〇リプライ検出: " + wUserInfoRes['Responce']['screen_name']
				CLS_OSIF.sPrn( wStr )
		
		#############################
		# 現時刻をメモる
		self.OBJ_Parent.CHR_GetReactionDate = str(gVal.STR_SystemInfo['TimeDate'])
		
		#############################
		# 正常終了
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
###			wStr = "●いいね送信期間外 処理スキップ" + '\n'
			wStr = "●いいね送信期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
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
		
		### 計測開始日付
		wNowTD = str(wGetLag['InputTime']).split(" ")
		wNowTD = wNowTD[0]
		
		### ヘッダの設定
		wTrendHeader_Pattern = "いいね情報(回数)送信"
		wTrendHeader = wTrendHeader_Pattern + " (" + wNowTD + " から" + str(gVal.DEF_STR_TLNUM['favoSendsCnt']) + "回以上)"
		
		wSendUserNum = 0
		wSendTweet = []
		wSendTweet.append( wTrendHeader + '\n' )
		wSendTweetIndex = 0
		wSendCnt = 0
		#############################
		# タグの設定
		wTrendTag = ""
		if gVal.STR_UserInfo['TrendTag']!="" and \
		   gVal.STR_UserInfo['TrendTag']!=None :
			wTrendTag = '\n' + "#" + gVal.STR_UserInfo['TrendTag']
		
		wFLG_Header = False
###		wKeylist = list( wARR_RateFavoDate )
		wKeylist = list( wARR_RateFavoDate.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			#############################
			# リアクション 規定回以上は送信
			if wARR_RateFavoDate[wID]['now_favo_cnt']>=gVal.DEF_STR_TLNUM['favoSendsCnt'] :
				
				wSendCnt += 1
				#############################
				# 1行設定
###				wLine = "@" + wARR_RateFavoDate[wID]['screen_name'] + " : " + \
###				        str(wARR_RateFavoDate[wID]['now_favo_cnt']) + \
###				        "(" + str(wARR_RateFavoDate[wID]['favo_cnt']) + ")" + '\n'
				wLine = wARR_RateFavoDate[wID]['screen_name'] + " : " + \
				        str(wARR_RateFavoDate[wID]['now_favo_cnt']) + \
				        "(" + str(wARR_RateFavoDate[wID]['favo_cnt']) + ")" + '\n'
				
				wFLG_Header = False
				if ( len( wSendTweet[wSendTweetIndex] ) + len( wLine ) + len( wTrendTag ) )<140 :
					wSendTweet[wSendTweetIndex] = wSendTweet[wSendTweetIndex] + wLine
				else:
					### タグの付加
					wSendTweet[wSendTweetIndex] = wSendTweet[wSendTweetIndex] + wTrendTag
					
					### 次のリストにヘッダの設定
					wSendTweet.append( wTrendHeader + '\n' + wLine )
					wSendTweetIndex += 1
					wFLG_Header = True
			
			#############################
			# リアクション 1回以下
			else:
				wSubRes = gVal.OBJ_DB_IF.SendedFavoData( wID, -1 )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "SendedFavoData(1) is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		if wSendCnt==0 :
			#############################
			# 送信者がいない場合
			#   いいね者送信日時を更新して終わる
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoDate( str( gVal.STR_SystemInfo['TimeDate'] ) )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateFavoDate is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			wStr = "●いいね情報 送信者はいませんでした" + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		### 最後のリストにタグの付加
		if wFLG_Header==False :
			wSendTweet[wSendTweetIndex] = wSendTweet[wSendTweetIndex] + wTrendTag
		
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
				
###				if wTweet['text'].find( wTrendHeader )==0 :
				if wTweet['text'].find( wTrendHeader_Pattern )==0 :
					###日時の変換
					wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
					if wTime['Result']!=True :
						wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweet['created_at'])
						gVal.OBJ_L.Log( "B", wRes )
						continue
					wTweet['created_at'] = wTime['TimeDate']
					
					###ユーザ単位のリアクションチェック
					wReactionRes = self.OBJ_Parent.ReactionUserCheck( wTweet['user'], wTweet )
					if wReactionRes['Result']!=True :
						wRes['Reason'] = "Twitter Error(ReactionUserCheck 4): Tweet ID: " + str(wTweet['id'])
						gVal.OBJ_L.Log( "B", wRes )
						continue
					
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
			wTweetRes = gVal.OBJ_Tw_IF.Tweet( wLine )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(3): " + wTweetRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			#############################
			# 送信完了
			wStr = "いいね情報を送信しました。" + '\n'
			wStr = wStr + "------------------------" + '\n'
			wStr = wStr + wLine + '\n'
			CLS_OSIF.sPrn( wStr )
			
		
		#############################
		# ログに記録
		wRes['Reason'] = "Send FavoInfo at twitter"
		gVal.OBJ_L.Log( "T", wRes )
		
		#############################
		# 送信済 いいね情報を更新する
		#   リアクション 2回以上
		for wID in wKeylist :
			wID = str( wID )
			
			if wARR_RateFavoDate[wID]['now_favo_cnt']>=gVal.DEF_STR_TLNUM['favoSendsCnt'] :
				wSubRes = gVal.OBJ_DB_IF.SendedFavoData( wID, wARR_RateFavoDate[wID]['favo_cnt'] )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "SendedFavoData(2) is failed"
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



#####################################################
# フォロワー状態の更新 確認
#####################################################
###	def FollowerConfirm(self):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterFollower"
###		wRes['Func']  = "FollowerConfirm"
###		
###		#############################
###		# DBのいいね情報取得
###		wQuery = "select id, screen_name, myfollow, myfollow_date, follower, follower_date " + \
###					"from tbl_favouser_data where " + \
###					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' " + \
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
###		wARR_DBData = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
###		
###		#############################
###		# データなし
###		if len(wARR_DBData)==0 :
###			wStr = "いいね情報がないため処理が継続できません。" + '\n'
###			CLS_OSIF.sPrn( wStr )
###			wRes['Result'] = True
###			return wRes
###		
###		#############################
###		# 画面クリア
###		CLS_OSIF.sDispClr()
###		
###		#############################
###		# ヘッダ表示
###		wStr = "--------------------" + '\n'
###		wStr = wStr + " フォロワー状態の更新 確認" + '\n'
###		wStr = wStr + "--------------------" + '\n'
###		CLS_OSIF.sPrn( wStr )
###		
###		wKeylist = list( wARR_DBData.keys() )
###		for wID in wKeylist :
###			wID = str(wID)
###			
###			wUpdate = False
###			#############################
###			# 規定以内のフォロー者か
###			wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData[wID]['myfollow_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forFollowerConfirmSec'] )
###			if wGetLag['Result']!=True :
###				wRes['Reason'] = "sTimeLag failed"
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###			if wGetLag['Beyond']==False :
###				### 規定内=更新あり
###				if wARR_DBData[wID]['myfollow']==True :
###					wStr = "○フォロー者　　: " + wARR_DBData[wID]['screen_name']
###				else:
###					if str( wARR_DBData[wID]['myfollow_date'] )!=gVal.OBJ_DB_IF.DEF_TIMEDATE :
###						wStr = "●リムーブ者　　: " + wARR_DBData[wID]['screen_name']
###				CLS_OSIF.sPrn( wStr )
###				wUpdate = True
###			
###			#############################
###			# 規定以内のフォロワーか
###			wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData[wID]['follower_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forFollowerConfirmSec'] )
###			if wGetLag['Result']!=True :
###				wRes['Reason'] = "sTimeLag failed"
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###			if wGetLag['Beyond']==False :
###				### 規定内=更新あり
###				if wARR_DBData[wID]['follower']==True :
###					wStr = "○フォロワー獲得: " + wARR_DBData[wID]['screen_name']
###				else:
###					if str( wARR_DBData[wID]['follower_date'] )!=gVal.OBJ_DB_IF.DEF_TIMEDATE :
###						wStr = "●リムーブされた: " + wARR_DBData[wID]['screen_name']
###				CLS_OSIF.sPrn( wStr )
###				wUpdate = True
###			
###			### 更新があれば1行開ける
###			if wUpdate==True :
###				CLS_OSIF.sPrn( "" )
###		
###		#############################
###		# 正常終了
###		wRes['Result'] = True
###		return wRes
###
###
###

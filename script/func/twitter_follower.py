#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 フォロワー監視系
#####################################################

###from htmlif import CLS_HTMLIF
from ktime import CLS_TIME
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
	def ReactionCheck( self, inFLG_Short=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "ReactionCheck"
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['reaction'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionSec'] )
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
		
		#############################
		# 取得開始の表示
		if inFLG_Short==False :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中（通常）" )
			wCount = gVal.DEF_STR_TLNUM['reactionTweetLine']
		else :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中（ショート）" )
			wCount = gVal.DEF_STR_TLNUM['reactionTweetLine_Short']
		
		#############################
		# 自分の直近のツイートを取得
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
			wTime = CLS_TIME.sTTchg( wRes, "(1)", wTweet['created_at'] )
			if wTime['Result']!=True :
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
			wTime = CLS_TIME.sTTchg( wRes, "(2)", wSubRes['Responce'][wReplyID]['created_at'] )
			if wTime['Result']!=True :
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
				
				### トラヒック記録
				CLS_Traffic.sP( "r_reaction" )
				CLS_Traffic.sP( "r_rep" )
				if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
					CLS_Traffic.sP( "r_in" )
				else:
					CLS_Traffic.sP( "r_out" )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "reaction", gVal.STR_Time['TimeDate'] )
		if wListRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['reaction']
		
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
		wGetLag = CLS_OSIF.sTimeLag( str(gVal.STR_Time['send_favo']), inThreshold=gVal.DEF_VAL_WEEK )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed(1)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			###期間内
			###  次へ
			wStr = "●いいね送信期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		wRes['Responce'] = False
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "いいね情報送信" )
		
###		#############################
###		# DBのいいね情報取得
###		# ・送信済 False=送信対象
###		wQuery = "select * from tbl_favouser_data where " + \
###					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
###					"sended = False " + \
###					"order by now_favo_cnt desc " + \
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
		# DBのいいね情報取得
		wResDB = gVal.OBJ_DB_IF.GetFavoData_SendFavo()
		if wResDB['Result']!=True :
			wRes['Reason'] = "GetFavoData_SendFavo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_RateFavoDate = wResDB['Responce']
		
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
		
		wARR_SendID = []	#送信したID
		wFLG_Header = False
		wKeylist = list( wARR_RateFavoDate.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			#############################
			# リアクション 規定回以上は送信
###			if wARR_RateFavoDate[wID]['now_favo_cnt']>=gVal.DEF_STR_TLNUM['favoSendsCnt'] :
			if wARR_RateFavoDate[wID]['rfavo_n_cnt']>=gVal.DEF_STR_TLNUM['favoSendsCnt'] :
				
				### 送信したIDで確定
				wARR_SendID.append( wID )
				
				wSendCnt += 1
				#############################
				# 1行設定
###				wLine = wARR_RateFavoDate[wID]['screen_name'] + " : " + \
###				        str(wARR_RateFavoDate[wID]['now_favo_cnt']) + \
###				        "(" + str(wARR_RateFavoDate[wID]['favo_cnt']) + ")" + '\n'
				wLine = wARR_RateFavoDate[wID]['screen_name'] + " : " + \
				        str(wARR_RateFavoDate[wID]['rfavo_n_cnt']) + \
				        "(" + str(wARR_RateFavoDate[wID]['rfavo_cnt']) + ")" + '\n'
				
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
			
		if wSendCnt==0 :
			#############################
			# 送信者がいない場合
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
				
				if wTweet['text'].find( wTrendHeader_Pattern )==0 :
					###日時の変換
					wTime = CLS_TIME.sTTchg( wRes, "(3)", wTweet['created_at'] )
					if wTime['Result']!=True :
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
		gVal.OBJ_L.Log( "T", wRes, "いいね情報送信(Twitter)" )
		
###		#############################
###		# 送信済 いいね情報を更新する
###		#   リアクション 2回以上
###		for wID in wKeylist :
###			wID = str( wID )
###			
###			if wARR_RateFavoDate[wID]['now_favo_cnt']>=gVal.DEF_STR_TLNUM['favoSendsCnt'] :
###				wSubRes = gVal.OBJ_DB_IF.SendedFavoData( wID, wARR_RateFavoDate[wID]['favo_cnt'] )
###				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_SendFavoInfo( wID, wARR_RateFavoDate[wID] )
###				if wSubRes['Result']!=True :
###					###失敗
###					wRes['Reason'] = "UpdateFavoData_SendFavoInfo(2) is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###		
###		#############################
###		# いいね者送信日時を更新する
###		wSubRes = gVal.OBJ_DB_IF.UpdateFavoDate( str( gVal.STR_Time['TimeDate'] ) )
###		if wSubRes['Result']!=True :
###			###失敗
###			wRes['Reason'] = "UpdateFavoDate is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
		#############################
		# いいね者送信日時を更新する
		wResDB = gVal.OBJ_DB_IF.UpdateFavoData_SendFavo( wARR_SendID )
		if wResDB['Result']!=True :
			wRes['Reason'] = "UpdateFavoData_SendFavo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 自動リムーブONの場合
		# トロフィー送信者のうち
		# 規定回数を超えたら昇格して相互フォローにする
		for wID in wARR_SendID :
			wID = str(wID)
			
			if wARR_RateFavoDate[wID]['myfollow']==True :
				#############################
				# 既にフォロー済の場合
				#   かつフォロワーで レベルEの場合
				#   レベルBに昇格する
				if wARR_RateFavoDate[wID]['follower']==True and \
				   wARR_RateFavoDate[wID]['level_tag']=="E" :
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "B" )
				continue
			if wARR_RateFavoDate[wID]['follower']==False :
				### フォロワーでなければ、スキップ
				continue
			if wARR_RateFavoDate[wID]['level_tag']!="B" :
				### レベルB以外は、スキップ
				continue
			
			wCnt = wARR_RateFavoDate[wID]['send_cnt']
			#############################
			# 昇格トロフィー回数=0の場合
			#   自動フォローしてレベルC昇格へ
			if wCnt==0 and \
			   wARR_RateFavoDate[wID]['level_tag']=="E" :
				
				### フォロー＆ミュートする
				wTweetRes = gVal.OBJ_Tw_IF.Follow( wID, inMute=True )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error: Follow" + wTweetRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					continue
				
				### 相互フォローリストに追加
				wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wID )
				
				### ユーザレベル変更
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "C" )
				
				### トラヒック記録（フォロー者増加）
				CLS_Traffic.sP( "p_myfollow" )
				
				### ログに記録
				gVal.OBJ_L.Log( "R", wRes, "自動フォロー（昇格）: " + wARR_RateFavoDate[wID]['screen_name'] )
				
				### DBに反映
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wID, inFLG_MyFollow=True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
				continue
			
			#############################
			# レベルB or C以外か、B+じゃなければここで終わり
			if ( wARR_RateFavoDate[wID]['level_tag']!="B" and \
			   wARR_RateFavoDate[wID]['level_tag']!="C" ) or \
			   wARR_RateFavoDate[wID]['level_tag']=="B+" :
				continue
			
			wCnt += 1
			#############################
			# 昇格トロフィー回数か
			if gVal.DEF_STR_TLNUM['LEVEL_B_Cnt']>wCnt :
				### 規定外 =昇格なし
				continue
			
			### ※昇格あり
			#############################
			# レベルB+昇格へ
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "B+" )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "send_favo", gVal.STR_Time['TimeDate'] )
		if wListRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['send_favo']
		
		wRes['Result'] = True
		return wRes



#####################################################
# 自動リムーブ
#####################################################
	def AutoRemove( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "AutoRemove"
		
		wRes['Responce'] = False	#自動リムーブ実行有無
		
		wUserID = str(inUser['id'])
		
		#############################
		# 自動リムーブが無効ならここで終わる
		if gVal.STR_UserInfo['AutoRemove']==False :
			wRes['Result'] = True
			return wRes
		
		wARR_DBData = None
		#############################
		# DBからいいね情報を取得する(1個)
		#   新規の場合、DB登録だけで終わる
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( inUser )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録
		if wSubRes['Responce']['Data']==None :
			wStr = "▽DB未登録ユーザに対する自動リムーブ検出"
			wRes['Reason'] = wStr + ": " + inUser['screen_name']
			gVal.OBJ_L.Log( "N", wRes )
		else:
			wARR_DBData = wSubRes['Responce']['Data']
		
		wFLG_Remove = False
		#############################
		# フォロー者の場合
		#   Twitterからリムーブする
		if gVal.OBJ_Tw_IF.CheckMyFollow( wUserID )==True :
			if wARR_DBData!=None :
				#############################
				# 期間比較値
				# いいねありの場合、
				#   =いいね日時
				# いいねなしの場合、
				#   =登録日時
				if str(wARR_DBData['favo_date'])!=gVal.DEF_TIMEDATE :
					### いいねあり= いいね日時
					wCompTimeDate = str(wARR_DBData['rfavo_date'])
				else:
					### いいねなし= 登録日時
					wCompTimeDate = str(wARR_DBData['regdate'])
				
				#############################
				# 自動リムーブ期間か
				wGetLag = CLS_OSIF.sTimeLag( wCompTimeDate, inThreshold=gVal.DEF_STR_TLNUM['forListFavoAutoRemoveSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外= 自動リムーブ対象
					wFLG_Remove = True
			else:
				wFLG_Remove = True
			
			if wFLG_Remove==True :
				#############################
				# リムーブ実行
				wTweetRes = gVal.OBJ_Tw_IF.Remove( wUserID )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error: Remove" + wTweetRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
###				### リストリムーブ
###				wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wUserID )
###				
				if wARR_DBData['follower']==True :
					### フォロー者OFF・フォロワーON
					wUserLevel = "D-"
				else:
					### フォロー者OFF・フォロワーOFF
					wUserLevel = "E-"
				
				### ユーザレベル変更
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
				
				### トラヒック記録（フォロワー減少）
				CLS_Traffic.sP( "d_follower" )
				
				#############################
				# ログに記録
				gVal.OBJ_L.Log( "R", wRes, "●自動リムーブ: " + inUser['screen_name'] )
				
				#############################
				# DBに反映
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, inFLG_MyFollow=False )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				wRes['Responce'] = True		#自動リムーブ実行
		
###		wFLG_ListRemove_Only = False
###		#############################
###		# 自動リムーブしていれば
###		#   リスト解除→自動リムーブリストへ
###		# 自動リムーブしていなければ
###		#   リスト解除のみ
###		if wFLG_Remove==False :
###			wFLG_ListRemove_Only = True
###		
###		#############################
###		# フォロワーじゃなければ
###		# リスト解除
###		if wFLG_Remove==True or \
###		   gVal.OBJ_Tw_IF.CheckFollower( wUserID )==False :
###			#############################
###			# 自動リムーブリストに登録
###			# (他のリスト登録は全削除)
###			wTweetRes = gVal.OBJ_Tw_IF.AutoRemove_AddUser( inUser, wFLG_ListRemove_Only )
###			if wTweetRes['Result']!=True :
###				wRes['Reason'] = "AutoRemove_AddUser is failed"
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
		#############################
		# 自動リムーブしていれば
		#   リスト解除→片フォロワーリストへ
		# 自動リムーブしていなければ
		#   リスト解除のみ
		if wFLG_Remove==True :
			### 片フォロワーリストへ
			wTweetRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( inUser )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "FollowerList_AddUser is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		else:
			### リスト解除へ
			wTweetRes = gVal.OBJ_Tw_IF.FollowerList_Remove( inUser )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "FollowerList_Remove is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes




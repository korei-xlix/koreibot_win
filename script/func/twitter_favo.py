#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 いいね監視系
#####################################################

from osif import CLS_OSIF
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterFavo():
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
	def RemFavo( self, inFLG_FirstDisp=True ):
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
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_Tw_ID ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		wRemTweet = 0
		wCancelNum = 0
		#############################
		# 期間を過ぎたいいねを解除していく
		for wID in wARR_Tw_ID :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			wID = str( wID )
			
			###日時の変換
			wTime = CLS_OSIF.sGetTimeformat_Twitter( wARR_TwData[wID]['created_at'] )
			if wTime['Result']!=True :
				wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wARR_TwData[wID]['created_at'])
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wARR_TwData[wID]['created_at'] = wTime['TimeDate']
			
			###期間を過ぎているか
			wGetLag = CLS_OSIF.sTimeLag( str(wARR_TwData[wID]['created_at']), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed(1)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				###期間内
				###  次へ
				wStr = "○解除対象外: " + str(wARR_TwData[wID]['created_at'])
				CLS_OSIF.sPrn( wStr )
				wCancelNum += 1
				if gVal.DEF_STR_TLNUM['favoCancelNum']<=wCancelNum :
					### 規定回数のスキップなので処理停止
					break
				continue
			
			wCancelNum = 0
			###  いいねを外す
			wRemoveRes = gVal.OBJ_Tw_IF.FavoRemove( wID )
			if wRemoveRes['Result']!=True :
				wRes['Reason'] = "Twitter Error"
				gVal.OBJ_L.Log( "B", wRes )
			
			if wRemoveRes['Responce']['Run']==True :
				wStr = "●解除いいね日時: " + str(wRemoveRes['Responce']['Data']['created_at'])
				CLS_OSIF.sPrn( wStr )
				wRemTweet += 1
			else:
				wRes['Reason'] = "FavoRemove failed: id=" + str(wID)
				gVal.OBJ_L.Log( "D", wRes )
				return wRes
			
			#############################
			# 正常
			continue	#次へ
		
		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "Twitterいいね数  : " + str( len(wARR_Tw_ID) )+ '\n'
		wStr = wStr + "いいね解除数     : " + str( wRemTweet )+ '\n'
		wStr = wStr + "最古いいね日時   : " + str( str( wARR_TwData[wARR_Tw_ID_LastKey]['created_at'] ) )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



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
		if self.OBJ_Parent.CHR_GetListFavoDate!=None :
			### 範囲時間内のツイートか
			wGetLag = CLS_OSIF.sTimeLag( str( self.OBJ_Parent.CHR_GetListFavoDate ), inThreshold=gVal.DEF_STR_TLNUM['forListFavoSec'] )
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
		
		self.OBJ_Parent.CHR_GetListFavoDate = None	#一度クリアしておく(異常時再取得するため)
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リストいいね実行中" )
		
		#############################
		# リストいいね リストとユーザの更新
		wSubRes = self.OBJ_Parent.UpdateListFavoUser( inUpdate=True )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateListFavoUser error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リストいいね一覧 取得
		wARR_TwListFavoData = gVal.OBJ_Tw_IF.GetFavoUser()
		
		#############################
		# いいねがない場合、処理を終わる
		if len(wARR_TwListFavoData)==0 :
			wStr = "いいねするリストユーザがないため、処理を終わります。"
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True	#正常終了
			return wRes
		
		#############################
		# リストいいねの初期化
		wResClear = gVal.OBJ_Tw_IF.ClearFavoUserData()
		if wResClear['Result']!=True :
			wRes['Reason'] = "ClearFavoUserData Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_TwListFavoData ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		wFavoTweet = 0
		wKeylist = list( wARR_TwListFavoData.keys() )
		#############################
		# 各ユーザのツイートをいいねしていく
		for wID in wKeylist :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			wID = str( wID )
			
			#############################
			# 自動いいね
			wResFavo = self.AutoFavo( wARR_TwListFavoData[wID] )
			if wResFavo['Result']!=True :
				wRes['Reason'] = "Twitter Error"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			if wResFavo['Responce']['flg_favo_run']==True :
				### いいね実施をカウント
				wFavoTweet += 1
			
			#############################
			# 正常
			continue	#次へ
		
		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "リストいいね数  : " + str( len(wARR_TwListFavoData) )+ '\n'
		wStr = wStr + "いいね実施数    : " + str( wFavoTweet )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 現時刻をメモる
		self.OBJ_Parent.CHR_GetListFavoDate = str(gVal.STR_SystemInfo['TimeDate'])
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 自動いいね
#####################################################
	def AutoFavo( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "AutoFavo"
		
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
			wStr = "●お返しいいね中止(いいね済ユーザ): " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		wNewUser = False
		#############################
		# DBからいいね情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wUserID )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録
		if wSubRes['Responce']==None :
			###DBに登録する
			wSetRes = gVal.OBJ_DB_IF.InsertFavoData( inData )
			if wSetRes['Result']!=True :
				###失敗
				wRes['Reason'] = "InsertFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
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
			
			wNewUser = True	#新規登録
		
		wARR_DBData = wSubRes['Responce']
		
		#############################
		# リストいいね期間外
		if gVal.OBJ_Tw_IF.CheckMyFollow( wUserID)==True :
			wLFavoDateLen = gVal.DEF_STR_TLNUM['forListFavoMyFollowSec']
		else:
			wLFavoDateLen = gVal.DEF_STR_TLNUM['forListFavoNoFollowSec']
		
		if wARR_DBData['lfavo_date']!=None and wARR_DBData['lfavo_date']!="" :
			wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['lfavo_date'] ), inThreshold=wLFavoDateLen )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				### 規定内は処理しない
###				wStr = "●お返しいいね中止(いいね期間内): " + inData['screen_name'] + '\n' ;
				wStr = "●お返しいいね中止(いいね期間内): " + inData['screen_name'] + " timedate=" + str(wARR_DBData['lfavo_date']) + '\n' ;
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
			wStr = "●お返しいいね中止(ツイートなし): " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		wCnt = 0
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
			wCnt += 1
			
			###日時の変換
			wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
			if wTime['Result']!=True :
				wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweet['created_at'])
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wTweet['created_at'] = wTime['TimeDate']
			
			wTweetID = str( wTweet['id'] )
			if wCnt==1 :
				#############################
				# 最初の1ツイート目の日付を設定
				wResUpdate = gVal.OBJ_Tw_IF.UpdateFavoUserData( wUserID, inLastTweetDate=wTweet['created_at'] )
				if wResUpdate['Result']!=True :
					wRes['Reason'] = "UpdateFavoUserData Error(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			### リプライは除外
			if wTweet['in_reply_to_status_id']!=None :
				continue
			### リツイートは除外
			if "retweeted_status" in wTweet :
				continue
			### 引用リツイートは除外
			if "quoted_status" in wTweet :
				continue
			### リプライは除外(ツイートの先頭が @文字=リプライ)
			if wTweet['text'].find("@")==0 :
				continue
			
			### 範囲時間内のツイートか
			wGetLag = CLS_OSIF.sTimeLag( str( wTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
###			if wGetLag['Beyond']==False :
###				### 規定以内は除外
			if wGetLag['Beyond']==True :
				### 規定外 =古いツイートなので除外
				continue
			
			### ツイートチェック
			wWordRes = self.OBJ_Parent.CheckExtWord( inData, wTweet['text'] )
			if wWordRes['Result']!=True :
				wRes['Reason'] = "CheckExtWord failed"
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
			wStr = "●お返しいいね中止(対象なし): " + inData['screen_name'] + '\n' ;
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
		if wSubRes['Responce']['Run']==True :
			wStr = "○自動いいね 実施: " + inData['screen_name'] + '\n' ;
			wRes['Responce']['flg_favo_run'] = True		#いいね済み
		else :
			wStr = "●自動いいね中止(いいね被り): " + inData['screen_name'] + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# リストいいね情報の更新
		wSubRes = gVal.OBJ_DB_IF.UpdateListFavoData( inData, wFavoID, str(gVal.STR_SystemInfo['TimeDate']) )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "UpdateListFavoData is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# いいねあり
		wResUpdate = gVal.OBJ_Tw_IF.UpdateFavoUserData( wUserID, inFLG_Favo=True, inLastTweetDate=None )
		if wResUpdate['Result']!=True :
			wRes['Reason'] = "UpdateFavoUserData Error(2)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Responce']['flg_favo'] = True		#いいね済み
		wRes['Result'] = True
		return wRes




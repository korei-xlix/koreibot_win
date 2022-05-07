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

	CHR_GetReactionDate = None
	ARR_ReacrionUserID = []
###	ARR_FavoUserID = []


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
		
#		#############################
#		# リアクションチェック
#		wSubRes = self.OBJ_TwitterFollower.ReactionCheck()
#		if wSubRes['Result']!=True :
#			wRes['Reason'] = "ReactionCheck"
#			gVal.OBJ_L.Log( "B", wRes )
#			return wRes
#		
#		#############################
#		# いいね情報送信
#		wSubRes = self.OBJ_TwitterFollower.SendFavoDate()
#		if wSubRes['Result']!=True :
#			wRes['Reason'] = "SendFavoDate"
#			gVal.OBJ_L.Log( "B", wRes )
#			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# Init
#####################################################
	def __init__(self):
		self.OBJ_TwitterFollower = CLS_TwitterFollower( parentObj=self )
		self.OBJ_TwitterFavo     = CLS_TwitterFavo( parentObj=self )
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
		# 除外文字読み込み
		wResSub = gVal.OBJ_DB_IF.GetExeWord()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetExcWord failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
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
# 自動監視
#####################################################
###	def AllRun(self):
	def AllRun( self, inFLG_Short=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "AllRun"
		
		#############################
		# ふぁぼ一覧 取得
		wFavoRes = gVal.OBJ_Tw_IF.GetFavo()
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "GetFavoData is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
###		self.ARR_FavoUserID = wFavoRes['Responce']['FavoUserID']
		#############################
		# いいね解除
		if inFLG_Short==False :
###			wSubRes = self.OBJ_TwitterFavo.RemFavo( inARR_Favo=wFavoRes['Responce'] )
###			wSubRes = self.OBJ_TwitterFavo.RemFavo( inARR_Favo=wFavoRes['Responce']['FavoData'] )
			wSubRes = self.OBJ_TwitterFavo.RemFavo()
			if wSubRes['Result']!=True :
				wRes['Reason'] = "RemFavo"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# リスト通知 リストとユーザの更新
		wSubRes = self.UpdateListIndUser( inUpdate=True )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateListIndUser error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リアクションチェック
		wSubRes = self.OBJ_TwitterFollower.ReactionCheck( inFLG_Short=inFLG_Short )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "ReactionCheck"
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
		# 古いいいね情報の削除
		if inFLG_Short==False :
			wSubRes = gVal.OBJ_DB_IF.DeleteFavoData()
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "DeleteFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
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
# いいね解除
#####################################################
###	def RemFavo(self):
###		wRes = self.OBJ_TwitterFavo.RemFavo()
###		return wRes
###
###

#####################################################
# トレンドツイート
#####################################################
	def TrendTweet(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "TrendTweet"
		
		#############################
		# リスト通知 リストとユーザの更新
		wSubRes = self.UpdateListIndUser()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateListIndUser error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes = self.OBJ_TwitterKeyword.TrendTweet()
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# トレンドタグ設定
#####################################################
	def SetTrendTag(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetTrendTag"
		
		wSubRes = gVal.OBJ_DB_IF.SetTrendTag()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetTrendTag Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# リスト通知設定
#####################################################
	def SetListInd(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetListInd"
		
		wListName = None
		#############################
		# Twitterキーの入力
		CLS_OSIF.sPrn( "リスト通知の設定をおこないます。" )
		CLS_OSIF.sPrn( "---------------------------------------" )
		while True :
			###初期化
			wListName = None
			
			#############################
			# 実行の確認
			wSelect = CLS_OSIF.sInp( "キャンセルしますか？(y)=> " )
			if wSelect=="y" :
				# 完了
				wRes['Result'] = True
				return wRes
			
			#############################
			# 入力
			wStr = "通知に設定するリスト名を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sInp( "List Name ？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "リスト名が未入力です" + '\n' )
				continue
			wListName = wKey
			
			###ここまでで入力は完了した
			break
		
		#############################
		# DBに登録する
		if wListName==None :
			wRes['Reason'] = "wListName: None"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
###		#############################
###		# リスト通知の更新
###		wSubRes = gVal.OBJ_Tw_IF.GetListInd( inUpdate=True )
###		if wSubRes['Result']!=True :
###			wRes['Reason'] = "GetListInd error"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
		#############################
		# リスト通知 リストとユーザの更新
		wSubRes = self.UpdateListIndUser( inUpdate=True )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateListIndUser error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リストがTwitterにあるか確認
		wSubRes = gVal.OBJ_Tw_IF.CheckListInd( inListName=wListName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
			CLS_OSIF.sPrn( "Twitterにないリストです: " + wListName + '\n' )
			wRes['Result'] = True
			return wRes
		
		#############################
		# DBに登録する
		wSubRes = gVal.OBJ_DB_IF.SetListInd( wListName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetTrendTag Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
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
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetListFavo"
		
		wListName = None
		#############################
		# Twitterキーの入力
		CLS_OSIF.sPrn( "リストいいねの設定をおこないます。" )
		CLS_OSIF.sPrn( "---------------------------------------" )
		while True :
			###初期化
			wListName = None
			
			#############################
			# 実行の確認
			wSelect = CLS_OSIF.sInp( "キャンセルしますか？(y)=> " )
			if wSelect=="y" :
				# 完了
				wRes['Result'] = True
				return wRes
			
			#############################
			# 入力
			wStr = "リストいいねに設定するリスト名を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sInp( "List Name ？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "リスト名が未入力です" + '\n' )
				continue
			wListName = wKey
			
			###ここまでで入力は完了した
			break
		
		#############################
		# DBに登録する
		if wListName==None :
			wRes['Reason'] = "wListName: None"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リストいいね リストとユーザの更新
		wSubRes = self.UpdateListIndUser( inUpdate=True )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateListIndUser error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リストがTwitterにあるか確認
		wSubRes = gVal.OBJ_Tw_IF.CheckListInd( inListName=wListName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
			CLS_OSIF.sPrn( "Twitterにないリストです: " + wListName + '\n' )
			wRes['Result'] = True
			return wRes
		
		#############################
		# DBに登録する
		wSubRes = gVal.OBJ_DB_IF.SetListFavo( wListName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetListFavo Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# リアクションツイートチェック
#####################################################
	def ReactionTweetCheck( self, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "ReactionTweetCheck"
		
		wTweet = inTweet
		
###		#############################
###		# 期間内のTweetか
###		wGetLag = CLS_OSIF.sTimeLag( str( wTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
###		if wGetLag['Result']!=True :
###			wRes['Reason'] = "sTimeLag failed(1)"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		if wGetLag['Beyond']==True :
###			###期間外= 古いツイートなので処理しない
###			wRes['Result'] = True
###			return wRes
###		
		wUserID = str( wTweet['user']['id'] )
		#############################
		# 自分のツイート以外は処理を抜ける
		if str(gVal.STR_UserInfo['id'])!=wUserID :
			### 自分のツイートではない＝正常終了
			wRes['Result'] = True
			return wRes
		
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
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wReactionRes['Responce']==True :
				wStr = "〇いいね検出: " + wSubRes['Responce'][wID]['screen_name'] ;
				CLS_OSIF.sPrn( wStr )
		
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
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 2): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wReactionRes['Responce']==True :
				wStr = "〇リツイート検出: " + wSubRes['Responce'][wID]['screen_name'] ;
				CLS_OSIF.sPrn( wStr )
		
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
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 3): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wReactionRes['Responce']==True :
				wStr = "〇引用リツイート検出: " + wSubRes['Responce'][wID]['screen_name'] ;
				CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# リアクションユーザチェック
#####################################################
	def ReactionUserCheck( self, inUser, inTweet ):
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
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wUserID )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録
		if wSubRes['Responce']==None :
			###DBに登録する
			wSetRes = gVal.OBJ_DB_IF.InsertFavoData( inUser )
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
		
		wTweetID = str( inTweet['id'] )
		#############################
		# 同じアクションはノーリアクション
		if wARR_DBData['favo_id']==wTweetID :
			wFLG_Action = False	#除外
		
		#############################
		# 前のリアクションより最新なら新アクション
		if wFLG_Action==True :
			wSubRes = CLS_OSIF.sCmpTime( inTweet['created_at'], inDstTD=wARR_DBData['favo_date'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "sCmpTime is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Future']==False :
				wFLG_Action = False	#除外
		
		#############################
		# リアクション禁止ユーザか
		if wARR_DBData['screen_name'] in gVal.DEF_STR_NOT_REACTION :
			if wFLG_Action==True :
				### 除外してない場合
				
				### いいね情報を更新する
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData( inUser, inTweet, wARR_DBData, False )
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
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData( inUser, inTweet, wARR_DBData )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			#############################
			# リアクション済みID
			self.ARR_ReacrionUserID.append( inUser['id'] )
			
			#############################
			# トラヒック計測：リアクション獲得数
			gVal.STR_TrafficInfo['get_reaction'] += 1
			
###			#############################
###			# 自動おかえしいいねする
###			if gVal.DEF_STR_TLNUM['autoRepFavo']==True :
###				wSubRes = self.__ReactionUserCheck_RepFavo( wARR_DBData )
###				if wSubRes['Result']!=True :
###					###失敗
###					wRes['Reason'] = "__ReactionUserCheck_RepFavo is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###			
###			#############################
###			# リスト通知をおこなう
###			if gVal.STR_UserInfo['ListName']!="" :
###				wSubRes = self.__ReactionUserCheck_ListInd( wARR_DBData )
###				if wSubRes['Result']!=True :
###					###失敗
###					wRes['Reason'] = "__ReactionUserCheck_ListInd is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###			
			#############################
			# リアクションへのリアクション
			wSubRes = self.__ReactionUserCheck_PutReaction( wARR_DBData, inTweet, wNewUser )
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
	def __ReactionUserCheck_PutReaction( self, inData, inTweet, inNewUser=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "__ReactionUserCheck_PutReaction"
		
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
			wSubRes = self.__ReactionUserCheck_RepFavo( inData )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "__ReactionUserCheck_RepFavo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# リスト通知をおこなう
		if gVal.STR_UserInfo['ListName']!="" :
			wSubRes = self.__ReactionUserCheck_ListInd( inData )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "__ReactionUserCheck_ListInd is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# 自動おかえしいいねする
	#####################################################
	def __ReactionUserCheck_RepFavo( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "__ReactionUserCheck_RepFavo"
		
		wUserID = str( inData['id'] )
		#############################
		# いいね一覧にあるユーザへは
		# おかえししない
###		if wUserID in self.ARR_FavoUserID :
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
			
			###日時の変換
			wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
			if wTime['Result']!=True :
				wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweet['created_at'])
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wTweet['created_at'] = wTime['TimeDate']
			
			### 範囲時間内のツイートか
###			wGetLag = CLS_OSIF.sTimeLag( str( wTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['autoRepFavoSec'] )
			wGetLag = CLS_OSIF.sTimeLag( str( wTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
###				### 規定外は除外
###				continue
				### 規定外は1つでもあれば いいねしない(これが最新だけど規定時間外)
				break
			
			### ツイートチェック
			wWordRes = self.CheckExtWord( inData, wTweet['text'] )
			if wWordRes['Result']!=True :
				wRes['Reason'] = "CheckExtWord failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wWordRes['Responce']==False :
				### 除外
				continue
			
			### ※いいねツイート確定
			wFavoID = wTweet['id']
			break
		
		#############################
		# いいねツイートなしはおわり
		if wFavoID==None :
			wRes['Result'] = True
			return wRes
		
		#############################
		# いいねする
		wSubRes = gVal.OBJ_Tw_IF.Favo( wFavoID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(Favo): user=" + inData['screen_name'] + " id=" + str(wFavoID)
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
###		wStr = "○お返しいいね済み: " + inData['screen_name'] + '\n' ;
###		if wSubRes['Responce']==True :
		if wSubRes['Responce']['Run']==True :
			wStr = "○お返しいいね 実施: " + inData['screen_name'] + '\n' ;
		else :
			wStr = "●お返しいいね中止(いいね被り): " + inData['screen_name'] + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
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
		wNowDate = str(gVal.STR_SystemInfo['TimeDate'])
		wNowDate = wNowDate.split(" ")
		wNowDate = wNowDate[0]
		wRateDate = str(inData['list_date'])
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
		wSubRes = gVal.OBJ_Tw_IF.InserttListIndUser( inData )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(InserttListIndUser): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
###		if wSubRes['Responce']==True :
		if wSubRes['Responce']==False :
			### 既に登録済み
			wStr = "●リスト通知済み: " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# DBに登録する
		wSubRes = gVal.OBJ_DB_IF.UpdateListIndData( inData )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateListIndData Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wStr = "○リスト通知の発行: " + inData['screen_name'] + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# リスト通知ユーザ更新
#####################################################
	def UpdateListIndUser( self, inUpdate=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "UpdateListIndUser"
		
		#############################
		# 処理時間の更新
		wSubRes = gVal.OBJ_DB_IF.UpdateListIndDate()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateListIndDate Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wFLG_NextDay = wSubRes['Responce']
		
		#############################
		# リスト通知の更新
		wSubRes = gVal.OBJ_Tw_IF.GetListInd( inUpdate=inUpdate )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetListInd error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# まだ今日の場合
		if wFLG_NextDay==False :
			#############################
			# リスト通知 ユーザの更新
			wSubRes = gVal.OBJ_Tw_IF.GetListIndUser( inUpdate=inUpdate )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "GetListIndUser error"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
###			wStr = "〇リスト通知ユーザ取: " + str( wSubRes['Responce'] ) + ".件" + '\n' ;
###			CLS_OSIF.sPrn( wStr )
			if wSubRes['Responce']['Update']==True :
				wStr = "〇リスト通知: " + str( wSubRes['Responce']['Num'] ) + ".件" + '\n' ;
			else:
				wStr = "●リスト通知 未更新: " + str( wSubRes['Responce']['Num'] ) + ".件" + '\n' ;
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# 翌日
		else:
			wSubRes = gVal.OBJ_Tw_IF.AllClearListInd()
			if wSubRes['Result']!=True :
				wRes['Reason'] = "AllClearListInd error"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			wStr = "●リスト通知を全クリアしました" + '\n' ;
			CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# リスト通知ユーザ表示
	def ViewListIndUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "ViewListIndUser"
		
		#############################
		# リスト通知の表示
		wSubRes = gVal.OBJ_Tw_IF.ViewListIndUser()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "ViewListIndUser error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# リストいいねユーザ更新
#####################################################
	def UpdateListFavoUser( self, inUpdate=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "UpdateListFavoUser"
		
		#############################
		# 処理時間の更新
		wSubRes = gVal.OBJ_DB_IF.UpdateListFavoDate()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateListFavoDate Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リストいいねの更新
		wSubRes = gVal.OBJ_Tw_IF.GetListFavo( inUpdate=inUpdate )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetListFavo error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リストいいね ユーザの更新
		wSubRes = gVal.OBJ_Tw_IF.GetListFavoUser( inUpdate=inUpdate )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetListFavoUser error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		if wSubRes['Responce']['Update']==True :
			wStr = "〇リストいいね: " + str( wSubRes['Responce']['Num'] ) + ".件" + '\n' ;
		else:
			wStr = "●リストいいね 未更新: " + str( wSubRes['Responce']['Num'] ) + ".件" + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# リストいいねユーザ表示
	def ViewListFavoUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "ViewListFavoUser"
		
		#############################
		# リストいいねの表示
		wSubRes = gVal.OBJ_Tw_IF.ViewListFavoUser()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "ViewListFavoUser error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
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
		if inWord in gVal.ARR_ExeWord :
			if gVal.ARR_ExeWord[inWord]['report']==True :
				wStr = "●報告対象の文字除外: id=" + inData['screen_name'] + '\n'
				wStr = wStr + inWord + '\n'
				CLS_OSIF.sPrn( wStr )
			
			### 除外
			wRes['Result'] = True
			return wRes
		
		#############################
		# 正常終了
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes




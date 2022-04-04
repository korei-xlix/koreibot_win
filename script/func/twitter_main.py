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

from osif import CLS_OSIF
from traffic import CLS_Traffic
from gval import gVal
#####################################################
class CLS_TwitterMain():
#####################################################
	OBJ_TwitterFollower = None
	OBJ_TwitterFavo     = None
	OBJ_TwitterKeyword  = None



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
		self.OBJ_TwitterFollower = CLS_TwitterFollower( parentObj=self )
		self.OBJ_TwitterFavo     = CLS_TwitterFavo( parentObj=self )
		self.OBJ_TwitterKeyword  = CLS_TwitterKeyword( parentObj=self )
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
	def AllRun(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "AllRun"
		
		#############################
		# いいね解除
		wSubRes = self.OBJ_TwitterFavo.RemFavo()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "RemFavo"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リアクションチェック
		wSubRes = self.OBJ_TwitterFollower.ReactionCheck()
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
		# 完了
		wRes['Result'] = True
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
		wRes = self.OBJ_TwitterKeyword.TrendTweet()
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
			gVal.OBJ_DB_IF.Close()
			return False
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes




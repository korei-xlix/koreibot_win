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
	VAL_ZanNum = 0

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
# いいね情報の取得
#####################################################
	def Get( self, inFLG_FirstDisp=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "Get"
		
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "いいね情報 取得中" )
		
		#############################
		# ふぁぼ一覧 取得
		wFavoRes = gVal.OBJ_Tw_IF.GetFavo()
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "GetFavoData is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		wARR_TwData = wFavoRes['Responce']
		
		#############################
		# DBふぁぼ一覧 取得
		wSubRes = gVal.OBJ_DB_IF.GetFavoData()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoData is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_DBData = wSubRes['Responce']
		wARR_DB_ID = list( wARR_DBData.keys() )
		
		wARR_Tw_ID = list( wARR_TwData.keys() )
		wARR_Tw_ID_LastKey = wARR_Tw_ID[-1]
		wCheckedID = []
		#############################
		# Twitter情報がDBに登録されているか
		for wID in wARR_Tw_ID :
			wID = str( wID )
			wCheckedID.append( wID )
			
			###DBに登録されているか
			if wID not in wARR_DB_ID :
				###登録されていない =新規登録
				wSubRes = gVal.OBJ_DB_IF.InsertFavoData( wARR_TwData[wID] )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "InsertFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# DBふぁぼ一覧 取得(再取得)
		wSubRes = gVal.OBJ_DB_IF.GetFavoData()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoData(2) is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_DBData = wSubRes['Responce']
		wARR_DB_ID = list( wSubRes['Responce'].keys() )
		
		#############################
		# DBデータの処理
		# ・いいねしたユーザがDBにない場合、収集する
		wGetFavoID = []
		for wID in wARR_DB_ID :
			wID = str( wID )
			
			wQuery = None
			#############################
			# Twitterにいいね情報があって、
			# 保存期間外の場合
			#   =リムーブ候補に設定する
			if wID in wARR_Tw_ID :
				wGetFavoID.append( wID )
				
				###保存期間外の場合
				###  リムーブ候補に設定する
				wGetLag = CLS_OSIF.sTimeLag( str(wARR_DBData[wID]['created_at']), inThreshold=gVal.DEF_STR_TLNUM['forFavoRemSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外
					###  limited をONにする
					wQuery = "update tbl_favo_data set " + \
								"limited = True " + \
								"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
								" and id = '" + wID + "' ;"
					
					wStr = "保存期間外いいね日時: " + str(wARR_DBData[wID]['created_at'])
					CLS_OSIF.sPrn( wStr )
			
			#############################
			# Twitterにいいね情報がなくて
			# DBがリムーブ済みになっていない
			#   =リムーブ済みにする
			else :
				if wARR_DBData[wID]['removed']==False :
					wQuery = "update tbl_favo_data set " + \
								"limited = False, " + \
								"removed = True " + \
								"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
								" and id = '" + wID + "' ;"
					
					wStr = "Twitterにない いいね日時: " + str(wARR_DBData[wID]['created_at'])
					CLS_OSIF.sPrn( wStr )
			
			#############################
			# ユーザがDBに登録されているか
			wUserID = str( wARR_DBData[wID]['user_id'] )
			if gVal.OBJ_DB_IF.CheckFollowerData(wUserID)==False :
				###登録されていない =新規登録
				wSubRes = self.OBJ_Parent.InsertNewFollower( wUserID )
				if wSubRes['Result']!=True :
					###  失敗したら、いいねを外す
					wRemoveRes = gVal.OBJ_Tw_IF.FavoRemove( wID )
					if wRemoveRes['Result']!=True :
						wRes['Reason'] = "Twitter Error"
						gVal.OBJ_L.Log( "B", wRes )
					
					###  limited をOFF、removed をONにする
					wQuery = "update tbl_favo_data set " + \
								"limited = False, " + \
								"removed = True " + \
								"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
								" and id = '" + wID + "' ;"
			
			###実行
			if wQuery!=None :
				wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
				if wResDB['Result']!=True :
					wRes['Reason'] = "Run Query is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "Twitterいいね数  : " + str( len(wARR_Tw_ID) )+ '\n'
		wStr = wStr + "DBいいね数       : " + str( len(wARR_DB_ID) )+ '\n'
		wStr = wStr + "取得数           : " + str( len(wGetFavoID) )+ '\n'
		wStr = wStr + "最古いいね日時   : " + str( str( wARR_TwData[wARR_Tw_ID_LastKey]['created_at'] ) )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# いいね情報の表示
#####################################################
	def View(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "View"
		
		#############################
		# DBいいね一覧 取得
		wSubRes = self.OBJ_Parent.GetDBFavo()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetDBFavo is failed: " + CLS_OSIF.sCatErr( wSubRes )
			return wRes
		wARR_RateFavo = wSubRes['Responce']
		
		#############################
		# DBフォロワー一覧 取得
		wSubRes = self.OBJ_Parent.GetDBFollower()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetDBFollower is failed: " + CLS_OSIF.sCatErr( wSubRes )
			return wRes
		wARR_RateFollowers = wSubRes['Responce']
		
		#############################
		# 画面クリア
		CLS_OSIF.sDispClr()
		
		wCntRemove  = 0
		wCntRemoved = 0
		#############################
		# ヘッダ表示
		wStr = "--------------------" + '\n'
		wStr = wStr + " 保持中のいいね情報" + '\n'
		wStr = wStr + "--------------------" + '\n'
		
		#############################
		# 情報組み立て
		wKeylist = list( wARR_RateFavo.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			if wARR_RateFavo[wID]['twitterid']!=gVal.STR_UserInfo['Account'] :
				continue	#自分以外の情報はスキップ
			
			wUserID = str( wARR_RateFavo[wID]['user_id'] )
			wStr = wStr + str(wARR_RateFavo[wID]['text']) + '\n'
			wStr = wStr + "ツイ日=" + str(wARR_RateFavo[wID]['created_at'])
			wStr = wStr + "  ユーザ=" + str(wARR_RateFollowers[wUserID]['user_name']) + "(@" + str(wARR_RateFollowers[wUserID]['screen_name']) + ")" + '\n'
			wStr = wStr + "登録日=" + str(wARR_RateFavo[wID]['regdate'])
			if wARR_RateFavo[wID]['removed']==True :
				wStr = wStr + " [☆いいね解除済み]"
				wCntRemoved += 1
			elif wARR_RateFavo[wID]['limited']==True :
				wStr = wStr + " [★いいね解除対象]"
				wCntRemove += 1
			
			wStr = wStr + '\n'
			wStr = wStr + "--------------------" + '\n'
		
		#############################
		# 統計
		wStr = wStr + "--------------------" + '\n'
		wStr = wStr + "解除対象 いいね数 = " + str( wCntRemove ) + '\n'
		wStr = wStr + "解除済み いいね数 = " + str( wCntRemoved ) + '\n'
		
		#############################
		# コンソールに表示
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# いいね監視の実行
#####################################################
	def Run(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "Run"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "いいね監視 実行中" )
		
		#############################
		# DBのいいね一覧取得
		wQuery = "select * from tbl_favo_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"limited = True " + \
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
		wARR_DBData = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_DBData ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		#############################
		# 解除数表示
		wStr = "解除いいね数: " + str( len(wARR_DBData) )
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# いいね解除していく
		wKeylist = list( wARR_DBData.keys() )
		for wID in wKeylist :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			wID = str( wID )
			
			###  いいねを外す
			wRemoveRes = gVal.OBJ_Tw_IF.FavoRemove( wID )
			if wRemoveRes['Result']!=True :
				wRes['Reason'] = "Twitter Error"
				gVal.OBJ_L.Log( "B", wRes )
			
			###  limited をOFF、removed をONにする
			wQuery = "update tbl_favo_data set " + \
						"limited = False, " + \
						"removed = True " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + wID + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			#############################
			# 解除表示
			wStr = "解除いいね日時: " + str(wARR_DBData[wID]['created_at'])
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# 正常
			continue	#次へ
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 通常いいね
#####################################################
	def NormalFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "NormalFavo"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "通常いいね 実行中" )
		
		#############################
		# いいね情報取得
		wSubRes = self.Get( inFLG_FirstDisp=False )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Favo Get is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# DBのフォロワー一覧取得( id のみ)
		# ・相互フォロー
		# ・監視ユーザ
		# ・リムーブ候補、非フォロワー、疑似リムーブではない
		# ・いいねを1回以上受信している
		# ・VIPは無条件
		wQuery = "select id from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"( " + \
					"rc_myfollow = True and " + \
					"rc_follower = True and " + \
					"un_follower = False and " + \
					"limited = False and " + \
					"removed = False and " + \
					"adm_agent = True and " + \
					"r_favo_cnt > 0 ) or " + \
					"vipuser = True " + \
					";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リスト型に整形
		wARR_DBDataID = gVal.OBJ_DB_IF.ChgList( wResDB['Responce'] )
		
		#############################
		# DBのいいね一覧取得( id のみ )
		wQuery = "select id from tbl_favo_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"limited = False and " + \
					"removed = False " + \
					";"
		
		wResDBFavo = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDBFavo['Result']!=True :
			wRes['Reason'] = "Run Query is failed(2)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リスト型に整形
		wARR_DBFavoID = gVal.OBJ_DB_IF.ChgList( wResDBFavo['Responce'] )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_DBDataID ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		#############################
		# ツイートをファボっていく
		wRateFollowerNum = len( wARR_DBDataID )
		for wID in wARR_DBDataID :
			wID = str( wID )
			
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			#############################
			# DBからユーザ情報を取得する(1個)
			wSubRes = self.GetFavoUser( wID )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoUser is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Responce']['Target']!=True :
				continue	#対象じゃない=除外
			wARR_DBData = wSubRes['Responce']['Data']
    		
			#############################
			# 非フォロー化の場合
			# ランダム抽選で受かったか
			if wARR_DBData['un_follower']==True :
				wRand = CLS_OSIF.sGetRand( 100 )
				if gVal.DEF_STR_TLNUM['normalFavoRand']<wRand :
					###不合格
					wStr = "▼非フォロー抽選不合格のためスキップします: 前回いいね日=" + str(wARR_DBData['favo_date']) + '\n'
					CLS_OSIF.sPrn( wStr )
			
			#############################
			# いいね処理
			wResFavo = self.FavoFavorite( wID, wARR_DBData, wResDBFavo, False )
			if wResFavo['Result']!=True :
				###失敗
				wRes['Reason'] = "FavoFavorite is failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			if wResFavo['Responce']!=None :
				wFavoID = wResFavo['Responce']	#いいねしたツイートIDを追加
				wARR_DBFavoID.append( wFavoID )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# VIPいいね
#####################################################
	def VIPFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "ItumenFavo"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "VIPいいね 実行中" )
		
		#############################
		# いいね情報取得
		wSubRes = self.Get( inFLG_FirstDisp=False )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Favo Get is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# DBのフォロワー一覧取得( id のみ)
		wQuery = "select id from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"vipuser = True " + \
					";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リスト型に整形
		wARR_DBDataID = gVal.OBJ_DB_IF.ChgList( wResDB['Responce'] )
		
		#############################
		# DBのいいね一覧取得( id のみ )
		wQuery = "select id from tbl_favo_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"limited = False and " + \
					"removed = False " + \
					";"
		
		wResDBFavo = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDBFavo['Result']!=True :
			wRes['Reason'] = "Run Query is failed(2)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リスト型に整形
		wARR_DBFavoID = gVal.OBJ_DB_IF.ChgList( wResDBFavo['Responce'] )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_DBDataID ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		#############################
		# ツイートをファボっていく
		wRateFollowerNum = len( wARR_DBDataID )
		for wID in wARR_DBDataID :
			wID = str( wID )
			
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			#############################
			# DBからユーザ情報を取得する(1個)
			wSubRes = self.GetFavoUser( wID )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoUser is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Responce']['Target']!=True :
				continue	#対象じゃない=除外
			wARR_DBData = wSubRes['Responce']['Data']
    		
			#############################
			# いいね処理
			wResFavo = self.FavoFavorite( wID, wARR_DBData, wResDBFavo, False )
			if wResFavo['Result']!=True :
				###失敗
				wRes['Reason'] = "FavoFavorite is failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			if wResFavo['Responce']!=None :
				wFavoID = wResFavo['Responce']	#いいねしたツイートIDを追加
				wARR_DBFavoID.append( wFavoID )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ちょっかいいいね
#####################################################
	def ChoFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "ChoFavo"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "ちょっかいいいね 実行中" )
		
		#############################
		# いいね情報取得
		wSubRes = self.Get( inFLG_FirstDisp=False )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Favo Get is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# DBのフォロワー一覧取得( id のみ)
		# ・相互フォロー
		# ・監視ユーザ
		# ・リムーブ候補、非フォロワー、疑似リムーブではない
		# ・いいね未受信
		# ・VIPは除外
		wQuery = "select id from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"( " + \
					"rc_myfollow = True and " + \
					"rc_follower = True and " + \
					"un_follower = False and " + \
					"limited = False and " + \
					"removed = False and " + \
					"adm_agent = True and " + \
					"r_favo_cnt = 0 ) or " + \
					"vipuser = False " + \
					";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リスト型に整形
		wARR_DBDataID = gVal.OBJ_DB_IF.ChgList( wResDB['Responce'] )
		
		#############################
		# DBのいいね一覧取得( id のみ )
		wQuery = "select id from tbl_favo_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"limited = False and " + \
					"removed = False " + \
					";"
		
		wResDBFavo = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDBFavo['Result']!=True :
			wRes['Reason'] = "Run Query is failed(2)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リスト型に整形
		wARR_DBFavoID = gVal.OBJ_DB_IF.ChgList( wResDBFavo['Responce'] )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_DBDataID ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		#############################
		# ツイートをファボっていく
		wRateFollowerNum = len( wARR_DBDataID )
		for wID in wARR_DBDataID :
			wID = str( wID )
			
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			#############################
			# DBからユーザ情報を取得する(1個)
			wSubRes = gVal.OBJ_DB_IF.GetFollowerDataOne( wID )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFollowerDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			wARR_DBData = wSubRes['Responce']
			
			#############################
			# 前回のいいねから期間がたったか
			wGetLag = CLS_OSIF.sTimeLag( str(wARR_DBData['favo_date']), inThreshold=gVal.DEF_STR_TLNUM['forChoFavoSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				### 期間内は除外
				wStr = "▼直近いいね済みなのでスキップします: 前回いいね日=" + str(wARR_DBData['favo_date']) + '\n'
				CLS_OSIF.sPrn( wStr )
				continue	#対象じゃない=除外
			
			#############################
			# いいね処理
			wResFavo = self.FavoFavorite( wID, wARR_DBData, wResDBFavo, False )
			if wResFavo['Result']!=True :
				###失敗
				wRes['Reason'] = "FavoFavorite is failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			if wResFavo['Responce']!=None :
				wFavoID = wResFavo['Responce']	#いいねしたツイートIDを追加
				wARR_DBFavoID.append( wFavoID )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# いいねユーザ取得
#####################################################
	def GetFavoUser( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "GetFavoUser"
		
		wRes['Responce'] = {
			"Target"	: False,
			"Data"		: None
		}
		#############################
		# DBからユーザ情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFollowerDataOne( inID )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFollowerDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_DBData = wSubRes['Responce']
		wRes['Responce']['Data'] = wARR_DBData
		
		#############################
		# 処理中ユーザ表示
		wStr = "選出ユーザ： @" + wARR_DBData['screen_name']
		CLS_OSIF.sPrn( wStr )
		
		### 以下いずれかに当てはまる場合は除外
		# ただしVIPは判定しない
		# ・フォロー者ではない
		# ・フォロワーではない
		# ・ブロック検出中
		# ・監視ユーザではない
		# ・リムーブ候補中
		# ・疑似リムーブ中
		if wARR_DBData['vipuser']==True :
			wStr = "〇VIPユーザ"
			CLS_OSIF.sPrn( wStr )
		else :
			if wARR_DBData['rc_myfollow']==False or \
			   wARR_DBData['rc_follower']==False or \
			   wARR_DBData['rc_blockby']==True or \
			   wARR_DBData['adm_agent']==False or \
			   wARR_DBData['limited']==True or \
			   wARR_DBData['removed']==True :
				# 正常として返す	
				wRes['Result'] = True
				return wRes
		
		#############################
		# 期間内であれば除外
		wGetLag = CLS_OSIF.sTimeLag( str(wARR_DBData['favo_date']), inThreshold=gVal.DEF_STR_TLNUM['forFavoriteSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			### 1日以内は除外
			wStr = "▼直近いいね済みなのでスキップします: 前回いいね日=" + str(wARR_DBData['favo_date']) + '\n'
			CLS_OSIF.sPrn( wStr )
			# 正常として返す
			wRes['Result'] = True
			return wRes
		
		#############################
		# 完了
		wRes['Responce']['Target'] = True
		wRes['Result'] = True
		return wRes



#####################################################
# いいね処理
#####################################################
	def FavoFavorite( self, inID, inARR_DBData, inARR_DBFavoID, inFLG_ForceFavo=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "FavoFavorite"
		
		#############################
		# ユーザの直近のツイートを取得
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
			 inID=inID, inCount=gVal.DEF_STR_TLNUM['favoTweetLine'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: @" + inARR_DBData['screen_name']
			gVal.OBJ_L.Log( "B", wRes )
			self.__FavoFailedMemo( inARR_DBData )
			return wRes
		if len(wTweetRes['Responce'])==0 :
			wStr = "▼処理するツイートがないためスキップします: 前回いいね日=" + str(inARR_DBData['favo_date']) + '\n'
			CLS_OSIF.sPrn( wStr )
			self.__FavoFailedMemo( inARR_DBData )
			wRes['Result'] = True
			return wRes
		
		wRIPcnt = 0
		#############################
		# いいねするツイートIDを取得する
		wFavoID = None
		for wTweet in wTweetRes['Responce'] :
			### 前回いいねしたIDは除外
			if inARR_DBData['favo_id']==str(wTweet['id']) :
				break	#これが最過去？なのでループ停止する
			
			### いいね済みのツイートは除外
			if str(wTweet['id']) in inARR_DBFavoID :
				continue
			
			### リプライは除外
			if wTweet['in_reply_to_status_id']!=None :
				continue
			
			### リツイートは除外
			if "retweeted_status" in wTweet :
				###連続リツイート上限越えはメモ
				self.__FavoRetweetMemo( inARR_DBData, wRIPcnt )
				continue
			### 引用リツイートは除外
			if "quoted_status" in wTweet :
				###連続リツイート上限越えはメモ
				self.__FavoRetweetMemo( inARR_DBData, wRIPcnt )
				continue
			
			wRIPcnt = 0
			### リプライは除外(ツイートの先頭が @文字=リプライ)
			if wTweet['text'].find("@")==0 :
				continue
			
			### 文字数不足は除外
			if len(wTweet['text'])<20 :
				continue
			###ツイートに除外文字が含まれている場合は除外
			if self.OBJ_Parent.CheckExcWord( wTweet['text'] )==False :
				continue
			
			###日時の変換
			wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
			if wTime['Result']!=True :
				wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweet['created_at'])
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wTweet['created_at'] = wTime['TimeDate']
			
			### 範囲時間内のツイートか
			wGetLag = CLS_OSIF.sTimeLag( str(wTweet['created_at']), inThreshold=gVal.DEF_STR_TLNUM['forFavoritePeriodSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wGetLag['Beyond']==True :
				### 1日超経過
				if inFLG_ForceFavo==True :
					wStr = "▽期間を過ぎたツイートですがいいねします" + '\n'
					CLS_OSIF.sPrn( wStr )
				else :
					continue	#スキップ
			
			### ID決定
			wFavoID = str(wTweet['id'])
			break
		
		###ファボIDを取得したか
		if wFavoID==None :
			self.__FavoFailedMemo( inARR_DBData )
			wStr = "▼いいねするツイートがないためスキップします: 前回いいね日=" + str(inARR_DBData['favo_date']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		# ※いいね確定
		#############################
		# いいね実行
		wFavoRes = gVal.OBJ_Tw_IF.Favo( wFavoID )
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wFavoRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			self.__FavoFailedMemo( inARR_DBData )
			return wRes
		
		###成功
		wStr = "◎いいねしました： @" + inARR_DBData['screen_name'] + '\n'
		wStr = wStr + wTweet['text'] + '\n'
		wStr = wStr + "【ツイート日時: " + str(wTweet['created_at']) + "】" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# DBにいいね追加
		wResDB = gVal.OBJ_DB_IF.InsertFavoData_Tweet( inARR_DBData['id'], wTweet )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wCnt = inARR_DBData['favo_cnt'] + 1
		#############################
		# DBに記録する
		wQuery = "update tbl_follower_data set " + \
					"favo_id = '"   + str(wFavoID) + "', " + \
					"favo_date = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "', " + \
					"favo_cnt = "   + str(wCnt) + " " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + str( inID ) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wFavoID
		wRes['Result'] = True
		return wRes

	#####################################################
	def __FavoFailedMemo( self, inData ):
		
		###ファボ失敗メモ カウントアップ
		wCnt = inData['favo_f_cnt'] + 1
		
		###実行
		wQuery = "update tbl_follower_data set " + \
					"favo_f_cnt = " + str(wCnt) + ", " + \
					"get_agent = True " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + str(inData['id']) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed(__FavoFailedMemo)"
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		return True

	#####################################################
	###連続リツイート上限越えはメモ
	def __FavoRetweetMemo( self, inData, outRIPcnt=0 ):
		pRIPcnt = outRIPcnt
		pRIPcnt += 1
		
		if gVal.DEF_STR_TLNUM['consRetweetLimit']>pRIPcnt :
			return True
		
		### ※上限越え：メモ
		CLS_OSIF.sPrn( "▼連続リツイート上限メモ")
		###リツイート回数メモ カウントアップ
		wCnt = inData['rt_cnt'] + 1
		
		###実行
		wQuery = "update tbl_follower_data set " + \
					"rt_cnt = " + str(wCnt) + ", " + \
					"get_agent = True " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + str(inData['id']) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed(__FavoRetweetMemo)"
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		return True




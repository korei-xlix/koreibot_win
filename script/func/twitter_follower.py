#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 フォロワー監視系
#####################################################

from htmlif import CLS_HTMLIF
from osif import CLS_OSIF
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterFollower():
#####################################################
	OBJ_Parent = ""				#親クラス実体
	
	CHR_GetReactionDate = None
	VAL_ZanNum = 0				#残り処理数(wait)
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
# ユーザ取得（DB and Twitter）
#####################################################
	def Get( self, inFLG_FirstDisp=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "GetUser"
		
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "ユーザ取得中" )
		
		wRes['Responce'] = False
		wUpdate = False
		#############################
		# フォロー一覧 取得
		wFollowRes = gVal.OBJ_Tw_IF.GetFollow()
		if wFollowRes['Result']!=True :
			wRes['Reason'] = "GetFollow is failed: " +  CLS_OSIF.sCatErr( wFollowRes )
			return wRes
		wARR_TwData = wFollowRes['Responce']['Date']
		if wFollowRes['Responce']['Update']==False :
			CLS_OSIF.sPrn( "データは未更新です" )
		
		#############################
		# DBフォロワー一覧 取得
		wSubRes = gVal.OBJ_DB_IF.GetFollowerDataID()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetDBFavo is failed: " + CLS_OSIF.sCatErr( wSubRes )
			return wRes
		wARR_DB_ID = wSubRes['Responce']
		
		wARR_Tw_ID = list( wARR_TwData.keys() )
		
		wCheckedID = []
		#############################
		# Twitter情報とDBをマッチさせる
		for wID in wARR_Tw_ID :
			wID = str( wID )
			wCheckedID.append( wID )
			
			wNewUser = False
			#############################
			# DBに登録されているか
			if gVal.OBJ_DB_IF.CheckFollowerData(wID)==False :
				###登録されていない =新規登録
				wSubRes = gVal.OBJ_DB_IF.InsertFollowerData( wARR_TwData[wID] )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "InsertFollowerData is failed: " + CLS_OSIF.sCatErr( wSubRes )
					return wRes
				
				###※DB登録
				wText = "DBに登録したユーザ: @" + str( wARR_TwData[wID]['screen_name'] )
				gVal.OBJ_L.Log( "U", wRes, wText )
				wNewUser = True
				wUpdate  = True
			
			#############################
			# DBから情報を取得する(1個)
			wSubRes = gVal.OBJ_DB_IF.GetFollowerDataOne( wID )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFollowerDataOne is failed: " + CLS_OSIF.sCatErr( wSubRes )
				return wRes
			wARR_DBData = wSubRes['Responce']
			
			#############################
			# 状態の変更
			
			#############################
			# 状態の変更：フォロー者に対する処理
			wQuery = None
			
			#############################
			# 記録上フォローしたことがない かつ フォロー
			#   =初フォロー
			if wARR_DBData['r_myfollow']==False and \
			   wARR_DBData['rc_myfollow']==False and \
			   wARR_TwData[wID]['myfollow']==True :
				wQuery = "update tbl_follower_data set " + \
							"r_myfollow = True, " + \
							"rc_myfollow = True, " + \
							"foldate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "', " + \
							"name = '" + str( wARR_TwData[wID]['name'] ) + "', " + \
							"screen_name = '" + str( wARR_TwData[wID]['screen_name'] ) + "', " + \
							"lastcount = " + str( wARR_TwData[wID]['statuses_count'] ) + ", " + \
							"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
							"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
							" and id = '" + wID + "' ;"
				
				if wARR_DBData['adm_agent']==True :
					# 自動ミュート
					wTwitterRes = gVal.OBJ_Tw_IF.Mute( wID )
					if wTwitterRes['Result']!=True :
						wRes['Reason'] = "Twitter API Error(Mute): " + wTwitterRes['Reason']
						gVal.OBJ_L.Log( "B", wRes )
				
				###※新規フォロー
				wText = "初回フォローのユーザ: @" + str( wARR_TwData[wID]['screen_name'] )
				gVal.OBJ_L.Log( "U", wRes, wText )
				wUpdate = True
			
			#############################
			# 再フォロー（ユーザ管理などによる）
			if wARR_DBData['r_myfollow']==True and \
			   wARR_DBData['rc_myfollow']==False and \
			   wARR_TwData[wID]['myfollow']==True :
				wQuery = "update tbl_follower_data set " + \
							"r_myfollow = True, " + \
							"rc_myfollow = True, " + \
							"removed = False, " + \
							"foldate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "', " + \
							"name = '" + str( wARR_TwData[wID]['name'] ) + "', " + \
							"screen_name = '" + str( wARR_TwData[wID]['screen_name'] ) + "', " + \
							"lastcount = " + str( wARR_TwData[wID]['statuses_count'] ) + ", " + \
							"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
							"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
							" and id = '" + wID + "' ;"
				
				if wARR_DBData['adm_agent']==True :
					# 自動ミュート
					wTwitterRes = gVal.OBJ_Tw_IF.Mute( wID )
					if wTwitterRes['Result']!=True :
						wRes['Reason'] = "Twitter API Error(Mute): " + wTwitterRes['Reason']
						gVal.OBJ_L.Log( "B", wRes )
				
				###※再フォロー
				wText = "再フォローのユーザ: @" + str( wARR_TwData[wID]['screen_name'] )
				gVal.OBJ_L.Log( "U", wRes, wText )
				wUpdate = True
			
			#############################
			# リムーブした
			elif wARR_DBData['rc_myfollow']==True and \
			     wARR_TwData[wID]['myfollow']==False :
				wQuery = "update tbl_follower_data set " + \
							"rc_myfollow = False, " + \
							"vipuser = False, " + \
							"name = '" + str( wARR_TwData[wID]['name'] ) + "', " + \
							"screen_name = '" + str( wARR_TwData[wID]['screen_name'] ) + "', " + \
							"lastcount = " + str( wARR_TwData[wID]['statuses_count'] ) + ", " + \
							"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
							"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
							" and id = '" + wID + "' ;"
				
				###※リムーブ
				wText = "リムーブのユーザ: @" + str( wARR_TwData[wID]['screen_name'] )
				gVal.OBJ_L.Log( "U", wRes, wText )
				if wARR_DBData['vipuser']==True :
					wText = "VIP設定が解除された: @" + str( wARR_TwData[wID]['screen_name'] )
					gVal.OBJ_L.Log( "U", wRes, wText )
				wUpdate = True
				#############################
				# トラヒック計測：リムーブフォロー者数
				gVal.STR_TrafficInfo['rem_myfollow'] += 1
			
			if wQuery!=None :
				###実行
				wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
				if wResDB['Result']!=True :
					wRes['Reason'] = "Run Query is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# 状態の変更：フォロワーに対する処理
			wQuery = None
			
			#############################
			# フォローされた
			if wARR_DBData['rc_follower']==False and \
			   wARR_TwData[wID]['follower']==True :
				# 片フォロワーかつ、フォローしたことがない、かつリムーブされたことがなければ
				#   監視を有効にする
				if wARR_TwData[wID]['myfollow']==False and \
				   wARR_TwData[wID]['r_myfollow']==False and \
				   wARR_TwData[wID]['r_remove']==False :
					wQuery = "update tbl_follower_data set " + \
								"adm_agent = True, " + \
								"rc_follower = True, " + \
								"name = '" + str( wARR_TwData[wID]['name'] ) + "', " + \
								"screen_name = '" + str( wARR_TwData[wID]['screen_name'] ) + "', " + \
								"lastcount = " + str( wARR_TwData[wID]['statuses_count'] ) + ", " + \
								"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
								"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
								" and id = '" + wID + "' ;"
					
					CLS_OSIF.sPrn( "監視ON: @" + str(wARR_DBData['screen_name']) )
					
				else:
					wQuery = "update tbl_follower_data set " + \
								"rc_follower = True, " + \
								"name = '" + str( wARR_TwData[wID]['name'] ) + "', " + \
								"screen_name = '" + str( wARR_TwData[wID]['screen_name'] ) + "', " + \
								"lastcount = " + str( wARR_TwData[wID]['statuses_count'] ) + ", " + \
								"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
								"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
								" and id = '" + wID + "' ;"
					
					if wARR_DBData['adm_agent']==True :
						CLS_OSIF.sPrn( "既に監視ONです: @" + str(wARR_DBData['screen_name']) )
				
				###※フォロワー
				wText = "フォロワーのユーザ: @" + str( wARR_TwData[wID]['screen_name'] )
				gVal.OBJ_L.Log( "U", wRes, wText )
				wUpdate = True
				#############################
				# トラヒック計測：フォロワー獲得数
				gVal.STR_TrafficInfo['get_follower'] += 1
			
			#############################
			# リムーブされた
			elif wARR_DBData['rc_follower']==True and \
			     wARR_TwData[wID]['follower']==False :
				wQuery = "update tbl_follower_data set " + \
							"r_remove = True, " + \
							"rc_follower = False, " + \
							"vipuser = False, " + \
							"name = '" + str( wARR_TwData[wID]['name'] ) + "', " + \
							"screen_name = '" + str( wARR_TwData[wID]['screen_name'] ) + "', " + \
							"lastcount = " + str( wARR_TwData[wID]['statuses_count'] ) + ", " + \
							"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
							"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
							" and id = '" + wID + "' ;"
				
				###※リムーブされた
				wText = "リムーブされたユーザ: @" + str( wARR_TwData[wID]['screen_name'] )
				gVal.OBJ_L.Log( "U", wRes, wText )
				
				wUpdate = True
				#############################
				# トラヒック計測：リムーブフォロワー数
				gVal.STR_TrafficInfo['rem_follower'] += 1
			
			#############################
			# 監視対象の片フォローへの対処（フォロー者 かつ フォロワーではない）
			#   フォローしてから一定期間経った場合
			#   =リムーブ（リムーブ候補設定）
			#   ただしVIPは除外する
			elif ( wARR_DBData['rc_myfollow']==True and wARR_DBData['rc_follower']==False ) and \
			     ( wARR_TwData[wID]['myfollow']==True and wARR_TwData[wID]['follower']==False ) and \
			     wARR_DBData['adm_agent']==True and wARR_DBData['vipuser']==False :
				###フォローしてからの時間が範囲外
				wGetLag = CLS_OSIF.sTimeLag( str(wARR_DBData['foldate']), inThreshold=gVal.DEF_STR_TLNUM['forFollowRemSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(41)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外 =自動リムーブ対象
					###  ＝Runでリムーブするユーザ
					wQuery = "update tbl_follower_data set " + \
								"limited = True, " + \
								"name = '" + str( wARR_TwData[wID]['name'] ) + "', " + \
								"screen_name = '" + str( wARR_TwData[wID]['screen_name'] ) + "', " + \
								"lastcount = " + str( wARR_TwData[wID]['statuses_count'] ) + ", " + \
								"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
								"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
								" and id = '" + wID + "' ;"
					
					wText = "リムーブ候補（一定期間内ノーリフォロー）: @" + str( wARR_TwData[wID]['screen_name'] )
					gVal.OBJ_L.Log( "U", wRes, wText )
					wUpdate = True
			
			#############################
			# 監視対象の相互フォローへの対処
			#   フォローしてから一定期間経った場合
			#   非フォロー化ではない場合、
			#     一定期間（短期間）いいねされない場合
			#     =非フォロー化
			#   非フォロー化の場合、
			#     一定期間（長期）いいねされない場合
			#     =疑似リムーブ
			#   ただしVIPは除外する
			elif ( wARR_DBData['rc_myfollow']==True and wARR_DBData['rc_follower']==True ) and \
			     wARR_DBData['adm_agent']==True and wARR_DBData['vipuser']==False :
				###フォローしてからの時間が範囲外
				wGetLag = CLS_OSIF.sTimeLag( str(wARR_DBData['foldate']), inThreshold=gVal.DEF_STR_TLNUM['forFollowRemSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(51)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外 =処理対象
					### 非フォローではない場合
					if wARR_DBData['un_follower']==False :
						###一定期間以上いいねされない（短期間）
						wGetLag = CLS_OSIF.sTimeLag( str(wARR_DBData['r_favo_date']), inThreshold=gVal.DEF_STR_TLNUM['forUnfollowSec'] )
						if wGetLag['Result']!=True :
							wRes['Reason'] = "sTimeLag failed(52)"
							gVal.OBJ_L.Log( "B", wRes )
							return wRes
						if wGetLag['Beyond']==True :
							###期間外 =非フォロー化
							wQuery = "update tbl_follower_data set " + \
										"limited = True, " + \
										"name = '" + str( wARR_TwData[wID]['name'] ) + "', " + \
										"screen_name = '" + str( wARR_TwData[wID]['screen_name'] ) + "', " + \
										"lastcount = " + str( wARR_TwData[wID]['statuses_count'] ) + ", " + \
										"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
										"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
										" and id = '" + wID + "' ;"
							
							wText = "リムーブ候補（非フォロー化）: @" + str( wARR_TwData[wID]['screen_name'] )
							gVal.OBJ_L.Log( "U", wRes, wText )
							wUpdate = True
					
					### 非フォロー化の場合
					else :
						# 一定期間以上いいねされない（長期間）場合、
						# かつ 疑似リムーブでない場合
						#   =疑似リムーブする
						if wARR_DBData['removed']==False :
							wGetLag = CLS_OSIF.sTimeLag( str(wARR_DBData['r_favo_date']), inThreshold=gVal.DEF_STR_TLNUM['forSoftRemSec'] )
							if wGetLag['Result']!=True :
								wRes['Reason'] = "sTimeLag failed(53)"
								gVal.OBJ_L.Log( "B", wRes )
								return wRes
							if wGetLag['Beyond']==True :
								###期間外 =疑似リムーブ
								wQuery = "update tbl_follower_data set " + \
											"limited = True, " + \
											"name = '" + str( wARR_TwData[wID]['name'] ) + "', " + \
											"screen_name = '" + str( wARR_TwData[wID]['screen_name'] ) + "', " + \
											"lastcount = " + str( wARR_TwData[wID]['statuses_count'] ) + ", " + \
											"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
											"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
											" and id = '" + wID + "' ;"
								
								wText = "疑似リムーブ（長期間ノーリアクション）: @" + str( wARR_TwData[wID]['screen_name'] )
								gVal.OBJ_L.Log( "U", wRes, wText )
								
								wUpdate = True
			
			#############################
			# 片フォロワー（疑似リムーブ・監視外含む）かつ長期間ノーリアクションの場合
			#  =疑似リムーブする
			#   ただしVIPは除外する
			elif ( wARR_DBData['rc_myfollow']==False and wARR_DBData['rc_follower']==True ) and \
			     ( wARR_TwData[wID]['myfollow']==False and wARR_TwData[wID]['follower']==True ) and \
			     wARR_DBData['vipuser']==False :
				###フォローしてからの時間が範囲外
				wGetLag = CLS_OSIF.sTimeLag( str(wARR_DBData['foldate']), inThreshold=gVal.DEF_STR_TLNUM['forSoftRemSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(59)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外の場合
					###一定期間ノーリアクションの場合
					wGetLag = CLS_OSIF.sTimeLag( str(wARR_DBData['r_favo_date']), inThreshold=gVal.DEF_STR_TLNUM['forSoftRemSec'] )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed(59)"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
					if wGetLag['Beyond']==True :
						###期間外 =疑似リムーブ
						wQuery = "update tbl_follower_data set " + \
									"limited = True, " + \
									"name = '" + str( wARR_TwData[wID]['name'] ) + "', " + \
									"screen_name = '" + str( wARR_TwData[wID]['screen_name'] ) + "', " + \
									"lastcount = " + str( wARR_TwData[wID]['statuses_count'] ) + ", " + \
									"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
									"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
									" and id = '" + wID + "' ;"
						
						wText = "●長期間ノーリアクションの片フォロワー: @" + str( wARR_TwData[wID]['screen_name'] )
						gVal.OBJ_L.Log( "U", wRes, wText )
						wUpdate = True
			
			### 更新がなければスキップ
			elif wARR_DBData['lastcount']==wARR_TwData[wID]['statuses_count'] :
				continue
			
			if wQuery==None :
				wQuery = "update tbl_follower_data set " + \
							"name = '" + str( wARR_TwData[wID]['name'] ) + "', " + \
							"screen_name = '" + str( wARR_TwData[wID]['screen_name'] ) + "', " + \
							"lastcount = " + str( wARR_TwData[wID]['statuses_count'] ) + ", " + \
							"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
							"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
							" and id = '" + wID + "' ;"
			
			###実行
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# Twitterに情報がない場合
		# ・相互ともリムーブ済み
		# ・ブロックされた
		wARR_FollowerID = gVal.OBJ_DB_IF.GetFollowerDataID_List()
		
		for wID in wARR_FollowerID :
			wID = str( wID )
			
			###Twitterに情報があるならスキップ(既に処理済み)
			if gVal.OBJ_Tw_IF.CheckMyFollow( wID ) :
				continue
			if gVal.OBJ_Tw_IF.CheckFollower( wID ) :
				continue
			###既にチェック済みならスキップ
			if wID in wCheckedID :
				continue
			wCheckedID.append( wID )
			
			#############################
			# DBから情報を取得する(1個)
			wSubRes = gVal.OBJ_DB_IF.GetFollowerDataOne( wID )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFollowerDataOne is failed: " + CLS_OSIF.sCatErr( wSubRes )
				return wRes
			wARR_DBData = wSubRes['Responce']
			
			###相互リムーブ済み
			if wARR_DBData['rc_myfollow']==True and wARR_DBData['rc_follower']==True :
				wQuery = "update tbl_follower_data set " + \
							"r_remove = True, " + \
							"rc_myfollow = False, " + \
							"rc_follower = False, " + \
							"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
							"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
							" and id = '" + wID + "' ;"
				
				###※相互リムーブ済み
				wText = "相互リムーブ済みのユーザ: @" + str( wARR_DBData['screen_name'] )
				gVal.OBJ_L.Log( "U", wRes, wText )
				wUpdate = True
				#############################
				# トラヒック計測：リムーブフォロー者数、リムーブフォロワー数
				gVal.STR_TrafficInfo['rem_myfollow'] += 1
				gVal.STR_TrafficInfo['rem_follower'] += 1
			
			###リムーブした
			elif wARR_DBData['rc_myfollow']==True :
				wQuery = "update tbl_follower_data set " + \
							"rc_myfollow = False, " + \
							"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
							"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
							" and id = '" + wID + "' ;"
				
				###※リムーブ済み
				wText = "リムーブ済みのユーザ: @" + str( wARR_DBData['screen_name'] )
				gVal.OBJ_L.Log( "U", wRes, wText )
				wUpdate = True
				#############################
				# トラヒック計測：リムーブフォロー者数
				gVal.STR_TrafficInfo['rem_myfollow'] += 1
			
			###リムーブされた or ブロックされた
			elif wARR_DBData['rc_follower']==True :
				wQuery = "update tbl_follower_data set " + \
							"r_remove = True, " + \
							"rc_follower = False, " + \
							"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
							"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
							" and id = '" + wID + "' ;"
				
				###※リムーブされた
				wText = "リムーブされたユーザ: @" + str( wARR_DBData['screen_name'] )
				gVal.OBJ_L.Log( "U", wRes, wText )
				wUpdate = True
				#############################
				# トラヒック計測：リムーブフォロワー数
				gVal.STR_TrafficInfo['rem_follower'] += 1
			
			else :
				###対象外
				continue
			
			###実行
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			#############################
			# ブロックチェック
			wUserinfoRes = gVal.OBJ_Tw_IF.GetFollowInfo( wID )
			if wUserinfoRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wUserinfoRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			if wUserinfoRes['Responce']['blocked_by']==True :
				### ブロックされていた
				wQuery = "update tbl_follower_data set " + \
							"rc_blockby = True " + \
							"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
							" and id = '" + str(wID) + "' ;"
				
				wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
				if wResDB['Result']!=True :
					wRes['Reason'] = "Run Query is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				CLS_OSIF.sPrn( "●ブロックを検知: @" + wARR_RateFollowers[wID]['screen_name'] )
				CLS_OSIF.sSleep( 10 )
		
		###ユーザ管理に動きがあるか
		if wUpdate==True :
			wRes['Responce'] = True
		
		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "Twitterユーザ数  : " + str( len(wARR_Tw_ID) )+ '\n'
		wStr = wStr + "DBユーザ数       : " + str( len(wARR_DB_ID) )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# リアクションチェック
#####################################################
	def ReactionCheck_new(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "ReactionCheck_new"
		
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
			# 自動リツイート対象のツイートかチェック
			wRetweetRes = self.OBJ_Parent.DetectAutoRetweet( wTweet['text'] )
			if wRetweetRes['Result']!=True :
				wRes['Reason'] = "DetectAutoRetweet error: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wFLG_AutoRetweet = wRetweetRes['Responce']
			
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
				wReactionRes = self.ReactionUserCheck( wID, wTweet )
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
				wReactionRes = self.ReactionUserCheck( wID, wTweet, wFLG_AutoRetweet, wARR_AutoRetUsers )
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
				wReactionRes = self.ReactionUserCheck( wID, wTweet )
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
			wReactionRes = self.ReactionUserCheck( wID, wSubRes['Responce'][wReplyID] )
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
		# リアクションを反映する
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中：DBチェック" )
		
		#############################
		# DBのフォロワー一覧取得
		# ・監視対象ユーザ
		# ・フォロワー
		# ・自動リムーブ or リムーブ済みではない
		# ・ブロックを検知してない
		wQuery = "select * from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"rc_follower = True and " + \
					"rc_blockby = False and " + \
					"removed = False " + \
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
		wARR_RateFollowers = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		wStr = "データ処理数: " + str(len( wARR_RateFollowers )) + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 自動リムーブ対象を設定する
		wKeylist = list( wARR_RateFollowers.keys() )
		for wID in wKeylist :
			wID = str( wID )
			wScreenName = wARR_RateFollowers[wID]['screen_name']
			
			wStr = "チェック中: @" + wScreenName
			CLS_OSIF.sPrn( wStr )
			wFLG_Remove = False
			
			#############################
			# リアクションありか
			
			#############################
			# =リアクションあり
			if wID in self.ARR_ReacrionUserID :
				#############################
				# 監視対象外のリアクション
				if wARR_RateFollowers[wID]['adm_agent']==False :
					wStr = "●監視対象外のリアクション" + '\n' ;
					CLS_OSIF.sPrn( wStr )
					continue
				
				if wARR_RateFollowers[wID]['vipuser']==False :
					wStr = "〇リアクションあり" + '\n' ;
				else:
					wStr = "▽VIPからのリアクション" + '\n' ;
				CLS_OSIF.sPrn( wStr )
				
				#############################
				# 相互フォロー かつ 非フォローの場合
				#   非フォローを解除する
				if wARR_RateFollowers[wID]['rc_myfollow']==True and \
				   wARR_RateFollowers[wID]['rc_follower']==True and \
				   wARR_RateFollowers[wID]['un_follower']==True :
					
					###前回のいいねが一定期間内の場合
					###  非フォローを解除する
					wGetLag = CLS_OSIF.sTimeLag( str(wARR_RateFollowers[wID]['r_favo_date']), inThreshold=gVal.DEF_STR_TLNUM['forUnfollowRemSec'] )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed(31)"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
					if wGetLag['Beyond']==True :
					###期間外 =リムーブ対象
						wStr = "●前回から期間を過ぎたため非フォロー継続" + '\n'
						CLS_OSIF.sPrn( wStr )
					else :
					###期間内 =非フォロー解除
						if wARR_RateFollowers[wID]['un_fol_lock']==False :
							# 非フォローロックされてなければ非フォロー化解除
							wAddRes = self.OBJ_Parent.SetActiveFollow( wARR_RateFollowers[wID] )
							if wAddRes['Result']!=True :
								wRes['Reason'] = "SetActiveFollow is failed: " + wAddRes['Reason']
								gVal.OBJ_L.Log( "B", wRes )
								continue
						else :
							# 非フォロー化ロックは解除しない
							wStr = "●非フォロー化ロック中のため非フォロー継続" + '\n'
							CLS_OSIF.sPrn( wStr )
				
				#############################
				# 正常
				continue	#次へ
			
			#############################
			# =リアクションなし
			else:
				# 監視対象外はスキップ
				if wARR_RateFollowers[wID]['adm_agent']==False :
					continue	#次へ
				# VIPはスキップ
				if wARR_RateFollowers[wID]['vipuser']==True :
					continue	#次へ
				
				wStr = "●今回はノーリアクション: @" + wScreenName + ": 前回いいね日=" + str(wARR_RateFollowers[wID]['r_favo_date']) + '\n'
				CLS_OSIF.sPrn( wStr )
				
				wFLG_Remove = False
				#############################
				# 相互フォローの場合
				if wARR_RateFollowers[wID]['rc_myfollow']==True :
					#############################
					# しばらく経った非フォロワーの処理
					# 疑似リムーブする
					# ・非フォロワー（ un_follower=True )
					# ・最後のいいね（もしくは登録日）から30日経った
					if wARR_RateFollowers[wID]['un_follower']==True and \
					   wARR_RateFollowers[wID]['limited']==False and \
					   wARR_RateFollowers[wID]['removed']==False :
						### 時間差を計算
						wGetLag = CLS_OSIF.sTimeLag( str(wARR_RateFollowers[wID]['r_favo_date']), inThreshold=gVal.DEF_STR_TLNUM['forSoftRemSec'] )
						if wGetLag['Result']!=True :
							wRes['Reason'] = "sTimeLag failed(2)" + ": @" + wScreenName
							gVal.OBJ_L.Log( "B", wRes )
							continue
						if wGetLag['Beyond']==True :
							###期間外 =30日経った
							wStr = "●30日以上ノーアクションの非フォロワー" + '\n'
							CLS_OSIF.sPrn( wStr )
							wQuery = "update tbl_follower_data set " + \
										"limited = True " + \
										"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
										" and id = '" + str(wID) + "' ;"
							
							wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
							if wResDB['Result']!=True :
								wRes['Reason'] = "Run Query is failed"
								gVal.OBJ_L.Log( "B", wRes )
								return wRes
							continue
					
					#############################
					# 期間内でノーリアクション
					### 既にリムーブ済か、リムーブ候補
					if wARR_RateFollowers[wID]['limited']==True or \
					   wARR_RateFollowers[wID]['removed']==True :
						continue
					### 既に非フォロワー
					if wARR_RateFollowers[wID]['un_follower']==True :
						continue
					
					### フォローしてから一定期間内なら、何もしない
					wGetLag = CLS_OSIF.sTimeLag( str(wARR_RateFollowers[wID]['foldate']), inThreshold=gVal.DEF_STR_TLNUM['forUnfollowSec'] )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed(3)" + ": @" + wScreenName
						gVal.OBJ_L.Log( "B", wRes )
						continue
					if wGetLag['Beyond']==False :
						###期間内 =対象外
						continue
					
					###ファボったことがない場合、何もしない
					if wARR_RateFollowers[wID]['favo_id']==None or wARR_RateFollowers[wID]['favo_date']==None :
						continue
					
					### ファボってから一定期間内かつ
					###   一定期間以上ファボられない場合
					###   非フォロー化
					wGetLag = CLS_OSIF.sTimeLag( str(wARR_RateFollowers[wID]['favo_date']), inThreshold=gVal.DEF_STR_TLNUM['forUnfollowSec'] )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed(4)" + ": @" + wScreenName
						gVal.OBJ_L.Log( "B", wRes )
						continue
					if wGetLag['Beyond']==False :
						###期間内
						wGetLag = CLS_OSIF.sTimeLag( str(wARR_RateFollowers[wID]['r_favo_date']), inThreshold=gVal.DEF_STR_TLNUM['forUnfollowSec'] )
						if wGetLag['Result']!=True :
							wRes['Reason'] = "sTimeLag failed(5)" + ": @" + wScreenName
							gVal.OBJ_L.Log( "B", wRes )
							continue
						if wGetLag['Beyond']==True :
							###期間外 =非フォロー化対象
							wAddRes = self.OBJ_Parent.SetUnfollow( wARR_RateFollowers[wID] )
							if wAddRes['Result']!=True :
								wRes['Reason'] = "SetUnfollow is failed: " + wAddRes['Reason']
								gVal.OBJ_L.Log( "B", wRes )
								return wRes
		
		#############################
		# 自動リツイート処理
		#   処理が有効かつ対象者あり
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "自動リツイート中" )
		
		if len(wARR_AutoRetUsers)>0 :
			wRetweetRes = self.OBJ_Parent.GoAutoRetweet( wARR_AutoRetUsers )
			if wRetweetRes['Result']!=True :
				wRes['Reason'] = "GoAutoRetweet error: "
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		else:
			wStr = "●今回は自動リツイートはありません" + '\n'
			CLS_OSIF.sPrn( wStr )
		
		###現時刻をメモる
		self.CHR_GetReactionDate = str(gVal.STR_SystemInfo['TimeDate'])
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# リアクションユーザチェック
# リアクションの条件：
# ・1ループでリアクション済みユーザはスキップ
# ・DB未登録ユーザは登録される
# ・同じアクションは除外
# ・前のアクションより古ければ除外
# ・以下のステータスは除外
#   リムーブ候補
#   ブロック検知済み
#   フォロワーではない
#####################################################
	def ReactionUserCheck( self, inID, inTweet, inFLG_AutoRetweet=False, outARR_AutoUsers=[] ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "ReactionUserCheck"
		
		wRes['Responce'] = {
			"Reaction" : False,		#リアクション更新済
			"Removed"  : False		#疑似リムーブユーザのアクション
		}
		
		### 自動リツイート対象ユーザリスト(ポインタ)
		pARR_AutoUsers = outARR_AutoUsers
		
		wFLG_Action = True
		#############################
		# リアクション済みのユーザは除外
		if inID in self.ARR_ReacrionUserID :
			wFLG_Action = False	#除外
		
		#############################
		# DBからユーザ情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFollowerDataOne( inID )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFollowerDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録
		if wSubRes['Responce']==None :
			###DBに登録する
			wSetRes = self.OBJ_Parent.InsertNewFollower( inID )
			if wSetRes['Result']!=True :
				###失敗
				wRes['Reason'] = "InsertNewFollower is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			wSubRes = gVal.OBJ_DB_IF.GetFollowerDataOne( inID )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFollowerDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB未登録（ありえない）
			if wSubRes['Responce']==None :
				wRes['Reason'] = "GetFollowerDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wARR_DBData = wSubRes['Responce']
		
		wTweetID = str( inTweet['id'] )
		#############################
		# 同じアクションはノーリアクション
		if wARR_DBData['r_favo_id']==wTweetID :
			wFLG_Action = False	#除外
		
		#############################
		# 前のリアクションより最新なら新アクション
		wSubRes = CLS_OSIF.sCmpTime( inTweet['created_at'], inDstTD=wARR_DBData['r_favo_date'] )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "sCmpTime is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		if wSubRes['Future']==False :
			wFLG_Action = False	#除外
		
		### 以下いずれかは リアクションチェック対象外
		# ・フォロワーではない
		# ・リムーブ候補
		# ・リムーブ済み
		# ・ブロックを検知している
		
		#############################
		# リムーブ候補
		if wARR_DBData['limited']==True and wFLG_Action==True :
			wFLG_Action = False	#除外
		#############################
		# ブロック検知済み
		elif wARR_DBData['rc_blockby']==True and wFLG_Action==True :
			wStr = "●ブロック検知済みユーザのリアクション: " + wARR_DBData['screen_name']
			wFLG_Action = False	#除外
		#############################
		# フォロワーではない
		elif wARR_DBData['rc_follower']==False and wFLG_Action==True :
			### CASE: 過去にリムーブされた
			if wARR_DBData['r_remove']==True :
				wStr = "●過去にリムーブされたユーザのリアクション: " + wARR_DBData['screen_name']
			### CASE: 過去にフォローしたことがある
			elif wARR_DBData['r_myfollow']==True :
				wStr = "●過去のフォローしたことがあるユーザのリアクション: " + wARR_DBData['screen_name']
			### CASE: その他、FF外アクション
			else:
				wStr = "●フォロワーでないユーザのリアクション: " + wARR_DBData['screen_name']
			CLS_OSIF.sPrn( wStr )
			wFLG_Action = False	#除外
			
			#############################
			# リアクションされたのに一定期間リフォローされないので
			#   リムーブ候補にする
			if wARR_DBData['rc_myfollow']==True :
				wGetLag = CLS_OSIF.sTimeLag( str(wARR_DBData['foldate']), inThreshold=gVal.DEF_STR_TLNUM['forFollowRemSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(41)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外 =自動リムーブ対象
					wQuery = "update tbl_follower_data set " + \
								"limited = True, " + \
								"name = '" + str( inTweet['user']['name'] ) + "', " + \
								"screen_name = '" + str( inTweet['user']['screen_name'] ) + "', " + \
								"lastcount = " + str( inTweet['user']['statuses_count'] ) + ", " + \
								"lastdate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "' " + \
								"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
								" and id = '" + wID + "' ;"
					
					wText = "リムーブ候補（リアクションされたのにノーリフォロー）: @" + str( inTweet['user']['screen_name'] )
					gVal.OBJ_L.Log( "U", wRes, wText )
					
					###実行
					wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
					if wResDB['Result']!=True :
						wRes['Reason'] = "Run Query is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
		
		#############################
		# 疑似リムーブのフォロワー
		elif wARR_DBData['removed']==True and wFLG_Action==True :
			wStr = "●疑似リムーブユーザのリアクション: " + wARR_DBData['screen_name']
			CLS_OSIF.sPrn( wStr )
			wFLG_Action = False	#除外
		
		#############################
		# アクション受信として記録（無条件）
		wCnt = wARR_DBData['r_favo_cnt'] + 1
		wWeekCnt = wARR_DBData['week_cnt'] + 1
		
		wQuery = "update tbl_follower_data set " + \
					"r_favo_cnt = " + str( wCnt ) + ", " + \
					"r_favo_id = '" + wTweetID + "', " + \
					"r_favo_date = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "', " + \
					"limited = False, " + \
					"week_cnt = " + str( wWeekCnt ) + " " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + str(inID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# アクションが有効なら、リアクション済みにする
		if wFLG_Action==True :
			#############################
			# リアクション済みID
			self.ARR_ReacrionUserID.append( inID )
			
			#############################
			# トラヒック計測：リアクション獲得数
			gVal.STR_TrafficInfo['get_reaction'] += 1
			
			#############################
			# リアクション済み
			wRes['Responce']['Reaction'] = True
		
		# ※アクションに関係なく実行される
		#############################
		# 以下の場合、自動リツイートを実施
		# ・自動リツイートが有効
		if inFLG_AutoRetweet==True and \
		   wARR_DBData['vipuser']==True :
			pARR_AutoUsers.append( inID )
			
			wStr = "〇自動リツイート対象検出: " + wARR_DBData['screen_name']
			CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# フォロワー情報の表示
#####################################################
	def View( self, inFLGall=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "View"
		
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
		
		#############################
		# ヘッダ表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "保持中のフォロワー情報", False )
		
		wARR_Count = {
			"Follower"  : 0,	#相互フォロー
			"PieFollow" : 0,	#片フォロー者
			"unFollower" : 0,	#非フォロー者
			"Remove"    : 0,	#疑似リムーブ
			"Reader"    : 0,	#片フォロワー
			"Num"       : 0		#表示件数
		}
		wFLG_Follower = False
		
		#############################
		# 情報組み立て
		wKeylist = list( wARR_RateFollowers.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			wFLG_Follower = False
			
			if wARR_RateFollowers[wID]['twitterid']!=gVal.STR_UserInfo['Account'] :
				continue	#自分以外の情報はスキップ
			if wARR_RateFollowers[wID]['adm_agent']==False :
				continue	#監視外はスキップ
			if wARR_RateFollowers[wID]['rc_myfollow']==False and wARR_RateFollowers[wID]['rc_follower']==False :
				continue	#フォロー者でもフォロワーでもなければスキップ
			
			wStr = "ユーザ=" + str(wARR_RateFollowers[wID]['name']) + "(@" + str(wARR_RateFollowers[wID]['screen_name']) + ") "
			
			if wARR_RateFollowers[wID]['rc_myfollow']==True and wARR_RateFollowers[wID]['rc_follower']==True :
				if wARR_RateFollowers[wID]['removed']==True :
					wStr = wStr + " [●疑似リムーブ]"
					wARR_Count['Remove'] += 1
				
				elif wARR_RateFollowers[wID]['un_follower']==True :
					wStr = wStr + " [△非フォロワー]"
					wARR_Count['unFollower'] += 1
				
				else :
					wStr = wStr + " [◎相互フォロー]"
					wARR_Count['Follower'] += 1
					wFLG_Follower = True
			
			elif wARR_RateFollowers[wID]['rc_myfollow']==True and wARR_RateFollowers[wID]['rc_follower']==False :
				wStr = wStr + " [〇片フォロー者]"
				wARR_Count['PieFollow'] += 1
			
			elif wARR_RateFollowers[wID]['rc_myfollow']==False and wARR_RateFollowers[wID]['rc_follower']==True :
				wStr = wStr + " [▲片フォロワー]"
				wARR_Count['Reader'] += 1
			else :
				continue	#条件に合わなければ表示しない
			
			wStr = wStr + '\n'
			
			# 以下の条件の場合、表示スキップ
			# ・全表示ではない
			# ・相互フォローではない
			# ・いいね受信数=0
			if inFLGall==False and wFLG_Follower==False :
				continue
			if wARR_RateFollowers[wID]['r_favo_cnt']<=3 :
				continue
			
			wStr = wStr + "いいねした=" + str(wARR_RateFollowers[wID]['favo_date']) + "(" + str(wARR_RateFollowers[wID]['favo_cnt']) + ")  " 
			wStr = wStr + "いいね受信=" + str(wARR_RateFollowers[wID]['r_favo_date']) + "(" + str(wARR_RateFollowers[wID]['r_favo_cnt']) + ")  " 
			wStr = wStr + '\n'
			
			wStr = wStr + "登録日=" + str(wARR_RateFollowers[wID]['regdate']) + "  ツイート更新日=" + str(wARR_RateFollowers[wID]['lastdate']) + "(" + str(wARR_RateFollowers[wID]['lastcount']) + ")" 
			wStr = wStr + '\n'
			wStr = wStr + "--------------------" + '\n'
			CLS_OSIF.sPrn( wStr )
			wARR_Count['Num'] += 1
		
		#############################
		# 統計
		wStr = "--------------------" + '\n'
		wStr = wStr + "◎相互フォロー   = " + str( wARR_Count['Follower'] ) + '\n'
		wStr = wStr + "〇片フォロー者   = " + str( wARR_Count['PieFollow'] ) + '\n'
		wStr = wStr + "△非フォロー者   = " + str( wARR_Count['unFollower'] ) + '\n'
		wStr = wStr + "●疑似リムーブ   = " + str( wARR_Count['Remove'] ) + '\n'
		wStr = wStr + "▲片フォロワー   = " + str( wARR_Count['Reader'] ) + '\n'
		wStr = wStr + "  表示件数       = " + str( wARR_Count['Num'] ) + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# フォロワー監視の実行
#####################################################
	def Run(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "Run"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "フォロワー監視 実行中" )
		
		#############################
		# DBのフォロワー一覧取得
		# ・自動リムーブ対象
		wQuery = "select * from tbl_follower_data where " + \
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
		wARR_RateFollowers = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_RateFollowers ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		#############################
		# 対象者を処理
		wKeylist = list( wARR_RateFollowers.keys() )
		for wID in wKeylist :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			wID = str( wID )
			
			#############################
			# 片フォロー者
			#   リムーブする
			if wARR_RateFollowers[wID]['rc_myfollow']==True and wARR_RateFollowers[wID]['rc_follower']==False :
				wSubRes = self.OBJ_Parent.RelRemove( wARR_RateFollowers[wID] )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "RelRemove is failed(2): " + wSubRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					continue
			
			#############################
			# 相互フォローで非フォローでない場合
			#   非フォロー化
			elif ( wARR_RateFollowers[wID]['rc_myfollow']==True and wARR_RateFollowers[wID]['rc_follower']==True ) and \
			   wARR_RateFollowers[wID]['un_follower']==False :
				wSubRes = self.OBJ_Parent.SetUnfollow( wARR_RateFollowers[wID] )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SetUnfollow is failed: " + wSubRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# それ以外（片フォロワー）の場合（かつリムーブ候補）
			#   疑似リムーブする
			else :
				wSubRes = self.OBJ_Parent.SoftRemove( wARR_RateFollowers[wID] )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SoftRemove is failed: " + wSubRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					continue
		
		#############################
		# ミュート解除の実行
		# ・フォロー者ではない
		# ・ミュート中
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "ミュート解除 実行" )
		
		wRemoveRes = gVal.OBJ_Tw_IF.AllMuteRemove()
		if wRemoveRes['Result']!=True :
			wRes['Reason'] = "Twitter Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wRemoveRes['Responce']==False :
			CLS_OSIF.sPrn( "ミュート解除対象はありませんでした。" + '\n' )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 被ブロックチェック
#####################################################
	def BlockCheck(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "BlockCheck"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "ブロックチェック中" )
		
		#############################
		# DBのフォロワー一覧取得
		# ・監視対象ユーザ
		# ・フォロー者でもリムーブ者でもない
		# ・一度フォローしたことがある
		# ・ブロックを検知してない
		wQuery = "select * from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"adm_agent = True and " + \
					"rc_myfollow = False and " + \
					"rc_follower = False and " + \
					"r_myfollow = True and " + \
					"rc_blockby = False " + \
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
		wARR_RateFollowers = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		wStr = "データ処理数: " + str(len( wARR_RateFollowers )) + '\n'
		CLS_OSIF.sPrn( wStr )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_RateFollowers ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		#############################
		# ブロックチェック
		wKeylist = list( wARR_RateFollowers.keys() )
		for wID in wKeylist :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			wID = str( wID )
			wScreenName = wARR_RateFollowers[wID]['screen_name']
			
			wStr = "チェック中: @" + wScreenName
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# Twitterからフォロー関係を取得する
			wUserinfoRes = gVal.OBJ_Tw_IF.GetFollowInfo( wID )
			if wUserinfoRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wUserinfoRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			if wUserinfoRes['Responce']['blocked_by']==True :
				### ブロックされていた
				wQuery = "update tbl_follower_data set " + \
							"rc_blockby = True " + \
							"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
							" and id = '" + str(wID) + "' ;"
				
				wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
				if wResDB['Result']!=True :
					wRes['Reason'] = "Run Query is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				CLS_OSIF.sPrn( "●ブロックを検知: @" + wARR_RateFollowers[wID]['screen_name'] )
			
			#############################
			# 正常
			continue	#次へ
		
		#############################
		# DBを再取得
		# ・被ブロック
		wQuery = "select * from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"adm_agent = True and " + \
					"rc_blockby = True " + \
					";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed(2)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		### 添え字をIDに差し替える
		wARR_RateFollowers = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		#############################
		# 被ブロック一覧を表示する
		if len(wARR_RateFollowers)>0 :
			CLS_OSIF.sPrn( "Screen Name | DB登録日 | いいね数 | 被いいね数" )
			
			wKeylist = list( wARR_RateFollowers.keys() )
			for wID in wKeylist :
				wID = str( wID )
				
				wStr = wARR_RateFollowers[wID]['screen_name'] + "  "
				wStr = wStr + str(wARR_RateFollowers[wID]['regdate']) + "  "
				wStr = wStr + str(wARR_RateFollowers[wID]['favo_cnt']) + "  "
				wStr = wStr + str(wARR_RateFollowers[wID]['r_favo_cnt'])
				CLS_OSIF.sPrn( wStr )
		else :
			CLS_OSIF.sPrn( "被ブロックユーザはありません。" )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 今週のトロフィー獲得者
#####################################################
	def TorpyGetter(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "TorpyGetter"
		
		wRes['Responce'] = False
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "今週のトロフィー獲得者" )
		
		#############################
		# DBのフォロワー一覧取得
		# ・監視対象ユーザ
		# ・フォロワー
		# ・自動リムーブ or リムーブ済みではない
		# ・ブロックを検知してない
		wQuery = "select * from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"rc_myfollow = True and " + \
					"rc_follower = True and " + \
					"rc_blockby = False and " + \
					"adm_agent = True and " + \
					"limited = False and " + \
					"removed = False and " + \
					"week_cnt > 0 " + \
					"order by week_cnt desc, r_favo_date desc " + \
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
		wARR_RateFollowers = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		if len( wARR_RateFollowers )==0 :
			CLS_OSIF.sPrn( "今週のトロフィー獲得者はいませんでした" + '\n' )
			wRes['Result'] = True
			return wRes
		
		#############################
		# トロフィー獲得者を選出
		# ・一番大きいカウントを選出。+1ポイント
		# ・同率は全員選出
		wKeylist = list( wARR_RateFollowers.keys() )
		wMostCnt = -1
		wTorpyUserID = []
		wCHR_Kakutoku = ""
		wCHR_KakutokuStr = ""
		for wID in wKeylist :
			wID = str( wID )
			
			###一番目に大きいカウントを選出
			if wMostCnt<wARR_RateFollowers[wID]['week_cnt'] :
				# 大きい場合、リセットして選出
				wTorpyUserID = []
				wTorpyUserID.append( wID )
				wMostCnt = wARR_RateFollowers[wID]['week_cnt']
				continue
			elif wMostCnt==wARR_RateFollowers[wID]['week_cnt'] :
				# 同率の場合、追加選出
				wTorpyUserID.append( wID )
				continue
		
		if len( wTorpyUserID )==0 :
			CLS_OSIF.sPrn( "今週のトロフィー獲得者はいませんでした" + '\n' )
			wRes['Result'] = True
			return wRes
		
		# ※トロフィー獲得者あり
		#############################
		# twitterへ送信する文章を作成する
		# ついで記録を付ける
		for wID in wTorpyUserID :
			wID = str( wID )
			
			###トロフィー獲得者
			wCnt = wARR_RateFollowers[wID]['tor_cnt'] + 1
			###Twitter用文章
			wCHR_Kakutoku = wCHR_Kakutoku + wARR_RateFollowers[wID]['screen_name'] + " (いいね数=" + str(wARR_RateFollowers[wID]['week_cnt']) + ") " + "(優勝数=" + str(wCnt) + "回目)" + '\n'
			###DB登録用文章
			wCHR_KakutokuStr = wCHR_KakutokuStr + wARR_RateFollowers[wID]['screen_name'] + " "
			
			###記録をつける
			wQuery = "update tbl_follower_data set " + \
						"tordate = '" + str(gVal.STR_SystemInfo['TimeDate']) + "', " + \
						"tor_cnt = " + str(wCnt) + " " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + str(wID) + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wRes['Responce'] = True
		#############################
		# twitterへ送信する文章を作成する
		wTweet = "@" + gVal.STR_UserInfo['Account'] + " 今週のトロフィー獲得者" + '\n' + wCHR_Kakutoku
		CLS_OSIF.sPrn( "Tweet: " +  wTweet )
		
		#############################
		# twitterへ送信
		wTwitterRes = gVal.OBJ_Tw_IF.Tweet( wTweet )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Tweet is failed"
			gVal.OBJ_L.Log( "B", wRes )
		
		#############################
		# 今週の記録をリセットする
		wQuery = "update tbl_follower_data set " + \
					"week_cnt = 0 " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' " + \
					";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		gVal.OBJ_L.Log( "U", wRes, "トロフィー獲得者: " + wCHR_KakutokuStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# 自動NEWフォロー
#####################################################
	def AutoNewFollow( self, inViewNum=1 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "AutoNewFollow"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "自動NEWフォロー 実行中" )
		
		#############################
		# DBのフォロワー一覧取得
		# ・フォロー者ではない
		# ・一度もフォローしたことがない
		# ・一度もリムーブされたことがない
		# ・ブロック検知なし
		# 既にフォロワーを優先
		wQuery = "select id,screen_name from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"rc_myfollow = False and " + \
					"r_myfollow = False and " + \
					"r_remove = False and " + \
					"rc_blockby = False " + \
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
		
		### キー作成
		wKeylist = list( wARR_DBData.keys() )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_DBData ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		#############################
		# フォローユーザのプロフを表示していく
		wUserNum = 0
		while True :
			wKeyLen = len( wKeylist )
			if wKeyLen==0 :
				break	#キーがないなった 終わり
			if inViewNum<=wUserNum :
				break	#選定数上限 終わり
			
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止w
			
			#############################
			# ランダム抽出
			#   選定したら消す
			wKey = CLS_OSIF.sGetRand( wKeyLen )
			wID  = wKeylist[wKey]
			wKeylist.remove( wID )
			
			### 既に選出済みIDか
			wSubRes = gVal.OBJ_DB_IF.CheckFollowAgent( wID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "CheckFollowAgent failed"
				gVal.OBJ_L.Log( "C", wRes )
				continue
			if wSubRes['Responce']!=True :
				continue
			
			#############################
			# WEBにプロフを表示する
			wURL = "https://twitter.com/" + wARR_DBData[wID]['screen_name']
			CLS_HTMLIF.sOpenURL( wURL )
			CLS_OSIF.sPrn( "  ○選出: ブラウザで表示しました" )
			
			wUserNum += 1
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# フォローサーチ
#####################################################
	def FollowSearch(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "FollowSearch"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "フォローサーチ中" )
		
		#############################
		# ホームタイムラインを取得
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="home", inFLG_Rep=False, inFLG_Rts=False,
			 inID=gVal.STR_UserInfo['id'], inCount=gVal.DEF_STR_TLNUM['followSearchLine'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetTL"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wTweetNum = len(wTweetRes['Responce'])
		if wTweetNum==0 :
			wRes['Reason'] = "Tweet is not get: me"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 取得ツイートから対象のツイートを選定する
		# ・リプライではない
		# ・いいね数、リツイート数の何れかが一定数以上か
		
		### キー作成
		wKeylist = list( range( len(wTweetRes['Responce']) ) )
		
		wSelTweetNum = 0	# Tweet選定数
		wSelUserNum  = 0	# ユーザ選定数
		wSkipNum     = 0
		wFLG_Break = False
		while True :
			wKeyLen = len( wKeylist )
			if wKeyLen==0 :
				break	#キーがないなった 終わり
			if wFLG_Break==True :
				break	#停止されたら終わり
			if gVal.DEF_STR_TLNUM['fsTweetNum']<=wSelTweetNum :
				break	#選定数上限 終わり
			if gVal.DEF_STR_TLNUM['fsUserNum']<=wSelUserNum :
				break	#選定数上限 終わり
			
			#############################
			# ランダム抽出
			#   選定したら消す
			wKey = CLS_OSIF.sGetRand( wKeyLen )
			wKey = wKeylist[wKey]
			wTweet = wTweetRes['Responce'][wKey]
			wKeylist.remove( wKey )
			
			#############################
			# 選定で使うか判断
			
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
			### いいね数、リツイート数ともに規定以下
			if wTweet['retweet_count']<100 and wTweet['favorite_count']<100 :
				continue
			
			# ※選定確定
			#############################
			# いいね、リツイートしたユーザを抜き出す
			wTweetID = str(wTweet['id'])
			
			wSubRes = gVal.OBJ_Tw_IF.GetLikesLookup( wTweetID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetLikesLookup): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wARR_UserID = list( wSubRes['Responce'] )
			
			wSubRes = gVal.OBJ_Tw_IF.GetRetweetLookup( wTweetID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetRetweetLookup): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wARR_UserID_Retweet = list( wSubRes['Responce'] )
			
			#############################
			# IDをマージする
			for wID in wARR_UserID_Retweet :
				wID = str(wID)
				if wID not in wARR_UserID :
					wARR_UserID.append( wID )
			
			#############################
			# チェック対象のツイート表示
			wUserID  = str(wTweet['user']['id'])
			
			###日時の変換
			wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
			if wTime['Result']!=True :
				wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweet['created_at'])
				gVal.OBJ_L.Log( "B", wRes )
				continue
			wTweet['created_at'] = wTime['TimeDate']
			
			wStr = '\n' + "選定中ツイート" + '\n' ;
			wStr = wStr + "--------------------" + '\n' ;
			wStr = wStr + wTweet['user']['name'] + " (@" + wTweet['user']['screen_name'] + ")" + '\n'
			wStr = wStr + "日時: " + str(wTweet['created_at']) + '\n'
			wStr = wStr + wTweet['text'] + '\n'
			CLS_OSIF.sPrn( wStr )
			
			###ウェイト初期化
			self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_UserID ), inWaitSec=gVal.DEF_STR_TLNUM['followSearchWaitSec'], inZanCount=gVal.DEF_STR_TLNUM['followSearchWaitCount'] )
			
			#############################
			# ユーザの選定
			
			### キー作成
			wKeylist2 = list( range( len(wARR_UserID) ) )
			
			wSkipNum = 0
			while True :
				wKeyLen2 = len( wKeylist2 )
				if wKeyLen2==0 :
					break	#キーがないなった 終わり
				if gVal.DEF_STR_TLNUM['fsUserNum']<=wSelUserNum :
					break	#選定数上限 終わり
				if gVal.DEF_STR_TLNUM['followSearchSkipRange']<=wSkipNum :
					break	#スキップ許容数超え
				
				###ウェイトカウントダウン
				if self.OBJ_Parent.Wait_Next()==False :
					wFLG_Break = True
					break	###ウェイト中止
				
				#############################
				# ランダム抽出
				#   選定したら消す
				wKey2 = CLS_OSIF.sGetRand( wKeyLen2 )
				wKey2 = wKeylist2[wKey2]
				wUserID = wARR_UserID[wKey2]
				wKeylist2.remove( wKey2 )
				
				###自分ならやり直し
				if str(gVal.STR_UserInfo['id'])==wUserID :
					continue
				
				#############################
				# DBからユーザ情報を取得する(1個)
				wSubRes = gVal.OBJ_DB_IF.GetFollowerDataOne( wUserID )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "GetFollowerDataOne is failed"
					gVal.OBJ_L.Log( "B", wRes )
					continue
				if wSubRes['Responce']!=None :
					wARR_DBData = wSubRes['Responce']
					### 条件にあてはまればスキップ
					#   ・既にフォロー者
					#   ・一度フォローしたことがある
					#   ・一度リムーブされたことがある
					#   ・ブロックON
					if wARR_DBData['rc_myfollow']==True or \
					   wARR_DBData['r_myfollow']==True or \
					   wARR_DBData['r_remove']==True or \
					   wARR_DBData['rc_blockby']==True :
						continue
				
				#############################
				# Twitterからユーザ情報取得
				wUserinfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=wUserID )
				if wUserinfoRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wUserinfoRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					continue
				
				wStr = "チェックユーザ: "
				wStr = wStr + wUserinfoRes['Responce']['name'] + " (@" + wUserinfoRes['Responce']['screen_name'] + ")"
				CLS_OSIF.sPrn( wStr )
				#############################
				# 条件による除外
				if wUserinfoRes['Responce']['friends_count']<=50 :
					CLS_OSIF.sPrn( "  除外: フォロー数50人以下" )
					continue
				if wUserinfoRes['Responce']['friends_count']>=500 :
					CLS_OSIF.sPrn( "  除外: フォロー数500人以上" )
					continue
				if wUserinfoRes['Responce']['followers_count']>=500 :
					CLS_OSIF.sPrn( "  除外: フォロワー数=500人以上" )
					continue
				if wUserinfoRes['Responce']['friends_count']>wTweet['user']['followers_count'] :
					CLS_OSIF.sPrn( "  除外: フォロー数よりフォロワーのが少ない" )
					continue
				if wUserinfoRes['Responce']['protected']==True :
					CLS_OSIF.sPrn( "  除外: 鍵垢" )
					continue
				if wUserinfoRes['Responce']['verified']==True :
					CLS_OSIF.sPrn( "  除外: 公式マーク" )
					continue
				if wUserinfoRes['Responce']['description']==None or \
				   wUserinfoRes['Responce']['description']=="" :
					CLS_OSIF.sPrn( "  除外: プロフ未設定" )
					continue
				if self.OBJ_Parent.CheckExcUser( wUserinfoRes['Responce']['description'] )==False :
					CLS_OSIF.sPrn( "  除外: プロフに除外文字あり" )
					continue
				wAliveRes = self.OBJ_Parent.CheckUserAlive( wUserID )
				if wAliveRes['Result']!=True :
					continue
				if wAliveRes['Responce']['Alive']==False :
					###活動低い？
					wSkipNum += 1
					CLS_OSIF.sPrn( "  除外: 活動力が低い" )
					continue
				if wAliveRes['Responce']['Retweet']==True :
					###活動低い？
					wSkipNum += 1
					CLS_OSIF.sPrn( "  除外: リツイート多め" )
					continue
				
				wSkipNum = 0	#確定したらスキップ回数リセット
				# ※確定
				#############################
				# WEBにプロフを表示する
				
				#############################
				# ブラウザ表示
				wURL = "https://twitter.com/" + wUserinfoRes['Responce']['screen_name']
				CLS_HTMLIF.sOpenURL( wURL )
				CLS_OSIF.sPrn( "  ○選出: ブラウザで表示しました" )
				
				#############################
				# DB登録がなければ枠を作る
				if gVal.OBJ_DB_IF.CheckFollowerData(wUserID)==False :
					###登録されていない =新規登録
					wSubRes = gVal.OBJ_DB_IF.InsertFollowerData( wUserinfoRes['Responce'] )
					if wSubRes['Result']!=True :
						###失敗
						wRes['Reason'] = "InsertFollowerData is failed: " + CLS_OSIF.sCatErr( wSubRes )
						continue
					
					###※DB登録
					wQuery = "update tbl_follower_data set " + \
								"adm_agent = True " + \
								"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
								" and id = '" + wUserID + "' ;"
					
					###実行
					wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
					if wResDB['Result']!=True :
						wRes['Reason'] = "Run Query is failed"
						gVal.OBJ_L.Log( "B", wRes )
						continue
					
					wText = "DBに登録したユーザ: @" + str( wUserinfoRes['Responce']['screen_name'] )
					gVal.OBJ_L.Log( "U", wRes, wText )
				
				#############################
				# 次のユーザ選定へ
				wSelUserNum += 1
			
			#############################
			# 次の選定へ
			wSelTweetNum += 1
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes




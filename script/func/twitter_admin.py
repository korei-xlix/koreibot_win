#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 管理系
#####################################################

from osif import CLS_OSIF
from htmlif import CLS_HTMLIF
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterAdmin():
#####################################################
	OBJ_Parent = ""				#親クラス実体

	DEF_VAL_SLEEP = 10			#Twitter処理遅延（秒）

#####################################################
# Init
#####################################################
	def __init__( self, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__init__"
		
		if parentObj==None :
			###親クラス実体の未設定
			wRes['Reason'] = "You have not set the parent class entity for parentObj"
			gVal.OBJ_L.Log( "A", wRes )
			return
		
		self.OBJ_Parent = parentObj
		gVal.STR_UserAdminInfo = self.GetUserAdminInfo()
		return



#####################################################
# ユーザ管理情報 枠取得
#####################################################
	def GetUserAdminInfo( self, inScreenName=None ):
		
		wSTR_UserAdminInfo = {
			"name"				: None,				#Twitterユーザ名(日本語)
			"screen_name"		: inScreenName,		#Twitterアカウント名(英語)
			"id"        		: -1,
			"statuses_count"	: -1,
			
			"DB_exist"			: False,
			
			"DB_r_myfollow"		: False,
			"DB_r_remove"		: False,
			
			"DB_limited"		: False,
			"DB_removed"		: False,
			"DB_unfollow"		: False,
			"DB_unfollock"		: False,
			"DB_vipuser"		: False,
			"DB_admagent"		: False,
			
			"DB_favo_date"		: None,
			"DB_favo_cnt"		: 0,
			"DB_r_favo_date"	: None,
			"DB_r_favo_cnt"		: 0,
			
			"Protect"			: False,
			"MyFollow"			: False,
			"Follower"			: False,
			
			"MyBlock"			: False,
			"Blocked"			: False
		}
		return wSTR_UserAdminInfo



#####################################################
# ユーザ管理
#####################################################
	def UserAdmin(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "UserAdmin"
		
		#############################
		# コンソールを表示
		while True :
			
			gVal.STR_UserAdminInfo['screen_name'] = None
			gVal.STR_UserAdminInfo['id']          = -1
			
			#############################
			# 画面クリア
			CLS_OSIF.sDispClr()
			
			#############################
			# ヘッダ表示
			wStr = "--------------------" + '\n'
			wStr = wStr + " ユーザ管理" + '\n'
			wStr = wStr + "--------------------" + '\n'
			wStr = wStr + "管理をおこないたいユーザのTwitter ID(@なし)を入力してください。" + '\n'
			wStr = wStr + "中止する場合は \q を入力してください" + '\n'
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# 実行の確認
			wTwitterID = CLS_OSIF.sInp( "Twitter ID(@なし)？(\\q=中止)=> " )
			if wTwitterID=="\\q" :
				##キャンセル
				wRes['Result'] = True
				return wRes
			
			#############################
			# 処理中表示
			CLS_OSIF.sPrn( "確認しています。しばらくお待ちください......" )
			
			#############################
			# ユーザ情報を取得する
			wUserinfoRes = self.GetUserInfo( wTwitterID )
			if wUserinfoRes['Result']!=True :
				wRes['Reason'] = "GetUserInfo is failed: " + wUserinfoRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				break
			
			if wUserinfoRes['Responce']==False :
				wStr = "そのユーザは存在しません。: " + wUserinfoRes['Reason'] + '\n'
				CLS_OSIF.sPrn( wStr )
				CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
				continue
			
			#############################
			# 管理の本画面を表示する
			while True :
				wWord = self.__view_UserAdmin()
				
				if wWord=="\\q" :
					###終了
					break
				if wWord=="" :
					###未入力は再度入力
					continue
				
				wResSearch = self.__run_UserAdmin( wWord )
				if wResSearch['Result']!=True :
					### 処理失敗
					continue
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# ユーザ管理 画面表示
	#####################################################
	def __view_UserAdmin(self):
		wResDisp = CLS_MyDisp.sViewDisp( "UserAdminConsole", -1 )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "D", wResDisp )
			return "\\q"	#失敗=強制終了
		
		wWord = CLS_OSIF.sInp( "コマンド？=> " )
		return wWord

	#####################################################
	# ユーザ管理 実行
	#####################################################
	def __run_UserAdmin( self, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_UserAdmin"
		
		#############################
		# コマンド：フォローする
		if inWord=="\\f" :
			wRes = self.__run_Follow()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# コマンド：疑似リムーブ
		elif inWord=="\\r" :
#		if inWord=="\\r" :
			wRes = self.__run_SoftRemove()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# コマンド：リムーブする
		elif inWord=="\\rm" :
			wRes = self.__run_Remove()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# コマンド：関係リセット
		elif inWord=="\\rma" :
			wRes = self.__run_Reset()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# コマンド：非フォロー化
		elif inWord=="\\uf" :
			wRes = self.__run_Unfollow()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# コマンド：非フォローロック
		elif inWord=="\\ufl" :
			wRes = self.__run_UnfollowLock()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# コマンド：解除候補の解除
		elif inWord=="\\ram" :
			wRes = self.__run_RemoveAgentRemove()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# コマンド：VIP設定
		elif inWord=="\\vp" :
			wRes = self.__run_Vipset()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# コマンド：監視設定
		elif inWord=="\\ag" :
			wRes = self.__run_AdmAgent()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# コマンド：SP設定
		elif inWord=="\\sp" :
			wRes = self.__run_Superset()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# コマンド：ブラウザで表示
		elif inWord=="\\v" :
			wRes = self.__view_Profile()
		
		#############################
		# 不明なコマンド
		else :
			CLS_OSIF.sPrn( "不明なコマンドです" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		return wRes



#####################################################
# フォロー実行
#####################################################
	def __run_Follow(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_Follow"
		
		#############################
		# フォローできるか確認する
		
		#############################
		# 既にフォロー済みか
		if gVal.STR_UserAdminInfo['MyFollow']==True :
			CLS_OSIF.sPrn( "既にフォロー済みです" + '\n' )
			return wRes
		
		#############################
		# 鍵アカウント
		if gVal.STR_UserAdminInfo['Protect']==True :
			CLS_OSIF.sPrn( "鍵アカウントのためフォローできません" + '\n' )
			return wRes
		
		#############################
		# ブロック or 被ブロック
		if gVal.STR_UserAdminInfo['MyBlock']==True :
			CLS_OSIF.sPrn( "ブロックしているためフォローできません" + '\n' )
			return wRes
		if gVal.STR_UserAdminInfo['Blocked']==True :
			CLS_OSIF.sPrn( "ブロックされているためフォローできません" + '\n' )
			return wRes
		
		wFLG_r_remove = False
		if gVal.STR_UserAdminInfo['DB_exist']==True :
			#############################
			# フォローしていないが、過去にフォローしたことがある
			if gVal.STR_UserAdminInfo['DB_r_myfollow']==True :
				CLS_OSIF.sPrn( "過去に一度フォローしたことがありますが、フォローしますか？" )
				wResGet = CLS_OSIF.sInp( "(y=Yes / other=No)=> " )
				if wResGet!="y" :
					return wRes
			
			#############################
			# 過去にリムーブされたことがある
			if gVal.STR_UserAdminInfo['DB_r_remove']==True :
				CLS_OSIF.sPrn( "過去に一度リムーブされたことがあります。フォローしますか？" )
				wResGet = CLS_OSIF.sInp( "(y=Yes / other=No)=> " )
				if wResGet!="y" :
					return wRes
				wFLG_r_remove = True
		
		# ※ここまででフォロー確定
		CLS_OSIF.sPrn( "フォロー処理をおこなってます。しばらくお待ちください......" )
		
		#############################
		# フォローする
		wSubRes = self.OBJ_Parent.SetMyFollow( gVal.STR_UserAdminInfo )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetMyFollow is failed: " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 情報反映
		wSubRes = self.GetUserInfo( inScreenName=gVal.STR_UserAdminInfo['screen_name'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetUserInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "フォローが正常終了しました" )
		wRes['Result'] = True
		return wRes



#####################################################
# リムーブ実行
#####################################################
	def __run_Remove(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_Remove"
		
		#############################
		# フォロー中か
		if gVal.STR_UserAdminInfo['MyFollow']!=True :
			CLS_OSIF.sPrn( "そのユーザはフォローしてません" + '\n' )
			return wRes
		
		CLS_OSIF.sPrn( "リムーブ処理をおこなってます。しばらくお待ちください......" )
		#############################
		# リムーブする
		wSubRes = self.OBJ_Parent.RelRemove( gVal.STR_UserAdminInfo )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "RelRemove is failed: " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			###失敗してもDB削除は継続する
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 情報反映
		wSubRes = self.GetUserInfo( inScreenName=gVal.STR_UserAdminInfo['screen_name'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetUserInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "リムーブが正常終了しました" )
		wRes['Result'] = True
		return wRes



#####################################################
# 関係リセット実行
#####################################################
	def __run_Reset(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_Reset"
		
		CLS_OSIF.sPrn( "リムーブ処理をおこなってます。しばらくお待ちください......" )
		#############################
		# ブロック＆リムーブする
		wSubRes = self.OBJ_Parent.BlockRemove( gVal.STR_UserAdminInfo )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "BlockRemove is failed: " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			###失敗してもDB削除は継続する
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 関係解除= DB削除
		if gVal.STR_UserAdminInfo['DB_exist']==True :
			wQuery = "delete from tbl_follower_data " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + str(gVal.STR_UserAdminInfo['id']) + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
		
		#############################
		# 情報反映
		gVal.STR_UserAdminInfo = self.GetUserAdminInfo( inScreenName=gVal.STR_UserAdminInfo['screen_name'] )
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "リムーブが正常終了しました" )
		wRes['Result'] = True
		return wRes



#####################################################
# フォロー解除候補 解除
#####################################################
	def __run_RemoveAgentRemove(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_RemoveAgentRemove"
		
		#############################
		# 設定できるか
		if gVal.STR_UserAdminInfo['DB_limited']==False :
			CLS_OSIF.sPrn( "解除候補でないため設定できません" + '\n' )
			return wRes
		
		#############################
		# 逆設定
		wFLG_Removed = False
		
		#############################
		# DBに記録する
		if gVal.STR_UserAdminInfo['DB_exist']==True :
			###DBに記録あり
			wQuery = "update tbl_follower_data set " + \
						"limited = " + str(wFLG_Removed) + " " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + gVal.STR_UserAdminInfo['id'] + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
		
		else:
			###DBに記録なし
			wRes['Reason'] = "記録がないユーザはリムーブできません。"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 情報反映
		wSubRes = self.GetUserInfo( inScreenName=gVal.STR_UserAdminInfo['screen_name'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetUserInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "解除候補の解除設定が正常終了しました" )
		wRes['Result'] = True
		return wRes



#####################################################
# 疑似リムーブ実行
#####################################################
	def __run_SoftRemove(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_SoftRemove"
		
		#############################
		# 設定できるか
		if gVal.STR_UserAdminInfo['DB_vipuser']==True :
			CLS_OSIF.sPrn( "VIP設定中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_admagent']==False :
			CLS_OSIF.sPrn( "監視設定でないため設定できません" + '\n' )
			return wRes
		
		#############################
		# 逆設定
		if gVal.STR_UserAdminInfo['DB_removed']==False :
			# 疑似リムーブ設定ON
			wFLG_Removed = True
		else:
			# 疑似リムーブ設定OFF
			wFLG_Removed = False
		
		#############################
		# DBに記録する
		if gVal.STR_UserAdminInfo['DB_exist']==True :
			###DBに記録あり
			wQuery = "update tbl_follower_data set " + \
						"removed = " + str(wFLG_Removed) + " " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + gVal.STR_UserAdminInfo['id'] + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
		
		else:
			###DBに記録なし
			wRes['Reason'] = "記録がないユーザはリムーブできません。"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 情報反映
		wSubRes = self.GetUserInfo( inScreenName=gVal.STR_UserAdminInfo['screen_name'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetUserInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "疑似リムーブ設定が正常終了しました" )
		wRes['Result'] = True
		return wRes



#####################################################
# 非フォロー化
#####################################################
	def __run_Unfollow(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_Unfollow"
		
		#############################
		# 設定できるか
		if gVal.STR_UserAdminInfo['MyFollow']!=True or \
		   gVal.STR_UserAdminInfo['Follower']!=True :
			CLS_OSIF.sPrn( "相互フォローでないため設定できません" + '\n' )
			return wRes
		if gVal.STR_UserAdminInfo['DB_removed']==True :
			CLS_OSIF.sPrn( "疑似リムーブ中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_unfollock']==True :
			CLS_OSIF.sPrn( "非フォローロック中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_vipuser']==True :
			CLS_OSIF.sPrn( "VIP設定中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_admagent']==False :
			CLS_OSIF.sPrn( "監視設定でないため設定できません" + '\n' )
			return wRes
		
		#############################
		# 逆設定
		if gVal.STR_UserAdminInfo['DB_unfollow']==False :
			wFLG_Unfollow = True
		else:
			wFLG_Unfollow = False
		
		#############################
		# DBに記録する
		if gVal.STR_UserAdminInfo['DB_exist']==True :
			###DBに記録あり
			wQuery = "update tbl_follower_data set " + \
						"un_follower = " + str(wFLG_Unfollow) + " " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + gVal.STR_UserAdminInfo['id'] + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
		
		else:
			###DBに記録なし
			wRes['Reason'] = "記録がないユーザは設定できません。"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 情報反映
		wSubRes = self.GetUserInfo( inScreenName=gVal.STR_UserAdminInfo['screen_name'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetUserInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "非フォロー設定が正常終了しました" )
		wRes['Result'] = True
		return wRes



#####################################################
# 非フォローロック
#####################################################
	def __run_UnfollowLock(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_UnfollowLock"
		
		#############################
		# 設定できるか
		if gVal.STR_UserAdminInfo['MyFollow']!=True or \
		   gVal.STR_UserAdminInfo['Follower']!=True :
			CLS_OSIF.sPrn( "相互フォローでないため設定できません" + '\n' )
			return wRes
		if gVal.STR_UserAdminInfo['DB_removed']==True :
			CLS_OSIF.sPrn( "疑似リムーブ中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_vipuser']==True :
			CLS_OSIF.sPrn( "VIP設定中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_admagent']==False :
			CLS_OSIF.sPrn( "監視設定でないため設定できません" + '\n' )
			return wRes
		
		#############################
		# 逆設定
		if gVal.STR_UserAdminInfo['DB_unfollock']==False :
			wFLG_Unfollow = True
		else:
			wFLG_Unfollow = False
		
		#############################
		# DBに記録する
		if gVal.STR_UserAdminInfo['DB_exist']==True :
			###DBに記録あり
			wQuery = "update tbl_follower_data set " + \
						"un_follower = " + str(wFLG_Unfollow) + ", " + \
						"un_fol_lock = " + str(wFLG_Unfollow) + " " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + gVal.STR_UserAdminInfo['id'] + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
		
		else:
			###DBに記録なし
			wRes['Reason'] = "記録がないユーザは設定できません。"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 情報反映
		wSubRes = self.GetUserInfo( inScreenName=gVal.STR_UserAdminInfo['screen_name'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetUserInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "非フォローロック設定が正常終了しました" )
		wRes['Result'] = True
		return wRes



#####################################################
# VIP設定実行
#####################################################
	def __run_Vipset(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_Vipset"
		
		#############################
		# 設定できるか
		if gVal.STR_UserAdminInfo['MyFollow']==False :
			CLS_OSIF.sPrn( "フォロー者でないため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_removed']==True :
			CLS_OSIF.sPrn( "疑似リムーブ中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_unfollow']==True :
			CLS_OSIF.sPrn( "非フォロー中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_unfollock']==True :
			CLS_OSIF.sPrn( "非フォローロック中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_admagent']==False :
			CLS_OSIF.sPrn( "監視設定でないため設定できません" + '\n' )
			return wRes
		
		#############################
		# 逆設定
		if gVal.STR_UserAdminInfo['DB_vipuser']==False :
			wFLG_AdmAgent = True
		else:
			wFLG_AdmAgent = False
		
		#############################
		# DBに記録する
		if gVal.STR_UserAdminInfo['DB_exist']==True :
			###DBに記録あり
			wQuery = "update tbl_follower_data set " + \
						"vipuser = " + str(wFLG_AdmAgent) + " " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + gVal.STR_UserAdminInfo['id'] + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
		
		else:
			###DBに記録なし
			wRes['Reason'] = "記録がないユーザは設定できません。"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 情報反映
		wSubRes = self.GetUserInfo( inScreenName=gVal.STR_UserAdminInfo['screen_name'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetUserInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "VIP設定が正常終了しました" )
		wRes['Result'] = True
		return wRes



#####################################################
# 監視設定実行
#####################################################
	def __run_AdmAgent(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_AdmAgent"
		
		#############################
		# 設定できるか
		if gVal.STR_UserAdminInfo['MyFollow']==False and \
		   gVal.STR_UserAdminInfo['Follower']==False :
			CLS_OSIF.sPrn( "フォロー者かフォロワーでないため設定できません" + '\n' )
			return wRes
		
		#############################
		# 逆設定
		if gVal.STR_UserAdminInfo['DB_admagent']==False :
			wFLG_AdmAgent = True
		else:
			wFLG_AdmAgent = False
		
		#############################
		# DBに記録する
		if gVal.STR_UserAdminInfo['DB_exist']==True :
			###DBに記録あり
			wQuery = "update tbl_follower_data set " + \
						"adm_agent = " + str(wFLG_AdmAgent) + " " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + gVal.STR_UserAdminInfo['id'] + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
		
		else:
			###DBに記録なし
			wRes['Reason'] = "記録がないユーザは設定できません。"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 情報反映
		wSubRes = self.GetUserInfo( inScreenName=gVal.STR_UserAdminInfo['screen_name'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetUserInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "監視設定が正常終了しました" )
		wRes['Result'] = True
		return wRes



#####################################################
# 監視/VIP設定実行
#####################################################
	def __run_Superset(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_Superset"
		
		#############################
		# 設定できるか
		if gVal.STR_UserAdminInfo['MyFollow']==False :
			CLS_OSIF.sPrn( "フォロー者でないため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_removed']==True :
			CLS_OSIF.sPrn( "疑似リムーブ中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_unfollow']==True :
			CLS_OSIF.sPrn( "非フォロー中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_unfollock']==True :
			CLS_OSIF.sPrn( "非フォローロック中のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_admagent']==True :
			CLS_OSIF.sPrn( "監視設定のため設定できません" + '\n' )
			return wRes
		
		if gVal.STR_UserAdminInfo['DB_vipuser']==True :
			CLS_OSIF.sPrn( "VIP設定のため設定できません" + '\n' )
			return wRes
		
		#############################
		# 設定
		wFLG_AdmAgent = True
		
		#############################
		# DBに記録する
		if gVal.STR_UserAdminInfo['DB_exist']==True :
			###DBに記録あり
			wQuery = "update tbl_follower_data set " + \
						"vipuser = " + str(wFLG_AdmAgent) + ", " + \
						"adm_agent = " + str(wFLG_AdmAgent) + " " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + gVal.STR_UserAdminInfo['id'] + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
		
		else:
			###DBに記録なし
			wRes['Reason'] = "記録がないユーザは設定できません。"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 情報反映
		wSubRes = self.GetUserInfo( inScreenName=gVal.STR_UserAdminInfo['screen_name'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetUserInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "監視/VIP設定が正常終了しました" )
		wRes['Result'] = True
		return wRes



#####################################################
# ブラウザ表示
#####################################################
	def __view_Profile(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__view_Profile"
		
		#############################
		# ブラウザ表示
		wURL = "https://twitter.com/" + gVal.STR_UserAdminInfo['screen_name']
		CLS_HTMLIF.sOpenURL( wURL )
		
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ情報取得
#####################################################
	def GetUserInfo( self, inScreenName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "GetUserInfo"
		
		wRes['Responce'] = False
		#############################
		# 退避枠初期化
		gVal.STR_UserAdminInfo = self.GetUserAdminInfo()
		
		#############################
		# Twitterからユーザ情報を取得する
		wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=inScreenName )
		if wUserInfoRes['Result']!=True :
			### 404エラーか
			if CLS_OSIF.sRe_Search( "404", wUserInfoRes['Reason'] )!=False :
				### ユーザが存在しない
				wRes['Responce'] = False
				wRes['Reason'] = "Twitterに存在しないユーザ"
				wRes['Result'] = True
				return wRes
			
			wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wUserInfoRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		### IDの取得
		wID = str( wUserInfoRes['Responce']['id'] )
		
		#############################
		# DBからユーザ情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFollowerDataOne( wID )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFollowerDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==None :
			### DBにユーザが存在しない=新規登録
			wSubRes = gVal.OBJ_DB_IF.InsertFollowerData( wUserInfoRes['Responce'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "InsertFollowerData is failed: " + CLS_OSIF.sCatErr( wSubRes )
				return wRes
			
			gVal.OBJ_L.Log( "U", wRes, "DBに登録したユーザ: @" + str( wUserInfoRes['Responce']['screen_name'] ) )
			
			#############################
			# DBから情報を取得する(1個)
			wSubRes = gVal.OBJ_DB_IF.GetFollowerDataOne( wUserInfoRes['Responce']['id'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFollowerDataOne is failed: " + CLS_OSIF.sCatErr( wSubRes )
				return wRes
		
		wARR_DBData = wSubRes['Responce']
		
		#############################
		# Twitterからフォロー関係を取得する
		wFollowInfoRes = gVal.OBJ_Tw_IF.GetFollowInfo( wID )
		if wFollowInfoRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wFollowInfoRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ブロック検知が更新されてたら
		# DBに反映する
		if wARR_DBData['rc_blockby']!=wFollowInfoRes['Responce']['blocked_by'] :
			wQuery = "update tbl_follower_data set " + \
						"rc_blockby = " + str( wFollowInfoRes['Responce']['blocked_by'] ) + " " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + str(wID) + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
		
		#############################
		# 退避に情報を反映する
		
		### Twitter UserInfo
		gVal.STR_UserAdminInfo['screen_name'] = inScreenName
		gVal.STR_UserAdminInfo['name']    = str( wUserInfoRes['Responce']['name'] )
		gVal.STR_UserAdminInfo['id']      = wID
		gVal.STR_UserAdminInfo['statuses_count'] = str(wUserInfoRes['Responce']['statuses_count'])
		gVal.STR_UserAdminInfo['Protect'] = wUserInfoRes['Responce']['protected']
		
		### Twitter Follow
		gVal.STR_UserAdminInfo['MyFollow'] = wFollowInfoRes['Responce']['following']
		gVal.STR_UserAdminInfo['Follower'] = wFollowInfoRes['Responce']['followed_by']
		gVal.STR_UserAdminInfo['MyBlock']  = wFollowInfoRes['Responce']['blocking']
		gVal.STR_UserAdminInfo['Blocked']  = wFollowInfoRes['Responce']['blocked_by']
		
		### DB
		gVal.STR_UserAdminInfo['DB_r_myfollow'] = wARR_DBData['r_myfollow']
		gVal.STR_UserAdminInfo['DB_r_remove']   = wARR_DBData['r_remove']
		gVal.STR_UserAdminInfo['DB_limited']    = wARR_DBData['limited']
		gVal.STR_UserAdminInfo['DB_removed']    = wARR_DBData['removed']
		gVal.STR_UserAdminInfo['DB_unfollow']   = wARR_DBData['un_follower']
		gVal.STR_UserAdminInfo['DB_unfollock']  = wARR_DBData['un_fol_lock']
		gVal.STR_UserAdminInfo['DB_vipuser']    = wARR_DBData['vipuser']
		gVal.STR_UserAdminInfo['DB_admagent']   = wARR_DBData['adm_agent']
		
		if wARR_DBData['favo_id']!=None :
			gVal.STR_UserAdminInfo['DB_favo_date'] = wARR_DBData['favo_date']
			gVal.STR_UserAdminInfo['DB_favo_cnt']  = wARR_DBData['favo_cnt']
		else:
			gVal.STR_UserAdminInfo['DB_favo_date'] = None
			gVal.STR_UserAdminInfo['DB_favo_cnt']  = 0
		
		if wARR_DBData['r_favo_id']!=None :
			gVal.STR_UserAdminInfo['DB_r_favo_date'] = wARR_DBData['r_favo_date']
			gVal.STR_UserAdminInfo['DB_r_favo_cnt']  = wARR_DBData['r_favo_cnt']
		else:
			gVal.STR_UserAdminInfo['DB_r_favo_date'] = None
			gVal.STR_UserAdminInfo['DB_r_favo_cnt']  = 0
		
		gVal.STR_UserAdminInfo['DB_exist'] = True
		
		#############################
		# 正常
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes




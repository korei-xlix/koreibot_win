#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 キーワード抽出
#####################################################

from osif import CLS_OSIF
from htmlif import CLS_HTMLIF
from filectrl import CLS_File
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterKeyword():
#####################################################
	STR_KeywordFavoInfo = None
	ARR_KeywordFavoUser = {}

	OBJ_Parent = ""				#親クラス実体

#####################################################
# Init
#####################################################
	def __init__( self, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterKeyword"
		wRes['Func']  = "__init__"
		
		if parentObj==None :
			###親クラス実体の未設定
			wRes['Reason'] = "You have not set the parent class entity for parentObj"
			gVal.OBJ_L.Log( "A", wRes )
			return
		
		self.OBJ_Parent = parentObj
		self.GetKeywordFavoInfo()
		return



#####################################################
# キーワードいいね情報 枠取得
#####################################################
	def GetKeywordFavoInfo(self):
		
		self.STR_KeywordFavoInfo = {
			"str_keyword"		: None,			# キーワード
			
			"max_searchnum"		: gVal.DEF_STR_TLNUM['KeywordTweetLen'],
			"searchnum"			: 0,
			"usernum"			: 0,
			"now_usernum"		: 0,
			"favo_usernum"		: 0
		}
		return



#####################################################
# キーワードいいね
#####################################################
###	def KeywordFavo(self):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterAdmin"
###		wRes['Func']  = "KeywordFavo"
###		
###		#############################
###		# コンソールを表示
###		while True :
###			
###			#############################
###			# キーワードいいね メイン画面
###			wWord = self.__view_KeywordFavo()
###			
###			if wWord=="\\q" :
###				###終了
###				break
###			if wWord=="" :
###				###未入力は再度入力
###				continue
###			
###			wResSearch = self.__run_KeywordFavo( wWord )
###			if wResSearch['Result']!=True :
###				break
###		
###		wRes['Result'] = True
###		return wRes
###
###	#####################################################
###	# キーワードいいね 画面表示
###	#####################################################
###	def __view_KeywordFavo(self):
###		wResDisp = CLS_MyDisp.sViewDisp( inDisp="KeywordConsole", inIndex=-1, inData=self.STR_KeywordFavoInfo )
###		if wResDisp['Result']==False :
###			gVal.OBJ_L.Log( "D", wResDisp )
###			return "\\q"	#失敗=強制終了
###		
###		wWord = CLS_OSIF.sInp( "コマンド？=> " )
###		return wWord
###
###	#####################################################
###	# キーワードいいね 実行
###	#####################################################
###	def __run_KeywordFavo( self, inWord ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterKeyword"
###		wRes['Func']  = "__run_KeywordFavo"
###		
###		#############################
###		# コマンド：検索実行
###		if inWord=="\\g" :
###			wRes = self.RunKeywordSearchFavo()
###			wRes['Result'] = True
###		
###		#############################
###		# 文字列設定
###		else :
###			self.STR_KeywordFavoInfo['str_keyword'] = str( inWord )
###			CLS_OSIF.sPrn( "文字列を設定しました" + '\n' )
###			wRes['Result'] = True
###		
###		CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
###		return wRes

#####################################################
# キーワードいいね
#####################################################
	def KeywordFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterKeyword"
		wRes['Func']  = "KeywordFavo"
		

#####################################################
# リストいいね設定
#####################################################
	def SetListFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "SetListFavo"
		
		#############################
		# コンソールを表示
		while True :
			
			#############################
			# データ表示
			self.__view_ListFavo()
			
			#############################
			# 実行の確認
			wListNumber = CLS_OSIF.sInp( "コマンド？(\\q=中止)=> " )
			if wListNumber=="\\q" :
				###  設定をセーブして終わる
				wSubRes = gVal.OBJ_DB_IF.SaveListFavo()
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SaveListFavo is failed"
					gVal.OBJ_L.Log( "B", wRes )

				wRes['Result'] = True
				return wRes
			
			#############################
			# コマンド処理
			wCommRes = self.__run_ListFavo( wListNumber )
			if wCommRes['Result']!=True :
				wRes['Reason'] = "__run_ListFavo is failed: " + wCommRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# 画面表示
	#####################################################
	def __view_ListFavo(self):
		
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		wListNum = 1
		wStr = ""
		for wI in wKeylist :
			wStr = wStr + "   : "
			
			### リスト番号
			wListData = wI + 1
			wListData = str(wListData)
			wListNumSpace = 4 - len( wListData )
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + "  "
			
			### 有効/無効
			if gVal.ARR_ListFavo[wI]['valid']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### フォロー者、フォロワーを含める
			if gVal.ARR_ListFavo[wI]['follow']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "    "
			
			### ユーザ名（screen_name）
			wListData = gVal.ARR_ListFavo[wI]['screen_name']
			wListNumSpace = gVal.DEF_SCREEN_NAME_SIZE - len(wListData)
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + ": "
			
			### リスト名
			wListData = gVal.ARR_ListFavo[wI]['list_name']
			wStr = wStr + wListData
			
			wStr = wStr + '\n'
		
		wResDisp = CLS_MyDisp.sViewDisp( inDisp="ListFavoConsole", inIndex=-1, inData=wStr )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "D", wResDisp )
		
		return

	#####################################################
	# コマンド処理
	#####################################################
	def __run_ListFavo( self, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__run_ListFavo"
		
		#############################
		# f: フォロー者反応
		if inWord=="\\f" :
			self.__view_ListFollower()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# チェック
		
		wARR_Comm = str(inWord).split("-")
		wCom = None
		if len(wARR_Comm)==1 :
			wNum = wARR_Comm[0]
			wCom = None
		elif len(wARR_Comm)==2 :
			wNum = wARR_Comm[0]
			wCom = wARR_Comm[1]
		else:
			CLS_OSIF.sPrn( "コマンドの書式が違います" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		### 整数か
		try:
			wNum = int(wNum)
		except ValueError:
			CLS_OSIF.sPrn( "LIST番号が整数ではありません" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		wNum = wNum - 1
		if wNum<0 or len(gVal.ARR_ListFavo)<=wNum :
			CLS_OSIF.sPrn( "LIST番号が範囲外です" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# コマンドの分岐
		
		#############################
		# コマンドなし: 指定の番号のリストの設定変更をする
		if wCom==None :
			if gVal.ARR_ListFavo[wNum]['valid']==True :
				gVal.ARR_ListFavo[wNum]['valid'] = False
			else:
				gVal.ARR_ListFavo[wNum]['valid'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# f: フォロー者、フォロワーを含める ON/OFF
		elif wCom=="f" :
			if gVal.ARR_ListFavo[wNum]['follow']==True :
				gVal.ARR_ListFavo[wNum]['follow'] = False
			else:
				gVal.ARR_ListFavo[wNum]['follow'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# v: リストユーザ表示
		elif wCom=="v" :
			self.__view_ListFavoUser( gVal.ARR_ListFavo[wNum]['list_name'] )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# 範囲外のコマンド
		else:
			CLS_OSIF.sPrn( "コマンドが違います" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# リストユーザ表示
	#####################################################
	def __view_ListFavoUser( self, inListName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__view_ListFavoUser"
		
		#############################
		# リストの取得にあるか確認
		wSubRes = gVal.OBJ_Tw_IF.GetList( inListName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
			wRes['Reason'] = "Twitter List not found: " + inListName
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# Twitterからリストのユーザ一覧を取得
		wSubRes = gVal.OBJ_Tw_IF.GetListMember( inListName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 画面表示
		wSubRes = self.__view_ListFavoUser_Disp( wSubRes['Responce'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "__view_ListFavoUser_Disp is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# フォロー者反応表示
	#####################################################
	def __view_ListFollower(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__view_ListFollower"
		
		#############################
		# Twitterからリストのユーザ一覧を取得
		wARR_FollowerData = gVal.OBJ_Tw_IF.GetFollowerData()
		if len(wARR_FollowerData)==0 :
			wRes['Reason'] = "FollowerData is zero"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 表示するユーザ情報の作成
		#   フォロー者 かつ FAVO送信ありユーザをセット
		wARR_ListUser = {}
		wKeylist = list( wARR_FollowerData.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			if wARR_FollowerData[wID]['myfollow']==False :
				### フォロー者じゃないので除外
				continue
			
			#############################
			# DBからいいね情報を取得する(1個)
			#   
			#   
			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( wID )
			if wDBRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB登録なし
			if wDBRes['Responce']==None :
				### 除外
				continue
			
			if str(wDBRes['Responce']['lfavo_date'])==gVal.OBJ_DB_IF.DEF_TIMEDATE or \
			   wDBRes['Responce']['lfavo_date']==None :
				### リストいいねしてないなら除外
				continue
			
			#############################
			# 対象なのでセット
			wCell = {
				"id"			: wARR_FollowerData[wID]['id'],
				"screen_name"	: wARR_FollowerData[wID]['screen_name']
			}
			wARR_ListUser.update({ wID : wCell })
		
		#############################
		# 相互フォローなし
		if len(wARR_ListUser)==0 :
			CLS_OSIF.sPrn( "相互フォローがありません" + '\n' )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 画面表示
		wSubRes = self.__view_ListFavoUser_Disp( wARR_ListUser )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "__view_ListFavoUser_Disp is failed"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# リスト画面表示
	#####################################################
	def __view_ListFavoUser_Disp( self, inARR_Data ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__view_ListFavoUser_Disp"
		

		#############################
		# ユーザなし
		if len( inARR_Data )==0 :
			CLS_OSIF.sPrn( "リスト登録のユーザはありません" )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# ヘッダの表示
		wStr = "USER NAME                FW者  FW受  FAVO受信(回数/日)   FAVO送信日   最終活動日" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# いいねユーザデータを作成する
		wKeylist = list( inARR_Data.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			wARR_DBData = {
				"favo_cnt"		: 0,
				"now_favo_cnt"	: 0,
				"favo_date"		: gVal.OBJ_DB_IF.DEF_TIMEDATE,
				"lfavo_date"	: gVal.OBJ_DB_IF.DEF_TIMEDATE,
				"update_date"	: gVal.OBJ_DB_IF.DEF_TIMEDATE
			}
			
			#############################
			# タイムラインを取得する
			#   最初の1ツイートの日時を最新の活動日とする
			wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=True,
				 inID=wID, inCount=1 )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: GetTL"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wTweetRes['Responce'])==1 :
				### 最新の活動日時
				
				###日時の変換をして、設定
				wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweetRes['Responce'][0]['created_at'] )
				if wTime['Result']!=True :
					wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweetRes['Responce'][0]['created_at'])
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				wARR_DBData['update_date'] = wTime['TimeDate']
			
			#############################
			# DBからいいね情報を取得する(1個)
			#   
			#   
			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( wID )
			if wDBRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB登録
			if wDBRes['Responce']!=None :
				wARR_DBData['favo_cnt']     = wDBRes['Responce']['favo_cnt']
				wARR_DBData['now_favo_cnt'] = wDBRes['Responce']['now_favo_cnt']
				wARR_DBData['favo_date']  = wDBRes['Responce']['favo_date']
				wARR_DBData['lfavo_date'] = wDBRes['Responce']['lfavo_date']
			
			#############################
			# 表示するデータ組み立て
			wStr = ""
			
			### 名前
			wListNumSpace = gVal.DEF_SCREEN_NAME_SIZE - len(inARR_Data[wID]['screen_name'])
			if wListNumSpace>0 :
				wListData = inARR_Data[wID]['screen_name'] + " " * wListNumSpace
			wStr = wStr + wListData + "  "
			
			### フォロー者
			if gVal.OBJ_Tw_IF.CheckMyFollow( wID )==True :
				wListData = "〇"
			else:
				wListData = "--"
			wStr = wStr + wListData + "    "
			
			### フォロワー
			if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
				wListData = "〇"
			else:
				wListData = "--"
			wStr = wStr + wListData + "    "
			
			### いいね回数
			wListNumSpace = 5 - len( str(wARR_DBData['favo_cnt']) )
			if wListNumSpace>0 :
				wListData = str(wARR_DBData['favo_cnt']) + " " * wListNumSpace
			wStr = wStr + wListData + ": "
			
			### いいね受信日
			if str(wARR_DBData['favo_date'])==gVal.OBJ_DB_IF.DEF_TIMEDATE or \
			   str(wARR_DBData['favo_date'])==None :
				wListData = "----/--/--"
			else:
				wListData = str(wARR_DBData['favo_date']).split(" ")
				wListData = wListData[0]
			wStr = wStr + wListData + "   "
			
			### いいね送信日
			if str(wARR_DBData['lfavo_date'])==gVal.OBJ_DB_IF.DEF_TIMEDATE or \
			   str(wARR_DBData['lfavo_date'])==None :
				wListData = "----/--/--"
			else:
				wListData = str(wARR_DBData['lfavo_date']).split(" ")
				wListData = wListData[0]
			wStr = wStr + wListData + "   "
			
			### 最終活動日
			if str(wARR_DBData['update_date'])==gVal.OBJ_DB_IF.DEF_TIMEDATE :
				wListData = "----/--/--"
			else:
				wListData = str(wARR_DBData['update_date']).split(" ")
				wListData = wListData[0]
			wStr = wStr + wListData + "   "
			
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 検索実行
#####################################################
	def RunKeywordSearchFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterKeyword"
		wRes['Func']  = "RunKeywordSearchFavo"
		
		#############################
		# 検索文字列が None ではない
		if self.STR_KeywordFavoInfo['str_keyword']==None or \
		   self.STR_KeywordFavoInfo['str_keyword']=="" :
			### ありえない？
			wRes['Reason'] = "str_keyword is None"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		self.STR_KeywordFavoInfo['searchnum'] = 0
		self.STR_KeywordFavoInfo['usernum']      = len( self.ARR_KeywordFavoUser )
		self.STR_KeywordFavoInfo['now_usernum']  = 0
		self.STR_KeywordFavoInfo['favo_usernum'] = 0
		
		CLS_OSIF.sPrn( "ツイートを検索してます。しばらくお待ちください......" )
		#############################
		# ツイートを検索する
		wTweetRes = gVal.OBJ_Tw_IF.GetSearch( 
		   self.STR_KeywordFavoInfo['str_keyword'],
		   inMaxResult=self.STR_KeywordFavoInfo['max_searchnum'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "GetSearch is failed: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		### 抽出ツイート数
		self.STR_KeywordFavoInfo['searchnum'] = len( wTweetRes['Responce'] )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		CLS_OSIF.sPrn( "抽出したツイートをいいねしていきます。しばらくお待ちください......" )
		wFavoNum = 0
		#############################
		# ツイートチェック
		# 以下は除外
		# ・リプライ
		# ・リツイート
		# ・引用リツイート
		# ・規定期間外のツイート
		# 該当なしは いいねしない
		for wTweet in wTweetRes['Responce'] :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			wID     = str( wTweet['id'] )
			wUserID = str( wTweet['user']['id'] )
			#############################
			# キーワードユーザ 追加 and チェック
			wSubRes = self.AddKeywordFavoUser( wTweet )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(Favo): user=" + str(wTweet['user']['screen_name']) + " id=" + str(wID)
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wSubRes['Responce']!=True :
				continue
			
			#############################
			# いいね一覧にあるユーザへは
			# おかえししない
			wResFavoUser = gVal.OBJ_Tw_IF.CheckFavoUser( wUserID )
			if wResFavoUser['Result']!=True :
				wRes['Reason'] = "Twitter Error: CheckFavoUser"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wResFavoUser['Responce']==True :
				### いいね済み
				continue
			
###			wTweetID = str( wTweet['id'] )
			### ノーマル以外は除外
			if wTweet['type']!="normal" :
				continue
			### リプライは除外(ツイートの先頭が @文字=リプライ)
			if wTweet['text'].find("@")==0 :
				continue
			
			#############################
			# 禁止ユーザは除外
###			if wTweet['user']['screen_name'] in gVal.DEF_STR_NOT_REACTION :
			if wTweet['user']['screen_name'] in gVal.ARR_NotReactionUser :
				continue
			
			#############################
			# フォロー者、フォロワーを除外
			if gVal.OBJ_Tw_IF.CheckMyFollow( wUserID)==True or \
			   gVal.OBJ_Tw_IF.CheckFollower( wUserID)==True :
				continue
			
			### 範囲時間内のツイートか
			wGetLag = CLS_OSIF.sTimeLag( str( wTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forKeywordObjectTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				### 規定外
				continue
			
			### ツイートチェック
			wWordRes = self.OBJ_Parent.CheckExtWord( wTweet['user'], wTweet['text'] )
			if wWordRes['Result']!=True :
				wRes['Reason'] = "CheckExtWord failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wWordRes['Responce']==False :
				### 除外
				continue
			
			### ※いいねツイート確定
			#############################
			# いいねする
			wSubRes = gVal.OBJ_Tw_IF.Favo( wID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(Favo): user=" + str(wTweet['user']['screen_name']) + " id=" + str(wID)
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wSubRes['Responce']['Run']!=True :
				continue
			
			self.STR_KeywordFavoInfo['favo_usernum'] += 1
			wFavoNum += 1
			#############################
			# いいね成功
			wStr = '\n' + "--------------------" + '\n' ;
			wStr = wStr + "いいね済み: @" + str(wTweet['user']['screen_name']) + " " + str(wTweet['created_at']) + '\n' ;
			wStr = wStr + wTweet['text'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# ログに記録
			wRes['Reason'] = "〇Run Favorite: user=" + str(wTweet['user']['screen_name']) + " id=" + str(wID)
			gVal.OBJ_L.Log( "T", wRes )
			
			### キーワードユーザ 更新
			wSubRes = self.UpdateKeywordFavoUser( wTweet )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(Favo): user=" + str(wTweet['user']['screen_name']) + " id=" + str(wFavoID)
				gVal.OBJ_L.Log( "B", wRes )
				continue
		
		#############################
		# 正常終了
		wStr = "------------------------------" + '\n'
		wStr = wStr + "検索ツイート数  : " + str( len(wTweetRes['Responce']) )+ '\n'
		wStr = wStr + "いいね実施数    : " + str( wFavoNum )+ '\n'
		wStr = wStr + '\n' + "キーワードいいねが正常終了しました" + '\n'
		CLS_OSIF.sPrn( wStr )
		wRes['Result'] = True
		return wRes

	#####################################################
	# キーワードユーザ 追加
	#####################################################
	def AddKeywordFavoUser( self, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterKeyword"
		wRes['Func']  = "AddKeywordFavoUser"
		
		wID     = str( inTweet['id'] )
		wUserID = str( inTweet['user']['id'] )
		
		wRes['Responce'] = False
		#############################
		# 設定済ユーザなら
		# IDと日時を確認する
		if wUserID in self.ARR_KeywordFavoUser :
			if self.ARR_KeywordFavoUser[wUserID]['id']==None :
				### 未設定なら対象にする
				self.STR_KeywordFavoInfo['now_usernum'] += 1
				wRes['Responce'] = True
				wRes['Result'] = True
				return wRes
			
			if self.ARR_KeywordFavoUser[wUserID]['id']==wID :
				### 同じIDなら対象外
				wRes['Result'] = True
				return wRes
			
			wGetLag = CLS_OSIF.sTimeLag( str( self.ARR_KeywordFavoUser[wUserID]['date'] ), inThreshold=gVal.DEF_STR_TLNUM['forKeywordTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				### 規定外= 今回対象
				self.STR_KeywordFavoInfo['now_usernum'] += 1
				wRes['Responce'] = True
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# 設定なしユーザは
		#   枠を追加する
		wCell = {
			"id"			: None,
			
			"user_id"		: wUserID,
			"screen_name"	: str( inTweet['user']['screen_name'] ),
			"date"			: None
		}
		self.ARR_KeywordFavoUser.update({ wUserID : wCell })
		self.STR_KeywordFavoInfo['usernum']     += 1
		self.STR_KeywordFavoInfo['now_usernum'] += 1
		
		wRes['Responce'] = True		#今回対象
		wRes['Result'] = True
		return wRes

	#####################################################
	# キーワードユーザ 更新
	#####################################################
	def UpdateKeywordFavoUser( self, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterKeyword"
		wRes['Func']  = "UpdateKeywordFavoUser"
		
		wID     = str( inTweet['id'] )
		wUserID = str( inTweet['user']['id'] )
		
		#############################
		# 設定済ユーザか
		if wUserID not in self.ARR_KeywordFavoUser :
			wRes['Reason'] = "unsett user id: " + wUserID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 更新
		self.ARR_KeywordFavoUser[wUserID]['id']   = wID
		self.ARR_KeywordFavoUser[wUserID]['date'] = str(gVal.STR_SystemInfo['TimeDate'])
		
		wRes['Result'] = True
		return wRes



#####################################################
# トレンドツイート
#####################################################
###	def TrendTweet(self):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterKeyword"
###		wRes['Func']  = "TrendTweet"
###		
###		#############################
###		# 取得開始の表示
###		wResDisp = CLS_MyDisp.sViewHeaderDisp( "トレンドツイート 実行中" )
###		
###		#############################
###		# トレンドの取得
###		wTrendRes = gVal.OBJ_Tw_IF.GetTrends()
###		if wTrendRes['Result']!=True :
###			###  失敗
###			wRes['Reason'] = "Twitter Error"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# ヘッダの設定
###		wCHR_TimeDate = str(wTrendRes['Responce']['as_of']).split(" ")
###		wCHR_Time     = wCHR_TimeDate[1].split(":")
###		wCHR_TimeDate = wCHR_TimeDate[0] + " " + wCHR_Time[0] + "時台"
###		
###		wTrendHeader = "Twitterトレンド"
######		wTrendTweet  = wTrendHeader + ": " + str(wTrendRes['Responce']['as_of']) + '\n'
###		wTrendTweet  = wTrendHeader + ": " + wCHR_TimeDate + '\n'
###		
###		#############################
###		# トレンドの表示
###		# ・10位までは取得
###		# ・11位以降は volume>0 以上は取得
###		# ・プロモは除外
###		wStr =        "現在のトレンド" + '\n'
###		wStr = wStr + "------------------------"
###		CLS_OSIF.sPrn( wStr )
###		
###		### トレンドタグの設定
###		wTrendTag = ""
###		if gVal.STR_UserInfo['TrendTag']!="" and \
###		   gVal.STR_UserInfo['TrendTag']!=None :
###			wTrendTag = '\n' + "#" + gVal.STR_UserInfo['TrendTag']
###		
###		wARR_Trend = wTrendRes['Responce']['trends']
###		wStr  = ""
###		wJuni = 0
######		wKeylist = list( wARR_Trend )
###		wKeylist = list( wARR_Trend.keys() )
###		for wIndex in wKeylist :
###			if wARR_Trend[wIndex]['promoted_content']!=None :
###				# プロモは除外
###				continue
###			wJuni += 1
###			if wJuni>10 :
###				if wARR_Trend[wIndex]['tweet_volume']==None :
###					# 11位以降、ボリュームなしは除外
###					continue
###			
###			wWord = str( wARR_Trend[wIndex]['name'] )
###			### タグがなければ追加する
###			if wWord.find("#")!=0 :
###				wWord = "#" + wWord
###			wLine = str(wJuni) + " : " + wWord
###			wStr = wStr + wLine
###			if ( len( wTrendTweet ) + len( wLine ) + len( wTrendTag ) )<140 :
###				wTrendTweet = wTrendTweet + wLine + '\n'
###			if wARR_Trend[wIndex]['tweet_volume']!=None :
###				wStr = wStr + " [" + str(wARR_Trend[wIndex]['tweet_volume']) + "]"
###			wStr = wStr + '\n'
###		
###		wTrendTweet = wTrendTweet + wTrendTag
###		if wStr!="" :
###			CLS_OSIF.sPrn( wStr )
###		
###		#############################
###		# 前のトレンドツイートを消す
###		
###		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
###			 inID=gVal.STR_UserInfo['id'], inCount=gVal.DEF_STR_TLNUM['favoTweetLine'] )
###		if wTweetRes['Result']!=True :
###			wRes['Reason'] = "Twitter Error: GetTL"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		if len(wTweetRes['Responce'])>0 :
###			for wTweet in wTweetRes['Responce'] :
###				wID = str(wTweet['id'])
###				
###				if wTweet['text'].find( wTrendHeader )==0 :
###					###日時の変換
###					wTime = CLS_OSIF.sGetTimeformat_Twitter( wTweet['created_at'] )
###					if wTime['Result']!=True :
###						wRes['Reason'] = "sGetTimeformat_Twitter is failed(1): " + str(wTweet['created_at'])
###						gVal.OBJ_L.Log( "B", wRes )
###						continue
###					wTweet['created_at'] = wTime['TimeDate']
###					
###					#############################
###					# ツイートチェック
###					wSubRes = self.OBJ_Parent.ReactionTweetCheck( wTweet )
###					if wSubRes['Result']!=True :
###						wRes['Reason'] = "ReactionTweetCheck"
###						gVal.OBJ_L.Log( "B", wRes )
###						continue
###					
###					wTweetRes = gVal.OBJ_Tw_IF.DelTweet( wID )
###					if wTweetRes['Result']!=True :
###						wRes['Reason'] = "Twitter API Error(2): " + wTweetRes['Reason'] + " id=" + str(wID)
###						gVal.OBJ_L.Log( "B", wRes )
###					else:
###						wStr = "トレンドツイートを削除しました。" + '\n'
###						wStr = wStr + "------------------------" + '\n'
###						wStr = wStr + wTweet['text'] + '\n'
###						CLS_OSIF.sPrn( wStr )
###		
###		#############################
###		# ツイートする
###		wTweetRes = gVal.OBJ_Tw_IF.Tweet( wTrendTweet )
###		if wTweetRes['Result']!=True :
###			wRes['Reason'] = "Twitter API Error(3): " + wTweetRes['Reason']
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# 送信完了
###		wStr = "トレンドを送信しました。" + '\n'
###		wStr = wStr + "------------------------" + '\n'
###		wStr = wStr + wTrendTweet + '\n'
###		CLS_OSIF.sPrn( wStr )
###		
###
###
###
###		#############################
###		# 正常終了
###		wRes['Result'] = True
###		return wRes
###
###
###


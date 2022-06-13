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
###			"str_keyword"		: None,			# キーワード
###			
			"max_searchnum"		: gVal.DEF_STR_TLNUM['KeywordTweetLen'],
			"searchnum"			: 0,
			"usernum"			: 0,
			"now_usernum"		: 0,
			"favo_usernum"		: 0,
			"list_data"			: ""
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
		
		#############################
		# コンソールを表示
		while True :
			
			#############################
			# データ表示
			self.__view_KeywordFavo()
			
			#############################
			# 実行の確認
			wListNumber = CLS_OSIF.sInp( "コマンド？(\\q=中止)=> " )
			if wListNumber=="\\q" :
				wRes['Result'] = True
				return wRes
			
			#############################
			# コマンド処理
			wCommRes = self.__run_KeywordFavo( wListNumber )
			if wCommRes['Result']!=True :
				wRes['Reason'] = "__run_ListFavo is failed: " + wCommRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# 画面表示
	#####################################################
	def __view_KeywordFavo(self):
		
		wKeylist = list( gVal.ARR_SearchData.keys() )
		wStr = ""
		for wI in wKeylist :
			wStr = wStr + "   : "
			
			### リスト番号
			wListData = str(gVal.ARR_SearchData[wI]['id'])
			wListNumSpace = 4 - len( wListData )
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + ": "
			
			### ヒットツイート数
			wListData = str(gVal.ARR_SearchData[wI]['hit_cnt'])
			wListNumSpace = 6 - len( wListData )
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + ": "
			
			### いいね数
			wListData = str(gVal.ARR_SearchData[wI]['favo_cnt'])
			wListNumSpace = 6 - len( wListData )
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + " "
			
			### 有効/無効
			if gVal.ARR_SearchData[wI]['valid']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### 検索ワード
			wListData = gVal.ARR_SearchData[wI]['word']
			wStr = wStr + wListData + '\n'
		
		self.STR_KeywordFavoInfo['list_data'] = wStr
		
		wResDisp = CLS_MyDisp.sViewDisp( inDisp="KeywordConsole", inIndex=-1, inData=self.STR_KeywordFavoInfo )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "D", wResDisp )
		
		return

	#####################################################
	# コマンド処理
	#####################################################
	def __run_KeywordFavo( self, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__run_ListFavo"
		
		#############################
		# g: 検索実行
		if inWord=="\\g" :
			self.RunKeywordSearchFavo()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# s: 検索ワード追加
		elif inWord=="\\s" :
			self.__set_KeywordFavo()
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# r: 全カウンタクリア
		elif inWord=="\\r" :
			self.__clear_KeywordFavo()
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
		
		#############################
		# リストのインデックス
		wNum = str(wNum)
		wKeylist = list( gVal.ARR_SearchData.keys() )
		wGetIndex = None
		for wIndex in wKeylist :
			if gVal.ARR_SearchData[wIndex]['id']==wNum :
				wGetIndex = str(wIndex)
				break
		
		if wGetIndex==None :
			CLS_OSIF.sPrn( "LIST番号が範囲外です" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# コマンドの分岐
		
		#############################
		# コマンドなし: 指定の番号のリストの設定変更をする
		if wCom==None :
			self.__valid_KeywordFavo( wGetIndex )
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# c: 検索ワード変更
		elif wCom=="c" :
			self.__change_KeywordFavo( wGetIndex )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# d: 検索ワード削除
		elif wCom=="d" :
			self.__delete_KeywordFavo( wGetIndex )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
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
	# 検索ワード追加
	#####################################################
	def __set_KeywordFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__set_KeywordFavo"
		
		#############################
		# コンソールを表示
		while True :
			
			#############################
			# 実行の確認
			wWord = CLS_OSIF.sInp( "検索ワード？(\\q=中止)=> " )
			if wWord=="\\q" :
				wRes['Result'] = True
				return wRes
			
			if wWord!="" :
				### 文字列あり= 入力完了
				break
		
		#############################
		# 実行の確認
		wSubRes = gVal.OBJ_DB_IF.SetSearchWord( wWord )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "SetSearchWord is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wStr = "〇検索ワードを登録: word=" + wWord
		CLS_OSIF.sInp( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# 全カウンタクリア
	#####################################################
	def __clear_KeywordFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__clear_KeywordFavo"
		
		#############################
		# コンソールを表示
		
		wWord = CLS_OSIF.sInp( "全カウンタをクリアします(\\y=YES / other=中止)=> " )
		if wWord!="y" :
			wRes['Result'] = True
			return wRes
		
		#############################
		# 実行の確認
		wSubRes = gVal.OBJ_DB_IF.ClearSearchWord()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "ClearSearchWord is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wStr = "全カウンタをクリアしました"
		CLS_OSIF.sInp( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# 検索ワード 有効/無効
	#####################################################
	def __valid_KeywordFavo( self, inNum ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__valid_KeywordFavo"
		
		#############################
		# 実行の確認
		wSubRes = gVal.OBJ_DB_IF.ValidSearchWord( inNum )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "DeleteSearchWord is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# 検索ワード変更
	#####################################################
	def __change_KeywordFavo( self, inNum ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__change_KeywordFavo"
		
		#############################
		# コンソールを表示
		
		wWord = CLS_OSIF.sInp( "検索ワード？(空欄=中止)=> " )
		if wWord=="" :
			wRes['Result'] = True
			return wRes
		
		#############################
		# 実行の確認
		wSubRes = gVal.OBJ_DB_IF.UpdateSearchWord( inNum, wWord )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "SetSearchWord is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# 検索ワード削除
	#####################################################
	def __delete_KeywordFavo( self, inNum ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__delete_KeywordFavo"
		
		#############################
		# コンソールを表示
		wStr = "検索ワード " + str(gVal.ARR_SearchData[inNum]['word']) + " を削除します"
		CLS_OSIF.sPrn( wStr )
		wWord = CLS_OSIF.sInp( "  \\y=YES / other=中止=> " )
		if wWord!="y" :
			wRes['Result'] = True
			return wRes
		
		#############################
		# 実行の確認
		wSubRes = gVal.OBJ_DB_IF.DeleteSearchWord( inNum )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "DeleteSearchWord is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wStr = "検索ワードを削除しました"
		CLS_OSIF.sInp( wStr )
		
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
		
###		#############################
###		# 検索文字列が None ではない
###		if self.STR_KeywordFavoInfo['str_keyword']==None or \
###		   self.STR_KeywordFavoInfo['str_keyword']=="" :
###			### ありえない？
###			wRes['Reason'] = "str_keyword is None"
###			gVal.OBJ_L.Log( "D", wRes )
###			return wRes
		
		self.STR_KeywordFavoInfo['searchnum'] = 0
		self.STR_KeywordFavoInfo['usernum']      = len( self.ARR_KeywordFavoUser )
		self.STR_KeywordFavoInfo['now_usernum']  = 0
		self.STR_KeywordFavoInfo['favo_usernum'] = 0
		
		CLS_OSIF.sPrn( "抽出したツイートをいいねしていきます。しばらくお待ちください......" )
		#############################
		# 検索実行
		wKeylist = list( gVal.ARR_SearchData.keys() )
		for wIndex in wKeylist :
			if gVal.ARR_SearchData[wIndex]['valid']!=True :
				### 有効じゃなければスキップ
				continue
			
			wSubRes = self.__runKeywordSearchFavo( wIndex )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "RunKeywordSearchFavo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 正常終了
###		wStr = "------------------------------" + '\n'
###		wStr = wStr + "検索ツイート数  : " + str( len(wTweetRes['Responce']) )+ '\n'
###		wStr = wStr + "いいね実施数    : " + str( wFavoNum )+ '\n'
		wStr = '\n' + "キーワードいいねが正常終了しました" + '\n'
		CLS_OSIF.sPrn( wStr )
		wRes['Result'] = True
		return wRes

	#####################################################
	def __runKeywordSearchFavo( self, inIndex ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterKeyword"
		wRes['Func']  = "__runKeywordSearchFavo"
		
		wWord = gVal.ARR_SearchData[inIndex]['word']
		CLS_OSIF.sPrn( "検索中のツイート: word=" + wWord )
		#############################
		# ツイートを検索する
		wTweetRes = gVal.OBJ_Tw_IF.GetSearch( 
		   wWord, inMaxResult=self.STR_KeywordFavoInfo['max_searchnum'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "GetSearch is failed: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		### 抽出ツイート数
###		self.STR_KeywordFavoInfo['searchnum'] = len( wTweetRes['Responce'] )
		wHitCnt = len( wTweetRes['Responce'] )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
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
			
			### ノーマル以外は除外
			if wTweet['type']!="normal" :
				continue
			### リプライは除外(ツイートの先頭が @文字=リプライ)
			if wTweet['text'].find("@")==0 :
				continue
			### センシティブなツイートは除外
			if "possibly_sensitive" in wTweet :
				continue
			
			#############################
			# 禁止ユーザは除外
###			if wTweet['user']['screen_name'] in gVal.ARR_NotReactionUser :
###				continue
			wUserRes = self.OBJ_Parent.CheckExtUser( wTweet['user']['screen_name'], "検索実行中" )
			if wUserRes['Result']!=True :
				wRes['Reason'] = "CheckExtUser failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wUserRes['Responce']==False :
				### 禁止あり=除外
				continue
			
###			#############################
###			# フォロー者、フォロワーを除外
###			if gVal.OBJ_Tw_IF.CheckMyFollow( wUserID)==True or \
###			   gVal.OBJ_Tw_IF.CheckFollower( wUserID)==True :
###				continue
###			
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
###			wRes['Reason'] = "〇Run Favorite: user=" + str(wTweet['user']['screen_name']) + " id=" + str(wID)
###			gVal.OBJ_L.Log( "T", wRes )
			wTextReason = "〇検索いいね実施: user=" + str(wTweet['user']['screen_name']) + " id=" + str(wID)
			gVal.OBJ_L.Log( "T", wRes, wTextReason )
			
			### キーワードユーザ 更新
			wSubRes = self.UpdateKeywordFavoUser( wTweet )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(Favo): user=" + str(wTweet['user']['screen_name']) + " id=" + str(wFavoID)
				gVal.OBJ_L.Log( "B", wRes )
				continue
		
		#############################
		# カウンタを進行
		wSubRes = gVal.OBJ_DB_IF.CountSearchWord( inIndex, inHitCnt=wHitCnt, inFavoCnt=wFavoNum )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "CountSearchWord is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
###		#############################
###		# 正常終了
###		wStr = "------------------------------" + '\n'
###		wStr = wStr + "検索ツイート数  : " + str( len(wTweetRes['Responce']) )+ '\n'
###		wStr = wStr + "いいね実施数    : " + str( wFavoNum )+ '\n'
###		wStr = wStr + '\n' + "キーワードいいねが正常終了しました" + '\n'
###		CLS_OSIF.sPrn( wStr )
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


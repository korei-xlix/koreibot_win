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
	def KeywordFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "KeywordFavo"
		
		#############################
		# コンソールを表示
		while True :
			
			#############################
			# キーワードいいね メイン画面
			wWord = self.__view_KeywordFavo()
			
			if wWord=="\\q" :
				###終了
				break
			if wWord=="" :
				###未入力は再度入力
				continue
			
			wResSearch = self.__run_KeywordFavo( wWord )
			if wResSearch['Result']!=True :
				break
		
		wRes['Result'] = True
		return wRes




	#####################################################
	# キーワードいいね 画面表示
	#####################################################
	def __view_KeywordFavo(self):
		wResDisp = CLS_MyDisp.sViewDisp( inDisp="KeywordConsole", inIndex=-1, inData=self.STR_KeywordFavoInfo )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "D", wResDisp )
			return "\\q"	#失敗=強制終了
		
		wWord = CLS_OSIF.sInp( "コマンド？=> " )
		return wWord

	#####################################################
	# キーワードいいね 実行
	#####################################################
	def __run_KeywordFavo( self, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterKeyword"
		wRes['Func']  = "__run_KeywordFavo"
		
		#############################
		# コマンド：検索実行
		if inWord=="\\g" :
			wRes = self.RunKeywordSearchFavo()
			wRes['Result'] = True
		
		#############################
		# 文字列設定
		else :
			self.STR_KeywordFavoInfo['str_keyword'] = str( inWord )
			CLS_OSIF.sPrn( "文字列を設定しました" + '\n' )
			wRes['Result'] = True
		
		CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
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
			
			wFavoNum += 1
			#############################
			# いいね成功
			wStr = '\n' + "--------------------" + '\n' ;
			wStr = wStr + "いいね済み: @" + str(wTweet['user']['screen_name']) + " " + str(wTweet['created_at']) + '\n' ;
			wStr = wStr + wTweet['text'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
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
	def TrendTweet(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterKeyword"
		wRes['Func']  = "TrendTweet"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "トレンドツイート 実行中" )
		
		#############################
		# トレンドの取得
		wTrendRes = gVal.OBJ_Tw_IF.GetTrends()
		if wTrendRes['Result']!=True :
			###  失敗
			wRes['Reason'] = "Twitter Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ヘッダの設定
		wCHR_TimeDate = str(wTrendRes['Responce']['as_of']).split(" ")
		wCHR_Time     = wCHR_TimeDate[1].split(":")
		wCHR_TimeDate = wCHR_TimeDate[0] + " " + wCHR_Time[0] + "時台"
		
		wTrendHeader = "Twitterトレンド"
###		wTrendTweet  = wTrendHeader + ": " + str(wTrendRes['Responce']['as_of']) + '\n'
		wTrendTweet  = wTrendHeader + ": " + wCHR_TimeDate + '\n'
		
		#############################
		# トレンドの表示
		# ・10位までは取得
		# ・11位以降は volume>0 以上は取得
		# ・プロモは除外
		wStr =        "現在のトレンド" + '\n'
		wStr = wStr + "------------------------"
		CLS_OSIF.sPrn( wStr )
		
		### トレンドタグの設定
		wTrendTag = ""
		if gVal.STR_UserInfo['TrendTag']!="" and \
		   gVal.STR_UserInfo['TrendTag']!=None :
			wTrendTag = '\n' + "#" + gVal.STR_UserInfo['TrendTag']
		
		wARR_Trend = wTrendRes['Responce']['trends']
		wStr  = ""
		wJuni = 0
###		wKeylist = list( wARR_Trend )
		wKeylist = list( wARR_Trend.keys() )
		for wIndex in wKeylist :
			if wARR_Trend[wIndex]['promoted_content']!=None :
				# プロモは除外
				continue
			wJuni += 1
			if wJuni>10 :
				if wARR_Trend[wIndex]['tweet_volume']==None :
					# 11位以降、ボリュームなしは除外
					continue
			
			wWord = str( wARR_Trend[wIndex]['name'] )
			### タグがなければ追加する
			if wWord.find("#")!=0 :
				wWord = "#" + wWord
			wLine = str(wJuni) + " : " + wWord
			wStr = wStr + wLine
			if ( len( wTrendTweet ) + len( wLine ) + len( wTrendTag ) )<140 :
				wTrendTweet = wTrendTweet + wLine + '\n'
			if wARR_Trend[wIndex]['tweet_volume']!=None :
				wStr = wStr + " [" + str(wARR_Trend[wIndex]['tweet_volume']) + "]"
			wStr = wStr + '\n'
		
		wTrendTweet = wTrendTweet + wTrendTag
		if wStr!="" :
			CLS_OSIF.sPrn( wStr )
		
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
				
				if wTweet['text'].find( wTrendHeader )==0 :
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
						continue
					
					wTweetRes = gVal.OBJ_Tw_IF.DelTweet( wID )
					if wTweetRes['Result']!=True :
						wRes['Reason'] = "Twitter API Error(2): " + wTweetRes['Reason'] + " id=" + str(wID)
						gVal.OBJ_L.Log( "B", wRes )
					else:
						wStr = "トレンドツイートを削除しました。" + '\n'
						wStr = wStr + "------------------------" + '\n'
						wStr = wStr + wTweet['text'] + '\n'
						CLS_OSIF.sPrn( wStr )
		
		#############################
		# ツイートする
		wTweetRes = gVal.OBJ_Tw_IF.Tweet( wTrendTweet )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(3): " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 送信完了
		wStr = "トレンドを送信しました。" + '\n'
		wStr = wStr + "------------------------" + '\n'
		wStr = wStr + wTrendTweet + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes




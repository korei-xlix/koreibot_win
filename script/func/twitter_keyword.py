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
		return



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
		wTrendHeader = "Twitterトレンド"
		wTrendTweet  = wTrendHeader + ": " + str(wTrendRes['Responce']['as_of']) + '\n'
		
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
		wKeylist = list( wARR_Trend )
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
###			if ( len( wTrendTweet ) + len( wLine ) )<140 :
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




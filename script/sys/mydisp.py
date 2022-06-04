#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : ディスプレイ表示
#####################################################

from osif import CLS_OSIF
from filectrl import CLS_File
from gval import gVal
#####################################################
class CLS_MyDisp():
#####################################################

#####################################################
# インプリメント処理
#####################################################
	@classmethod
###	def sDispInp( cls, inDisp, inLine, inIndex ):
	def sDispInp( cls, inDisp, inLine, inIndex, inData={} ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MyDisp"
		wRes['Func']  = "sDispInp"
		
		###メイン画面
		if inDisp=="MainConsole" :
			cls.__dispInp_Main( inLine, wRes )
###		###検索モード画面
###		elif inDisp=="SearchConsole" :
###			cls.__dispInp_SearchMode( inLine, inIndex, wRes )
###		###キーユーザ変更画面
###		elif inDisp=="KeyuserConsole" :
###			cls.__dispInp_Keyuser( inLine, wRes )
		###ユーザ管理画面
		elif inDisp=="UserAdminConsole" :
###			cls.__dispInp_UserAdmin( inLine, wRes )
			cls.__dispInp_UserAdmin( inLine, wRes, inData )
###		###自動いいね設定画面
###		elif inDisp=="AutoFavoConsole" :
###			cls.__dispInp_AutoFavo( inLine, wRes )
		###キーワードいいね画面
		elif inDisp=="KeywordConsole" :
			cls.__dispInp_Keyword( inLine, wRes, inData )
		###リストいいね設定画面
		elif inDisp=="ListFavoConsole" :
			cls.__dispInp_ListFavo( inLine, wRes, inData )
		
		return wRes

	#####################################################
	# メイン画面
	@classmethod
	def __dispInp_Main( cls, inLine, outRes ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：ユーザアカウント
		if "[@USER-ACCOUNT@]"==inLine :
			pRes['Responce'] = "Twitter ID : " + gVal.STR_UserInfo['Account']
		
		#############################
		# 正常
		pRes['Result'] = True
		return

###	#####################################################
###	# 検索モード画面
###	@classmethod
###	def __dispInp_SearchMode( cls, inLine, inIndex, outRes ):
###		pRes = outRes
###		#############################
###		# Indexが範囲内かチェック
###		wLen = len(gVal.STR_SearchMode)
###		if inIndex<=-1 and wLen<=inIndex :
###			pRes['Reason'] = "Index is out of range value=" + str(inIndex)
###			return
###		
###		#############################
###		# インプリメント処理
###		
###		###インプリ：検索 画像を含める
###		if "[@SEARCH-IMAGE@]"==inLine :
###			wJPstr = cls.__get_JPstr_Dual( gVal.STR_SearchMode[inIndex]['IncImage'], gVal.STR_SearchMode[inIndex]['ExcImage'] )
###			if wJPstr==None :
###				pRes['Reason'] = "フラグ取り扱い矛盾: 検索に画像を含める Dual flag is True"
###				return
###			pRes['Responce'] = "    検索に画像を含める    [\\i]: " + wJPstr
###		
###		###インプリ：検索 動画を含める
###		elif "[@SEARCH-VIDEO@]"==inLine :
###			wJPstr = cls.__get_JPstr_Dual( gVal.STR_SearchMode[inIndex]['IncVideo'], gVal.STR_SearchMode[inIndex]['ExcVideo'] )
###			if wJPstr==None :
###				pRes['Reason'] = "フラグ取り扱い矛盾: 検索に動画を含める Dual flag is True"
###				return
###			pRes['Responce'] = "    検索に動画を含める    [\\v]: " + wJPstr
###		
###		###インプリ：検索 リンクを含める
###		elif "[@SEARCH-LINK@]"==inLine :
###			wJPstr = cls.__get_JPstr_Dual( gVal.STR_SearchMode[inIndex]['IncLink'], gVal.STR_SearchMode[inIndex]['ExcLink'] )
###			if wJPstr==None :
###				pRes['Reason'] = "フラグ取り扱い矛盾: 検索にリンクを含める Dual flag is True"
###				return
###			pRes['Responce'] = "    検索にリンクを含める  [\\l]: " + wJPstr
###		
###		###インプリ：検索 公式マークのみ
###		elif "[@SEARCH-OFFICIAL@]"==inLine :
###			pRes['Responce'] = "    検索は公式マークのみ  [\\o]: " + cls.__get_JPstr_Single( gVal.STR_SearchMode[inIndex]['OFonly'] )
###		
###		###インプリ：検索 日本語のみ
###		elif "[@SEARCH-JPONLY@]"==inLine :
###			pRes['Responce'] = "    検索は日本語のみ     [\\jp]: " + cls.__get_JPstr_Single( gVal.STR_SearchMode[inIndex]['JPonly'] )
###		
###		###インプリ：検索 リツイート含む
###		elif "[@SEARCH-RT@]"==inLine :
###			pRes['Responce'] = "    リツイート含めない   [\\rt]: " + cls.__get_JPstr_Single( gVal.STR_SearchMode[inIndex]['ExcRT'] )
###		
###		###インプリ：検索 センシティブな内容を含めない
###		elif "[@SEARCH-SENSI@]"==inLine :
###			pRes['Responce'] = "    センシティブを除外   [\\sn]: " + cls.__get_JPstr_Single( gVal.STR_SearchMode[inIndex]['ExcSensi'] )
###		
###		###インプリ：検索 荒らし除去をおこなう
###		elif "[@SEARCH-ARASHI@]"==inLine :
###			pRes['Responce'] = "    荒らし除去           [\\tr]: " + cls.__get_JPstr_Single( gVal.STR_SearchMode[inIndex]['Arashi'] )
###		
###		###インプリ：検索文字
###		elif "[@SEARCH-KEYWORD@]"==inLine :
###			if gVal.STR_SearchMode[inIndex]['Keyword']=="" :
###				pRes['Responce'] = "    検索文字: " + "(未設定)"
###			else:
###				pRes['Responce'] = "    検索文字: " + gVal.STR_SearchMode[inIndex]['Keyword']
###
###		
###		#############################
###		# 正常
###		pRes['Result'] = True
###		return

###	#####################################################
###	# キーユーザ変更画面
###	@classmethod
###	def __dispInp_Keyuser( cls, inLine, outRes ):
###		pRes = outRes
###		#############################
###		# インプリメント処理
###		
###		###インプリ：キーユーザ一覧
###		if "[@KEYUSER-LIST@]"==inLine :
###			wRange = len( gVal.STR_SearchMode )
###			wList = ""
###			wCell = 1
###			for wIndex in range( wRange ) :
###				if gVal.STR_SearchMode[wIndex]['id']==0 :
###					###手動用は表示しない
###					continue
###				
###				wList = wList + "    "
###				if gVal.STR_SearchMode[wIndex]['Choice']==True :
###					wList = wList + "■ "
###				else :
###					wList = wList + "□ "
###				
###				###データ組み立て
###				wList = wList + str(gVal.STR_SearchMode[wIndex]['id']) + ": "
###				wLen = 10 - len( str(gVal.STR_SearchMode[wIndex]['Count']) )
###				wBlank = " " * wLen
###				wList = wList + wBlank + str(gVal.STR_SearchMode[wIndex]['Count']) + "  " + gVal.STR_SearchMode[wIndex]['Keyword']
###				
###				###最終行でなければ改行する
###				if wCell!=wRange :
###					wList = wList + '\n'
###			
###			if wList!="" :
###				###リストの後ろに改行
###				wList = wList + '\n'
###				pRes['Responce'] = wList
###			else:
###				pRes['Responce'] = "    (キーユーザ設定がありません)" + '\n'
###	
###		#############################
###		# 正常
###		pRes['Result'] = True
###		return

	#####################################################
	# ユーザ管理画面
	@classmethod
###	def __dispInp_UserAdmin( cls, inLine, outRes ):
	def __dispInp_UserAdmin( cls, inLine, outRes, inData={} ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：対象ユーザ
		if "[@USERADMIN-TWITTER@]"==inLine :
			pRes['Responce'] = "対象ユーザ  @" + inData['screen_name']
		
		elif "[@USERADMIN-TWITTER-ID@]"==inLine :
			pRes['Responce'] = "ユーザID     " + str(inData['id'])
		
		###インプリ：フォロー者
		elif "[@USERADMIN-MYFOLLOW@]"==inLine :
			if inData['myfollow']==True :
				wStr = "〇はい"
			else:
				wStr = "▼いいえ"
			pRes['Responce'] = "    フォロー中                  : " + wStr
		
		###インプリ：フォロワー
		elif "[@USERADMIN-FOLLOWER@]"==inLine :
			if inData['follower']==True :
				wStr = "〇はい"
			else:
				wStr = "▼いいえ"
			pRes['Responce'] = "    フォロワー                  : " + wStr
		
		###インプリ：鍵アカウント
		elif "[@USERADMIN-PROTECT@]"==inLine :
			if inData['protected']==True :
				wStr = "●はい"
			else:
				wStr = "  いいえ"
			pRes['Responce'] = "    鍵アカウント                : " + wStr
		
		###インプリ：ブロック中
		elif "[@USERADMIN-MYBLOCK@]"==inLine :
			if inData['blocking']==True :
				wStr = "●はい"
			else:
				wStr = "  いいえ"
			pRes['Responce'] = "    ブロック中                  : " + wStr
		
		###インプリ：被ブロック
		elif "[@USERADMIN-BLOCKED@]"==inLine :
			if inData['blocked_by']==True :
				wStr = "●はい"
			else:
				wStr = "  いいえ"
			pRes['Responce'] = "    被ブロック                  : " + wStr
		
		###インプリ：いいね送信回数
		elif "[@USERADMIN-SEND_CNT@]"==inLine :
			if inData['flg_db_set']==False :
				wStr = "－－－"
			elif inData['send_cnt']>0 :
				wStr = str( inData['send_cnt'] )
			else:
				wStr = "  なし"
			pRes['Responce'] = "    いいね送信回数              : " + wStr
		
		###インプリ：いいね総回数
		elif "[@USERADMIN-FAVO_CNT@]"==inLine :
			if inData['flg_db_set']==False :
				wStr = "－－－"
			elif inData['favo_cnt']>0 :
				wStr = str( inData['favo_cnt'] )
			else:
				wStr = "  なし"
			pRes['Responce'] = "    いいね総回数                : " + wStr
		
		###インプリ：いいね今週数
		elif "[@USERADMIN-NOW_FAVO_CNT@]"==inLine :
			if inData['flg_db_set']==False :
				wStr = "－－－"
			elif inData['now_favo_cnt']>0 :
				wStr = str( inData['now_favo_cnt'] )
			else:
				wStr = "  なし"
			pRes['Responce'] = "    いいね今週数                : " + wStr
		
		###インプリ：最終いいね実施日
		elif "[@USERADMIN-FAVO_DATE@]"==inLine :
			if inData['flg_db_set']==False or \
			   inData['favo_date']==None :
				wStr = "－－－"
			else:
				wStr = str( inData['favo_date'] )
			pRes['Responce'] = "    最終いいね実施日            : " + wStr
		
		###インプリ：最終リスト通知日
		elif "[@USERADMIN-LIST_DATE@]"==inLine :
			if inData['flg_db_set']==False or \
			   inData['list_date']==None :
				wStr = "－－－"
			else:
				wStr = str( inData['list_date'] )
			pRes['Responce'] = "    最終リスト通知日            : " + wStr
		
		###インプリ：DB情報あり
		elif "[@USERADMIN-EXIST@]"==inLine :
			if inData['flg_db_set']==True :
				wStr = "〇はい"
			else:
				wStr = "▼いいえ"
			pRes['Responce'] = "    DB情報あり                  : " + wStr
		
		###インプリ：DB登録日
		elif "[@USERADMIN-DB_REGDATE@]"==inLine :
			if inData['flg_db_set']==False or \
			   inData['regdate']==None :
				wStr = "－－－"
			else:
				wStr = str( inData['regdate'] )
			pRes['Responce'] = "    DB登録日                    : " + wStr
		
		#############################
		# 正常
		pRes['Result'] = True
		return



	#####################################################
	# キーワードいいね画面
	@classmethod
	def __dispInp_Keyword( cls, inLine, outRes, inData={} ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：キーワードいいね文字列
		if "[@KEYWORD-STRING@]"==inLine :
			if inData['str_keyword']!=None :
				wStr = str( inData['str_keyword'] )
			else:
				wStr = "(設定なし)"
			pRes['Responce'] = "設定文字列: " + wStr
		
		###インプリ：最大ツイート取得数
		elif "[@KEYWORD-MAXSEARCHNUM@]"==inLine :
			pRes['Responce'] = "    最大ツイート取得数: " + str( inData['max_searchnum'] )
		
		###インプリ：抽出ツイート数
		elif "[@KEYWORD-SEARCHNUM@]"==inLine :
			pRes['Responce'] = "    抽出ツイート数    : " + str( inData['searchnum'] )
		
		###インプリ：記憶ユーザ数
		elif "[@KEYWORD-USERNUM@]"==inLine :
			pRes['Responce'] = "    記憶ユーザ数      : " + str( inData['usernum'] )
		
		###インプリ：抽出ユーザ数
		elif "[@KEYWORD-USERNUM@]"==inLine :
			pRes['Responce'] = "    抽出ユーザ数      : " + str( inData['now_usernum'] )
		
		###インプリ：いいね実行数
		elif "[@KEYWORD-FAVOUSERNUM@]"==inLine :
			pRes['Responce'] = "    いいね実行数      : " + str( inData['favo_usernum'] )
		
		#############################
		# 正常
		pRes['Result'] = True
		return



###	#####################################################
###	# 自動いいね設定画面
###	@classmethod
###	def __dispInp_AutoFavo( cls, inLine, outRes ):
###		pRes = outRes
###		#############################
###		# インプリメント処理
###		
###		###インプリ：リプライを含める
###		if "[@AUTOFAVO-RIP@]"==inLine :
###			if gVal.STR_AutoFavo['Rip']==True :
###				wStr = "含める"
###			else:
###				wStr = "除外する"
###			pRes['Responce'] = "    リプライ            : " + wStr
###		
###		###インプリ：リツイートを含める
###		elif "[@AUTOFAVO-RETWEET@]"==inLine :
###			if gVal.STR_AutoFavo['Ret']==True :
###				wStr = "含める"
###			else:
###				wStr = "除外する"
###			pRes['Responce'] = "    リツイート          : " + wStr
###		
###		###インプリ：引用リツイートを含める
###		elif "[@AUTOFAVO-INYOURT@]"==inLine :
###			if gVal.STR_AutoFavo['iRet']==True :
###				wStr = "含める"
###			else:
###				wStr = "除外する"
###			pRes['Responce'] = "    引用リツイート      : " + wStr
###		
###		###インプリ：タグを含める
###		elif "[@AUTOFAVO-TAG@]"==inLine :
###			if gVal.STR_AutoFavo['Tag']==True :
###				wStr = "含める"
###			else:
###				wStr = "除外する"
###			pRes['Responce'] = "    タグ                : " + wStr
###		
###		###インプリ：片フォローを含める
###		elif "[@AUTOFAVO-PIEFOLLOW@]"==inLine :
###			if gVal.STR_AutoFavo['PieF']==True :
###				wStr = "含める"
###			else:
###				wStr = "除外する"
###			pRes['Responce'] = "    片フォロー          : " + wStr
###		
###		###インプリ：対象時間
###		elif "[@AUTOFAVO-LENGTH@]"==inLine :
###			pRes['Responce'] = "    対象範囲時間        : " + str( gVal.STR_AutoFavo['Len'] )
###		
###		#############################
###		# 正常
###		pRes['Result'] = True
###		return
###
###

	#####################################################
	# リストいいね設定画面
	@classmethod
	def __dispInp_ListFavo( cls, inLine, outRes, inData=None ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：リストいいね設定 一覧
		if "[@LISTFAVO_LIST@]"==inLine :
			pRes['Responce'] = inData
		
		#############################
		# 正常
		pRes['Result'] = True
		return



#####################################################
# ディスプレイファイル 読み込み→画面表示
#####################################################
	@classmethod
###	def sViewDisp( cls, inDisp, inIndex=-1, inClear=True ):
	def sViewDisp( cls, inDisp, inIndex=-1, inClear=True, inData={} ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MyDisp"
		wRes['Func']  = "sViewDisp"
		
		#############################
		# ディスプレイファイルの確認
		wKeylist = gVal.DEF_STR_DISPFILE.keys()
		if inDisp not in wKeylist :
			###キーがない(指定ミス)
			wRes['Reason'] = "Display key is not found: inDisp= " + inDisp
			return wRes
		
		if CLS_File.sExist( gVal.DEF_STR_DISPFILE[inDisp] )!=True :
			###ファイルがない...(消した？)
			wRes['Reason'] = "Displayファイルがない: file=" + gVal.DEF_STR_DISPFILE[inDisp]
			return wRes
		
		#############################
		# ディスプレイファイルの読み込み
		wDispFile = []
		if CLS_File.sReadFile( gVal.DEF_STR_DISPFILE[inDisp], outLine=wDispFile, inStrip=False )!=True :
			wRes['Reason'] = "Displayファイルがない(sReadFile): file=" + gVal.DEF_STR_DISPFILE[inDisp]
			return wRes
		
		if len(wDispFile)<=1 :
			wRes['Reason'] = "Displayファイルが空: file=" + gVal.DEF_STR_DISPFILE[inDisp]
			return wRes
		
		#############################
		# 画面クリア(=通常モード時)
		if gVal.FLG_Test_Mode==False and inClear==True :
			CLS_OSIF.sDispClr()
		
		#############################
		# 画面に表示する
		for wLine in wDispFile :
			###コメントはスキップ
			if wLine.find("#")==0 :
				continue
			
			###インプリメント
###			wResInp = cls.sDispInp( inDisp, wLine, inIndex )
			wResInp = cls.sDispInp( inDisp, wLine, inIndex, inData )
			if wResInp['Result']!=True :
				wRes['Reason'] = "sDispInp is failed: reasin=" + wResInp['Reason']
				return wRes
			if wResInp['Responce']!=None :
				###インプリメントされていれば差し替える
				wLine = wResInp['Responce']
			
			#############################
			# print表示
			CLS_OSIF.sPrn( wLine )
		
		#############################
		# 正常処理
		wRes['Result'] = True
		return wRes

	#####################################################
	@classmethod
	def __get_JPstr_Single( cls, inFLG_Inc ):
		if inFLG_Inc==True :
			wStr = "はい"
		else:
			wStr = "いいえ"
		return wStr


	#####################################################
	@classmethod
	def __get_JPstr_Dual( cls, inFLG_Inc, inFLG_Exc ):
		if inFLG_Inc==True and inFLG_Exc==False :
			wStr = "含める"
		elif inFLG_Inc==False and inFLG_Exc==True :
			wStr = "除外する"
		elif inFLG_Inc==False and inFLG_Exc==False :
			wStr = "無条件"
		else:
			wStr = None
		return wStr



#####################################################
# ヘッダ表示
#####################################################
	@classmethod
	def sViewHeaderDisp( cls, inText, inFLG_Prossessing=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MyDisp"
		wRes['Func']  = "sViewHeaderDisp"
		
		wStr =        "******************************" + '\n'
		wStr = wStr + inText + '\n'
		wStr = wStr + "******************************" + '\n'
		
		if inFLG_Prossessing==True :
			wStr = wStr + "処理中です。しばらくお待ちください......" + '\n'
		
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常
		wRes['Result'] = True
		return




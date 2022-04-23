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
	def sDispInp( cls, inDisp, inLine, inIndex ):
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
			cls.__dispInp_UserAdmin( inLine, wRes )
###		###自動いいね設定画面
###		elif inDisp=="AutoFavoConsole" :
###			cls.__dispInp_AutoFavo( inLine, wRes )
###		
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
	def __dispInp_UserAdmin( cls, inLine, outRes ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：対象ユーザ
		if "[@USERADMIN-TWITTER@]"==inLine :
			pRes['Responce'] = "対象ユーザ  @" + gVal.STR_UserAdminInfo['screen_name']
		
		###インプリ：フォロー者
		elif "[@USERADMIN-MYFOLLOW@]"==inLine :
			if gVal.STR_UserAdminInfo['MyFollow']==True :
				wStr = "〇はい"
			else:
				wStr = "▼いいえ"
			pRes['Responce'] = "    フォロー中                  : " + wStr
		
		###インプリ：フォロワー
		elif "[@USERADMIN-FOLLOWER@]"==inLine :
			if gVal.STR_UserAdminInfo['Follower']==True :
				wStr = "〇はい"
			else:
				wStr = "▼いいえ"
			pRes['Responce'] = "    フォロワー                  : " + wStr
		
		###インプリ：一度フォローしたことがある
		elif "[@USERADMIN-R_MYFOLLOW@]"==inLine :
			if gVal.STR_UserAdminInfo['DB_r_myfollow']==True :
				wStr = "  はい"
			else:
				if gVal.STR_UserAdminInfo['DB_exist']==True :
					wStr = "  いいえ"
				else:
					wStr = "  －－－"
			pRes['Responce'] = "    １度フォローしたことがある  : " + wStr
		
		###インプリ：一度リムーブされたことがある
		elif "[@USERADMIN-R_REMOVE@]"==inLine :
			if gVal.STR_UserAdminInfo['DB_r_remove']==True :
				wStr = "  はい"
			else:
				wStr = "  いいえ"
			pRes['Responce'] = "    １度リムーブされたことがある: " + wStr
		
		###インプリ：フォロー解除候補
		elif "[@USERADMIN-LIMITED@]"==inLine :
			if gVal.STR_UserAdminInfo['DB_limited']==True :
				wStr = "●はい"
			else:
				if gVal.STR_UserAdminInfo['DB_exist']==True :
					wStr = "  いいえ"
				else:
					wStr = "  －－－"
			pRes['Responce'] = "    フォロー解除候補            : " + wStr
		
		###インプリ：鍵アカウント
		elif "[@USERADMIN-PROTECT@]"==inLine :
			if gVal.STR_UserAdminInfo['Protect']==True :
				wStr = "●はい"
			else:
				wStr = "  いいえ"
			pRes['Responce'] = "    鍵アカウント                : " + wStr
		
		###インプリ：ブロック中
		elif "[@USERADMIN-MYBLOCK@]"==inLine :
			if gVal.STR_UserAdminInfo['MyBlock']==True :
				wStr = "●はい"
			else:
				wStr = "  いいえ"
			pRes['Responce'] = "    ブロック中                  : " + wStr
		
		###インプリ：被ブロック
		elif "[@USERADMIN-BLOCKED@]"==inLine :
			if gVal.STR_UserAdminInfo['Blocked']==True :
				wStr = "●はい"
			else:
				wStr = "  いいえ"
			pRes['Responce'] = "    被ブロック                  : " + wStr
		
		###インプリ：疑似リムーブ
		elif "[@USERADMIN-REMOVED@]"==inLine :
			if gVal.STR_UserAdminInfo['DB_removed']==True :
				wStr = "●リムーブON"
			else:
				wStr = "  解除"
			pRes['Responce'] = "    疑似リムーブー              : " + wStr
		
		
		###インプリ：非フォロー化
		elif "[@USERADMIN-UNFOLLOW@]"==inLine :
			if gVal.STR_UserAdminInfo['DB_unfollow']==True :
				wStr = "●非フォローON"
			else:
				wStr = "  解除"
			pRes['Responce'] = "    非フォロー化                : " + wStr
		
		###インプリ：非フォローロック
		elif "[@USERADMIN-UNFOLLOCK@]"==inLine :
			if gVal.STR_UserAdminInfo['DB_unfollock']==True :
				wStr = "●ロックON"
			else:
				wStr = "  解除"
			pRes['Responce'] = "    非フォローロック            : " + wStr
		
		###インプリ：VIP設定
		elif "[@USERADMIN-VIPSET@]"==inLine :
			if gVal.STR_UserAdminInfo['DB_vipuser']==True :
				wStr = "〇VIP"
			else:
				wStr = "  一般"
			pRes['Responce'] = "    VIP設定                     : " + wStr
		
		###インプリ：監視設定
		elif "[@USERADMIN-ADMAGENT@]"==inLine :
			if gVal.STR_UserAdminInfo['DB_admagent']==True :
				wStr = "〇監視ユーザ"
			else:
				wStr = "  監視外"
			pRes['Responce'] = "    監視設定                    : " + wStr
		
		###インプリ：ファボった日
		elif "[@USERADMIN-FAVO_DATE@]"==inLine :
			if gVal.STR_UserAdminInfo['DB_favo_cnt']>0 :
				wStr = str(gVal.STR_UserAdminInfo['DB_favo_date'])
			else:
				wStr = "  なし"
			pRes['Responce'] = "    ファボった日                : " + wStr
		
		###インプリ：ファボられた日
		elif "[@USERADMIN-FAVO_R_DATE@]"==inLine :
			if gVal.STR_UserAdminInfo['DB_r_favo_cnt']>0 :
				wStr = str(gVal.STR_UserAdminInfo['DB_r_favo_date'])
			else:
				wStr = "  なし"
			pRes['Responce'] = "    ファボられた日              : " + wStr
		
		###インプリ：DB情報あり
		elif "[@USERADMIN-EXIST@]"==inLine :
			if gVal.STR_UserAdminInfo['DB_exist']==True :
				wStr = "〇はい"
			else:
				wStr = "▼いいえ"
			pRes['Responce'] = "    DB情報あり                  : " + wStr
		
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
# ディスプレイファイル 読み込み→画面表示
#####################################################
	@classmethod
	def sViewDisp( cls, inDisp, inIndex=-1, inClear=True ):
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
			wResInp = cls.sDispInp( inDisp, wLine, inIndex )
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




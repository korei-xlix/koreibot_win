#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : ログ処理
#####################################################
# 書式:
#	A :	gVal.OBJ_L.Log( "A", wRes )				致命的エラー: プログラム停止 ロジックエラーなどソフト側の問題
#	B :	gVal.OBJ_L.Log( "B", wRes )				内部的エラー: プログラム停止か実行不可 コール先からのエラー
#	C :	gVal.OBJ_L.Log( "C", wRes )				外部のエラー: プログラム停止か実行不可 外部モジュールやハードの問題
#	D :	gVal.OBJ_L.Log( "D", wRes )				潜在的エラー: ユーザ入力など予想外 or 後に問題を起こす可能性がある
#	E :	gVal.OBJ_L.Log( "E", wRes )				不明なエラー: 判断がつかないエラー ありえないルートなど
#
#	S:	gVal.OBJ_L.Log( "S", wRes, "<理由>" )	システム    : botの実行、停止、再起動
#	SC:	gVal.OBJ_L.Log( "SC", wRes, "<理由>" )	システム    : システムの設定変更
#	SR:	gVal.OBJ_L.Log( "SR", wRes, "<理由>" )	システム    : システムの規制制御、自律制御
#	R:	gVal.OBJ_L.Log( "R", wRes, "<理由>" )	ユーザ      : ユーザ登録、削除、抹消
#	RC:	gVal.OBJ_L.Log( "RC", wRes, "<理由>" )	ユーザ      : ユーザ設定変更
#	RR:	gVal.OBJ_L.Log( "RR", wRes, "<理由>" )	ユーザ      : ユーザ個別の規制制御、自律制御
#	T:	gVal.OBJ_L.Log( "T", wRes, "<理由>" )	トラヒック  : システムトラヒック、期間トラヒック、通信トラヒック(統計)
#
#	P :	gVal.OBJ_L.Log( "P", wRes )				データベース操作
#	N :	gVal.OBJ_L.Log( "N", wRes, "<理由>" )	非表示の情報
#	X :	gVal.OBJ_L.Log( "X", wRes )				テスト用ログ
#
#####################################################

from osif import CLS_OSIF
from filectrl import CLS_File
from gval import gVal
#####################################################
class CLS_Mylog():
#####################################################

#############################
# ログレベル 日本語ローカライズ
	DEF_STR_LEVEL = {
		"A"			: "",
		"B"			: "",
		"C"			: "",
		"D"			: "",
		"E"			: "",
		
		"S"			: "",
		"SC"		: "",
		"SR"		: "",
		"R"			: "",
		"RC"		: "",
		"RR"		: "",
		"T"			: "",
		
		"P"			: "",
		"N"			: "",
		"X"			: "",
		
		"0"			: "",
		"(dummy)"	: ""
	}

#############################
# ログ表示モード
	DEF_STR_VIEW_LEVEL = {
		"F"			: "",		# 全ログ
		"A"			: "",		# 全ログ(期間)
		"V"			: "",		# 運用ログ
		"R"			: "",		# 運用ログ(操作のみ)
		"T"			: "",		# トラヒック
		"U"			: "",		# ユーザログ
		"E"			: "",		# 異常ログ
		"(dummy)"	: ""
	}

	DEF_VIEW_CONSOLE = True		#デフォルトのコンソール表示
	DEF_OUT_FILE     = False	#デフォルトのファイル出力



#####################################################
# ロギング
#####################################################
	def Log( self, inLevel, inRes, inText=None, inARR_Data=[], inViewConsole=DEF_VIEW_CONSOLE, inOutFile=DEF_OUT_FILE ):
		#############################
		# ログ文字セット
		wSTR_Log = {
			"LogClass" : None,
			"LogFunc"  : None,
			"Reason"   : None }
		
		#############################
		# ログレベルのチェック
		wLevel = inLevel
		if wLevel==None or wLevel=="" :
			wLevel = "0"
		###大文字変換
		try:
			wLevel = wLevel.upper()
		except ValueError as err :
			wLevel = "0"
		###定義チェック
		if wLevel not in self.DEF_STR_LEVEL :
			wLevel = "0"
		
		#############################
		# ログクラスのチェック
		if "Class" not in inRes :
			wLogClass = "(none)"
		else:
			wLogClass = inRes['Class']
		
		if wLogClass==None or wLogClass=="" :
			wLogClass = "(none)"
		
		#############################
		# ログファンクのチェック
		if "Func" not in inRes :
			wLogFunc = "(none)"
		else:
			wLogFunc = inRes['Func']
		
		if wLogFunc==None or wLogFunc=="" :
			wLogFunc = "(none)"
		
		#############################
		# 理由のチェック
		if inText!=None :
			wReason = str( inText )
		elif "Reason" not in inRes :
			wReason = "(none)"
		else:
			wReason = str( inRes['Reason'] )
		
		if wReason=="None" or wReason=="" :
			wReason = "(none)"
		### ' を　'' に置き換える
		wReason = wReason.replace( "'", "''" )
		
		#############################
		# 構造体に突っ込む
		wSTR_Log['LogClass'] = wLogClass
		wSTR_Log['LogFunc'] = wLogFunc
		wSTR_Log['Reason'] = wReason
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		### wTD['TimeDate']
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			CLS_OSIF.sPrn( "CLS_Mylog: Log: PC時間の取得に失敗しました" )
			wCHR_TimeDate = "1901-01-01 00:00:00"
			
			###いちおデータベースにも記録する
			wQuery = "insert into tbl_log_data values (" + \
						"'" + gVal.STR_UserInfo['Account'] + "'," + \
						"'C'," + \
						"'CLS_Mylog'," + \
						"'Log'," + \
						"'CLS_OSIF.sGetTime is failed'," + \
						"'" + wCHR_TimeDate + "'" + \
						") ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery, False )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "C", wRes )
		
		else:
			wCHR_TimeDate = str(wTD['TimeDate'])
		
		#############################
		# データベースに記録する
		wQuery = "insert into tbl_log_data values (" + \
					"'" + gVal.STR_UserInfo['Account'] + "'," + \
					"'" + wLevel + "'," + \
					"'" + wSTR_Log['LogClass'] + "'," + \
					"'" + wSTR_Log['LogFunc'] + "'," + \
					"'" + wSTR_Log['Reason'] + "'," + \
					"'" + wCHR_TimeDate + "'" + \
					") ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "C", wRes )
			##以後の記録処理は継続する
		
		#############################
		# ログの組み立て
		if ( wLevel=="S" or wLevel=="R" or wLevel=="U" or wLevel=="T" \
		   and inText!=None ) :
			wOutLog = wLevel + ": " + wSTR_Log['Reason']
		else:
			wOutLog = wLevel + ": "
			wOutLog = wOutLog + wSTR_Log['LogClass'] + ": "
			wOutLog = wOutLog + wSTR_Log['LogFunc'] + ": "
			wOutLog = wOutLog + wSTR_Log['Reason']
		
		#############################
		# データの組み立て
		wData = []
		if len(inARR_Data)>0 :
			###ブランク文字
			wBlank = " " * len( wCHR_TimeDate )
			###データのセット
			for wLine in inARR_Data :
				wIncLine = wBlank + ' ' + wLine + '\n'
				wData.append( wIncLine )
		
		#############################
		# コンソールに表示する
		# = システムログに出る
		wFLG_View = False
		
		### A・B・X（致命的エラー・テストログ）
		###   =表示
		if wLevel=="A" or wLevel=="B" or wLevel=="X" :
			wFLG_View = True
		
		### S・SC・SR・TS（運用ログ・トラヒック）
		###   =テキストが設定されていれば表示
		elif wLevel=="S" or wLevel=="SC" or wLevel=="SR" or wLevel=="T" :
			if  inText!=None :
				wFLG_View = True
		
		### R・RC・RR（ユーザ操作）
		###   =表示
		elif wLevel=="R" or wLevel=="RC" or wLevel=="RR" :
			wFLG_View = True
		
		### P・N（データベース操作・非表示の情報）
		###   =非表示
		elif wLevel=="P" or wLevel=="N" :
			wFLG_View = False
		
		### その他はコントロールオプションに従う
		else :
			if inViewConsole==True :
				wFLG_View = True
		
		if wFLG_View==True :
			CLS_OSIF.sPrn( wOutLog )
			for wLineData in wData :
				CLS_OSIF.sPrn( wLineData )
		
		#############################
		# ファイル書き出し
		if inOutFile==True :
			wFileRes = self.__writeFile( wCHR_TimeDate, wOutLog, wData )
		
		return wOutLog



#####################################################
# ファイルへの書き出し
#####################################################
	def __writeFile( self, inTimeDate, inLog, inARR_Data=[] ):
		#############################
		# ユーザフォルダの存在チェック
		wLogPath = gVal.DEF_STR_FILE['LogBackup_path']
		if CLS_File.sExist( wLogPath )!=True :
			###フォルダがなければ諦める
			return False
		
		#############################
		# ログフォルダの作成
		if CLS_File.sExist( wLogPath )!=True :
			###まだ未生成なら諦める
			return False
		
		#############################
		# ファイル名、フルパスの生成
		wFilePath = inTimeDate.split(" ")
		wFilePath_Date = wFilePath[0]
		wFilePath_Date = wFilePath_Date.replace( "-", "" )
		wFilePath_Time = wFilePath[1]
		wFilePath_Time = wFilePath_Time.replace( ":", "" )
		
		wFilePath = wFilePath_Date + "_" + wFilePath_Time + ".log"
		wLogPath = wLogPath + "/" + wFilePath
		
		wSetLine = []
		#############################
		# 1行目
		wLine = inTimeDate + ' ' + inLog + '\n'
		wSetLine.append( wLine )
		
		#############################
		# 2行目以降
		if len(inARR_Data)>0 :
			for wLineData in inARR_Data :
				wSetLine.append( wLineData )
		
		#############################
		# ファイル追加書き込み
		wRes = CLS_File.sAddFile( wLogPath, wSetLine, inExist=False )
		if wRes!=True :
			###失敗
			return False
		
		return True



#####################################################
# ログの表示
#####################################################
	def View( self, inShortMode=True, inViewMode="A" ):
		#############################
		# 運用モード
		wViewMode = inViewMode.upper()
		if inViewMode not in self.DEF_STR_VIEW_LEVEL :
			wViewMode = "A"
		###大文字変換
		try:
			wViewMode = wViewMode.upper()
		except ValueError as err :
			wViewMode = "A"
		
		#############################
		# 画面クリア
		CLS_OSIF.sDispClr()
		
		#############################
		# ヘッダ表示
		wStr = "--------------------" + '\n'
		wStr = wStr + " ログの表示" + '\n'
		wStr = wStr + "--------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# ログ取得
		### wViewMode=V 運用ログ
		if wViewMode=="V" :
			wQuery = "select * from tbl_log_data where " + \
						"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
						"( " + \
						"level = 'S' or " + \
						"level = 'SC' or " + \
						"level = 'SR' or " + \
						"level = 'RR' or " + \
						"level = 'T' or " + \
						"level = 'P' or " + \
						"level = 'N' " + \
						") and " + \
						"( lupdate > now() - interval '2 week' ) " + \
						"order by lupdate DESC ;"
		
		### wViewMode=R 運用ログ(操作のみ)
		if wViewMode=="R" :
			wQuery = "select * from tbl_log_data where " + \
						"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
						"( " + \
						"level = 'S' or " + \
						"level = 'SC' or " + \
						"level = 'SR' or " + \
						"level = 'RR' or " + \
						"level = 'N' " + \
						") and " + \
						"( lupdate > now() - interval '2 week' ) " + \
						"order by lupdate DESC ;"
		
		### wViewMode=T トラヒック
		if wViewMode=="T" :
			wQuery = "select * from tbl_log_data where " + \
						"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
						"level = 'T' and " + \
						"( lupdate > now() - interval '2 week' ) " + \
						"order by lupdate DESC ;"
		
		### wViewMode=E 異常ログ
		elif wViewMode=="E" :
			wQuery = "select * from tbl_log_data where " + \
						"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
						"( " + \
						"level = 'A' or " + \
						"level = 'B' or " + \
						"level = 'C' or " + \
						"level = 'D' or " + \
						"level = 'E' or " + \
						"level = 'X' or " + \
						"level = '0' " + \
						") and " + \
						"( lupdate > now() - interval '2 week' ) " + \
						"order by lupdate DESC ;"
		
		### wViewMode=U ユーザ操作ログ
		elif wViewMode=="U" :
			wQuery = "select * from tbl_log_data where " + \
						"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
						"( " + \
						"level = 'R' or " + \
						"level = 'RC' " + \
						") and " + \
						"( lupdate > now() - interval '2 week' ) " + \
						"order by lupdate DESC ;"
		
		### wViewMode=F 全ログ
		elif wViewMode=="F" :
			wQuery = "select * from tbl_log_data where " + \
						"twitterid = '" + gVal.STR_UserInfo['Account'] + "' " + \
						"order by lupdate DESC ;"
		
		### wViewMode=A 全ログ(期間)
		else:
			wQuery = "select * from tbl_log_data where " + \
						"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
						"( lupdate > now() - interval '2 week' ) " + \
						"order by lupdate DESC ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 辞書型に整形
		wARR_Log = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# ログ表示長のセット
		wOutLen = len(wARR_Log)
		if wOutLen==0 :
			wStr = "ログがありません。処理を中止します。" + '\n'
			CLS_OSIF.sPrn( wStr )
			return True
		
		if inShortMode==True :
			wOutLen = gVal.DEF_STR_TLNUM['logShortLen']
		
		#############################
		# ログ表示
		wKeylist = wARR_Log.keys()
		wIndex = 0
		for wKey in wKeylist :
			wTD    = str(wARR_Log[wKey]['lupdate'])
			wBlank = " " * len( wTD ) + " "
			
			if wViewMode=="U" :
				### ユーザ記録
				wLine = wTD + " " + wARR_Log[wKey]['reason']
				CLS_OSIF.sPrn( wLine )
			else:
				### ユーザ記録以外
				wLine = wTD + " " + wARR_Log[wKey]['level'] + " "
				wLine = wLine + "[" + wARR_Log[wKey]['log_class'] + "] "
				wLine = wLine + "[" + wARR_Log[wKey]['log_func'] + "]"
				CLS_OSIF.sPrn( wLine )
				
				wLine = wBlank + wARR_Log[wKey]['reason']
				CLS_OSIF.sPrn( wLine )
			
			wIndex += 1
			if wOutLen<=wIndex :
				break
		
		return True

#############################
#	twitterid   TEXT  NOT NULL
#	level       CHAR(1) DEFAULT '-'
#	log_class   TEXT  NOT NULL
#	log_func    TEXT  NOT NULL
#	reason      TEXT  NOT NULL
#	lupdate     TIMESTAMP
#############################



#####################################################
# ログクリア
#####################################################
	def Clear( self, inAllClear=False ):
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			CLS_OSIF.sPrn( "CLS_Mylog: Clear: PC時間の取得に失敗しました" )
			return False
		wTimeDate = str(wTD['TimeDate'])
		
		#############################
		# 画面クリア
		CLS_OSIF.sDispClr()
		
		#############################
		# ヘッダ表示
		wStr = "--------------------" + '\n'
		wStr = wStr + " ログ退避中" + '\n'
		wStr = wStr + "--------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 実行の確認
		wStr = "データベースのログを全てファイルに退避したあと、全てクリアします。" + '\n'
		CLS_OSIF.sPrn( wStr )
		wSelect = CLS_OSIF.sInp( "よろしいですか？(y/N)=> " )
		if wSelect!="y" :
			##キャンセル
			CLS_OSIF.sPrn( "中止しました。" )
			return True
		
		#############################
		# 全ログ取得
		wQuery = "select * from tbl_log_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' " + \
					"order by lupdate ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 辞書型に整形
		wARR_Log = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# ログ表示長のセット
		wOutLen = len(wARR_Log)
		if wOutLen==0 :
			wStr = "ログがありません。処理を中止します。" + '\n'
			CLS_OSIF.sPrn( wStr )
			return True
		
		wARR_Output = []
		#############################
		# 出力組み立て
		wKeylist = wARR_Log.keys()
		for wKey in wKeylist :
			wTD    = str(wARR_Log[wKey]['lupdate'])
			wBlank = " " * len( wTD ) + " "
			
			wLine = wTD + "," + wARR_Log[wKey]['level'] + ","
			wLine = wLine + wARR_Log[wKey]['log_class'] + ","
			wLine = wLine + wARR_Log[wKey]['log_func'] + ","
			wLine = wLine + wARR_Log[wKey]['reason'] + "," + '\n'
			wARR_Output.append( wLine )
		
		#############################
		# ログ出力
		self.__writeLogFile( wTimeDate, inARR_Data=wARR_Output )
		
		#############################
		# ログ消去
		if inAllClear==True :
			### 全ログ消去
			wQuery = "delete from tbl_log_data where " + \
						"twitterid = '" + gVal.STR_UserInfo['Account'] + "' " + \
						";"
		else:
			### エラーと運用のみクリア
			wQuery = "delete from tbl_log_data where " + \
						"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
						"(" + \
						"not level = 'R' and " + \
						"not level = 'RC' ) " + \
						";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 結果表示
		wStr = "データベースのログを全てクリアしました。" + '\n'
		CLS_OSIF.sPrn( wStr )
		return True



#####################################################
# ログ退避 書き出し
#####################################################
	def __writeLogFile( self, inTimeDate, inARR_Data=[] ):
		#############################
		# ログフォルダの作成
		wLogPath = gVal.DEF_STR_FILE['LogBackup_path']
		if CLS_File.sExist( wLogPath )!=True :
			###まだ未生成なら作成する
			if CLS_File.sMkdir( wLogPath )!=True :
				###作れなければ諦める
				return False
		
		#############################
		# ファイル名、フルパスの生成
		wFilePath = inTimeDate.split(" ")
		wFilePath_Date = wFilePath[0]
		wFilePath_Date = wFilePath_Date.split("-")
		
		wFilePath = wFilePath_Date[0] + wFilePath_Date[1] + ".csv"
		wLogPath = wLogPath + "/" + wFilePath
		
		#############################
		# ファイル追加書き込み
		wRes = CLS_File.sAddFile( wLogPath, inARR_Data, inExist=False )
		if wRes!=True :
			###失敗
			return False
		
		wStr = "ログをファイルに退避しました: " + wFilePath
		CLS_OSIF.sPrn( wStr )
		
		return True




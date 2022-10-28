#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 フォロワー監視系
#####################################################

from ktime import CLS_TIME
from osif import CLS_OSIF
from traffic import CLS_Traffic
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterFollower():
#####################################################
	OBJ_Parent = ""				#親クラス実体
	
	ARR_AgentUsers  = {}
	VAL_ReactionCnt = 0
	ARR_Mentions    = {}
	ARR_Reaction    = {}
	
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
# リアクションチェック
#####################################################
	def ReactionCheck( self, inFLG_Short=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "ReactionCheck"
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['reaction'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			### 規定以内は除外
			wStr = "●リアクション期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		self.VAL_ReactionCnt = 0
		self.ARR_Mentions    = {}
		self.ARR_Reaction    = {}
		#############################
		# 取得開始の表示
		if inFLG_Short==False :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中（通常）" )
			wCount = gVal.DEF_STR_TLNUM['reactionTweetLine']
		else :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中（ショート）" )
			wCount = gVal.DEF_STR_TLNUM['reactionTweetLine_Short']
		
		#############################
		# 自分の直近のツイートを取得
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
			 inID=gVal.STR_UserInfo['id'], inCount=wCount )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetTL"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if len(wTweetRes['Responce'])==0 :
			wRes['Reason'] = "Tweet is not get: me"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# チェック
		# いいね、リツイート、引用リツイートしたユーザ
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		wFLG_ZanCountSkip = False
		self.OBJ_Parent.ARR_ReacrionUserID = []
		for wTweet in wTweetRes['Responce'] :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
				break	###ウェイト中止
			wFLG_ZanCountSkip = False
			
			###日時の変換
			wTime = CLS_TIME.sTTchg( wRes, "(1)", wTweet['created_at'] )
			if wTime['Result']!=True :
				continue
			wTweet['created_at'] = wTime['TimeDate']
			
			#############################
			# 期間内のTweetか
			wGetLag = CLS_OSIF.sTimeLag( str( wTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed(1)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				###期間外= 古いツイートなので処理しない
				wFLG_ZanCountSkip = True
				continue
			
			#############################
			# 質問ツイートか
			wMention = False
			if gVal.STR_UserInfo['QuestionTag']!=gVal.DEF_NOTEXT :
				if wTweet['text'].find( gVal.STR_UserInfo['QuestionTag'] )>=0 :
					wMention = True
			
			#############################
			# ツイートチェック
###			wSubRes = self.OBJ_Parent.ReactionTweetCheck( str(gVal.STR_UserInfo['id']), wTweet )
			wSubRes = self.OBJ_Parent.ReactionTweetCheck( str(gVal.STR_UserInfo['id']), wTweet, inMention=wMention )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "ReactionTweetCheck"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
###			if wSubRes['Responce']==True :
			if wSubRes['Responce']['Reaction']==True :
				### リアクション回数+
				self.VAL_ReactionCnt += 1
				
				wKeyuser = list( wSubRes['Responce']['users'].keys() )
				for wUserID in wKeyuser :
					if wUserID not in self.ARR_Reaction :
						wCell = {
							"user"	: wSubRes['Responce']['users'][wUserID]['user'],
							"cnt"	: wSubRes['Responce']['users'][wUserID]['cnt']
						}
						self.ARR_Reaction.update({ wUserID : wCell })
						
						
						print("xxx1")
						
					else :

						print("xxx2")

						self.ARR_Reaction[wUserID]['cnt'] += wSubRes['Responce']['users'][wUserID]['cnt']
		
		#############################
		# チェック
		# メンションしたユーザ
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中：メンション" )
		
		wSubRes = gVal.OBJ_Tw_IF.GetMyMentionLookup()
		if wSubRes['Result']!=True :
###			wRes['Reason'] = "Twitter Error(GetRefRetweetLookup): Tweet ID: " + wTweetID
			wRes['Reason'] = "Twitter Error(GetMyMentionLookup)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wSubRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
###		wARR_MentionUsers = {}
		wFLG_ZanCountSkip = False
		wKeylist = list( wSubRes['Responce'].keys() )
		for wReplyID in wKeylist :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
				break	###ウェイト中止
			wFLG_ZanCountSkip = False
			
			###日時の変換
			wTime = CLS_TIME.sTTchg( wRes, "(2)", wSubRes['Responce'][wReplyID]['created_at'] )
			if wTime['Result']!=True :
				continue
			wSubRes['Responce'][wReplyID]['created_at'] = wTime['TimeDate']
			
			#############################
			# 期間内のTweetか
			wGetLag = CLS_OSIF.sTimeLag( str( wSubRes['Responce'][wReplyID]['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed(2)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				###期間外= 古いツイートなので処理しない
				wFLG_ZanCountSkip = True
				continue
			
			#############################
			# チェック対象のツイート表示
			wStr = '\n' + "--------------------" + '\n' ;
			wStr = wStr + "チェック中: " + '\n' ;
			wStr = wStr + wSubRes['Responce'][wReplyID]['reply_text'] ;
			CLS_OSIF.sPrn( wStr )
			
			wID = str(wSubRes['Responce'][wReplyID]['id'])
			
			#############################
			# ユーザ情報を取得する
			wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=wID )
			if wUserInfoRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: @" + wUserInfoRes['Responce']['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			###ユーザ単位のリアクションチェック
###			wReactionRes = self.OBJ_Parent.ReactionUserCheck( wUserInfoRes['Responce'], wSubRes['Responce'][wReplyID] )
			wReactionRes = self.OBJ_Parent.ReactionUserCheck( wUserInfoRes['Responce'], wSubRes['Responce'][wReplyID], inMention=True )
			if wReactionRes['Result']!=True :
###				wRes['Reason'] = "Twitter Error(ReactionUserCheck 4): Tweet ID: " + str(wSubRes['Responce'][wReplyID]['id'])
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 4): Tweet ID: " + wID
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wReactionRes['Responce']==True :
				wStr = "〇リプライ検出: " + wUserInfoRes['Responce']['screen_name']
				CLS_OSIF.sPrn( wStr )
				
				### リアクション回数+
				self.VAL_ReactionCnt += 1
				
				### メンションユーザ情報
###				wARR_MentionUsers.update({ wID : wUserInfoRes['Responce'] })
###				wCellMention = {
###					"mention"	: True,
###					"user"		: wUserInfoRes['Responce']
###				}
###				wARR_MentionUsers.update({ wID : wCellMention })
				if wReplyID not in self.ARR_Mentions :
					wCell = {
						"id"	: wSubRes['Responce'][wReplyID]['reply_id'],
						"text"	: wSubRes['Responce'][wReplyID]['reply_text'],
						"users"	: {}
					}
					self.ARR_Mentions.update({ wReplyID : wCell })
				
				if wID not in self.ARR_Mentions['users'] :
					self.ARR_Mentions['users'].update({ wID : wUserInfoRes['Responce'] })
				
				### トラヒック記録
				CLS_Traffic.sP( "r_reaction" )
				CLS_Traffic.sP( "r_rep" )
				if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
					CLS_Traffic.sP( "r_in" )
				else:
					CLS_Traffic.sP( "r_out" )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "reaction", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['reaction']
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# リアクション結果表示
#####################################################
	def ReactionResult(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "ReactionResult"
		
###		#############################
###		# 結果表示
###		wStr = "------------------------------" + '\n'
###		wStr = wStr + "リアクション結果" + '\n'
###		wStr = wStr + "------------------------------" + '\n'
###		wStr = wStr + "  新規受信数: " + str( self.VAL_ReactionCnt ) + " .件" + '\n'
###		CLS_OSIF.sPrn( wStr )
###		
###		if len(self.ARR_Mentions)==0 :
###			return False
###		
###		#############################
###		# メンション情報の表示
###		wARR_MentionUsers = {}
###		wStr = ""
###		wKeylist = list( self.ARR_Mentions.keys() )
###		for wID in wKeylist :
###			wStr = wStr + self.ARR_Mentions[wID]['text'] + '\n'
###			wStr = wStr + "  users: "
###			
###			wKeylist2 = list( self.ARR_Mentions[wID]['users'].keys() )
###			for wUserID in wKeylist2 :
###				wScreenName = self.ARR_Mentions[wID]['users'][wUserID]['screen_name']
###				wStr = wStr + wScreenName + " "
###				
###				if wScreenName not in wARR_MentionUsers :
###					wCell = {
###						"id"			: wUserID,
###						"screen_name"	: wScreenName,
###						"cnt"			: 1 
###					}
###					wARR_MentionUsers.update({ wUserID : wCell })
###				else:
###					wARR_MentionUsers[wUserID]['cnt'] += 1
###			
###			wStr = wStr + '\n' + "    --------------------------" + '\n'
###		
		#############################
		# メンション情報 表示
		wStr = "------------------------------" + '\n'
		wStr = wStr + "メンション結果" + '\n'
		wStr = wStr + "------------------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wStr = ""
		if len(self.ARR_Mentions)==0 :
			### 情報なしの場合
			wStr = "(情報なし)" + '\n'
		
		else:
			### 情報ありの場合
			
			#############################
			# メンション情報の表示
			wKeylist = list( self.ARR_Mentions.keys() )
			for wID in wKeylist :
				wStr = wStr + self.ARR_Mentions[wID]['text'] + '\n'
				wStr = wStr + "  users: "
				wKeylist2 = list( self.ARR_Mentions[wID]['users'].keys() )
				for wUserID in wKeylist2 :
					wStr = wStr + self.ARR_Mentions[wID]['users'][wUserID]['screen_name'] + " "
		
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 非絡みユーザ一覧の取得（自動設定のみ）
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserBList( inAutoOnly=True )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "UpdateFavoData_UserLevel is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_RateUserB = wSubRes['Responce']
		
		#############################
		# 自動非絡みでリアクションがなかったら、
		#   解除する
		wKeylist = list( wARR_RateUserB.keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			### リアクションがなければ
			###  0 を設定しておく
			if wID not in self.ARR_Reaction :
				wCell = {
					"user"	: wARR_RateUserB[wID],
					"cnt"	: 0
				}
				self.ARR_Reaction.update({ wID : wCell })
		
		#############################
		# 結果表示
		wStr = "------------------------------" + '\n'
		wStr = wStr + "リアクション結果" + '\n'
		wStr = wStr + "------------------------------" + '\n'
		wStr = wStr + "  新規受信数: " + str( self.VAL_ReactionCnt ) + " .件" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wStr = ""
		if len(self.ARR_Reaction)==0 :
			### リアクションがなければ、ここで終わり
			wStr = "(情報なし)" + '\n'
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# 非絡みユーザのユーザレベル変更
		wKeylist = list( self.ARR_Reaction.keys() )
		for wID in wKeylist :
			#############################
			# DBからいいね情報を取得する(1個)
			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( self.ARR_Reaction[wID]['user'], inFLG_New=False )
			if wDBRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			### DB未登録ならスキップ
			if wDBRes['Responce']['Data']==None :
				continue
			wARR_DBData = wDBRes['Responce']['Data']
			
			#############################
			# 登録ユーザはスルー
			if gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )!=False :
				continue
			
			#############################
			# 連ふぁぼのカウント処理
			if self.ARR_Reaction[wID]['cnt']>=1 :
				### リアクションありの場合
				###   強制回数以上は、リアクションcnt分カウント
				###   その他は +1 カウント
				if self.ARR_Reaction[wID]['cnt']>=gVal.DEF_STR_TLNUM['renFavoForceCnt'] :
					wCnt = self.ARR_Reaction[wID]['cnt'] + 1
				else:
					wCnt = wARR_DBData['renfavo_cnt'] + 1
			else:
				### リアクションなしの場合
				###   非絡み設定中の場合は -1 カウント
				###   その他は 0 カウント
				if wARR_DBData['renfavo_cnt']>=1 :
					wCnt = wARR_DBData['renfavo_cnt'] - 1
				else:
					wCnt = 0
			
			wUserLevel = None
###			if wARR_MentionUsers[wUserID]['cnt']>=2 :
###				#############################
###				# 相互フォロー中か
###				if ( self.STR_UserAdminInfo['level_tag']=="B" or self.STR_UserAdminInfo['level_tag']=="B+" or \
###				     self.STR_UserAdminInfo['level_tag']=="C" or self.STR_UserAdminInfo['level_tag']=="C+" ) and \
###				   ( self.STR_UserAdminInfo['level_tag']!="G" or self.STR_UserAdminInfo['level_tag']!="H" ) :
###					if wCnt>=gVal.DEF_STR_TLNUM['renFavoOnCnt'] :
###						wUserLevel = "G"
###				
###				#############################
###				# 片フォロワーか
###				elif self.STR_UserAdminInfo['level_tag']=="E" and \
###				     ( self.STR_UserAdminInfo['level_tag']!="G" or self.STR_UserAdminInfo['level_tag']!="H" ) :
###					
###					wUserLevel = "H"
###			
###			elif wARR_MentionUsers[wUserID]['cnt']==1 :
###				#############################
###				# 相互フォロー中 解除か
###				if self.STR_UserAdminInfo['level_tag']=="G" :
###					if self.STR_UserAdminInfo['send_cnt']>=gVal.DEF_STR_TLNUM['LEVEL_B_Cnt'] :
###						wUserLevel = "B+"
###					elif self.STR_UserAdminInfo['send_cnt']>=1 :
###						wUserLevel = "B"
###					else:
###						wUserLevel = "C+"
###				
###				#############################
###				# 片フォロワー 解除か
###				elif self.STR_UserAdminInfo['level_tag']=="H" :
###					
###					wUserLevel = "E"
###			
			
			if wCnt>=gVal.DEF_STR_TLNUM['renFavoOnCnt'] :
				#############################
				# 相互フォロー中か
				if ( wARR_DBData['level_tag']=="B" or wARR_DBData['level_tag']=="B+" or \
				     wARR_DBData['level_tag']=="C" or wARR_DBData['level_tag']=="C+" ) and \
				   ( wARR_DBData['level_tag']!="G" or wARR_DBData['level_tag']!="H" ) :
					wUserLevel = "G"
				
				#############################
				# 片フォロワーか
				elif wARR_DBData['level_tag']=="E" and \
				     ( wARR_DBData['level_tag']!="G" or wARR_DBData['level_tag']!="H" ) :
					
					wUserLevel = "H"
			
			elif wCnt==0 :
				#############################
				# 相互フォロー中 解除か
				if wARR_DBData['level_tag']=="G" :
					if wARR_DBData['send_cnt']>=gVal.DEF_STR_TLNUM['LEVEL_B_Cnt'] :
						wUserLevel = "B+"
					elif wARR_DBData['send_cnt']>=1 :
						wUserLevel = "B"
					else:
						wUserLevel = "C+"
				
				#############################
				# 片フォロワー 解除か
				elif wARR_DBData['level_tag']=="H" :
					
					wUserLevel = "E"
			
			#############################
			# 連ファボカウント更新
			if wARR_DBData['renfavo_cnt']!=wCnt :

				print("xxx1")

				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_RenFavo( wID, wCnt )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_RenFavo is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# ユーザレベルの変更の実行
			if wUserLevel!=None :
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_UserLevel is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# VIPリアクション監視チェック
#####################################################
	def VIP_ReactionCheck( self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "VIP_ReactionCheck"
		
		#############################
		# VIP監視ユーザの取得
		wARR_VIPuser = self.OBJ_Parent.GetVIPUser()
		if len( wARR_VIPuser )==0 :
			### 規定以内は除外
			wStr = "●VIP監視対象がないため 処理スキップ" + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['vip_ope'] ), inThreshold=gVal.DEF_STR_TLNUM['forVipOperationSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			### 規定以内は除外
			wStr = "●VIPリアクション監視期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		self.OBJ_Parent.ARR_ReacrionUserID = []
		for wUserID in wARR_VIPuser :
			wUserID = str(wUserID)
			
			#############################
			# 取得開始の表示
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "VIPリアクションチェック中: user=" + gVal.ARR_NotReactionUser[wUserID]['screen_name'] )
			wCount = gVal.DEF_STR_TLNUM['vipReactionTweetLine']
			
			#############################
			# 直近のツイートを取得
			wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
				 inID=wUserID, inCount=wCount )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: GetTL"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wTweetRes['Responce'])==0 :
				wRes['Reason'] = "Tweet is not get: user=" + gVal.ARR_NotReactionUser[wUserID]['screen_name']
				gVal.OBJ_L.Log( "D", wRes )
				continue
			
			#############################
			# チェック
			# いいね、リツイート、引用リツイートしたユーザ
			
			###ウェイト初期化
			self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
			
			wFLG_ZanCountSkip = False
			for wTweet in wTweetRes['Responce'] :
				###ウェイトカウントダウン
				if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
					break	###ウェイト中止
				wFLG_ZanCountSkip = False
				
				###日時の変換
				wTime = CLS_TIME.sTTchg( wRes, "(1)", wTweet['created_at'] )
				if wTime['Result']!=True :
					continue
				wTweet['created_at'] = wTime['TimeDate']
				
				#############################
				# 期間内のTweetか
				wGetLag = CLS_OSIF.sTimeLag( str( wTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forVipReactionTweetSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外= 古いツイートなので処理しない
###					wStr = "●古いリプライのためスキップします"
###					CLS_OSIF.sPrn( wStr )
					wFLG_ZanCountSkip = True
					continue
				
				#############################
				# ツイートチェック
###				wSubRes = self.OBJ_Parent.ReactionTweetCheck( wUserID, wTweet )
###				wSubRes = self.OBJ_Parent.ReactionTweetCheck( wUserID, wTweet, True )
				wSubRes = self.OBJ_Parent.ReactionTweetCheck( wUserID, wTweet, inMention=False, inVIPon=True )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "ReactionTweetCheck is failed"
					gVal.OBJ_L.Log( "B", wRes )
					continue
			
			#############################
			# チェック
			# メンションしたユーザ
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "VIPリアクションチェック中：メンション: user=" + gVal.ARR_NotReactionUser[wUserID]['screen_name'] )
			
			wSubRes = gVal.OBJ_Tw_IF.GetMyMentionLookup( wUserID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetRefRetweetLookup): Tweet ID: " + wTweetID + " user=" + gVal.ARR_NotReactionUser[wUserID]['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			###ウェイト初期化
			self.OBJ_Parent.Wait_Init( inZanNum=len( wSubRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
			
			wFLG_ZanCountSkip = False
			wKeylist = list( wSubRes['Responce'].keys() )
			for wReplyID in wKeylist :
				###ウェイトカウントダウン
				if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
					break	###ウェイト中止
				wFLG_ZanCountSkip = False
				
				###日時の変換
				wTime = CLS_TIME.sTTchg( wRes, "(2)", wSubRes['Responce'][wReplyID]['created_at'] )
				if wTime['Result']!=True :
					continue
				wSubRes['Responce'][wReplyID]['created_at'] = wTime['TimeDate']
				
				#############################
				# 期間内のTweetか
				wGetLag = CLS_OSIF.sTimeLag( str( wSubRes['Responce'][wReplyID]['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forVipReactionTweetSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(2)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外= 古いツイートなので処理しない
###					wStr = "●古いリプライのためスキップします"
###					CLS_OSIF.sPrn( wStr )
					wFLG_ZanCountSkip = True
					continue
				
				#############################
				# チェック対象のツイート表示
				wStr = '\n' + "--------------------" + '\n' ;
				wStr = wStr + "チェック中: " + '\n' ;
				wStr = wStr + wSubRes['Responce'][wReplyID]['reply_text'] ;
				CLS_OSIF.sPrn( wStr )
				
				wID = str(wSubRes['Responce'][wReplyID]['id'])
				
				#############################
				# ユーザ情報を取得する
				wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=wID )
				if wUserInfoRes['Result']!=True :
					wRes['Reason'] = "Twitter Error: @" + wUserInfoRes['Responce']['screen_name']
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				###ユーザ単位のリアクションチェック
###				wReactionRes = self.OBJ_Parent.ReactionUserCheck( wUserInfoRes['Responce'], wSubRes['Responce'][wReplyID] )
				wReactionRes = self.OBJ_Parent.ReactionUserCheck( wUserInfoRes['Responce'], wSubRes['Responce'][wReplyID], inMention=True, inVIPon=True )
				if wReactionRes['Result']!=True :
					wRes['Reason'] = "Twitter Error(ReactionUserCheck 4): Tweet ID: " + str(wSubRes['Responce'][wReplyID]['id'])
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wReactionRes['Responce']==True :
					wStr = "〇リプライ検出: " + wUserInfoRes['Responce']['screen_name']
					CLS_OSIF.sPrn( wStr )
					
					### トラヒック記録
					CLS_Traffic.sP( "r_vip" )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "vip_ope", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['reaction']
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# いいね情報送信
#####################################################
	def SendFavoDate( self, inFLG_Force=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "SendFavoDate"
		
		#############################
		# いいね情報を送信する日時か
		wGetLag = CLS_OSIF.sTimeLag( str(gVal.STR_Time['send_favo']), inThreshold=gVal.DEF_VAL_WEEK )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed(1)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		###強制じゃなければ判定する
		if inFLG_Force==False :
			if wGetLag['Beyond']==False :
				###期間内
				###  次へ
				wStr = "●いいね送信期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
				CLS_OSIF.sPrn( wStr )
				wRes['Result'] = True
				return wRes
		
		wRes['Responce'] = False
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "いいね情報送信" )
		
		#############################
		# DBのいいね情報取得
		wResDB = gVal.OBJ_DB_IF.GetFavoData_SendFavo()
		if wResDB['Result']!=True :
			wRes['Reason'] = "GetFavoData_SendFavo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_RateFavoDate = wResDB['Responce']
		
		if len( wARR_RateFavoDate )==0 :
			#############################
			# 現時間を設定
			wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "send_favo", gVal.STR_Time['TimeDate'] )
			if wTimeRes['Result']!=True :
				wRes['Reason'] = "SetTimeInfo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			###	gVal.STR_Time['send_favo']
			
			wStr = "●いいね情報 送信者はいませんでした" + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		### 計測開始日付
		wNowTD = str(wGetLag['InputTime']).split(" ")
		wNowTD = wNowTD[0]
		
		### ヘッダの設定
		wTrendHeader_Pattern = "いいね情報(回数)送信"
		wTrendHeader = wTrendHeader_Pattern + " (" + wNowTD + " から" + str(gVal.DEF_STR_TLNUM['favoSendsCnt']) + "回以上)"
		
		wSendUserNum = 0
		wSendTweet = []
		wSendTweet.append( wTrendHeader + '\n' )
		wSendTweetIndex = 0
		wSendCnt = 0
		#############################
		# タグの設定
		wTrendTag = ""
		if gVal.STR_UserInfo['TrendTag']!="" and \
		   gVal.STR_UserInfo['TrendTag']!=None :
			wTrendTag = '\n' + "#" + gVal.STR_UserInfo['TrendTag']
		
		wARR_SendID = []	#送信したID
		wFLG_Header = False
		wKeylist = list( wARR_RateFavoDate.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			#############################
			# リアクション 規定回以上は送信
			
			#############################
			# リアクション禁止ユーザは除外する
			wUserRes = self.OBJ_Parent.CheckExtUser( wARR_RateFavoDate[wID], "リアクション禁止ユーザ", False )
			if wUserRes['Result']!=True :
				wRes['Reason'] = "CheckExtUser failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wUserRes['Responce']==False :
				### 禁止あり=除外
				continue
			
			#############################
			# 無反応レベルは除外する
###			if wARR_RateFavoDate[wID]['level_tag']=="D-" or wARR_RateFavoDate[wID]['level_tag']=="G" or wARR_RateFavoDate[wID]['level_tag']=="G-" :
			if wARR_RateFavoDate[wID]['level_tag']=="D-" or wARR_RateFavoDate[wID]['level_tag']=="G" or wARR_RateFavoDate[wID]['level_tag']=="G+" or \
			   wARR_RateFavoDate[wID]['level_tag']=="H"  or wARR_RateFavoDate[wID]['level_tag']=="H+" :
				continue
			
			#############################
			# リアクション 規定回以上は送信
			if wARR_RateFavoDate[wID]['rfavo_n_cnt']>=gVal.DEF_STR_TLNUM['favoSendsCnt'] :
				
				### 送信したIDで確定
				wARR_SendID.append( wID )
				
				wSendCnt += 1
				#############################
				# 1行設定
				wLine = wARR_RateFavoDate[wID]['screen_name'] + " : " + \
				        str(wARR_RateFavoDate[wID]['rfavo_n_cnt']) + \
				        "(" + str(wARR_RateFavoDate[wID]['rfavo_cnt']) + ")" + '\n'
				
				wFLG_Header = False
				if ( len( wSendTweet[wSendTweetIndex] ) + len( wLine ) + len( wTrendTag ) )<140 :
					wSendTweet[wSendTweetIndex] = wSendTweet[wSendTweetIndex] + wLine
				else:
					### タグの付加
					wSendTweet[wSendTweetIndex] = wSendTweet[wSendTweetIndex] + wTrendTag
					
					### 次のリストにヘッダの設定
					wSendTweet.append( wTrendHeader + '\n' + wLine )
					wSendTweetIndex += 1
					wFLG_Header = True
			
		if wSendCnt==0 :
			#############################
			# 送信者がいない場合
			
			#############################
			# 現時間を設定
			wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "send_favo", gVal.STR_Time['TimeDate'] )
			if wTimeRes['Result']!=True :
				wRes['Reason'] = "SetTimeInfo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			###	gVal.STR_Time['send_favo']
			
			wStr = "●いいね情報 送信者はいませんでした" + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		### 最後のリストにタグの付加
		if wFLG_Header==False :
			wSendTweet[wSendTweetIndex] = wSendTweet[wSendTweetIndex] + wTrendTag
		
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
				
				if wTweet['text'].find( wTrendHeader_Pattern )==0 :
					###日時の変換
					wTime = CLS_TIME.sTTchg( wRes, "(3)", wTweet['created_at'] )
					if wTime['Result']!=True :
						continue
					wTweet['created_at'] = wTime['TimeDate']
					
					###ユーザ単位のリアクションチェック
					wReactionRes = self.OBJ_Parent.ReactionUserCheck( wTweet['user'], wTweet )
					if wReactionRes['Result']!=True :
						wRes['Reason'] = "Twitter Error(ReactionUserCheck 4): Tweet ID: " + str(wTweet['id'])
						gVal.OBJ_L.Log( "B", wRes )
						continue
					
					wTweetRes = gVal.OBJ_Tw_IF.DelTweet( wID )
					if wTweetRes['Result']!=True :
						wRes['Reason'] = "Twitter API Error(2): " + wTweetRes['Reason'] + " id=" + str(wID)
						gVal.OBJ_L.Log( "B", wRes )
					else:
						wStr = "いいね情報ツイートを削除しました。" + '\n'
						wStr = wStr + "------------------------" + '\n'
						wStr = wStr + wTweet['text'] + '\n'
						CLS_OSIF.sPrn( wStr )
		
		#############################
		# ツイートする
		for wLine in wSendTweet :
			wTweetRes = gVal.OBJ_Tw_IF.Tweet( wLine )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(3): " + wTweetRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			#############################
			# 送信完了
			wStr = "いいね情報を送信しました。" + '\n'
			wStr = wStr + "------------------------" + '\n'
			wStr = wStr + wLine + '\n'
			CLS_OSIF.sPrn( wStr )
			
		
		#############################
		# ログに記録
		gVal.OBJ_L.Log( "T", wRes, "いいね情報送信(Twitter)" )
		
		#############################
		# いいね者送信日時を更新する
		wResDB = gVal.OBJ_DB_IF.UpdateFavoData_SendFavo( wARR_SendID )
		if wResDB['Result']!=True :
			wRes['Reason'] = "UpdateFavoData_SendFavo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 自動リムーブONの場合
		# トロフィー送信者のうち
		# 規定回数を超えたら昇格して相互フォローにする
		for wID in wARR_SendID :
			wID = str(wID)
			
			if wARR_RateFavoDate[wID]['myfollow']==True :
				#############################
				# 既にフォロー済の場合
				#   かつフォロワーで レベルEの場合
				#   レベルBに昇格する
				if wARR_RateFavoDate[wID]['follower']==True and \
				   wARR_RateFavoDate[wID]['level_tag']=="E" :
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "B" )
				continue
			if wARR_RateFavoDate[wID]['follower']==False :
				### フォロワーでなければ、スキップ
				continue
			wCnt = wARR_RateFavoDate[wID]['send_cnt']
			#############################
			# レベルB or C以外か、B+じゃなければここで終わり
			if ( wARR_RateFavoDate[wID]['level_tag']!="B" and \
			   wARR_RateFavoDate[wID]['level_tag']!="C" ) or \
			   wARR_RateFavoDate[wID]['level_tag']=="B+" :
				continue
			
			wCnt += 1
			#############################
			# 昇格トロフィー回数か
			if gVal.DEF_STR_TLNUM['LEVEL_B_Cnt']>wCnt :
				### 規定外 =昇格なし
				continue
			
			### ※昇格あり
			#############################
			# レベルB+昇格へ
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "B+" )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "send_favo", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['send_favo']
		
		wRes['Result'] = True
		return wRes



#####################################################
# 自動リムーブ
#####################################################
###	def AutoRemove( self, inUser ):
	def AutoRemove( self, inUser, inFLG_Force=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "AutoRemove"
		
		wRes['Responce'] = False	#自動リムーブ実行有無
		
		wUserID = str(inUser['id'])
		
		#############################
		# 自動リムーブが無効ならここで終わる
		if gVal.STR_UserInfo['AutoRemove']==False :
			wRes['Result'] = True
			return wRes
		
		wARR_DBData = None
		#############################
		# DBからいいね情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( inUser, inFLG_New=False )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録
		if wSubRes['Responce']['Data']==None :
			wStr = "▽DB未登録ユーザに対する自動リムーブ検出"
			wRes['Reason'] = wStr + ": " + inUser['screen_name']
			gVal.OBJ_L.Log( "N", wRes )
		else:
			wARR_DBData = wSubRes['Responce']['Data']
		
		wFLG_Remove = False
		#############################
		# フォロー者の場合
		#   Twitterからリムーブする
		if gVal.OBJ_Tw_IF.CheckMyFollow( wUserID )==True :
###			if wARR_DBData!=None :
			if wARR_DBData!=None and inFLG_Force==False:
				#############################
				# 期間比較値
				# いいねありの場合、
				#   =いいね日時
				# いいねなしの場合、
				#   =登録日時
				if str(wARR_DBData['rfavo_date'])!=gVal.DEF_TIMEDATE :
					### いいねあり= いいね日時
					wCompTimeDate = str(wARR_DBData['rfavo_date'])
					wThreshold = gVal.DEF_STR_TLNUM['forListFavoAutoRemoveSec']
				
				else:
					### いいねなし= 登録日時
					wCompTimeDate = str(wARR_DBData['regdate'])
					
					if ( wARR_DBData['level_tag']=="D" or wARR_DBData['level_tag']=="D+" ) and \
					   gVal.OBJ_Tw_IF.CheckFollower( wUserID )==False and \
					   str(wARR_DBData['pfavo_date'])!=gVal.DEF_TIMEDATE :
						### 片フォロー者で、いいねしたことがあるユーザは期間が短い
						wThreshold = gVal.DEF_STR_TLNUM['forListFavoAutoRemoveSec_Short']
					else:
						wThreshold = gVal.DEF_STR_TLNUM['forListFavoAutoRemoveSec']
				
				#############################
				# 自動リムーブ期間か
				wGetLag = CLS_OSIF.sTimeLag( wCompTimeDate, inThreshold=wThreshold )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外= 自動リムーブ対象
					wFLG_Remove = True
			else:
				wFLG_Remove = True
			
			if wFLG_Remove==True :
				#############################
				# リムーブ実行
				wTweetRes = gVal.OBJ_Tw_IF.Remove( wUserID )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error: Remove" + wTweetRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				if wARR_DBData['follower']==True :
					### フォロー者OFF・フォロワーON
					wUserLevel = "D-"
				else:
					### フォロー者OFF・フォロワーOFF
					wUserLevel = "E-"
				
				### ユーザレベル変更
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
				
				### トラヒック記録（フォロー者減少）
				CLS_Traffic.sP( "d_myfollow" )
				
				#############################
				# ログに記録
###				gVal.OBJ_L.Log( "R", wRes, "●自動リムーブ: " + inUser['screen_name'], inID=wUserID )
				if inFLG_Force==True :
					gVal.OBJ_L.Log( "R", wRes, "●自動リムーブ(強制): " + inUser['screen_name'], inID=wUserID )
				else:
					gVal.OBJ_L.Log( "R", wRes, "●自動リムーブ: " + inUser['screen_name'], inID=wUserID )
				
				#############################
				# DBに反映
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, inFLG_MyFollow=False )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				wRes['Responce'] = True		#自動リムーブ実行
		
		#############################
		# 自動リムーブしていれば
		# フォロワーなら
		#   リスト解除→片フォロワーリストへ
		# フォロワーでなければ
		#   リスト解除のみ
		if wFLG_Remove==True :
			if gVal.OBJ_Tw_IF.CheckFollower( wUserID )==True :
				### 片フォロワーリストへ
				wTweetRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( inUser )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "FollowerList_AddUser is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			else:
				### リスト解除へ
				wTweetRes = gVal.OBJ_Tw_IF.FollowerList_Remove( inUser )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "FollowerList_Remove is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		wFLG_Remove = False
		#############################
		# 片フォロワー かつ 片フォローリストの場合
		# あまりにスルーが酷ければ追い出す
		if gVal.OBJ_Tw_IF.CheckFollowListUser( wUserID )==True and \
		   gVal.OBJ_Tw_IF.CheckMyFollow( wUserID )==False and \
		   gVal.OBJ_Tw_IF.CheckFollower( wUserID )==True :
			
			if wARR_DBData!=None :
				if wARR_DBData['level_tag']!="F+" :
					#############################
					# 期間比較値
					# いいねありの場合、
					#   =いいね日時
					# いいねなしの場合、
					#   =登録日時
					if str(wARR_DBData['rfavo_date'])!=gVal.DEF_TIMEDATE :
						### いいねあり= いいね日時
						wCompTimeDate = str(wARR_DBData['rfavo_date'])
					else:
						### いいねなし= 登録日時
						wCompTimeDate = str(wARR_DBData['regdate'])
						
						### 送信回数が規定回数超えてれば、追い出し対象にする
						if gVal.DEF_STR_TLNUM['forAutoRemoveIgnoreCompletelyCnt']<=wARR_DBData['pfavo_cnt'] :
							wFLG_Remove = True
					
					#############################
					# 自動リムーブ期間か
					wGetLag = CLS_OSIF.sTimeLag( wCompTimeDate, inThreshold=gVal.DEF_STR_TLNUM['forAutoRemoveIgnoreCompletelySec'] )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed(1)"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
					if wGetLag['Beyond']==True :
						###期間外= 自動リムーブ対象
						wFLG_Remove = True
			else:
				wFLG_Remove = True
			
			if wFLG_Remove==True :
###				#############################
###				# ブロック→リムーブする
###				wBlockRes = gVal.OBJ_Tw_IF.BlockRemove( wUserID )
###				if wBlockRes['Result']!=True :
###					wRes['Reason'] = "Twitter API Error(BlockRemove): " + wBlockRes['Reason'] + " screen_name=" + str(inUser['screen_name'])
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###				
				### ユーザレベル変更
				wUserLevel = "F+"
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
				
				### トラヒック記録（フォロワー減少）
				CLS_Traffic.sP( "d_follower" )
				
				### ユーザ記録
###				wStr = "●完全スルー期間外のため追い出し"
###				gVal.OBJ_L.Log( "R", wRes, wStr + ": " + str(inUser['screen_name']) )
				wStr = "●完全スルー期間外のため、以後無視"
				gVal.OBJ_L.Log( "R", wRes, wStr + ": " + str(inUser['screen_name']), inID=wUserID )
				
###				#############################
###				# DBに反映
###				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, inFLG_Follower=False )
###				if wSubRes['Result']!=True :
###					###失敗
###					wRes['Reason'] = "UpdateFavoData_Follower is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 自動フォロー
#####################################################
	def AutoFollow( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "AutoFollow"
		
		wRes['Responce'] = False	#自動フォロー実行有無
		
		wUserID = str(inUser['id'])
		
		#############################
		# 自動リムーブが無効ならここで終わる
		if gVal.STR_UserInfo['AutoRemove']==False :
			wRes['Result'] = True
			return wRes
		
		#############################
		# ユーザ情報の取得
		wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=wUserID )
		if wUserInfoRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: @" + inUser['screen_name']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wUser = wUserInfoRes['Responce']
		
		#############################
		# ユーザの状態チェック
		# 以下は除外
		# ・鍵垢
		# ・公式垢
		# ・フォロー者数=0
		# ・フォロー者数=1000以上
		# ・フォロワー数=100未満
		# ・フォロー者＜フォロワー数
		# ・いいね数=0
		# ・ツイート数=100未満
		if wUser['protected']==True or \
		   wUser['verified']==True or \
		   wUser['friends_count']==0 or \
		   wUser['friends_count']>=1000 or \
		   wUser['followers_count']<100 or \
		   wUser['friends_count']<wUser['followers_count'] or \
		   wUser['favourites_count']==0 or \
		   wUser['statuses_count']<100 :
			wRes['Result'] = True
			return wRes
		
		#############################
		# DBからいいね情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wUser )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed(2)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録（ありえない）
		if wSubRes['Responce']['Data']==None :
			wRes['Reason'] = "GetFavoDataOne is no data"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']['FLG_New']==True :
			#############################
			# 新規情報の設定
			wSubRes = self.OBJ_Parent.SetNewFavoData( wUser, wSubRes['Responce']['Data'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "SetNewFavoData is failed(2)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wARR_DBData = wSubRes['Responce']['Data']
		
		#############################
		# いいね情報のチェック
		# 以下は除外
		# ・ユーザレベル F以外
		# ・フォロー者ON
		# ・フォロワーON
		# ・過去にフォローしたこと、されたことがある
		if wARR_DBData['level_tag']!="F" or \
		   wARR_DBData['myfollow']==True or \
		   str(wARR_DBData['myfollow_date'])!=gVal.DEF_TIMEDATE or \
		   wARR_DBData['follower']==True or \
		   str(wARR_DBData['follower_date'])!=gVal.DEF_TIMEDATE :
			wRes['Result'] = True
			return wRes
		
		#############################
		# フォローする
		wTweetRes = gVal.OBJ_Tw_IF.Follow( wUserID, inMute=True )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(Follow): " + wTweetRes['Reason'] + " screen_name=" + str(inUser['screen_name'])
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Responce'] = True		#自動フォロー実行
		
		### 相互フォローリストに追加
		wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wARR_DBData )
		
		### ユーザレベル変更
		wUserLevel = "D+"
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
		
		### トラヒック記録（フォロー者増加）
		CLS_Traffic.sP( "p_myfollow" )
		
		### ユーザ記録
		wStr = "〇自動フォロー"
###		gVal.OBJ_L.Log( "R", wRes, wStr + ": " + str(inUser['screen_name']) )
		gVal.OBJ_L.Log( "R", wRes, wStr + ": " + str(inUser['screen_name']), inID=wUserID )
		
		#############################
		# DBに反映
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, inFLG_MyFollow=True )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "UpdateFavoData_Follower is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# タイムラインフォロー
#####################################################
	def TimelineFollow( self , inCheck=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "TimelineFollow"
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['tl_follow'] ), inThreshold=gVal.DEF_STR_TLNUM['forTimelineFollowSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
###		if wGetLag['Beyond']==False :
		if wGetLag['Beyond']==False and inCheck==True :
			### 規定以内は除外
			wStr = "●タイムラインフォロー期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "タイムラインフォロー中" )
		
		#############################
		# ツイートj情報
		# ※元ソースは見ない仕様とする
		wSTR_User = {
			"id"				: None,
			"name"				: None,
			"screen_name"		: None,
			"description"		: None
		}
#		wSTR_SrcUser = {
#			"id"				: None,
#			"name"				: None,
#			"screen_name"		: None,
#			"description"		: None
#		}
		wSTR_Tweet = {
			"kind"				: None,
			"id"				: None,
			"text"				: None,
#			"sensitive"			: False,
			"created_at"		: None,
			"user"				: wSTR_User,
#			"src_user"			: wSTR_SrcUser,
#			"FLG_agent"			: False,			# いいね候補
			"reason"			: None				# NG理由
		}
		
		#############################
		# 直近のホームタイムラインを取得
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="home", inFLG_Rep=False, inFLG_Rts=True,
			 inID=gVal.STR_UserInfo['id'], inCount=gVal.DEF_STR_TLNUM['TimelineFollowTweetLine'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetTL"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if len(wTweetRes['Responce'])==0 :
			wRes['Reason'] = "Tweet is not get: home timeline"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		#############################
		# チェック
		
		wFLG_ZanCountSkip  = False
		self.ARR_AgentUser = {}
		wTLCnt   = 0
		wFavoCnt = 0
		wFollowNum = 0
		for wTweet in wTweetRes['Responce'] :
			wTLCnt += 1
			###先頭スキップ
			if gVal.DEF_STR_TLNUM['TimelineFollowTweetLine_Skip']>=wTLCnt :
				continue
			
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
				break	###ウェイト中止
			wFLG_ZanCountSkip = False
			
			### いいねチェック回数の限界
			if gVal.DEF_STR_TLNUM['TimelineFollowFavoCheckNum']<=wFavoCnt :
				wStr = "〇完了: いいねチェック回数に到達" ;
				CLS_OSIF.sPrn( wStr )
				break
			
			### フォロー人数の限界
			if gVal.DEF_STR_TLNUM['TimelineFollowNum']<=wFollowNum :
				wStr = "〇完了: フォロー人数の上限に到達" ;
				CLS_OSIF.sPrn( wStr )
				break
			
			###日時の変換
			wTime = CLS_TIME.sTTchg( wRes, "(1)", wTweet['created_at'] )
			if wTime['Result']!=True :
				continue
			wSTR_Tweet['created_at'] = wTime['TimeDate']
			
			#############################
			# ツイート情報を取得
			wSTR_Tweet['id']   = str(wTweet['id'])
			wSTR_Tweet['text'] = str(wTweet['text'])
			wSTR_Tweet['user']['id']          = str(wTweet['user']['id'])
			wSTR_Tweet['user']['name']        = str(wTweet['user']['name'])
			wSTR_Tweet['user']['screen_name'] = str(wTweet['user']['screen_name'])
			wSTR_Tweet['user']['description'] = str(wTweet['user']['description'])
			
			### リツイート
			if "retweeted_status" in wTweet :
				wSTR_Tweet['kind'] = "retweet"
			
			### 引用リツイート
			elif "quoted_status" in wTweet :
				wSTR_Tweet['kind'] = "quoted"
			
			### リプライ
			elif wSTR_Tweet['text'].find("@")>=0 :
				wSTR_Tweet['kind'] = "reply"
			
			### 通常ツイート
			else:
				wSTR_Tweet['kind'] = "normal"
			
			#############################
			# チェック対象のツイート表示
			wStr = '\n' + "--------------------" + '\n' ;
			wStr = wStr + wSTR_Tweet['text'] + '\n' ;
			wStr = wStr + "  time: " + wSTR_Tweet['created_at'] + "  screen_name: " + wSTR_Tweet['user']['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# 相互フォロー もしくは 片フォローの場合
			# スキップする
			if gVal.OBJ_Tw_IF.CheckMutualListUser( wSTR_Tweet['user']['id'] )==True or \
			   gVal.OBJ_Tw_IF.CheckFollowListUser( wSTR_Tweet['user']['id'] )==True :
				wStr = "●スキップ: 相互もしくは片フォロワー" ;
				CLS_OSIF.sPrn( wStr )
				continue
			
			#############################
			# いいね、リツイートしてるユーザ一覧を取得する
			
			#############################
			# いいねの場合
			wSubRes = gVal.OBJ_Tw_IF.GetLikesLookup( wSTR_Tweet['id'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetLikesLookup): Tweet ID: " + wSTR_Tweet['id']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			self.__add_TimelineFollow_AgentUser( wSubRes['Responce'] )
			
			#############################
			# リツイートの場合
			wSubRes = gVal.OBJ_Tw_IF.GetRetweetLookup( wSTR_Tweet['id'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetRetweetLookup): Tweet ID: " + wSTR_Tweet['id']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			self.__add_TimelineFollow_AgentUser( wSubRes['Responce'] )
			
			#############################
			# 引用リツイートの場合
			wSubRes = gVal.OBJ_Tw_IF.GetRefRetweetLookup( wSTR_Tweet['id'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetRefRetweetLookup): Tweet ID: " + wSTR_Tweet['id']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			self.__add_TimelineFollow_AgentUser( wSubRes['Responce'] )
			
			wFavoCnt += 1
			
			#############################
			# 自動フォローしていく
			wKeylist = list( self.ARR_AgentUsers.keys() )
			for wID in wKeylist :
				wID = str(wID)
				
				### フォロー人数の限界
				if gVal.DEF_STR_TLNUM['TimelineFollowNum']<=wFollowNum :
					break
				
				### 自動フォロー
				wSubRes = self.OBJ_Parent.OBJ_TwitterFollower.AutoFollow( self.ARR_AgentUsers[wID] )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "AutoFollow is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				if wSubRes['Responce']==False :
					### 未フォロー
					continue
				
				wFollowNum += 1	#フォローしたのでカウント
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "tl_follow", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['reaction']
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes

	#####################################################
	def __add_TimelineFollow_AgentUser( self, inARR_Users ):
		
		wKeylist = list( inARR_Users.keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			if wID in self.ARR_AgentUsers :
				continue
			
			wSTR_User = {
				"id"				: str(inARR_Users[wID]['id']),
				"name"				: str(inARR_Users[wID]['name']),
				"screen_name"		: str(inARR_Users[wID]['screen_name']),
				"description"		: str(inARR_Users[wID]['description'])
###				
###				"FLG_Checked"		: False
			}
			self.ARR_AgentUsers.update({ wID : wSTR_User })
		
		return




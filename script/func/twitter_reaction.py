#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : リアクション処理
#####################################################

from ktime import CLS_TIME
from osif import CLS_OSIF
from traffic import CLS_Traffic
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterReaction():
#####################################################
	OBJ_Parent = ""				#親クラス実体

	VAL_ReactionCnt = 0			# リアクション回数
###	ARR_Mentions    = {}
	ARR_ReactionTweet = {}		# リアクションツイート情報
	ARR_ReactionUser  = {}		# リアクションユーザ情報
###	ARR_ReacrionUserID = []



#####################################################
# Init
#####################################################
	def __init__( self, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "__init__"
		
		if parentObj==None :
			###親クラス実体の未設定
			wRes['Reason'] = "You have not set the parent class entity for parentObj"
			gVal.OBJ_L.Log( "A", wRes )
			return
		
		self.OBJ_Parent = parentObj
		return



#####################################################
# リアクション設定
#####################################################
	def __setReactionTweet( self, inUser, inTweet, inFLG_Cnt=True, inFLG_Mention=False ):
		
		wID      = str(inUser['id'])
		wTweetID = str(inTweet['id'])
		wText    = str(inTweet['text']).replace( "'", "''" )
		#############################
		# リアクション情報の枠がなければ
		# 枠を作成する
		if wTweetID not in self.ARR_ReactionTweet :
			wCell = {
				"mention"	: inFLG_Mention,	# メンションか True=Mention, False=Mentuin以外
				"id"		: wID,				# ツイートID
				"text"		: wText,			# ツイートテキスト
				"users"		: []				# アクションしたユーザID
			}
			self.ARR_ReactionTweet.update({ wTweetID : wCell })
		
		self.ARR_ReactionTweet[wTweetID]['users'].append( wID )
		
		#############################
		# リアクションユーザ情報の枠がなければ
		# 枠を作成する
		if wID not in self.ARR_ReactionUser :
			wCell = {
				"id"			: wID,
				"screen_name"	: inUser['screen_name'],
				"cnt"			: 0
			}
			self.ARR_ReactionUser.update({ wID : wCell })
		
		#############################
		# メンションではない かつ
		# Cnt = ON の場合、カウントする
		if self.ARR_ReactionTweet[wTweetID]['mention']==False and \
		   inFLG_Cnt==True :
			self.ARR_ReactionUser[wID]['cnt'] += 1
			self.VAL_ReactionCnt += 1
		else:
			return False
		
		return True

	#####################################################
	def __getReactionTweet( self, inTweetID ):
		
		wTweetID = str(inTweetID)
		#############################
		# リアクションユーザ情報の枠
		if wTweetID not in self.ARR_ReactionTweet :
			return None
		
		return self.ARR_ReactionTweet[wTweetID]

	#####################################################
	def __getReactionUser( self, inUserID ):
		
		wUserID = str(inUserID)
		#############################
		# リアクションユーザ情報の枠
		if wUserID not in self.ARR_ReactionUser :
			return None
		
		return self.ARR_ReactionUser[wUserID]

	#####################################################
	def __checkReactionUser( self, inUser ):
		
		wID = str(inUser['id'])
		#############################
		# リアクションユーザ情報の枠
		if wID not in self.ARR_ReactionUser :
			return False	# リアクションなし
		
		if self.ARR_ReactionUser[wID]['cnt']==0 :
			return False	# リアクションなし
		
		return True			# リアクションあり

	#####################################################
	def __getReactionResult(self):
		wResult = {
###			"Judged"		: False,	# 判定済み           True=済み
			"Accept"		: False,	# 受け入れ           True=済み
			"reReaction"	: False		# お返しリアクション True=済み
		}
		return wResult



#####################################################
# リアクションチェック
#####################################################
	def ReactionCheck( self, inFLG_Short=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
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
###		self.ARR_Mentions    = {}
###		self.ARR_Reaction    = {}
		self.ARR_ReactionTweet = {}
		self.ARR_ReactionUser  = {}
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
###		self.OBJ_Parent.ARR_ReacrionUserID = []
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
###			wSubRes = self.OBJ_Parent.ReactionTweetCheck( str(gVal.STR_UserInfo['id']), wTweet, inMention=wMention )
			wSubRes = self.ReactionTweetCheck( str(gVal.STR_UserInfo['id']), wTweet, inMention=wMention )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "ReactionTweetCheck"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
###			if wSubRes['Responce']['Reaction']==True :
###				### リアクション回数+
###				self.VAL_ReactionCnt += 1
###				
###				wKeyuser = list( wSubRes['Responce']['users'].keys() )
###				for wUserID in wKeyuser :
###					if wUserID not in self.ARR_Reaction :
###						wCell = {
###							"user"	: wSubRes['Responce']['users'][wUserID]['user'],
###							"cnt"	: wSubRes['Responce']['users'][wUserID]['cnt']
###						}
###						self.ARR_Reaction.update({ wUserID : wCell })
###					else :
###						self.ARR_Reaction[wUserID]['cnt'] += wSubRes['Responce']['users'][wUserID]['cnt']
###		
		
		#############################
		# チェック
		# メンションしたユーザ
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中：メンション" )
		
		wSubRes = gVal.OBJ_Tw_IF.GetMyMentionLookup()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetMyMentionLookup)"
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
			
###			###日時の変換
###			wTime = CLS_TIME.sTTchg( wRes, "(2)", wSubRes['Responce'][wReplyID]['created_at'] )
###			if wTime['Result']!=True :
###				continue
###			wSubRes['Responce'][wReplyID]['created_at'] = wTime['TimeDate']
###			
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
###			wStr = wStr + wSubRes['Responce'][wReplyID]['reply_text'] ;
			wStr = wStr + wSubRes['Responce'][wReplyID]['text'] ;
			CLS_OSIF.sPrn( wStr )
			
			wID = str(wSubRes['Responce'][wReplyID]['user']['id'])
###			wID = str(wSubRes['Responce'][wReplyID]['id'])
###			
###			#############################
###			# ユーザ情報を取得する
###			wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=wID )
###			if wUserInfoRes['Result']!=True :
###				wRes['Reason'] = "Twitter Error: @" + wUserInfoRes['Responce']['screen_name']
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###			
			###ユーザ単位のリアクションチェック
###			wReactionRes = self.ReactionUserCheck( wUserInfoRes['Responce'], wSubRes['Responce'][wReplyID], inMention=True )
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wReplyID]['user'], wSubRes['Responce'][wReplyID], inMention=True )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 4): Tweet ID: " + wID
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
###			if wReactionRes['Responce']==True :
			if wReactionRes['Responce']['Accept']==True :
###				wStr = "〇リプライ検出: " + wUserInfoRes['Responce']['screen_name']
				wStr = "〇リプライ検出: " + wSubRes['Responce'][wReplyID]['user']['screen_name']
				CLS_OSIF.sPrn( wStr )
				
###				### リアクション回数+
###				self.VAL_ReactionCnt += 1
###				
###				### メンションユーザ情報
###				if wReplyID not in self.ARR_Mentions :
###					wCell = {
###						"id"	: wSubRes['Responce'][wReplyID]['reply_id'],
###						"text"	: wSubRes['Responce'][wReplyID]['reply_text'],
###						"users"	: {}
###					}
###					self.ARR_Mentions.update({ wReplyID : wCell })
###				
###				if wID not in self.ARR_Mentions['users'] :
###					self.ARR_Mentions['users'].update({ wID : wUserInfoRes['Responce'] })
###				
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
# リアクションツイートチェック
#####################################################
	def ReactionTweetCheck( self, inMyUserID, inTweet, inMention=False, inVIPon=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "ReactionTweetCheck"
		
###		wRes['Responce'] = {
###			"Reaction"	: False,
###			"users"		: {}
###		}
###		
		wTweet = inTweet
		
		wUserID      = str( wTweet['user']['id'] )
		wTweet['id'] = str(wTweet['id'])
		wTweetID     = wTweet['id']
		#############################
		# 自分のツイート以外は処理を抜ける
		if inMyUserID!=wUserID :
			### 自分のツイートではない＝正常終了
			wRes['Result'] = True
			return wRes
		
		#############################
		# 警告ツイートは除外
		wSubRes = gVal.OBJ_DB_IF.CheckCautionTweet( wTweetID )
		if wSubRes==True :
			### 警告ツイートは除外＝正常終了
			wRes['Result'] = True
			return wRes
		
		#############################
		# 自分かのフラグ
		wFLG_MyUser = False
		if str(gVal.STR_UserInfo['id'])==wUserID :
			wFLG_MyUser = True
		
		#############################
		# チェック対象のツイート表示
		wStr = '\n' + "--------------------" + '\n' ;
		wStr = wStr + "チェック中: " + str(wTweet['created_at']) + '\n' ;
		wStr = wStr + wTweet['text'] + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# いいねチェック
		wSubRes = gVal.OBJ_Tw_IF.GetLikesLookup( wTweetID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetLikesLookup): Tweet ID: " + wTweetID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wKeylist = list( wSubRes['Responce'].keys() )
		for wID in wKeylist :
			wID = str(wID)
			###ユーザ単位のリアクションチェック
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet, wFLG_MyUser, inMention=inMention )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
###			if wReactionRes['Responce']==True :
			if wReactionRes['Responce']['Accept']==True :
				wStr = "〇いいね検出: " + wSubRes['Responce'][wID]['screen_name'] + '\n'
				CLS_OSIF.sPrn( wStr )
				
###				### リアクション済み
###				wRes['Responce']['Reaction'] = wReactionRes['Responce']
###				
###				if wID not in wRes['Responce']['users'] :
###					wCell = {
###						"user"	: wSubRes['Responce'][wID],
###						"cnt"	: 1
###					}
###					wRes['Responce']['users'].update({ wID : wCell })
###				else :
###					wRes['Responce']['users'][wID]['cnt'] += 1
				
				### トラヒック記録
				if wFLG_MyUser==True :
					CLS_Traffic.sP( "r_reaction" )
					CLS_Traffic.sP( "r_favo" )
					if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
						CLS_Traffic.sP( "r_in" )
					else:
						CLS_Traffic.sP( "r_out" )
				else:
					CLS_Traffic.sP( "r_vip" )
		
		wFLG_VIPretweet = False
		#############################
		# VIP かつ VIPリツイートが有効で
		# VIPリツイートタグを含む場合
		#   VIPリツイート対象にする
		if inVIPon==True and gVal.STR_UserInfo['VipTag']!=gVal.DEF_NOTEXT :
			wTag = "#" + gVal.STR_UserInfo['VipTag']
			if wTweet['text'].find( wTag )>=0 :
				wFLG_VIPretweet = True
		
		#############################
		# リツイートチェック
		wSubRes = gVal.OBJ_Tw_IF.GetRetweetLookup( wTweetID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetRetweetLookup): Tweet ID: " + wTweetID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wKeylist = list( wSubRes['Responce'].keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			### VIPリツイート対象のツイートで
			### 既にリツイート済みなら フラグを落とす
			if wFLG_VIPretweet==True :
				if str(gVal.STR_UserInfo['id'])==wID :
					wFLG_VIPretweet = False	#フラグ落とす
			
			###ユーザ単位のリアクションチェック
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet, wFLG_MyUser, inMention=inMention )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 2): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
###			if wReactionRes['Responce']==True :
			if wReactionRes['Responce']['Accept']==True :
				wStr = "〇リツイート検出: " + wSubRes['Responce'][wID]['screen_name']
				CLS_OSIF.sPrn( wStr )
				
###				### リアクション済み
###				wRes['Responce']['Reaction'] = wReactionRes['Responce']
###				
###				if wID not in wRes['Responce']['users'] :
###					wCell = {
###						"user"	: wSubRes['Responce'][wID],
###						"cnt"	: 1
###					}
###					wRes['Responce']['users'].update({ wID : wCell })
###				else :
###					wRes['Responce']['users'][wID]['cnt'] += 1
###				
				### トラヒック記録
				if wFLG_MyUser==True :
					CLS_Traffic.sP( "r_reaction" )
					CLS_Traffic.sP( "r_favo" )
					if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
						CLS_Traffic.sP( "r_in" )
					else:
						CLS_Traffic.sP( "r_out" )
				else:
					CLS_Traffic.sP( "r_vip" )
		
		#############################
		# VIPリツイート対象なら
		# リツイートする
		if wFLG_VIPretweet==True :
			### リツイート実施
			wSubRes = gVal.OBJ_Tw_IF.Retweet( wTweetID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(Retweet): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
			else:
				wStr = "〇VIPリツイート実行"
				CLS_OSIF.sPrn( wStr )
		
		#############################
		# 引用リツイートチェック
		wSubRes = gVal.OBJ_Tw_IF.GetRefRetweetLookup( wTweetID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetRefRetweetLookup): Tweet ID: " + wTweetID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wKeylist = list( wSubRes['Responce'].keys() )
		for wID in wKeylist :
			wID = str(wID)
			###ユーザ単位のリアクションチェック
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet, wFLG_MyUser, inMention=inMention )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 3): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
###			if wReactionRes['Responce']==True :
			if wReactionRes['Responce']['Accept']==True :
				wStr = "〇引用リツイート検出: " + wSubRes['Responce'][wID]['screen_name'] ;
				CLS_OSIF.sPrn( wStr )
				
###				### リアクション済み
###				wRes['Responce']['Reaction'] = wReactionRes['Responce']
###				
###				if wID not in wRes['Responce']['users'] :
###					wCell = {
###						"user"	: wSubRes['Responce'][wID],
###						"cnt"	: 1
###					}
###					wRes['Responce']['users'].update({ wID : wCell })
###				else :
###					wRes['Responce']['users'][wID]['cnt'] += 1
###				
				### トラヒック記録
				if wFLG_MyUser==True :
					CLS_Traffic.sP( "r_reaction" )
					CLS_Traffic.sP( "r_favo" )
					if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
						CLS_Traffic.sP( "r_in" )
					else:
						CLS_Traffic.sP( "r_out" )
				else:
					CLS_Traffic.sP( "r_vip" )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# リアクションユーザチェック
#####################################################
	def ReactionUserCheck( self, inUser, inTweet, inFLG_MyUser=True, inMention=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "ReactionUserCheck"
		
###		wRes['Responce'] = {
###			"Judged"	: False,	# 判定済み     True=済み
###			"Accept"	: False,	# 受け入れ     True=済み
###			"Reaction"	: False		# リアクション True=済み
###		}
		wRes['Responce'] = self.__getReactionResult()
		
		wUserID = str(inUser['id'])
		
		wFLG_Action = True
		#############################
		# リアクション済みのユーザは除外
###		if wUserID in self.ARR_ReacrionUserID :
###			wFLG_Action = False	#除外
		if self.__checkReactionUser(inUser)==True :
			wFLG_Action = False	#除外
		
		wNewUser = False
		#############################
		# DBからいいね情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( inUser )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録
		if wSubRes['Responce']['Data']==None :
			wRes['Reason'] = "GetFavoDataOne is no data"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']['FLG_New']==True :
			wNewUser = True	#新規登録
			#############################
			# 新規情報の設定
###			wSubRes = self.SetNewFavoData( inUser, wSubRes['Responce']['Data'] )
			wSubRes = self.OBJ_Parent.SetNewFavoData( inUser, wSubRes['Responce']['Data'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "SetNewFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wARR_DBData = wSubRes['Responce']['Data']
		
		wTweetID = str( inTweet['id'] )
		#############################
		# 同じアクションはノーリアクション
		if wARR_DBData['rfavo_id']==wTweetID :
			wFLG_Action = False	#除外
		
		#############################
		# 前のリアクションより最新なら新アクション
		if wFLG_Action==True :
			wSubRes = CLS_OSIF.sCmpTime( inTweet['created_at'], inDstTD=wARR_DBData['rfavo_date'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "sCmpTime is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Future']==False :
				### 古いアクションなので除外
				wFLG_Action = False	#除外
		
		#############################
		# リアクション禁止ユーザか
###		wUserRes = self.CheckExtUser( wARR_DBData, "リアクション検出" )
		wUserRes = self.OBJ_Parent.CheckExtUser( wARR_DBData, "リアクション検出" )
		if wUserRes['Result']!=True :
			wRes['Reason'] = "CheckExtUser failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wUserRes['Responce']==False :
			### 禁止あり=除外
			
			if wFLG_Action==True :
				### 除外してない場合
				
				### いいね情報を更新する
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				### リアクション情報設定・カウントなし
				self.__setReactionTweet( inUser, inTweet, inFLG_Cnt=False, inFLG_Mention=inMention )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# 無反応のレベルタグ
		if wARR_DBData['level_tag']=="C-" or wARR_DBData['level_tag']=="D-" or wARR_DBData['level_tag']=="E+" or wARR_DBData['level_tag']=="E-" or \
		   wARR_DBData['level_tag']=="H-" or wARR_DBData['level_tag']=="L" or wARR_DBData['level_tag']=="Z" or wARR_DBData['level_tag']=="Z-" :
			
			### 報告対象の表示と、ログに記録
			gVal.OBJ_L.Log( "RR", wRes, "●リアクション拒否(レベルタグ) ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wARR_DBData['level_tag'], inID=wUserID )
			
			if wFLG_Action==True :
				### 除外してない場合
				
				### いいね情報を更新する
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				### リアクション情報設定・カウントなし
				self.__setReactionTweet( inUser, inTweet, inFLG_Cnt=False, inFLG_Mention=inMention )
			
###			wRes['Responce']['Judged'] = True	#判定済み
			wRes['Result'] = True
			return wRes
		
		#############################
		# レベルタグによるランダム実行
		elif wARR_DBData['level_tag']=="G" or wARR_DBData['level_tag']=="G+" or wARR_DBData['level_tag']=="H" or wARR_DBData['level_tag']=="H+" :
			if wFLG_Action==False :
				### 除外してる場合、終わり
				wRes['Result'] = True
				return wRes
			
			wRand = CLS_OSIF.sGetRand(100)
			if wRand>=gVal.DEF_STR_TLNUM['forAutoFavoLevelRunRand'] :
				### 乱数による拒否
				
				### いいね情報を更新する
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				### リアクション情報設定・カウントなし
				self.__setReactionTweet( inUser, inTweet, inFLG_Cnt=False, inFLG_Mention=inMention )
				
				### 報告対象の表示と、ログに記録
				gVal.OBJ_L.Log( "RR", wRes, "●リアクション拒否(ランダム) ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wARR_DBData['level_tag'], inID=wUserID )
				
###				wRes['Responce']['Judged'] = True	#判定済み
				wRes['Result'] = True
				return wRes
			
			#############################
			# 期間を過ぎたツイートは除外
			wGetLag = CLS_OSIF.sTimeLag( str( inTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forAutoFavoTweet_B_Sec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				### 規定外 =古いツイートなので除外
				
				### いいね情報を更新する
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				### リアクション情報設定・カウントなし
				self.__setReactionTweet( inUser, inTweet, inFLG_Cnt=False, inFLG_Mention=inMention )
				
				### 報告対象の表示と、ログに記録
				gVal.OBJ_L.Log( "RR", wRes, "●リアクション拒否(古いツイート) ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wARR_DBData['level_tag'], inID=wUserID )
				
###				wRes['Responce']['Judged'] = True	#判定済み
				wRes['Result'] = True
				return wRes
		
		#############################
		# アクションが有効なら、リアクション済みにする
		if wFLG_Action==True :
			#############################
			# いいね情報を更新する
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			### リアクション情報設定・カウントあり
			self.__setReactionTweet( inUser, inTweet, inFLG_Cnt=True, inFLG_Mention=inMention )
			
			#############################
			# リアクション済みID
###			self.ARR_ReacrionUserID.append( wUserID )
			wRes['Responce']['Accept'] = True	#リアクション受け入れ
			
			#############################
			# レベル昇格
			# 前提: フォロワー
			wUserLevel = None
			wCnt = wARR_DBData['rfavo_n_cnt'] + 1
			if wARR_DBData['level_tag']=="C-" or wARR_DBData['level_tag']=="E+" or wARR_DBData['level_tag']=="E-" or wARR_DBData['level_tag']=="F+" :
				if gVal.OBJ_Tw_IF.CheckMyFollow( wUserID )==True and \
				   gVal.OBJ_Tw_IF.CheckFollower( wUserID )==True :
					wUserLevel = "C+"
				
				elif gVal.OBJ_Tw_IF.CheckMyFollow( wUserID )==False and \
				   gVal.OBJ_Tw_IF.CheckFollower( wUserID )==True :
					wUserLevel = "E"
				
				if wUserLevel!=None :
					### ユーザレベル変更
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
					
					### 報告対象の表示と、ログに記録
					gVal.OBJ_L.Log( "RR", wRes, "〇リアクションにより昇格 ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wUserLevel, inID=wUserID )
			
			#############################
			# 相互レベルCへ昇格
			# ・トロフィー資格者
			# ・レベルE
			# ・フォロー者OFF
			# ・フォロワーON
			elif wCnt>=gVal.DEF_STR_TLNUM['favoSendsCnt'] and \
			     wARR_DBData['level_tag']=="E" and \
			     gVal.OBJ_Tw_IF.CheckMyFollow( wUserID )==False and \
			     gVal.OBJ_Tw_IF.CheckFollower( wUserID )==True :
				
				### フォロー＆ミュートする
				wTweetRes = gVal.OBJ_Tw_IF.Follow( wUserID, inMute=True )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error: Follow" + wTweetRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
				
				### 相互フォローリストに追加
				wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wARR_DBData )
				
				### ユーザレベル変更
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, "C" )
				
				### トラヒック記録（フォロー者増加）
				CLS_Traffic.sP( "p_myfollow" )
				
				### ログに記録
				gVal.OBJ_L.Log( "R", wRes, "自動フォロー（昇格）: " + wARR_DBData['screen_name'], inID=wUserID )
				
				### DBに反映
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, inFLG_MyFollow=True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
			
			#############################
			# リアクションへのリアクション
			wSubRes = self.__ReactionUserCheck_PutReaction( inUser, wARR_DBData, inTweet, inFLG_MyUser, wNewUser, inMention )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "__ReactionUserCheck_ListInd is failed"
				gVal.OBJ_L.Log( "B", wRes )
			
			#############################
			# リアクション済み
###			wRes['Responce']['Reaction'] = True	#リアクション済み
###			wRes['Responce']['Judged']   = True	#判定済み
			wRes['Responce']['reReaction'] = True	#お返しリアクション済み
		
		wRes['Result'] = True
		return wRes



	#####################################################
	# リアクションユーザへのリアクション
	#####################################################
	def __ReactionUserCheck_PutReaction( self, inUser, inData, inTweet, inFLG_MyUser=True, inNewUser=False, inMention=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "__ReactionUserCheck_PutReaction"
		
		if inFLG_MyUser==True :
			#############################
			# 期間外のTweetで 新規ユーザに対しては
			# リアクションを返さない(仕様)
			if inNewUser==True :
				wGetLag = CLS_OSIF.sTimeLag( str( inTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外= とりま通知しない
					wStr = "●新規ユーザのため非通知: " + inData['screen_name'] + '\n' ;
					CLS_OSIF.sPrn( wStr )
					
					wRes['Result'] = True
					return wRes
			
			#############################
			# 相互フォローリスト かつ 片フォローの場合
			# リムーブ処理する
			if gVal.OBJ_Tw_IF.CheckMutualListUser( inUser['id'] )==True and \
			   inData['myfollow']==True and inData['follower']==False :
				### 自動リムーブする
				wSubRes = self.OBJ_Parent.OBJ_TwitterFollower.AutoRemove( inUser=inUser, inFLG_Force=True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "AutoRemove is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				if wSubRes['Responce']==True :
					### 自動リムーブしたらここで終わる
					wRes['Result'] = True
					return wRes
			
			wFLG_Iine = False
			#############################
			# 相互フォローリスト もしくは 片フォロワーリスト の場合
			#   ランダム抽選で受かれば、おかえしいいね
			if gVal.OBJ_Tw_IF.CheckSubscribeListUser( inUser['id'] )==False and \
			   ( gVal.OBJ_Tw_IF.CheckMutualListUser( inUser['id'] )==True or gVal.OBJ_Tw_IF.CheckFollowListUser( inUser['id'] )==True ) :
				
				wRand = CLS_OSIF.sGetRand(100)
				if wRand<gVal.DEF_STR_TLNUM['forReactionListUserRand'] :
					wFLG_Iine = True
			
			else:
				wFLG_Iine = True
			
			#############################
			# 自動おかえしいいねする
			if gVal.DEF_STR_TLNUM['autoRepFavo']==True and wFLG_Iine==True and inMention==False :
				wSubRes = self.OBJ_Parent.OBJ_TwitterFavo.AutoFavo( inUser, gVal.DEF_STR_TLNUM['forAutoFavoReturnFavoSec'] )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "AutoFavo is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# リスト通知をおこなう
		if gVal.STR_UserInfo['ListName']!=gVal.DEF_NOTEXT :
			wSubRes = self.__ReactionUserCheck_ListInd( inData )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "__ReactionUserCheck_ListInd is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 自動フォローする
		# ※おそらく新規ユーザ
		if inMention==False :
			wSubRes = self.OBJ_Parent.OBJ_TwitterFollower.AutoFollow( inUser )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "AutoFollow is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wRes['Result'] = True
		return wRes



	#####################################################
	# リスト通知をおこなう
	#####################################################
	def __ReactionUserCheck_ListInd( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "__ReactionUserCheck_ListInd"
		
		#############################
		# 前回が今日以外なら通知する
		wNowDate = str(gVal.STR_Time['TimeDate'])
		wNowDate = wNowDate.split(" ")
		wNowDate = wNowDate[0]
		wRateDate = str(inData['list_ind_date'])
		wRateDate = wRateDate.split(" ")
		wRateDate = wRateDate[0]
		if wNowDate==wRateDate :
			### 今日なので通知しない
			wStr = "●今日は通知済み: " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# リストがTwitterにあるか確認
		wSubRes = gVal.OBJ_Tw_IF.ListInd_AddUser( inData )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(InserttListIndUser): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
			### 既に登録済み
			wStr = "●リスト通知済み: " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# DBに登録する
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_ListIndData( inData )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateFavoData_ListIndData Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wTextReason = "リスト通知: " + inData['screen_name']
		gVal.OBJ_L.Log( "RR", wRes, wTextReason, inID=inData['id'] )
		
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
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "ReactionResult"
		
		#############################
		# メンション情報 表示
		wStr = "------------------------------" + '\n'
		wStr = wStr + "メンション結果" + '\n'
		wStr = wStr + "------------------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
###		wStr = ""
###		if len(self.ARR_Mentions)==0 :
###			### 情報なしの場合
###			wStr = "(情報なし)" + '\n'
###		
###		else:
###			### 情報ありの場合
###			
###			#############################
###			# メンション情報の表示
###			wKeylist = list( self.ARR_Mentions.keys() )
###			for wID in wKeylist :
###				wStr = wStr + self.ARR_Mentions[wID]['text'] + '\n'
###				wStr = wStr + "  users: "
###				wKeylist2 = list( self.ARR_Mentions[wID]['users'].keys() )
###				for wUserID in wKeylist2 :
###					wStr = wStr + self.ARR_Mentions[wID]['users'][wUserID]['screen_name'] + " "
		wStr = ""
		wKeylist = list( self.ARR_ReactionTweet.keys() )
		wFLG_Mention = False
		for wID in wKeylist :
			if self.ARR_ReactionTweet[wID]['mention']==False :
				continue
			
			### メンションユーザ名
			wUserName = self.__getReactionUser( inUserID )
			if wUserName==None :
				### ありえない
				wUserName = "(?none?)"
			
			wStr = wStr + self.ARR_Mentions[wID]['text'] + '\n'
			wStr = wStr + "  user: " + wUserName['screen_name'] + '\n' + '\n'
			wFLG_Mention = True
		
		if wFLG_Mention==False :
			### 情報なしの場合
			wStr = "(情報なし)" + '\n'
		
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
###			if wID not in self.ARR_Reaction :
###				wCell = {
###					"user"	: wARR_RateUserB[wID],
###					"cnt"	: 0
###				}
###				self.ARR_Reaction.update({ wID : wCell })
			if wID not in self.ARR_ReactionUser :
				wCell = {
					"id"			: wID,
###					"screen_name"	: inUser['screen_name'],
					"screen_name"	: wARR_RateUserB[wID]['screen_name'],
					"cnt"			: 0
				}
				self.ARR_ReactionUser.update({ wID : wCell })
		
		#############################
		# 結果表示
		wStr = "------------------------------" + '\n'
		wStr = wStr + "リアクション結果" + '\n'
		wStr = wStr + "------------------------------" + '\n'
		wStr = wStr + "  新規受信数: " + str( self.VAL_ReactionCnt ) + " .件" + '\n'
		CLS_OSIF.sPrn( wStr )
		
###		wStr = ""
		if len(self.ARR_ReactionUser)==0 :
			### リアクションがなければ、ここで終わり
			wStr = "(情報なし)" + '\n'
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		wStr = ""
		#############################
		# 非絡みユーザのユーザレベル変更
###		wKeylist = list( self.ARR_Reaction.keys() )
		wKeylist = list( self.ARR_ReactionUser.keys() )
		for wID in wKeylist :
			#############################
			# DBからいいね情報を取得する(1個)
###			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( self.ARR_Reaction[wID]['user'], inFLG_New=False )
			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( self.ARR_ReactionUser[wID], inFLG_New=False )
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
			
###			#############################
###			# 連ふぁぼのカウント処理
###			if self.ARR_Reaction[wID]['cnt']>=1 :
###				### リアクションありの場合
###				###   強制回数以上は、リアクションcnt分カウント
###				###   その他は +1 カウント
###				if self.ARR_Reaction[wID]['cnt']>=gVal.DEF_STR_TLNUM['renFavoForceCnt'] :
###					wCnt = self.ARR_Reaction[wID]['cnt'] + 1
###				else:
###					wCnt = wARR_DBData['renfavo_cnt'] + 1
###			else:
###				### リアクションなしの場合
###				###   非絡み設定中の場合は -1 カウント
###				###   その他は 0 カウント
###				if wARR_DBData['renfavo_cnt']>=1 :
###					wCnt = wARR_DBData['renfavo_cnt'] - 1
###				else:
###					wCnt = 0
			#############################
			# 連ふぁぼのカウント処理
			if self.ARR_ReactionUser[wID]['cnt']>=1 :
				### リアクションありの場合
				###   強制回数以上は、リアクションcnt分カウント
				###   その他は +1 カウント
				if self.ARR_ReactionUser[wID]['cnt']>=gVal.DEF_STR_TLNUM['renFavoForceCnt'] :
					wCnt = self.ARR_ReactionUser[wID]['cnt'] + 1
				else:
					wCnt = wARR_DBData['renfavo_cnt'] + 1
			else:
				### リアクションなしの場合
				###   非絡み設定中の場合は -1 カウント
				###   その他は 0 カウント
				if wARR_DBData['renfavo_cnt']>=1 :
###					wCnt = wARR_DBData['renfavo_cnt'] - 1
###					
					wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['rfavo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forRenFavoSec'] )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed(1)"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
					if wGetLag['Beyond']==True :
						### 規定外はリセット
						wCnt = 0
					else:
						wCnt = wARR_DBData['renfavo_cnt'] - 1
				
				else:
					wCnt = 0
			
			wUserLevel = None
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
		wRes['Class'] = "CLS_TwitterReaction"
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
		
###		self.OBJ_Parent.ARR_ReacrionUserID = []
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
					wFLG_ZanCountSkip = True
					continue
				
				#############################
				# ツイートチェック
###				wSubRes = self.OBJ_Parent.ReactionTweetCheck( wUserID, wTweet, inMention=False, inVIPon=True )
				wSubRes = self.ReactionTweetCheck( wUserID, wTweet, inMention=False, inVIPon=True )
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
				
###				###日時の変換
###				wTime = CLS_TIME.sTTchg( wRes, "(2)", wSubRes['Responce'][wReplyID]['created_at'] )
###				if wTime['Result']!=True :
###					continue
###				wSubRes['Responce'][wReplyID]['created_at'] = wTime['TimeDate']
###				
				#############################
				# 期間内のTweetか
				wGetLag = CLS_OSIF.sTimeLag( str( wSubRes['Responce'][wReplyID]['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forVipReactionTweetSec'] )
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
				
				wID = str(wSubRes['Responce'][wReplyID]['user']['id'])
###				wID = str(wSubRes['Responce'][wReplyID]['id'])
###				
###				#############################
###				# ユーザ情報を取得する
###				wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=wID )
###				if wUserInfoRes['Result']!=True :
###					wRes['Reason'] = "Twitter Error: @" + wUserInfoRes['Responce']['screen_name']
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###				
				###ユーザ単位のリアクションチェック
###				wReactionRes = self.ReactionUserCheck( wUserInfoRes['Responce'], wSubRes['Responce'][wReplyID], inMention=True, inVIPon=True )
				wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wReplyID]['user'], wSubRes['Responce'][wReplyID], inMention=True, inVIPon=True )
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




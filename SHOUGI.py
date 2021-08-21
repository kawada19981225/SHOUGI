#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame
from pygame.locals import *
import sys
import random
import copy
import numpy as np
import math
from itertools import product


# In[3]:


SBoard = [
    [4,5,6,7,8,7,6,5,4],
    [0,3,0,0,0,0,0,2,0],
    [1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]

STable = [[1,2,3,4,5,6,7,8],
          [0,0,0,0,0,0,0,0]]

Pawn = 1#歩兵
Rook = 2#飛車
Bishop = 3#角
Lance = 4#香車
Knight = 5#桂馬
Silver_general = 6#銀将
Gold_general = 7#金将
King = 8#王将

P_Pawn = 9#歩兵
P_Rook = 10#飛車
P_Bishop = 11#角
P_Lance = 12#香車
P_Knight = 13#桂馬
P_Silver_general = 14#銀将
P_Gold_general = 15#金将
P_King = 16#王将

Name = ["歩","飛","角","香","桂","銀","金","王",
        "金","竜","馬","金","金","金","金","王"]
EN_Name = [Pawn,Rook,Bishop,Lance,Knight,Silver_general,Gold_general,King,
           P_Pawn,P_Rook,P_Bishop,P_Lance,P_Knight,P_Silver_general,P_Gold_general,P_King]

PMotion = [
    [[0,-1]],
    [[1,0],[0,1],[-1,0],[0,-1]],
    [[1,1],[-1,-1],[1,-1],[-1,1]],
    [[0,-1]],
    [[-1,-2],[1,-2]],
    [[0,-1],[1,-1],[-1,-1],[-1,1],[1,1]],
    [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[0,1]],
    [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]],
    
    [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[0,1]],
    [[[1,0],[0,1],[-1,0],[0,-1]],[[1,1],[-1,-1],[1,-1],[-1,1]]],
    [[[1,1],[-1,-1],[1,-1],[-1,1]],[[1,0],[0,1],[-1,0],[0,-1]]],
    [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[0,1]],
    [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[0,1]],
    [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[0,1]],
    [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[0,1]],
    [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
]


# In[4]:


class Game():#各クラスの初期化
    def __init__(self):
        self.Board = Board()
        self.Table_1 = Table([700,100,1])
        self.Table_2 = Table([700,350,2])
        self.Pieces_1 = Pieces(np.array(self.Board.board),1)
        self.Pieces_2 = Pieces(np.flipud(np.fliplr(self.Board.board)),2)
        self.PromoteButton = PromoteButton()
        self.motion = Motion([None,None,None,None])
        self.motionFtable = MotionFtable(None)
        self.Player_1 = None
        self.Player_2 = None
        self.TryMovePiece = None
        self.TryPromotePiece = None
    def start(self):
        self.Player_1 = Player(self.Pieces_1,self.Table_1)
        self.Player_2 = Player(self.Pieces_2,self.Table_2)
        self.motion.MoveP = []
        self.motionFtable.MoveP = []
        self.turn = 1
        self.flag = True
    def drawCPlayer(self,screen):
        font = pygame.font.Font('ipaexg.ttf', 18)
        screen.fill((0,0,0),(50,25,550,25))
        if self.flag and self.turn != 3:
            text = font.render("Now Playing → Player 1", True, (255, 255, 255))
            screen.blit(text,(50,25))
        elif self.flag and self.turn == 3:
            text = font.render("Now Playing → Player 1　駒の移動方向を選んでください", True, (255, 255, 255))
            screen.blit(text,(50,25))
        elif not(self.flag) and self.turn != 3:
            text = font.render("Now Playing → Player 2", True, (255, 255, 255))
            screen.blit(text,(50,25))
        elif not(self.flag) and self.turn ==3:
            text = font.render("Now Playing → Player 2　駒の移動方向を選んでください", True, (255, 255, 255))
            screen.blit(text,(50,25))
    def drawPromote(self,screen):
        font = pygame.font.Font('ipaexg.ttf', 18)
        screen.fill((0,0,0),(650,550,500,50))
        if self.turn == 5:
            text = font.render(f"「成る」ことが出来る駒が存在します。成りますか？", True, (255, 255, 255))
            screen.blit(text,(650,550))
        else:
            text = font.render(f"「成る」ことが出来る駒が存在しません", True, (255, 255, 255))
            screen.blit(text,(650,550))
    def gameover(self,screen):
        if self.Player_1.table.table[1][7] == 1:
            screen.fill((0,0,0),(100,650,250,100))
            self.text = pygame.font.Font('ipaexg.ttf', 25).render("Player_1の勝ちです!!", True, (255, 255, 255))
            screen.blit(self.text,(100,675))
        elif self.Player_2.table.table[1][7] == 1:
            screen.fill((0,0,0),(100,650,250,100))
            self.text = pygame.font.Font('ipaexg.ttf', 25).render("Player_2の勝ちです!!", True, (255, 255, 255))
            screen.blit(self.text,(100,675))


# In[5]:


class Board():#将棋盤の設定
    def __init__(self):
        self.board = copy.deepcopy(SBoard)
        self.gridY = [[[x,100],[x,100+50*len(self.board)]] for x in range(100,100+50*len(self.board[0])+1,50)]
        self.gridX = [[[100,y],[100+50*len(self.board[0]),y]] for y in range(100,100+50*len(self.board)+1,50)]
    def draw(self,screen):
        pygame.draw.rect(screen,(140,118,96),(50,50,50+50*(len(self.board[0])+1),50+50*(len(self.board)+1)))
        for la_v in range(10):
            pygame.draw.lines(screen, (255,255,255),False,self.gridY[la_v], width=1)
            pygame.draw.lines(screen, (255,255,255),False,self.gridX[la_v], width=1)


# In[6]:


class Table():#駒台の描画
    def __init__(self,userInfo):
        self.table = copy.deepcopy(STable)
        self.x,self.y,self.id = userInfo
        self.gridY = [[[x,self.y],[x,self.y+50*len(self.table)]] for x in range(self.x,self.x+50*len(self.table[0])+1,50)]
        self.gridX = [[[self.x,y],[self.x+50*len(self.table[0]),y]] for y in range(self.y,self.y+50*len(self.table)+1,50)]
        self.tableOP = TableOP(self.table,self.x,self.y,self.id)
    def draw(self,screen):
        self.text = pygame.font.Font('ipaexg.ttf', 18).render(f"Player{self.id}の駒台(個)↓", True, (255, 255, 255))
        screen.fill((0,0,0),(self.x-50,self.y-75,250,25))
        screen.blit(self.text,(self.x-50,self.y-75))
        pygame.draw.rect(screen,(140,118,96),(self.x-50,self.y-50,50+50*(len(self.table[0])+1),50+50*(len(self.table)+1)))
        for la_vY,la_vX in product(range(len(self.gridY)),range(len(self.gridX))):
            pygame.draw.lines(screen, (255,255,255),False,self.gridY[la_vY], width=1)
            pygame.draw.lines(screen, (255,255,255),False,self.gridX[la_vX], width=1)
        self.tableOP.draw(screen)


# In[7]:


class PromoteButton():
    def __init__(self):
        font = pygame.font.Font('ipaexg.ttf', 18)
        self.text1 = font.render("Yes", True, (255, 255, 255))
        self.text2 = font.render("No", True, (255, 255, 255))
        self.button = [pygame.Rect(650+150*p,600,100,50) for p in range(2)]
    def draw(self,screen):
        pygame.draw.rect(screen,(140,118,96),(650,600,100,50))
        pygame.draw.rect(screen,(140,118,96),(800,600,100,50))
        screen.blit(self.text1,(650+25+50/6,600+25-50/6))
        screen.blit(self.text2,(800+25+50/6,600+25-50/6))


# In[8]:


class TableOP():
    def __init__(self,table,X,Y,id):
        self.table = table
        self.x = X
        self.y = Y
        self.pieces = [Piece(x,0,table[0][x],id,self.x,self.y) if table[0][x] in EN_Name else None for x in range(len(table[0]))]
    def draw(self,screen):
        for x in range(len(self.pieces)):
            if self.pieces[x] != None:
                self.pieces[x].draw(screen)
        for x in range(len(self.pieces)):
            screen.fill((140,118,96),(self.x+x*50+2,self.y+50+2,45,45))
            self.text = pygame.font.Font('ipaexg.ttf', 25).render(str(self.table[1][x]), True, (255, 255, 255))
            screen.blit(self.text,(self.x+x*50+50/3,self.y+50+50/4))


# In[9]:


class Pieces():#プレイヤーごとの将棋駒を管理
    def __init__(self,board,id):
        self.board  = board
        self.pieces = [Piece(x,y,self.board[y][x],id,100,100) if self.board[y][x] in EN_Name else None for y in range(len(self.board)) for x in range(len(self.board[0]))]
        self.pieces = np.array(self.pieces).reshape(-1,9)
    def draw(self,screen):
        for y,x in product(range(len(self.pieces)),range(len(self.pieces[0]))):
            if self.pieces[y][x] != None:
                self.pieces[y][x].draw(screen)


# In[10]:


class Piece():#将棋駒の設定
    def __init__(self,x,y,type,id,baseX,baseY):
        self.x = x 
        self.y = y 
        self.type = type
        self.id = id
        self.info = self.x,self.y,self.type,self.id
        self.angle = 75 if self.id == 1 else 105
        self.color = (255,255,204) if self.id == 1 else (204,204,255)
        self.button = pygame.Rect(baseX+self.x*50,baseY+self.y*50,50,50)
        self.baseX = baseX
        self.baseY = baseY
    def promote(self,piece):
        self.piece = piece
        if self.piece.id == 1 and self.piece.y >= 6 and self.piece.type<=8:
            return True
        elif self.piece.id == 2 and self.piece.y <=2 and self.piece.type<=8:
            return True
    def changeType(self,Ptype):
        self.type+=Ptype
        self.info = self.x,self.y,self.type,self.id
    def draw(self,screen):
        self.Piece_text = AttachName(self.type)
        self.vertex = [[self.baseX+25+self.x*50+20*np.sin(math.radians(((360/5)*(i-1))+self.angle)),
                        self.baseY+25+self.y*50+20*np.cos(math.radians(((360/5)*(i-1))+self.angle))] for i in range(1,6)]
        pygame.draw.polygon(screen,self.color,self.vertex, width=0)
        screen.blit(self.Piece_text, (self.baseX+25+self.x*50-50/6, self.baseY+25+self.y*50-50/6))
    def move(self,cord,piece_Main,piece_Sub):
        x,y = cord
        piece_Main.pieces.pieces[y][x] = Piece(x,y,self.type,self.id,self.baseX,self.baseY)
        piece_Main.pieces.pieces[self.y][self.x] = None
        if piece_Sub.pieces.pieces[y][x] != None:
            if piece_Sub.pieces.pieces[y][x].type>8:
                piece_Main.table.table[1][(piece_Sub.pieces.pieces[y][x].type-8)-1]+=1
                piece_Sub.pieces.pieces[y][x] = None
            else:
                piece_Main.table.table[1][piece_Sub.pieces.pieces[y][x].type-1]+=1
                piece_Sub.pieces.pieces[y][x] = None
    def moveFtable(self,cord,piece_Main):
        x,y = cord
        piece_Main.pieces.pieces[y][x] = Piece(x,y,self.type,self.id,100,100)
        piece_Main.table.table[1][piece_Main.pieces.pieces[y][x].type-1]-=1


# In[11]:


class Motion():#将棋駒ごとに設定されている役の動きを設定する
    def __init__(self,info):
        self.x,self.y,self.type,self.id = info
        self.button = []
    def MoveableRBL(self,Piece_Main,Piece_Sub):#Rook,Bishop,Lance
        self.button = []
        Step = [True]*len(self.motion)
        mag = 1
        while (True in Step):
            for i,(x,y) in enumerate(self.motion):
                if Step[i] == True:
                    moveX = self.x + x*mag
                    moveY = self.y + y*mag
                    if  ((moveY>8 or moveY<0) or (moveX>8 or moveX<0)) or Piece_Main[moveY][moveX] != None:
                        Step[i] = False
                    elif Piece_Main[moveY][moveX] == None:
                        (self.button).append([moveX,moveY])
                        if Piece_Sub[moveY][moveX] != None:
                            Step[i] = False
            mag+=1
            
    def MoveablePKSGK(self,Piece_Main,Piece_Sub):#Pawn,Knight,Silver_general,Gold_general,King
        self.button = []
        for x,y in (self.motion):
            moveX = self.x + x
            moveY = self.y + y
            if (0<=moveY<=8 and 0<=moveX<=8) and (Piece_Main[moveY][moveX] == None or Piece_Sub[moveY][moveX] != None):
                (self.button).append([moveX,moveY])
    
    def MoveableP_RB(self,Piece_Main,Piece_Sub):#P_Rook,P_Bishop
        self.button = []
        Step = [True]*len(self.motion[0])
        mag = 1
        while (True in Step):
            for i,(x,y) in enumerate(self.motion[0]):
                if Step[i] == True:
                    moveX = self.x + x*mag
                    moveY = self.y + y*mag
                    if  ((moveY>8 or moveY<0) or (moveX>8 or moveX<0)) or Piece_Main[moveY][moveX] != None:
                        Step[i] = False
                    elif Piece_Main[moveY][moveX] == None:
                        (self.button).append([moveX,moveY])
                        if Piece_Sub[moveY][moveX] != None:
                            Step[i] = False
            mag+=1

        for x,y in (self.motion[1]):
            moveX = self.x + x
            moveY = self.y + y
            if (0<=moveY<=8 and 0<=moveX<=8) and (Piece_Main[moveY][moveX] == None or Piece_Sub[moveY][moveX] != None):
                (self.button).append([moveX,moveY]) 
    
    def MoveableP_PKLSGK(self,Piece_Main,Piece_Sub):#P_Pawn,P_Lance,P_Knight,P_Silver_general,P_Gold_general,P_King
        self.button = []
        for x,y in (self.motion):
            moveX = self.x + x
            moveY = self.y + y
            if (0<=moveY<=8 and 0<=moveX<=8) and (Piece_Main[moveY][moveX] == None or Piece_Sub[moveY][moveX] != None):
                (self.button).append([moveX,moveY])
    
    def genMoveP(self,Piece_Main,Piece_Sub):
        self.MoveP = []
        self.motion = np.array(PMotion[self.type-1])*[-1,-1] if self.id==1 else PMotion[self.type-1]
        
        if self.type in [Rook,Bishop,Lance]:
            self.MoveableRBL(Piece_Main,Piece_Sub)
        elif self.type in [Pawn,Knight,Silver_general,Gold_general,King]:
            self.MoveablePKSGK(Piece_Main,Piece_Sub)
        elif self.type in [P_Rook,P_Bishop]:
            self.MoveableP_RB(Piece_Main,Piece_Sub)
        elif self.type in [P_Pawn,P_Lance,P_Knight,P_Silver_general,P_Gold_general,P_King]:
            self.MoveableP_PKLSGK(Piece_Main,Piece_Sub)
            
        if len(self.button) != 0:
            self.MoveP = [pygame.Rect(100+x*50,100+y*50,50,50) for x,y in self.button]
            return True
        else:
            return False
        
    def draw(self,screen):
        for x,y in self.button:
            pygame.draw.circle(screen,(255,128,128),[125+x*50,125+y*50],20,width=0)


# In[12]:


class MotionFtable():
    def __init__(self,type):
        self.type = type
        self.button = []
    def MoveableP(self,Piece_Main,Piece_Sub):#Pawn
        self.button = []
        Mlist = []
        arrayM = np.array(Piece_Main).copy().T
        arrayS = np.array(Piece_Sub).copy().T
                
        for y in range(len(arrayM)):
            flag = True
            for x in range(len(arrayM[0])):
                if arrayM[y][x] != None and arrayM[y][x].type == Pawn:
                    flag = False
            if flag:
                Mlist.append(y)
                
        for y,x in product(Mlist,range(len(arrayM[0]))):
            if (arrayM[y][x] == None and arrayS[y][x] == None):
                (self.button).append([y,x])
                
    def MoveableRBLKSGK(self,Piece_Main,Piece_Sub):#Pawn以外
        self.button = []
        for y,x in product(range(len(Piece_Main)),range(len(Piece_Main[0]))):
            if Piece_Main[y][x] == None and Piece_Sub[y][x] == None:
                (self.button).append([x,y])
                
    def genMoveP(self,Piece_Main,Piece_Sub):
        self.MoveP = []
        self.MoveableP(Piece_Main,Piece_Sub) if self.type in [Pawn] else self.MoveableRBLKSGK(Piece_Main,Piece_Sub)
        if len(self.button) != 0:
            self.MoveP = [pygame.Rect(100+x*50,100+y*50,50,50) for x,y in self.button]
            return True
        else:
            return False
    def draw(self,screen):
        for x,y in self.button:
            pygame.draw.circle(screen,(255,128,128),[125+x*50,125+y*50],20,width=0)


# In[13]:


class Player():
    def __init__(self,Pieces,Table):
        self.pieces = Pieces
        self.table = Table


# In[14]:


def Event(game,screen):#キーボード操作によって動作を変える
    while True:
        game.drawCPlayer(screen)
        game.Board.draw(screen)
        if len(game.motion.button) > 0:
            game.motion.draw(screen)
        if len(game.motionFtable.button) > 0:
            game.motionFtable.draw(screen)
        if game.turn == 5:
            game.PromoteButton.draw(screen)
        else:
            screen.fill((0,0,0),(650,600,250,50))
        game.Player_1.table.draw(screen)
        game.Player_2.table.draw(screen)
        game.Player_1.pieces.draw(screen)
        game.Player_2.pieces.draw(screen)
        game.drawPromote(screen)
        game.gameover(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for y,x in product(range(len(game.Board.board)),range(len(game.Board.board[0]))):
                    if game.Player_1.pieces.pieces[y][x] != None and (game.Player_1.pieces.pieces[y][x].button).collidepoint(event.pos) and game.turn == 1:
                        game.motion = Motion(game.Player_1.pieces.pieces[y][x].info)
                        if game.motion.genMoveP(game.Player_1.pieces.pieces,game.Player_2.pieces.pieces):
                            game.TryMovePiece = game.Player_1.pieces.pieces[y][x]
                            game.turn = 3
                    elif game.Player_2.pieces.pieces[y][x] != None and (game.Player_2.pieces.pieces[y][x].button).collidepoint(event.pos) and game.turn == 2:
                        game.motion = Motion(game.Player_2.pieces.pieces[y][x].info)
                        if game.motion.genMoveP(game.Player_2.pieces.pieces,game.Player_1.pieces.pieces):
                            game.TryMovePiece = game.Player_2.pieces.pieces[y][x]
                            game.turn = 3
                        
                for i in range(len(game.Player_1.table.tableOP.pieces)):
                    if (game.Player_1.table.tableOP.pieces[i].button).collidepoint(event.pos) and game.Player_1.table.table[1][i] >0 and game.turn == 1:
                        game.motionFtable = MotionFtable(game.Player_1.table.tableOP.pieces[i].type)
                        if game.motionFtable.genMoveP(game.Player_1.pieces.pieces,game.Player_2.pieces.pieces):
                            game.TryMovePiece = game.Player_1.table.tableOP.pieces[i]
                            game.turn = 4
                    elif (game.Player_2.table.tableOP.pieces[i].button).collidepoint(event.pos) and game.Player_2.table.table[1][i] >0 and game.turn == 2:
                        game.motionFtable = MotionFtable(game.Player_1.table.tableOP.pieces[i].type)
                        if game.motionFtable.genMoveP(game.Player_2.pieces.pieces,game.Player_1.pieces.pieces):
                            game.TryMovePiece = game.Player_2.table.tableOP.pieces[i]
                            game.turn = 4
                            
                for i in range(len(game.motion.MoveP)):
                    if (game.motion.MoveP[i]).collidepoint(event.pos) and game.turn == 3 and game.flag:
                        game.TryMovePiece.move(game.motion.button[i],game.Player_1,game.Player_2)
                        if game.Player_1.pieces.pieces[game.motion.button[i][1]][game.motion.button[i][0]].promote(game.Player_1.pieces.pieces[game.motion.button[i][1]][game.motion.button[i][0]]):
                            game.turn = 5
                            game.TryPromotePiece = game.Player_1.pieces.pieces[game.motion.button[i][1]][game.motion.button[i][0]]
                            game.motion.button = []
                        else:
                            game.turn = 2
                            game.flag = False
                            game.motion.button = []
                    elif (game.motion.MoveP[i]).collidepoint(event.pos) and game.turn == 3 and not(game.flag):
                        game.TryMovePiece.move(game.motion.button[i],game.Player_2,game.Player_1)
                        if game.Player_2.pieces.pieces[game.motion.button[i][1]][game.motion.button[i][0]].promote(game.Player_2.pieces.pieces[game.motion.button[i][1]][game.motion.button[i][0]]):
                            game.turn = 5
                            game.TryPromotePiece = game.Player_2.pieces.pieces[game.motion.button[i][1]][game.motion.button[i][0]]
                            game.motion.button = []
                        else:
                            game.turn = 1
                            game.flag = True
                            game.motion.button = []
                            
                for i in range(len(game.motionFtable.MoveP)):
                    if (game.motionFtable.MoveP[i]).collidepoint(event.pos) and game.turn == 4 and game.flag:
                        game.TryMovePiece.moveFtable(game.motionFtable.button[i],game.Player_1)
                        game.motionFtable.button = []
                        game.turn = 2
                        game.flag = False
                    elif (game.motionFtable.MoveP[i]).collidepoint(event.pos) and game.turn == 4 and not(game.flag):
                        game.TryMovePiece.moveFtable(game.motionFtable.button[i],game.Player_2)
                        game.motionFtable.button = []
                        game.turn = 1
                        game.flag = True
                
                for i in range(len(game.PromoteButton.button)):
                    if (game.PromoteButton.button[0]).collidepoint(event.pos) and game.turn == 5 :
                        if game.TryPromotePiece.type <= 8:
                            game.TryPromotePiece.changeType(8)
                        game.turn = 2 if game.flag else 1
                        game.flag = not(game.flag)
                    elif (game.PromoteButton.button[1]).collidepoint(event.pos) and game.turn == 5 :
                        game.turn = 2 if game.flag else 1
                        game.flag = not(game.flag)
        pygame.display.update()


# In[15]:


def AttachName(Type):#駒に名前を付ける
    font = pygame.font.Font('ipaexg.ttf', 18)
    for i in range(len(Name)):
        if Type == i+1:
            return font.render(Name[i], True, (0, 0, 0))


# In[16]:


def AttachName(Type):#駒に名前を付ける
    font = pygame.font.Font('ipaexg.ttf', 18)
    if Type<=8:
        return font.render(Name[Type-1], True, (0, 0, 0))
    else:
        return font.render(Name[Type-1], True, (255, 0, 0))


# In[17]:


def main():
    pygame.init()
    screen = pygame.display.set_mode((1400,800))
    pygame.display.set_caption("将棋プログラム")
    
    game = Game()
    game.start()
    Event(game,screen)


# In[19]:


if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





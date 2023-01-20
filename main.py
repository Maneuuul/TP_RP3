import pygame
import random
import copy
from pygame.locals import *
from math import inf
from tkinter import * 
import time
computer = 1
human = -1
alpha = -inf
beta = +inf
depth = 5
dictplayer = {
        'A': 4,
        'B': 4,
        'C': 4,
        'D': 4,
        'E': 4,
        'F': 4,
        'magp' : 0,
    }
dictcomputer = {
        'G': 4,
        'H': 4,
        'I': 4,
        'J': 4,
        'K': 4,
        'L': 4,
        'magc' : 0,
    }
tuplep = ('A','B','C','D','E','F','magp')
tuplec = ('G','H','I','J','K','L','magc')


class etat():
    
    def __init__(self,dictplayer,dictcomputer,tuplep,tuplec):
        self.dictplayer = dictplayer
        self.dictcomputer = dictcomputer
        self.tuplec = tuplec
        self.tuplep = tuplep
    
    def possiblemoves(self,dictplayer,dictcomputer,player):
        # va retourner les fosses ou il reste des graines du joueur
        self.listep = []
        self.listec = []
        if player == -1 :
            for key, value in dictplayer.items():
                if value > 0 and key != 'magp' : 
                    self.listep.append(key)
            return self.listep
        if player == 1 :
            for key1, value1 in dictcomputer.items():
                if value1 > 0  and key1 != 'magc': 
                    self.listec.append(key1)
            return self.listec

    def domove(self,dictplayer,dictcomputer,player,case):
        #maj du board 
        # retourner le prochain joueur
        key = '' 
        if player == computer : 
            #print(case)
            #print(dictcomputer[case])
            nb_graine = dictcomputer[case]
            dictcomputer[case] = 0 
            key_list = [k for (k, val) in dictcomputer.items() if ((k > case))]
            #print(key_list)
            for key in key_list :
                if nb_graine > 0 :
                    dictcomputer[key] += 1
                    nb_graine -= 1
                else : 
                    break
            # cas graine dep dans une case vide 
            if key != '' : 
                if (dictcomputer[key]== 1 and key != 'magc'):
                    x = tuplec.index(key)
                    print(x)
                    y = [key for key in dictplayer.keys()][x]
                    print(y)
                    cpt = dictplayer[y]
                    dictcomputer['magc'] = dictcomputer['magc'] + (cpt+1)
                    dictplayer[y] = 0
                    
                # condition rejouer ou bien passer au case de l'adversaire 
                elif (key == 'magc'):
                    if nb_graine == 0 :
                        return player 
                    else : 
                        while nb_graine != 0:
                            for key in dictplayer.keys():
                                if nb_graine > 0 :
                                    if key != 'magp':
                                        dictplayer[key] += 1
                                        nb_graine -= 1
                                else : 
                                    break
                            if nb_graine == 0 :
                                break
                            else : 
                                for key in dictcomputer.keys():
                                    if nb_graine > 0 :
                                        dictcomputer[key] += 1
                                        nb_graine -= 1
                                    else : 
                                        break 
                                if(key == 'magc') and nb_graine == 0 : 
                                    return player 
                        return human
                return human
            
        if player == human : 
            nb_graine = dictplayer[case]
            dictplayer[case] = 0 
            key_list = [k for (k, val) in dictplayer.items() if ((k > case))]
            for key in key_list :
                if nb_graine > 0 :
                    dictplayer[key] += 1
                    nb_graine -= 1
                else : 
                    break
            # cas graine dep dans une case vide 
            if key != '':
                if (dictplayer[key]== 1 and key != 'magp'):
                    x = tuplep.index(key)
                    y = [key for key in dictcomputer.keys()][x]
                    print(y)
                    cpt = dictcomputer[y]
                    dictplayer['magp'] = dictplayer['magp'] + (cpt+1)
                    dictcomputer[y] = 0
                # condition rejouer ou bien passer au case de l'adversaire 
                elif (key == 'magp'):
                    if nb_graine == 0 :
                        return player 
                    else : 
                        while nb_graine != 0 : 
                            for key in dictcomputer.keys():
                                if nb_graine > 0 :
                                    if key != 'magc':
                                        dictcomputer[key] += 1
                                        nb_graine -= 1
                                else : 
                                    break
                            if nb_graine == 0 :
                                break 
                            else : 
                                for key in dictplayer.keys():
                                    if nb_graine > 0 :
                                        dictplayer[key] += 1 
                                        nb_graine -= 1 
                                    else:
                                        break
                                if key == 'magp' and nb_graine == 0 : 
                                    return player 
                        return computer
                return computer

class game():
    def __init__(self,state,playerside):
        self.state = state 
        self.playerside = playerside
    def gameover(self):
        cptc = 0
        cpth = 0 
        #les fosses d'un des joueurs sont vides 
        for key in  self.state.dictcomputer.keys():
            if self.state.dictcomputer[key] == 0  and key != 'magc':
                cptc += 1
        for key in  self.state.dictplayer.keys():
            if self.state.dictplayer[key] == 0  and key != 'magp':
                cpth += 1
        # est ce qu'on remet les casse a 0 quand on a game over ?
        if cptc == 6 :
            for key in self.state.dictplayer.keys():
                if key != 'magp':
                    self.state.dictplayer['magp'] = self.state.dictplayer['magp']+self.state.dictplayer[key]
                    self.state.dictplayer[key] = 0
            return 0 
        if cpth == 6 :
            for key in self.state.dictcomputer.keys():
                if key != 'magc':
                    self.state.dictcomputer['magc'] = self.state.dictcomputer['magc']+self.state.dictcomputer[key]
                    self.state.dictcomputer[key] = 0
            return 0 # 0 donc game over         
    def findwinner(self):
        gainC = self.state.dictcomputer['magc']
        gainH = self.state.dictplayer['magp']
        if gainC > gainH :
            return computer
        else : 
            return human
    def evaluate(self,dictplayer,dictcomputer):
        # est ce que c'est human - comp ou le contraire 
        value = dictplayer['magp']-dictcomputer['magc']
        return value

class Play():
    def __init__(self,state,game):
        self.state = state 
        self.game = game 
    def humanTurn(self,dictplayer,dictcomputer,player):
        listep = self.state.possiblemoves(dictplayer,dictcomputer,player)
        fosse = input("Choisir une fosse A,B,C,D,E,F:  ")
        while fosse not in listep :
            fosse = input("Choisir une fosse A,B,C,D,E,F:  ")
        if self.game.gameover() != 0 : 
            val = self.state.domove(dictplayer,dictcomputer,human,fosse)
            return val

    def computerTurn(self,dictplayer,dictcomputer):
        if self.game.gameover() != 0 :
            #alpha beta on l'appel avec computer seulement. 
            #value,pit = self.alpha_beta(self.game,computer,depth,alpha,beta)
            value,_ = self.Min_Max(self.game,computer,depth)
            #return(self.state.domove(dictplayer,dictplayer,computer,pit))

    def Min_Max(self,game,player,depth):
        # game instance de la classse game 
        print(dictcomputer)
        print(dictplayer)
        print('#############################')
        if game.gameover() or depth == 1 : 
            bestValue = game.evaluate(dictplayer,dictcomputer)
            bestPit = None
            if player == human :
                self.humanTurn(dictplayer,dictcomputer,-1)
                bestValue = -bestValue
            return bestValue,bestPit
        bestValue = - inf
        bestPit = None
        game.playerside = player 
        liste = game.state.possiblemoves(dictplayer,dictcomputer,game.playerside)
        for pit in liste :
            child_game = copy.copy(game) #faut voir la bibliotheque adapter
            joueur = child_game.state.domove(dictplayer,dictcomputer,game.playerside,pit)
            #print(joueur)
            #print('#########################')
            value,x = self.Min_Max(child_game,joueur,depth-1)
            value = -value
            if value > bestValue : 
                bestValue = value
                bestPit = pit
        return bestValue,bestPit
    
    def alpha_beta (self,game,player,depth,alpha,beta):
        if game.gameover()== 0 or depth == 1:
            bestValue = game.evaluate(dictplayer,dictcomputer)
            bestPit = None 
            if player == human :
                bestValue = -bestValue
            return bestValue,bestPit
        bestValue = -inf
        bestPit = None
        game.playerside = player 
        #print(game.state.possiblemoves(dictplayer,dictcomputer,game.playerside))
        #print('-------------------------------------')
        for pit in game.state.possiblemoves(dictplayer,dictcomputer,game.playerside):
            child_game = copy.copy(game)
            joueur = child_game.state.domove(dictplayer,dictcomputer,game.playerside,pit)
            print(dictcomputer)
            print('****************************')
            if joueur == human and game.gameover() != 0 :
                joueur = self.humanTurn(dictplayer,dictcomputer,-1)
                print(dictplayer)
                print('#############################')
            value,_ = self.alpha_beta(child_game,joueur, depth-1 , -alpha , -beta)
            value = - value
            if value > bestValue : 
                bestValue = value
                bestPit = pit
            if bestValue > alpha : 
                alpha = bestValue
            if beta <= alpha : 
                break 
        return bestValue,bestPit

etatt = etat(dictplayer,dictcomputer,tuplep,tuplec)
gamee = game(etatt,human)
playy = Play(etatt,gamee)
print(dictcomputer)
print(dictplayer)
print('#############################')
#POUR RECOMMENCER 
while gamee.gameover() != 0:
    playy.computerTurn(dictplayer,dictcomputer)
 
gamee.gameover()
var = gamee.findwinner()
if var == computer : 
    print('Computer a gagner')
else : 
    print('Player a gagner')

print(dictcomputer)
print(dictplayer)
print('#############################')
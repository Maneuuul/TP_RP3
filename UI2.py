
from tkinter import * 
from tkinter import messagebox
import copy
from pygame.locals import *
from math import inf
import time
# init 
computer = 1
human = -1
egalite = 0
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
        'G': 0,
        'H': 0,
        'I': 0,
        'J': 0,
        'K': 0,
        'L': 1,
        'magc' : 0,
    }
tuplep = ('A','B','C','D','E','F','magp')
tuplec = ('G','H','I','J','K','L','magc')
#FONCTION POUR GET DU CHOIX DU JOUEUR 

def getentry1():
    res = E1.get()
    gui.destroy()
    return res 

#CLASSE ETAT
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
                    y = [key for key in dictplayer.keys()][x]
                    cpt = dictplayer[y]
                    dictcomputer[key]=0
                    dictcomputer['magc'] = dictcomputer['magc'] + (cpt+1)
                    dictplayer[y] = 0
                    return human
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
                    cpt = dictcomputer[y]
                    dictplayer[key]=0
                    dictplayer['magp'] = dictplayer['magp'] + (cpt+1)
                    dictcomputer[y] = 0
                    return computer
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

#CLASSE GAME
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
        elif cpth == 6 :
            for key in self.state.dictcomputer.keys():
                if key != 'magc':
                    self.state.dictcomputer['magc'] = self.state.dictcomputer['magc']+self.state.dictcomputer[key]
                    self.state.dictcomputer[key] = 0
            return 0 # 0 donc game over 
        else : return 1        
    def findwinner(self):
        gainC = self.state.dictcomputer['magc']
        gainH = self.state.dictplayer['magp']
        if gainC > gainH :
            return computer
        elif gainC < gainH : 
            return human
        else:
            return egalite
    def evaluate(self,dictplayer,dictcomputer):
        # est ce que c'est human - comp ou le contraire 
        value = dictplayer['magp']-dictcomputer['magc']
        return value

#CLASSE PLAY 
class Play():
    def __init__(self,state,game):
        self.state = state 
        self.game = game 
    def humanTurn(self,dictplayer,dictcomputer,player,var):
        listep = self.state.possiblemoves(dictplayer,dictcomputer,player)
        if var not in listep :
            messagebox.showinfo(title='Attention', message= 'Veuillez rejouer une case pleine')
        if self.game.gameover() != 0 : 
            val = self.state.domove(dictplayer,dictcomputer,human,var)
            init_fen()
            return val
    def computerTurn(self):
        if self.game.gameover() != 0 :
            #alpha beta on l'appel avec computer seulement. 
            value,pit = self.alpha_beta(self.game,computer,depth,alpha,beta)
        else : 
            pass
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
    def getentry(self):
        res = self.E1.get()
        self.gui.destroy()
        return res   
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
            init_fen()
            if joueur == human and game.gameover() != 0 :
                var = True
                while var :
                    j = "Choisir une fosse :"
                    listep = self.state.possiblemoves(dictplayer,dictcomputer,joueur)
                    for i in listep:
                        j = j+" "+i
                    self.gui = Tk()
                    self.gui.title("Mancala")
                    self.gui.iconbitmap('logo.ico')
                    self.gui.config(bg="#c78594")
                    self.gui.geometry("640x520")
                    self.text1 = Label(self.gui,text="",bg="#c78594",font= ("Arial",20))
                    self.text1.pack(pady= 20)
                    self.frame1 = Frame(self.gui,bd=10,bg = "#f0b1bf",width = 410 , height= 100)
                    self.frame1.pack()
                    self.A = Label(self.gui,text="A",bg="#c78594",font= ("Arial",10))
                    self.A.place(x=140,y=55)
                    self.b1 = Label(self.frame1, text=dictplayer['A'],bg="#823547", fg='white') 
                    self.b1.place(width=50,height=80)
                    self.B = Label(self.gui,text="B",bg="#c78594",font= ("Arial",10))
                    self.B.place(x=210,y=55)
                    self.b2 = Label(self.frame1, text=dictplayer['B'],bg="#823547", fg='white') 
                    self.b2.place(x=67 ,width=50,height=80)
                    self.C = Label(self.gui,text="C",bg="#c78594",font= ("Arial",10))
                    self.C.place(x=280,y=55)
                    self.b3 = Label(self.frame1, text=dictplayer['C'],bg="#823547", fg='white') 
                    self.b3.place(x=134 ,width=50,height=80)
                    self.D = Label(self.gui,text="D",bg="#c78594",font= ("Arial",10))
                    self.D.place(x=345,y=55)
                    self.b4 = Label(self.frame1, text=dictplayer['D'],bg="#823547", fg='white') 
                    self.b4.place(x=201 ,width=50,height=80)
                    self.E = Label(self.gui,text="E",bg="#c78594",font= ("Arial",10))
                    self.E.place(x=410,y=55)
                    self.b5 = Label(self.frame1, text=dictplayer['E'],bg="#823547", fg='white') 
                    self.b5.place(x=268 ,width=50,height=80)
                    self.F = Label(self.gui,text="F",bg="#c78594",font= ("Arial",10))
                    self.F.place(x=480,y=55)
                    self.b6 = Label(self.frame1, text=dictplayer['F'],bg="#823547", fg='white') 
                    self.b6.place(x=335 ,width=50,height=80)
        
                    self.label1 = Label(self.gui,text=j,bg="#c78594",font= ("Arial",15))
                    self.label1.pack(pady=10)
                    self.E1 = Entry(self.gui, width=40)
                    self.E1.pack(pady=10)
                    self.btn = Button(self.gui, height=1, width=10, text=" Entrée " , command= self.gui.quit)
                    self.btn.pack(pady=10)
                    self.frame2 = Frame(self.gui,bd=10,bg = "#f0b1bf",width = 410 , height= 100)
                    self.frame2.pack(pady= 40)
                    self.G = Label(self.gui,text="G",bg="#c78594",font= ("Arial",10))
                    self.G.place(x=140,y=455)
                    self.b7 = Label(self.frame2, text=dictcomputer['G'],bg="#823547", fg='white') 
                    self.b7.place(width=50,height=80)
                    self.H = Label(self.gui,text="H",bg="#c78594",font= ("Arial",10))
                    self.H.place(x=210,y=455)
                    self.b8 = Label(self.frame2, text=dictcomputer['H'],bg="#823547", fg='white') 
                    self.b8.place(x=67 ,width=50,height=80)
                    self.I = Label(self.gui,text="I",bg="#c78594",font= ("Arial",10))
                    self.I.place(x=280,y=455)
                    self.b9 = Label(self.frame2,text=dictcomputer['I'],bg="#823547", fg='white') 
                    self.b9.place(x=134 ,width=50,height=80)
                    self.J = Label(self.gui,text="J",bg="#c78594",font= ("Arial",10))
                    self.J.place(x=345,y=455)
                    self.b10 = Label(self.frame2, text=dictcomputer['J'],bg="#823547", fg='white') 
                    self.b10.place(x=201 ,width=50,height=80)
                    self.K = Label(self.gui,text="K",bg="#c78594",font= ("Arial",10))
                    self.K.place(x=410,y=455)
                    self.b11= Label(self.frame2, text=dictcomputer['K'],bg="#823547", fg='white') 
                    self.b11.place(x=268 ,width=50,height=80)
                    self.L = Label(self.gui,text="L",bg="#c78594",font= ("Arial",10))
                    self.L.place(x=480,y=455)
                    self.b12 = Label(self.frame2, text=dictcomputer['L'],bg="#823547", fg='white') 
                    self.b12.place(x=335 ,width=50,height=80)
                    #playy.humanTurn(dictplayer,dictcomputer,human,var)
                    self.gui.mainloop()
                    var = self.getentry()
                    joueur = self.humanTurn(dictplayer,dictcomputer,human,var)
                    if joueur == computer :
                        var = False
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

#MAIN 
#INIT DES CLASSES 

etatt = etat(dictplayer,dictcomputer,tuplep,tuplec)
gamee = game(etatt,human)
playy = Play(etatt,gamee)

#BOARD INIT 

def init_fen():
    fen = Tk()
    fen.title("Mancala")
    fen.iconbitmap('logo.ico')
    fen.config(background= "#c78594")
    fen.geometry("640x480")
    text1 = Label(fen,text="",bg="#c78594",font= ("Arial",20))
    text1.pack(pady= 20)
    #premier Frame player  
    frame1 = Frame(fen,bd=10,bg = "#f0b1bf",width = 410 , height= 100)
    frame1.pack()
    A = Label(fen,text="A",bg="#c78594",font= ("Arial",10))
    A.place(x=140,y=55)
    b1 = Label(frame1, text=dictplayer['A'],bg="#823547", fg='white') 
    b1.place(width=50,height=80)
    B = Label(fen,text="B",bg="#c78594",font= ("Arial",10))
    B.place(x=210,y=55)
    b2 = Label(frame1, text=dictplayer['B'],bg="#823547", fg='white') 
    b2.place(x=67 ,width=50,height=80)
    C = Label(fen,text="C",bg="#c78594",font= ("Arial",10))
    C.place(x=280,y=55)
    b3 = Label(frame1, text=dictplayer['C'],bg="#823547", fg='white') 
    b3.place(x=134 ,width=50,height=80)
    D = Label(fen,text="D",bg="#c78594",font= ("Arial",10))
    D.place(x=345,y=55)
    b4 = Label(frame1, text=dictplayer['D'],bg="#823547", fg='white') 
    b4.place(x=201 ,width=50,height=80)
    E = Label(fen,text="E",bg="#c78594",font= ("Arial",10))
    E.place(x=410,y=55)
    b5 = Label(frame1, text=dictplayer['E'],bg="#823547", fg='white') 
    b5.place(x=268 ,width=50,height=80)
    F = Label(fen,text="F",bg="#c78594",font= ("Arial",10))
    F.place(x=480,y=55)
    b6 = Label(frame1, text=dictplayer['F'],bg="#823547", fg='white') 
    b6.place(x=335 ,width=50,height=80)
    '''text2 = Label(fen,text="Human : ",bg="#c78594",font= ("Arial",15))
    text2.place(x=10 , y= 115)'''
    magp = Label(fen,text="MAG",bg="#c78594",font= ("Arial",10))
    magp.place(x=20,y=55)
    bouton = Label(fen, text=dictplayer['magp'],bg="#823547", fg='white')
    bouton.place(x=15,y=85 ,width=50,height=275)
    magp2 = Label(fen,text="Human",bg="#c78594",font= ("Arial",10))
    magp2.place(x=15,y=370)
    # deuxieme frame computer 
    frame2 = Frame(fen,bd=10,bg = "#f0b1bf",width = 410 , height= 100)
    frame2.pack(pady= 90)
    G = Label(fen,text="G",bg="#c78594",font= ("Arial",10))
    G.place(x=140,y=370)
    b7 = Label(frame2, text=dictcomputer['G'],bg="#823547", fg='white') 
    b7.place(width=50,height=80)
    H = Label(fen,text="H",bg="#c78594",font= ("Arial",10))
    H.place(x=210,y=370)
    b8 = Label(frame2, text=dictcomputer['H'],bg="#823547", fg='white') 
    b8.place(x=67 ,width=50,height=80)
    I = Label(fen,text="I",bg="#c78594",font= ("Arial",10))
    I.place(x=280,y=370)
    b9 = Label(frame2,text=dictcomputer['I'],bg="#823547", fg='white') 
    b9.place(x=134 ,width=50,height=80)
    J = Label(fen,text="J",bg="#c78594",font= ("Arial",10))
    J.place(x=345,y=370)
    b10 = Label(frame2, text=dictcomputer['J'],bg="#823547", fg='white') 
    b10.place(x=201 ,width=50,height=80)
    K = Label(fen,text="K",bg="#c78594",font= ("Arial",10))
    K.place(x=410,y=370)
    b11= Label(frame2, text=dictcomputer['K'],bg="#823547", fg='white') 
    b11.place(x=268 ,width=50,height=80)
    L = Label(fen,text="L",bg="#c78594",font= ("Arial",10))
    L.place(x=480,y=370)
    b12 = Label(frame2, text=dictcomputer['L'],bg="#823547", fg='white') 
    b12.place(x=335 ,width=50,height=80)
    '''text3 = Label(fen,text="Computer :",bg="#c78594",font= ("Arial",15))
    text3.place(x=5 , y= 300)'''
    magc = Label(fen,text="MAG",bg="#c78594",font= ("Arial",10))
    magc.place(x=580,y=370)
    bouton1 = Label(fen, text=dictcomputer['magc'],bg="#823547", fg='white')
    bouton1.place(x=575, y = 85 ,width=50,height=275)
    magc2 = Label(fen,text="Computer",bg="#c78594",font= ("Arial",10))
    magc2.place(x=565,y=55)
    bouton4 = Button(fen, text= 'Jouer',bg="#823547", fg='white',command=fen.destroy)
    bouton4.place(x=300, y = 415 ,width=60,height=30)
    fen.mainloop()

#BOARD DE FIN 

def init_fenover():
    fen = Tk()
    fen.title("Mancala")
    fen.iconbitmap('logo.ico')
    fen.config(background= "#c78594")
    fen.geometry("640x480")
    text1 = Label(fen,text="",bg="#c78594",font= ("Arial",20))
    text1.pack(pady= 20)
    #premier Frame player  
    frame1 = Frame(fen,bd=10,bg = "#f0b1bf",width = 410 , height= 100)
    frame1.pack()
    A = Label(fen,text="A",bg="#c78594",font= ("Arial",10))
    A.place(x=140,y=55)
    b1 = Label(frame1, text=dictplayer['A'],bg="#823547", fg='white') 
    b1.place(width=50,height=80)
    B = Label(fen,text="B",bg="#c78594",font= ("Arial",10))
    B.place(x=210,y=55)
    b2 = Label(frame1, text=dictplayer['B'],bg="#823547", fg='white') 
    b2.place(x=67 ,width=50,height=80)
    C = Label(fen,text="C",bg="#c78594",font= ("Arial",10))
    C.place(x=280,y=55)
    b3 = Label(frame1, text=dictplayer['C'],bg="#823547", fg='white') 
    b3.place(x=134 ,width=50,height=80)
    D = Label(fen,text="D",bg="#c78594",font= ("Arial",10))
    D.place(x=345,y=55)
    b4 = Label(frame1, text=dictplayer['D'],bg="#823547", fg='white') 
    b4.place(x=201 ,width=50,height=80)
    E = Label(fen,text="E",bg="#c78594",font= ("Arial",10))
    E.place(x=410,y=55)
    b5 = Label(frame1, text=dictplayer['E'],bg="#823547", fg='white') 
    b5.place(x=268 ,width=50,height=80)
    F = Label(fen,text="F",bg="#c78594",font= ("Arial",10))
    F.place(x=480,y=55)
    b6 = Label(frame1, text=dictplayer['F'],bg="#823547", fg='white') 
    b6.place(x=335 ,width=50,height=80)
    '''text2 = Label(fen,text="Human : ",bg="#c78594",font= ("Arial",15))
    text2.place(x=10 , y= 115)'''
    magp = Label(fen,text="MAG",bg="#c78594",font= ("Arial",10))
    magp.place(x=20,y=55)
    bouton = Label(fen, text=dictplayer['magp'],bg="#823547", fg='white')
    bouton.place(x=15,y=85 ,width=50,height=275)
    magp2 = Label(fen,text="Human",bg="#c78594",font= ("Arial",10))
    magp2.place(x=15,y=370)
    # deuxieme frame computer 
    frame2 = Frame(fen,bd=10,bg = "#f0b1bf",width = 410 , height= 100)
    frame2.pack(pady= 90)
    G = Label(fen,text="G",bg="#c78594",font= ("Arial",10))
    G.place(x=140,y=370)
    b7 = Label(frame2, text=dictcomputer['G'],bg="#823547", fg='white') 
    b7.place(width=50,height=80)
    H = Label(fen,text="H",bg="#c78594",font= ("Arial",10))
    H.place(x=210,y=370)
    b8 = Label(frame2, text=dictcomputer['H'],bg="#823547", fg='white') 
    b8.place(x=67 ,width=50,height=80)
    I = Label(fen,text="I",bg="#c78594",font= ("Arial",10))
    I.place(x=280,y=370)
    b9 = Label(frame2,text=dictcomputer['I'],bg="#823547", fg='white') 
    b9.place(x=134 ,width=50,height=80)
    J = Label(fen,text="J",bg="#c78594",font= ("Arial",10))
    J.place(x=345,y=370)
    b10 = Label(frame2, text=dictcomputer['J'],bg="#823547", fg='white') 
    b10.place(x=201 ,width=50,height=80)
    K = Label(fen,text="K",bg="#c78594",font= ("Arial",10))
    K.place(x=410,y=370)
    b11= Label(frame2, text=dictcomputer['K'],bg="#823547", fg='white') 
    b11.place(x=268 ,width=50,height=80)
    L = Label(fen,text="L",bg="#c78594",font= ("Arial",10))
    L.place(x=480,y=370)
    b12 = Label(frame2, text=dictcomputer['L'],bg="#823547", fg='white') 
    b12.place(x=335 ,width=50,height=80)
    '''text3 = Label(fen,text="Computer :",bg="#c78594",font= ("Arial",15))
    text3.place(x=5 , y= 300)'''
    magc = Label(fen,text="MAG",bg="#c78594",font= ("Arial",10))
    magc.place(x=580,y=370)
    bouton1 = Label(fen, text=dictcomputer['magc'],bg="#823547", fg='white')
    bouton1.place(x=575, y = 85 ,width=50,height=275)
    magc2 = Label(fen,text="Computer",bg="#c78594",font= ("Arial",10))
    magc2.place(x=565,y=55)
    bouton4 = Button(fen, text= 'FIN',bg="#823547", fg='white',command=fen.destroy)
    bouton4.place(x=300, y = 415 ,width=60,height=30)
    fen.mainloop()

#FENETRE DES REGLES DU JEU 

def regles_jeu ():
    wind = Tk()
    wind.title("Mancala")
    wind.iconbitmap('logo.ico')
    wind.config(background= "#fac8e5")
    wind.geometry("950x500")
    text = Label(wind,text="Les Règles De Mancala ",bg="#fac8e5",font= ("Arial",20,'italic','underline'))
    text.pack(pady= 10)
    text1 = Label(wind,text="-Le premier joueur choisit une fosse de son côté du plateau et ramasse toutes ses graines",bg="#fac8e5",font= ("Arial",12))
    text1.pack(pady= 5)
    text2 = Label(wind,text="-Dans le sens inverse des aiguilles d’une montre, le joueur dépose une pierre dans chaque fosse \n jusqu’à ce qu’ils n’aient plus de graines dans sa main",bg="#fac8e5",font= ("Arial",12))
    text2.pack(pady=5)
    text3 = Label(wind,text="-Le joueur peut déposer une graine dans n’importe quelle fosse du plateau (y compris son magasin) \n à l’exception du magasin de l’adversaire",bg="#fac8e5",font= ("Arial",12))
    text3.pack(pady=5)
    text4 = Label(wind,text="-Si la dernière graine déposée atterrit dans le magasin du joueur, ce joueur peut jouer un tour supplémentaire",bg="#fac8e5",font= ("Arial",12))
    text4.pack(pady=5)
    text5 = Label(wind,text="-Si la dernière graine déposée atterrit dans une fosse vide du côté du joueur,\n cette graine et toutes les graines dans la fosse du côté opposé (c’est-à-dire une fosse de l’adversaire) vont à ce joueur,\n et sont placées dans son magasin",bg="#fac8e5",font= ("Arial",12))
    text5.pack(pady=5)
    text6 = Label(wind,text="-Lorsqu’un joueur n’a plus de graines dans toutes les fosses de son côté, la partie se termine, \net le joueur adverse peut prendre toutes les graines restantes et les placer dans son propre magasin",bg="#fac8e5",font= ("Arial",12))
    text6.pack(pady=5)
    text7 = Label(wind,text="-Le joueur avec le plus de graines dans son magasin, gagne",bg="#fac8e5",font= ("Arial",12))
    text7.pack(pady=5)
    btn = Button(wind, height=2, width=40,text="Jouer" ,font=("Arial",10),command= wind.destroy)
    btn.pack(pady=10)
    wind.mainloop()

#FENETRE PRINCIPALE  

fenetre1 = Tk()
fenetre1.title("Mancala")
fenetre1.iconbitmap('logo.ico')
img = PhotoImage(file="1.gif", master= fenetre1)
fenetre1.geometry("539x360")
can = Canvas(fenetre1,height=480,width=640)
can.create_image(0,0,anchor= NW , image =img )
can.place(x=0,y=0)
text1 = Label(fenetre1,text="Jouer à Mancala ",bg="#c78594",font= ("Arial",25,'bold','italic'))
text1.pack(pady= 30)
btn = Button(fenetre1, height=2, width=40,text="Jouer" ,font=("Arial",10) ,command= fenetre1.quit)
btn.pack(pady=20)
btn1 = Button(fenetre1, height=2, width=40,text="Règles du jeu" ,font=("Arial",10) ,command= regles_jeu)
btn1.pack(pady=10)
fenetre1.mainloop()

#FENETRE CHOIX DU JOUEUR  

def getplayer():
    if var1.get() == 1 : 
        fen_choix_joueur.destroy()
        return human
    if var2.get() == 1 : 
        fen_choix_joueur.destroy()
        return computer
fenetre1.destroy()
fen_choix_joueur = Tk()
fen_choix_joueur.title("Mancala")
fen_choix_joueur.iconbitmap('logo.ico')
fen_choix_joueur.geometry("539x360")
fen_choix_joueur.config(background= "#c78594")
text1 = Label(fen_choix_joueur,text="It's time to play Mancala ",bg="#c78594",font= ("Arial",20,'bold','italic'))
text1.pack(pady= 20)
text1 = Label(fen_choix_joueur,text="choose who will start : ",bg="#c78594",font= ("Arial",15,'italic'))
text1.pack(pady= 20)
var1 = IntVar()
var2 = IntVar()
bouton = Checkbutton(fen_choix_joueur, text="Player      ",bg="#c78594",font=(("Arial",13)) ,variable= var1 ,onvalue=1, offvalue=0)
bouton.pack(pady=20)
bouton2 = Checkbutton(fen_choix_joueur, text="Computer",bg = "#c78594", font=("Arial",13), variable= var2 , onvalue=1, offvalue=0)
bouton2.pack(pady=20)
btn = Button(fen_choix_joueur, height=2, width=30, bg= "#c995b8",text="GOO !" ,font=("Arial",10) ,command= fen_choix_joueur.quit)
btn.pack(pady=10)
fen_choix_joueur.mainloop()
player = getplayer()
if player == human :
    var = True 
else : 
    var = False 
print(var)

#LANCEMENT DU JEU 

while gamee.gameover()!= 0:
    while var :
        gui = Tk()
        gui.title("Mancala")
        gui.iconbitmap('logo.ico')
        gui.config(bg="#c78594")
        gui.geometry("640x520")
        text1 = Label(gui,text="",bg="#c78594",font= ("Arial",20))
        text1.pack(pady= 20)
        frame1 = Frame(gui,bd=10,bg = "#f0b1bf",width = 410 , height= 100)
        frame1.pack()
        A = Label(gui,text="A",bg="#c78594",font= ("Arial",10))
        A.place(x=140,y=55)
        b1 = Label(frame1, text=dictplayer['A'],bg="#823547", fg='white') 
        b1.place(width=50,height=80)
        B = Label(gui,text="B",bg="#c78594",font= ("Arial",10))
        B.place(x=210,y=55)
        b2 = Label(frame1, text=dictplayer['B'],bg="#823547", fg='white') 
        b2.place(x=67 ,width=50,height=80)
        C = Label(gui,text="C",bg="#c78594",font= ("Arial",10))
        C.place(x=280,y=55)
        b3 = Label(frame1, text=dictplayer['C'],bg="#823547", fg='white') 
        b3.place(x=134 ,width=50,height=80)
        D = Label(gui,text="D",bg="#c78594",font= ("Arial",10))
        D.place(x=345,y=55)
        b4 = Label(frame1, text=dictplayer['D'],bg="#823547", fg='white') 
        b4.place(x=201 ,width=50,height=80)
        E = Label(gui,text="E",bg="#c78594",font= ("Arial",10))
        E.place(x=410,y=55)
        b5 = Label(frame1, text=dictplayer['E'],bg="#823547", fg='white') 
        b5.place(x=268 ,width=50,height=80)
        F = Label(gui,text="F",bg="#c78594",font= ("Arial",10))
        F.place(x=480,y=55)
        b6 = Label(frame1, text=dictplayer['F'],bg="#823547", fg='white') 
        b6.place(x=335 ,width=50,height=80)
        '''text2 = Label(gui,text="Human : ",bg="#c78594",font= ("Arial",15))
        text2.place(x=10 , y= 115)'''
        label1 = Label(gui,text="Choisir une fosse A,B,C,D,E,F:  ",bg="#c78594",font= ("Arial",15))
        label1.pack(pady=10)
        E1 = Entry(gui, width=40)
        E1.pack(pady=10)
        btn = Button(gui, height=1, width=10, text=" Entrée " , command= gui.quit)
        btn.pack(pady=10)
        frame2 = Frame(gui,bd=10,bg = "#f0b1bf",width = 410 , height= 100)
        frame2.pack(pady= 40)
        G = Label(gui,text="G",bg="#c78594",font= ("Arial",10))
        G.place(x=140,y=455)
        b7 = Label(frame2, text=dictcomputer['G'],bg="#823547", fg='white') 
        b7.place(width=50,height=80)
        H = Label(gui,text="H",bg="#c78594",font= ("Arial",10))
        H.place(x=210,y=455)
        b8 = Label(frame2, text=dictcomputer['H'],bg="#823547", fg='white') 
        b8.place(x=67 ,width=50,height=80)
        I = Label(gui,text="I",bg="#c78594",font= ("Arial",10))
        I.place(x=280,y=455)
        b9 = Label(frame2,text=dictcomputer['I'],bg="#823547", fg='white') 
        b9.place(x=134 ,width=50,height=80)
        J = Label(gui,text="J",bg="#c78594",font= ("Arial",10))
        J.place(x=345,y=455)
        b10 = Label(frame2, text=dictcomputer['J'],bg="#823547", fg='white') 
        b10.place(x=201 ,width=50,height=80)
        K = Label(gui,text="K",bg="#c78594",font= ("Arial",10))
        K.place(x=410,y=455)
        b11= Label(frame2, text=dictcomputer['K'],bg="#823547", fg='white') 
        b11.place(x=268 ,width=50,height=80)
        L = Label(gui,text="L",bg="#c78594",font= ("Arial",10))
        L.place(x=480,y=455)
        b12 = Label(frame2, text=dictcomputer['L'],bg="#823547", fg='white') 
        b12.place(x=335 ,width=50,height=80)
        #playy.humanTurn(dictplayer,dictcomputer,human,var)
        gui.mainloop()
        var = getentry1()
        x = playy.humanTurn(dictplayer,dictcomputer,human,var)
        #init_fen()
        if x == computer :
            var = False 
    else:
        playy.computerTurn() # c'est OK ca retourne computer 

gamee.gameover()
init_fenover()
var = gamee.findwinner()
if var == computer : 
    print('Computer a gagner')
    fenetre = Tk()
    fenetre.title("Mancala")
    fenetre.iconbitmap('logo.ico')
    fenetre.config(background= "#c78594")
    fenetre.geometry("640x300")
    text = Label(fenetre,text="Le gagant est : COMPUTER",bg="#c78594",font= ("Arial",25,'bold','italic'))
    text.pack(pady= 20)
    textt = Label(fenetre,text="Score Final ",bg="#c78594",font= ("Arial",20,'bold'))
    textt.pack(pady= 30)
    textt1 = Label(fenetre,text="Vous : "+str(dictplayer["magp"]),bg="#c78594",font= ("Arial",15))
    textt1.place(x= 100,y=200)
    textt1 = Label(fenetre,text="Computer : "+str(dictcomputer["magc"]),bg="#c78594",font= ("Arial",15))
    textt1.place(x= 400, y = 200)
    btn = Button(fenetre, height=1, width=10, text=" FIN " , command= fenetre.destroy)
    btn.place(x=270,y=250)
    fenetre.mainloop()
    # afficher le gagant puis les 2 scores
elif var == human : 
    print('Player a gagner')
    fenetre = Tk()
    fenetre.title("Mancala")
    fenetre.iconbitmap('logo.ico')
    fenetre.config(background= "#c78594")
    fenetre.geometry("640x300")
    text = Label(fenetre,text="Vous avez Gagner",bg="#c78594",font= ("Arial",25,'bold','italic'))
    text.pack(pady= 20)
    textt = Label(fenetre,text="Score Final ",bg="#c78594",font= ("Arial",20,'bold'))
    textt.pack(pady= 30)
    textt1 = Label(fenetre,text="Human : "+str(dictplayer["magp"]),bg="#c78594",font= ("Arial",15))
    textt1.place(x= 100,y=200)
    textt1 = Label(fenetre,text="Computer : "+str(dictcomputer["magc"]),bg="#c78594",font= ("Arial",15))
    textt1.place(x= 400, y = 200)
    btn = Button(fenetre, height=1, width=10, text=" FIN " , command= fenetre.destroy)
    btn.place(x=270,y=250)
    fenetre.mainloop()
    # afficher le gagant puis les 2 scores
else : 
    print("egalité")
    fenetre = Tk()
    fenetre.title("Mancala")
    fenetre.iconbitmap('logo.ico')
    fenetre.config(background= "#c78594")
    fenetre.geometry("640x300")
    text = Label(fenetre,text="Egalité",bg="#c78594",font= ("Arial",25,'bold','italic'))
    text.pack(pady= 20)
    textt = Label(fenetre,text="Score Final ",bg="#c78594",font= ("Arial",20,'bold'))
    textt.pack(pady= 30)
    textt1 = Label(fenetre,text="Human : "+str(dictplayer["magp"]),bg="#c78594",font= ("Arial",15))
    textt1.place(x= 100,y=200)
    textt1 = Label(fenetre,text="Computer : "+str(dictcomputer["magc"]),bg="#c78594",font= ("Arial",15))
    textt1.place(x= 400, y = 200)
    btn = Button(fenetre, height=1, width=10, text=" FIN " , command= fenetre.destroy)
    btn.place(x=270,y=250)
    fenetre.mainloop()
    # afficher le gagant puis les 2 scores
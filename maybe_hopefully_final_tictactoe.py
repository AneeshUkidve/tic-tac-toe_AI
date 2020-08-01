import pygame
pygame.init()

#######################################################################################################################################################################
wn=pygame.display.set_mode((699, 699))
pygame.display.set_caption("Tic Tac Toe")

font = pygame.font.Font("freesansbold.ttf", 32)
white=(255,255,255)
red=(255,0,0)
orange=(255,140,0)

board=pygame.image.load("board.bmp")
cross=pygame.image.load("cross.bmp")
circle=pygame.image.load("circle.bmp")

plist = [board, cross, circle]

wn.blit(board, (0, 0))
pygame.display.update()

triplets = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]

sqlist=[]
class cell:
    def __init__(self, ccid):
        self.cid=ccid
        self.content=0
        sqlist.append(self)
        if self.cid%3!=0:
            self.x=(self.cid//3) * 233
        else:
            self.x=(self.cid//3 - 1) * 233
        self.y=(self.cid%3-1) * 233
        if self.y==-233:
            self.y=466
        self.xbound=[self.x, self.x+233]
        self.ybound=[self.y, self.y+233]

    def isinbounds(self, x, y):
        if x>=self.xbound[0] and x<=self.xbound[1] and y>=self.ybound[0] and y<=self.ybound[1]:
            yea=True
        else:
            yea=False
        return yea

    def display(self):
        wn.blit(plist[self.content], (self.x, self.y))
        

def locatesq(x):
    bang=False
    for i in sqlist:
        if i.cid==x:
            bang=i
    return bang

def genn():
    for g in range(9):
        abdull=cell(g+1)
genn()

go_ahead = True
    
def check_hit(tup):
    if go_ahead:
        x = tup[0]
        y = tup[1]
        b="no"
        for i in sqlist:
            if i.isinbounds(x,y):
                b = i.cid
        return b
    else:
        return "no"

def check_finish():
    global go_ahead
    phrase=False
    b=0
    for i in sqlist:
        if not i.content:
            b+=1
    if not b:
        go_ahead=False
        phrase= "No one"
        
    for i in triplets:
        if locatesq(i[1]).content and locatesq(i[2]).content and locatesq(i[0]).content:
            if locatesq(i[0]).content==locatesq(i[1]).content==locatesq(i[2]).content:
                go_ahead=False
                phrase = locatesq(i[1]).content
    return phrase
    
    
#######################################################################################################################################################################
'''

corner = 3
center = 2
edge = 1              <----- evaluation function values
double = 7
win = 1000
draw = 0

'''
#######################################################################################################################################################################
'''this section is dedicated to the Evaluate function
This aproach is going to revolve around the Position rather than the transformations to reach there

eg:[0,0,0,0,0,0,0,0] is position and [] is traansformation

While writing, I realized that I required much more clarity on how it needed to function...
Therefore, instead of dooing the entire thing, minimax tree and all, I created something that just looks one move ahead

Hopefully next file will be the last (including minimax tree).

'''

class evaluator:
    def __init__(self, location, team, addlist):
        self.loc = location
        self.team = team
        addlist.append(self)

def locate_eval(lister, value):
    retvar = False
    for element in lister:
        if element.loc == value:
            retvar = element
    return retvar

def pices(position):
    t1=0
    t2=0
    redundant = 0
    twislis = [redundant, t1, t2]
    for ob in position:
        if ob.loc == 1 or ob.loc == 3 or ob.loc == 7 or ob.loc == 9:
            twislis[ob.team] = twislis[ob.team] + 3
        elif ob.loc == 2 or ob.loc == 4 or ob.loc == 6 or ob.loc == 8:
            twislis[ob.team] += 1
        elif ob.loc == 5:
            twislis[ob.team] += 2
    pospic = twislis[1] - twislis[2]
    return pospic

def endcheck(position):
    remcel = 0
    for ppl in position:
        if ppl.team == 0:
            remcel += 1
    hasend = 0
    if remcel == 0:
        hasend = 1

    for trio in triplets:
        if locate_eval(position, trio[0]):
            if locate_eval(position, trio[0]).team:
                if locate_eval(position, trio[0]).team == locate_eval(position, trio[1]).team ==locate_eval(position, trio[2]).team:
                    if locate_eval(position, trio[0]).team == 1:
                        hasend = 2
                    else:
                        hasend = 3
    if hasend == 0:
        return False, 0
    elif hasend == 1:
        return True, 0
    elif hasend  == 2:
        return True, 1000
    elif hasend == 3:
        return True, -1000
    

def threats(position):
    p1 = 0
    p2 = 0
    for trio in triplets:
        concel1 = 0
        concel2 = 0
        for nos in trio:
            if locate_eval(position, nos).team == 1:
                concel1 += 1
            elif locate_eval(position, nos).team == 2:
                concel2 += 1
        if (concel1 == 2) and (concel2 == 0):
            p1 += 1
        if (concel1 == 0) and (concel2 == 2):
            p2 += 1
    nthreats = (p1 - p2)
    nthreats *= 8
    return nthreats

def evaluate(pos_array):
    list_of_evaluators = [] 
    for i in range(len(pos_array)):
        eman = evaluator(i+1, pos_array[i], list_of_evaluators)
    evalue = 0
    game_end, wldval = endcheck(list_of_evaluators)
    if game_end:
        evalue = wldval
    else:
        evalue += pices(list_of_evaluators)
        evalue += threats(list_of_evaluators)

    return game_end, evalue

def extract():
    retlist = []
    for ceel in sqlist:
        retlist.append(ceel.content)
    return retlist

def left_indices(poslist):
    retleft = []
    for i in range(len(poslist)):
        if poslist[i] == 0:
            retleft.append(i)
    return retleft

target_depth = 6

class listing:
    def __init__(self, deep, arr):
        self.deep = deep
        self.container = []
        arr.append(self)

def locdeep(array, num):
    req = False
    for i in array:
        if i.deep == num:
            req = i
    return req

class node:
    def __init__(self, board, parent, depth, fullist):
        self.board = board
        self.parent = parent
        self.depth = depth
        self.worth = 9999
        self.minimaxlist = []
        self.disposable_list = []
        self.left_indices = []
        self.cofactor = 1
        locdeep(fullist, self.depth).container.append(self)
        jojobool, nwor = evaluate(self.board)
        if self.depth == 1 and jojobool:
            self.worth = nwor*10            
        elif jojobool or self.depth == target_depth:
            self.worth = nwor
        else:
            if self.depth%2 == 0:
                self.keyword = 1
            else:
                self.keyword = 2
            self.left_indices = left_indices(self.board)

            for lk in self.left_indices:
                self.disposable_list = []
                for x in self.board:
                    self.disposable_list.append(x)
                self.disposable_list[lk] = self.keyword
                momo = node(self.disposable_list, self, (self.depth+1), fullist)

            
    def evalfunc(self):
        if self.worth == 9999:
            if self.keyword == 1:
                self.worth = max(self.minimaxlist)
            elif self.keyword == 2:
                self.worth = min(self.minimaxlist)
        else:
            self.worth *= self.cofactor
        if self.depth != 0:
            self.parent.minimaxlist.append(self.worth)
            
                    
def complay():
    skay = extract()
    art = []
    for i in range(target_depth+1):
        ksas = listing(i, art)
    start = node(skay, None, 0, art)
    for bags in range(target_depth + 1):
        for each in art[target_depth - bags].container:
            each.evalfunc()
    brak = False
    for hk in art[1].container:
        if hk.worth == start.worth:
            brak = hk
            break
    for i in range(9):
        if start.board[i] != brak.board[i]:
            sar = i+1
            break
    locatesq(sar).content = 1
    locatesq(sar).display()

#######################################################################################################################################################################

def resetg():
    global turn
    global go_ahead
    turn = 1
    go_ahead = True
    for jin in sqlist:
        jin.content = 0
        jin.display()
        pygame.display.update()
    print("reset")

locatesq(2).content = 1
locatesq(2).display()
pygame.display.update()

turn = 2
def main(cel):
    global selected
    global turn
    global posit
    if turn == 1:
         complay()
         turn = 2
    elif turn==2:
        if not locatesq(cel).content:
            locatesq(cel).content = (turn)
            locatesq(cel).display()
            rekt = check_finish()
            if go_ahead == True:
                complay()        

    
    ret = check_finish()
    if go_ahead==False:
        text = font.render(str(ret) + " wins", True, white, red)
        textRect=text.get_rect()
        textRect.center=(350,350)
        wn.blit(text, textRect)
    pygame.display.update()



loop=True
while loop:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            loop=False
        if event.type== pygame.MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            avagadro = check_hit(pos)
            if avagadro != "no":
                main(avagadro)
    keys=pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        resetg()

pygame.quit()

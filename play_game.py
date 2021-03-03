# Grupa 231 - TALMACEL SERGIU

from copy import deepcopy, copy
import pygame, sys
import time


def bounded(x, y):
    return 0 <= x < 8 and 0 <= y < 8


class Game:
    SYMBOLS = ['n', 'a']
    JMIN = None
    JMAX = None
    MAX_DEPTH = None

    def __init__(self):
        # tabla este o matrice de 8x8
        self.matrix = [['.' for j in range(8)] for i in range(8)]

    def init_game(self):
        # pregateste tabla de joc punand piesele pe pozitiile lor
        for i in range(3):
            if i % 2 == 0:
                for j in range(1, len(self.matrix[i]), 2):
                    self.matrix[i][j] = 'a'
                for j in range(0, len(self.matrix[i]), 2):
                    self.matrix[7 - i][j] = 'n'
            else:
                for j in range(0, len(self.matrix[i]), 2):
                    self.matrix[i][j] = 'a'
                for j in range(1, len(self.matrix[i]), 2):
                    self.matrix[7 - i][j] = 'n'


class Stare:

    def __init__(self, matrix, current_depth, score, current_player, move=None,
                 multi_move=False,
                 possible_moves=None,
                 selected_state=None):
        self.matrix = deepcopy(matrix)
        self.current_depth = current_depth
        self.score = score
        self.move = move
        self.multi_move = multi_move
        self.possible_moves = copy(possible_moves) or []
        self.current_player = current_player
        # self.black_disks = black_disks
        # self.white_disks = white_disks
        self.selected_state = selected_state

    def opponent(self):
        return 'n' if self.current_player in 'a' else 'a'

    def bounded(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def stop(self, board, x, y, dx, dy, player):
        # functie folosita pentru o miscare multipla
        # cand nu mai pot sa sar peste un openent ma opresc
        opponent = self.opponent()
        vx = x + dx
        vy = y + dy
        next_x = vx + dx
        next_y = vy + dy

        # daca nu mai am unde sa sar
        if not bounded(next_x, next_y):
            return True
        # daca nu am un vecin oponent peste care sa sar
        if board[vx][vy] != opponent and board[vx][vy] != opponent.upper():
            return True
        # daca am un vecin oponent , verific daca in noua pozitie se afla ceva sau nu
        if board[next_x][next_y] != '.':
            return True

        return False

    def countDisks(self, matrix, player):
        cnt = 0
        for i in range(8):
            for j in range(8):
                if matrix[i][j] in player:
                    cnt += 1
        return cnt

    def moves(self, player, checkExistence=False):
        """

        :param player: current player
        :param checkExistence: False - will generate all the possible moves of the player from the current board configuration
                               True - used in self.final() method to check the existence of a move
        :return: the moves of the player from the current configuration depending on the checkExistence flag
        """

        l_moves = []
        opp = 'n' if player == 'a' else 'a'
        # ofera directiile in functie de culoarea piesei lui player

        # daca este piesa rege adauga toate directiile

        if self.multi_move and not checkExistence:
            # print("IE MULTIMOVE")
            x, y = self.move
            if player.upper() == self.matrix[x][y]:
                directs = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
            else:
                directs = [[-1, -1], [-1, 1]] if player == 'n' else [[1, -1], [1, 1]]

            for directie in directs:
                vx, vy = x + directie[0], y + directie[1]
                next_x, next_y = vx + directie[0], vy + directie[1]
                if self.bounded(vx, vy) and not self.stop(self.matrix, x, y, directie[0], directie[1],
                                                          self.current_player):

                    baseline = 0 if player in ['n', 'N'] else 7

                    temp = deepcopy(self.matrix)
                    piesa = temp[x][y]

                    if next_x == baseline:
                        temp[next_x][next_y] = piesa.upper()
                    else:
                        temp[next_x][next_y] = piesa

                    temp[x][y] = '.'
                    temp[vx][vy] = '.'
                    l_moves.append(
                        Stare(temp, self.current_depth - 1, None, self.opponent(), move=[next_x, next_y],
                              multi_move=True))


        else:

            for i in range(8):
                for j in range(8):

                    # pentru fiecare piesa de tip player
                    if self.matrix[i][j] == player or self.matrix[i][j] == player.upper():

                        # daca e piesa rege se poate deplasa in toate cele 4 directii
                        if player.upper() == self.matrix[i][j]:
                            directs = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
                        else:
                            directs = [[-1, -1], [-1, 1]] if player == 'n' else [[1, -1], [1, 1]]

                        for k in range(len(directs)):

                            vx = i + directs[k][0]
                            vy = j + directs[k][1]
                            # daca celula vecina pe diagonala exista
                            if self.bounded(vx, vy):
                                # print(opp, opp.upper(), self.stop(self.matrix, i, j,
                                #                                   dir[k][0],
                                #                                   dir[k][1],
                                #                                   self.current_player))

                                # daca acel loc este gol se poate face o mutare simpla
                                if self.matrix[vx][vy] == '.':

                                    temp = deepcopy(self.matrix)
                                    piesa = temp[i][j]
                                    temp[i][j] = '.'
                                    # daca ajung pe baseline piesa devine rege
                                    baseline = 0 if player in ['n', 'N'] else 7
                                    if vx == baseline:
                                        temp[vx][vy] = piesa.upper()
                                    else:
                                        temp[vx][vy] = piesa
                                    # adauga mutarea simpla la lista de mutari
                                    l_moves.append(
                                        Stare(temp, self.current_depth - 1, None, self.opponent(), move=[vx, vy]))

                                    # atlfel celula vecina contine o piesa

                                # daca este o piesa de culoarea jucatorului opus si se poate sari peste aceasta
                                elif self.matrix[vx][vy] in [opp, opp.upper()] and not self.stop(self.matrix, i, j,
                                                                                                 directs[k][0],
                                                                                                 directs[k][1],
                                                                                                 self.current_player):
                                    # print("UITE O MUTARE CU ELIMINARE")

                                    next_x, next_y = vx + directs[k][0], vy + directs[k][1]
                                    temp = deepcopy(self.matrix)
                                    piesa = temp[i][j]
                                    temp[i][j] = '.'
                                    temp[vx][vy] = '.'
                                    temp[next_x][next_y] = piesa

                                    baseline = 0 if piesa in ['n', 'N'] else 7
                                    if next_x == baseline:
                                        temp[next_x][next_y] = piesa.upper()
                                    l_moves.append(
                                        Stare(temp, self.current_depth - 1, None, self.opponent(),
                                              move=[next_x, next_y], multi_move=True))
                                else:
                                    pass
                                    # print("NU IE NICIO MUTARE")

        return l_moves

    def final(self):
        """
        :return: n/a/tie if there the game has ended, False otherwise
        """
        ai_moves = self.moves(Game.JMAX, checkExistence=True)
        user_moves = self.moves(Game.JMIN, checkExistence=True)

        # daca nu mai are mutari jucatorul, atunci pierde jocul
        if len(ai_moves) == 0:
            return Game.JMIN
        if len(user_moves) == 0:
            return Game.JMAX

        # daca nu mai este nicio piesa pe tabla
        blacks, whites = self.countDisks(self.matrix, ['N', 'n']), self.countDisks(self.matrix, ['a', 'A'])
        if blacks == 0 or whites == 0:
            if blacks > whites:
                return Game.JMIN if Game.JMIN == 'n' else Game.JMAX
            elif blacks < whites:
                return Game.JMAX if Game.JMAX == 'a' else Game.JMIN
            return 'tie'

        return False

    def afis_final(self):
        """
        :return: prints the winner of the game and returns True if the game has ended
        """
        final = self.final()
        if final:
            if final == Game.JMIN:
                print("A castigat " + Game.JMIN)
            elif final == Game.JMAX:
                print("A castigat " + Game.JMAX)
            else:
                print("Remiza")
            return True
        return False

    def estimate_score(self):
        final = self.final()
        if final:
            if final == Game.JMAX:
                return 9999 + self.current_depth
            elif final == Game.JMIN:
                return -9999 - self.current_depth
            return 0
        return self.heuristic()
        # return self.second_heuristic()

    def find_piesa(self, x, y, dir):
        x += dir[0]
        y += dir[1]
        while self.bounded(x, y) and self.matrix[x][y] in ['.', self.current_player, self.current_player.upper()]:
            x += dir[0]
            y += dir[1]
        if self.bounded(x, y):
            return x, y
        return None, None

    def heuristic(self):

        """
        Aceasta euristica este prielnica jocatorului MAX, deoarece s-au folosit strategii
        de joc ce asigura punerea in dificultate a adversaruilui.S-a luat in considerare
        protejarea pieselor, atacarea celor vulnerabile si strategia de aparare a bazei
        pentru a opri adversarul sa obtina piese de tip rege.

        evaluam configuratia de joc dupa urmatoarele criterii
        1. weight-ul unei piese de culoarea current_player pe tabla = 5
        2.  weight-ul unei piese piese rege ale jucatorului curent = 7.75
        3.  weight-ul unei piese piese de culoare current_player de pe baseline-ul sau = 4
        4. weight-ul unei piese afla in mijlocul tablei de joc = 2.5
        5.  weight-ul unei piese care poate fi luata de adversar = -3
        :return: h_estimate
        """
        # 1.
        blacks, whites = 0, 0
        weights = [0 for _ in range(6)]
        directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
        user_dir = directions[:2] if self.current_player == 'n' else directions[2:]
        for i in range(8):
            for j in range(8):
                blacks += 1 if self.matrix[i][j] in ['N', 'n'] else 0
                whites += 1 if self.matrix[i][j] in ['A', 'a'] else 0
                if self.matrix[i][j] == self.current_player or self.matrix[i][j] == self.current_player.upper():

                    # numarul de piese rege
                    if self.matrix[i][j] == self.current_player.upper():
                        weights[1] += 7.75

                    # numarul de piese normale
                    else:
                        weights[0] += 5

                    # numarul de piese de pe baseline in functie de tipul de piesa
                    # conform strategiilor de joc este o strategie buna sa ai cat mai multe
                    # piesa pe baseline pentru a preveni creare de piese de tip rege ale adversarului
                    if self.current_player in ['n', 'N']:
                        if i == 7:
                            weights[2] += 4
                    elif self.current_player in ['a', 'A']:
                        if i == 0:
                            weights[2] += 4

                    # numarul de piese din mijlocul tablei
                    # la fel este o strategie buna pentru atac
                    if 3 <= i <= 4 and 3 <= j <= 4:
                        weights[3] += 2

                    # numar piese vulnerabile
                    # adica piese ce pot fi capturate de oponent la urmatoare tura
                    for d in user_dir:

                        vx = d[0] + i
                        vy = d[1] + j
                        back_x = i - d[0]
                        back_y = j - d[1]
                        next_x, next_y = vx + d[0], vy + d[1]
                        if self.bounded(vx, vy) and self.matrix[vx][vy] in [self.opponent(), self.opponent().upper()]:
                            if self.bounded(back_x, back_y) and self.matrix[back_x][back_y] == '.':
                                weights[4] -= 3
                        if self.bounded(vx, vy) and self.matrix[vx][vy] in [self.opponent(), self.opponent().upper()]:
                            if self.bounded(next_x, next_y) and self.matrix[next_x][next_y] == '.':
                                # daca elimin o piesa rege este o mutare mai buna
                                if self.matrix[vx][vy] == self.opponent().upper():
                                    weights[5] += 10
                                else:
                                    weights[5] += 7

        diff = (blacks - whites) if self.current_player == 'n' else (whites - blacks)
        # cand sunt mai putin piese, AI adopta o tactica mai ofensiva
        if blacks + whites <= 10:
            return sum(weights) + diff
        return sum(weights)


def second_heuristic(self):
    """
    Aceasta a doua euristica foloseste cateva elemente din euristica anterioara,
    insa face niste completari care pun accent si pe tipul piesei care este
    vulnerabila sau care poate fi atacata(cea rege avand un scor mai mare);
    am luat in considerare si modul in care piesele se deplaseaza spre baza
    adversarului, dar si pozitionarea pieselor de tip rege, favorizand o
    amplasare mai apropiata de vecinatatea pieselor oponentului.

    1. weight-ul unei piese de culoarea current_player pe tabla = 4
       weight-ul unei piese piese rege ale jucatorului curent =8
    2. cat de aproape este piesa de a deveni rege
    3. in cazul pieselor rege, cat de departe sunt de piesele adversarului(suma de distante euclidiene)
    4. diferenta dintre numarul de piese al jucatorului curent - piesele oponentului

    :return:
    """
    directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
    # aceasta matrice indica valoarea pe care o are mutarea unei piese pe o celula aleasa
    # se va aduna la media ponderilor adunate in lista weights

    # mijlocul tablei este punctul cel mai vulnerabil
    # in timp ce lateralele sunt sigure,iar linia bazei transforma piesa in rege

    points = [[0, 4, 0, 4, 0, 4, 0, 4],
              [4, 0, 3, 0, 3, 0, 3, 0],
              [0, 3, 0, 2, 0, 2, 0, 4],
              [4, 0, 2, 0, 1, 0, 3, 0],
              [0, 3, 0, 1, 0, 2, 0, 4],
              [4, 0, 2, 0, 1, 0, 3, 0],
              [0, 3, 0, 2, 0, 2, 0, 4],
              [4, 0, 4, 0, 4, 0, 4, 0]]

    weights = [0 for i in range(4)]
    whites, blacks = 0, 0
    for i in range(8):
        for j in range(8):

            # numaram discurile de fiecare culoarea
            blacks += 1 if self.matrix[i][j] in ['N', 'n'] else 0
            whites += 1 if self.matrix[i][j] in ['A', 'a'] else 0

            if self.matrix[i][j] in [self.current_player, self.current_player.upper()]:

                # daca e piesa normala
                if self.matrix[i][j] == self.current_player:
                    weights[0] += 4

                    # cat de aproape este piesa de a deveni rege ( nr de linii din tabla - cate mai are pana ajunge pe ultima linie)

                    # cu cat se apropie piesa mai multe de a deveni rege, scorul creste( negru - rege pentru i=0, alb -rege pentru i =7)
                    if self.matrix[i][j] == 'n':
                        weights[1] += (7 - i)
                    elif self.matrix[i][j] == 'a':
                        weights[1] += i
                else:
                    # daca e piesa rege
                    weights[0] += 8

                # cat de aproape este piesa rege de celelalte piese
                for d in directions:
                    if self.matrix[i][j] == self.current_player.upper():
                        # gaseste pe diagonala in directia d, o piesa adversara,daca exista
                        x, y = self.find_piesa(i, j, d)
                        if x and y:
                            weights[2] += (x - i) * (x - i) + (y - j) * (y - j)
                    vx = d[0] + i
                    vy = d[1] + j
                    back_x = i - d[0]
                    back_y = j - d[1]
                    next_x, next_y = vx + d[0], vy + d[1]
                    # piesele pe care le poate captura jucatorul, daca e piesa rege are un scor mai mare
                    if self.bounded(vx, vy) and self.matrix[vx][vy] in [self.opponent(), self.opponent().upper()]:
                        if self.bounded(next_x, next_y) and self.matrix[next_x][next_y] == '.':
                            if self.matrix[next_x][next_y] == self.opponent().upper():
                                weights[3] += 7
                            else:
                                weights[3] += 4
                    # piese care pot fi capturate; la fel daca este piesa rege atunci se scade mai mult scorul
                    if self.bounded(vx, vy) and self.matrix[vx][vy] in [self.opponent(), self.opponent().upper()]:
                        if self.bounded(back_x, back_y) and self.matrix[back_x][back_y] == '.':
                            if self.matrix[vx][vy] == self.opponent().upper():
                                weights[3] -= 6
                            else:
                                weights[3] -= 3
        # adunam piesa la media sumei date pentru a face AI-ul in caz de egalitate a scorului
        # sa imi aleaga piesa care ma pozitioneaza mai bine
        if self.move:
            return sum(weights) / 4 + points[self.move[0]][self.move[1]]
        return sum(weights) / 4

    def __str__(self):
        s = '  '
        for i in range(8):
            s += str(i) + ' '
        s += '\n'
        for index, line in enumerate(self.matrix):
            s += str(chr(index + ord('a'))) + ' '
            for el in line:
                s += str(el) + ' '
            s += '\n'

        return s


def minimax(state):
    moves = state.moves(state.current_player)
    if state.final() or state.current_depth == 0 or len(moves) == 0:
        state.score = state.estimate_score()
        return state
    mutari_score = [minimax(move) for move in moves]

    if state.current_player == Game.JMIN:
        state.selected_state = min(mutari_score, key=lambda x: x.score)
    else:
        state.selected_state = max(mutari_score, key=lambda x: x.score)

    state.score = state.selected_state.score
    return state


def alpha_beta(alpha, beta, state):
    possible_moves = state.moves(state.current_player)
    if state.final() or len(possible_moves) == 0 or state.current_depth == 0:
        state.score = state.estimate_score()
        return state

    if state.current_player == Game.JMIN:
        state.score = float('inf')
        for move in possible_moves:
            stare_noua = alpha_beta(alpha, beta, move)
            if stare_noua.score < state.score:
                state.score = stare_noua.score
                state.selected_state = stare_noua

            if stare_noua.score < beta:
                beta = stare_noua.score
                if alpha >= beta:
                    break

    elif state.current_player == Game.JMAX:
        state.score = float('-inf')

        for move in possible_moves:
            stare_noua = alpha_beta(alpha, beta, move)
            if stare_noua.score > state.score:
                state.score = stare_noua.score
                state.selected_state = stare_noua
            if stare_noua.score > alpha:
                alpha = stare_noua.score
                if alpha >= beta:
                    break

    state.score = state.selected_state.score
    return state


def deseneaza_grid(display, tabla):
    """
    :param display: the screen of the game
    :param tabla: the current config of the board
    :return: a list of squares composing the board
    """
    # the width and height of a square
    w_gr, h_gr = 50, 50

    drt = [[None for j in range(8)] for i in range(8)]
    for linie in range(8):
        for coloana in range(8):

            patr = pygame.Rect(coloana * (w_gr + 1), linie * (h_gr + 1), w_gr, h_gr)
            drt[linie][coloana] = patr

            if linie % 2 == 0:
                if coloana % 2 == 0:
                    pygame.draw.rect(display, (255, 255, 255), patr)
                else:
                    pygame.draw.rect(display, (0, 0, 0), patr)
            else:
                if coloana % 2:
                    pygame.draw.rect(display, (255, 255, 255), patr)
                else:
                    pygame.draw.rect(display, (0, 0, 0), patr)

            if tabla[linie][coloana] == 'a':

                pygame.draw.circle(display, (255, 255, 255),
                                   (coloana * (w_gr + 1) + 25, linie * (h_gr + 1) + 25), 20)
            elif tabla[linie][coloana] == 'A':
                pygame.draw.circle(display, (255, 0, 0),
                                   (coloana * (w_gr + 1) + 25, linie * (h_gr + 1) + 25), 20)
                pygame.draw.circle(display, (255, 255, 255),
                                   (coloana * (w_gr + 1) + 25, linie * (h_gr + 1) + 25), 17)
            elif tabla[linie][coloana] == 'N':
                pygame.draw.circle(display, (255, 0, 0),
                                   (coloana * (w_gr + 1) + 25, linie * (h_gr + 1) + 25), 20)
                pygame.draw.circle(display, (0, 0, 0),
                                   (coloana * (w_gr + 1) + 25, linie * (h_gr + 1) + 25), 17)

            elif tabla[linie][coloana] == 'n':
                pygame.draw.circle(display, (255, 255, 255),
                                   (coloana * (w_gr + 1) + 25, linie * (h_gr + 1) + 25), 20)
                pygame.draw.circle(display, (0, 0, 0),
                                   (coloana * (w_gr + 1) + 25, linie * (h_gr + 1) + 25), 19)

        pygame.display.flip()
    time.sleep(0.3)

    return drt


def check_simple_move(current_state, vx, vy):
    """
    :param current_state:
    :param vx: coordonata x vecina pe o directie selectata
    :param vy: coordonata y vecina pe o directie selectata
    :return: True daca pot deplasa piesa pe (vx,vy), altfel False
    """
    return current_state.bounded(vx, vy) and current_state.matrix[vx][vy] == '.'


def check_elimination_move(current_state, vx, vy, next_x, next_y):
    """

    :param current_state:
    :param vx: coord x vecina pe o diag
    :param vy: coord y vecina pe o diag
    :param next_x: coord x pentru o mutare cu eliminare
    :param next_y: coord y pentru o mutare cu eliminare
    :return: True daca pot sa mut eliminand piesa oponentului de pe (vx,vy), altfel False
    """
    return current_state.bounded(vx, vy) and current_state.matrix[vx][
        vy] in [current_state.opponent(), current_state.opponent().upper()] and current_state.bounded(next_x,
                                                                                                      next_y) and \
           current_state.matrix[next_x][
               next_y] == '.'


# folosita pentru UI, atunci cand userul apasa pe o piesa
# pe care vrea sa o mute, i se afiseaza mutarea de la (x,y)
def draw_possible_move(screen, x, y):
    pygame.draw.circle(screen, (255, 255, 255),
                       (y * (50 + 1) + 25, x * (50 + 1) + 25), 20)
    pygame.draw.circle(screen, (225, 225, 0),
                       (y * (50 + 1) + 25, x * (50 + 1) + 25), 19)


# arata miscarile posibile cand apas pe o piesa
def show_moves(current_state, screen, x, y, interface=True):
    """
    :param current_state: config. curenta a tablei de joc
    :param screen: ecranul pe care se deseneaza
    :param x: coord x a piesei pe care vreau sa o mut
    :param y: coord y a piesei pe care vreau sa o mut
    :param interface: implicit True, in cazul in care vreau sa desenez-optiunea cu UI, False pentru a rula jocul din consola
    :return: mutarile posibile, coordonatele piesei intiale si un flag pentru a indica daca exista mutari cu eliminare folosit pentru mutarile mutiple
    """
    moves = []
    hasEliminationMove = False
    directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
    # setez directiile in functie de piesa
    if current_state.matrix[x][y] in ['N', 'A']:
        user_dir = directions
    else:
        user_dir = directions[:2] if current_state.current_player == 'n' else directions[2:]
    for i in range(len(user_dir)):
        vx, vy = x + user_dir[i][0], y + user_dir[i][1]
        next_x, next_y = vx + user_dir[i][0], vy + user_dir[i][1]
        # generez posibilele mutari
        # daca e mutari simpla o adaug
        if check_simple_move(current_state, vx, vy):
            # daca aleg sa joc cu UI atunci desenez
            if interface:
                draw_possible_move(screen, vx, vy)
            moves.append([vx, vy, 0])
        # daca e mutare multipla atunci marcheaza ca exista cel putin o mutare de acest tip
        # si adauga la lista de mutari
        elif check_elimination_move(current_state, vx, vy, next_x, next_y):

            # daca aleg sa joc cu UI atunci desenez
            if interface:
                draw_possible_move(screen, next_x, next_y)

            hasEliminationMove = True
            moves.append([next_x, next_y, 1])
    return moves, (x, y), hasEliminationMove


def print_mutari(mutari, name):
    print("Mutari " + name)
    for m in mutari:
        for line in m.matrix:
            print(line)
        print()


def get_user_input():
    """
    Cere si valideaza datele de la user si initializeaza tabla de joc  si stare de start
    :return: stare initiala la jocului,stare initiala, directiile de deplasare ale userului,alg. ales
    """
    game = Game()
    game.init_game()

    while True:
        user_disk = input("Chose the colour of your disk: \'a\' or \'n\' ")
        if len(user_disk) > 1 or user_disk[0] not in ['a', 'n']:
            print("Please enter a valid disk colour")
        else:
            break

    while True:
        try:
            algo = int(input("Choose the algorithm:\n 1.Minimax\n 2.Alpha-Beta\n"))
            if 0 < algo <= 2:
                break
            else:
                print("Choose a valid algorithm")

        except ValueError:
            print("Choose a valid algorithm")

    while True:
        try:
            depth = int(input('Choose the game difficulty(0-Easy, 1-Intermediate , 2 - Hard) '))
            if 0 <= depth <= 2:
                break
            else:
                print("Please enter a valid level")

        except ValueError:
            print("Please enter a valid level")

    if depth == 0:
        Game.MAX_DEPTH = 2
    elif depth == 1:
        Game.MAX_DEPTH = 3
    else:
        Game.MAX_DEPTH = 4

    Game.JMIN = user_disk
    Game.JMAX = 'n' if Game.JMIN == 'a' else 'a'

    # alege directiile user-ului in functie de culoarea aleasa
    directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]

    user_dir = directions[:2] if user_disk == 'n' else directions[2:]
    ai_dir = directions[2:] if user_disk == 'n' else directions[:2]

    # initializeaza stare de start a jocului
    current_state = Stare(game.matrix, Game.MAX_DEPTH, None, Game.SYMBOLS[0])
    return game, current_state, algo, directions


def print_board(matrix):
    # afiseaza tabla de joc

    print(' ', end='  ')
    for lit in range(8):
        print(lit, end=' ')
    print()
    for index, line in enumerate(matrix):
        print(chr(ord('a') + index), end='  ')
        for el in line:
            print(el, end=' ')
        print()


def play():
    # functie in care userului alege cum vrea sa joace jocul UI/consola
    # porneste jocul in functie de alegerea lui
    while True:
        try:
            tip_joc = int(input("Selectati cum doriti sa jucati jocul(0 - Consola, 1- Interfata grafica) "))
            if 0 <= tip_joc <= 1:
                break
            print("Please enter a valid number")

        except ValueError:
            print("Va rugam alegeti o modalitate de joc corecta")

    # porneste jocul in functie de alegerea lui

    if tip_joc == 0:
        play_console()
    elif tip_joc == 1:
        play_UI()


def request_user_move():
    exit = False
    lin, col = -1, -1
    # userul are posibilitatea de a selecta oprirea jocului
    # atunci cand ii se cere sa introduca linia
    while True:
        # verifica daca este o linie valida
        lin = input("Select a row (a-h) or type 'exit' to end the game ")
        if lin.lower() == 'exit':
            exit = True
            break
        if len(lin) > 1:
            print("Enter a valid row")

        lin = ord(lin[0]) - ord('a')
        if 0 <= lin <= 7:
            break
        else:
            print("Enter a valid row")

    while True and not exit:
        # verifica daca este o coloana valida
        try:
            col = int(input("Select a column(0-7)"))
            if 0 <= col <= 7:
                break
            else:
                print("Please enter a valid column")
        except ValueError:
            print("Please enter a valid column")
    # daca userul a selectat exit, vom avea in col valoarea  -1
    return lin, col


def play_console():
    user_count, ai_count = 0, 0
    game, current_state, algo, directions = get_user_input()

    print_board(current_state.matrix)
    while True:

        if current_state.afis_final():
            game_end_time = int(round(time.time() * 1000))
            print_time(game_start_time, game_end_time, 'Jocul a durat ')
            print("Mutari user: " + str(user_count) + ' ' + 'Mutari AI: ' + str(ai_count))
            return
        if current_state.current_player == Game.JMIN:
            linie, col = -1, - 1

            if len(current_state.moves(Game.JMIN)) > 0:

                user_count += 1

                print("Este randul userului")
                user_turn_start = int(round(time.time() * 1000))

                mutat = False
                mutari_curente = []
                wrong_direction = False
                while not mutat:
                    # daca imi continui tura
                    if current_state.multi_move:

                        # gasesc mutarile posibile
                        mutari_curente, start_move, hasEliminationMove = show_moves(current_state, None,
                                                                                    current_state.move[0],
                                                                                    current_state.move[1],
                                                                                    interface=False)
                        # daca nu pot continua mutarea( nu pot captura o piesa = hasEliminationMove)
                        if not hasEliminationMove:
                            # ma opresc,am mutat pe tura mea, urmeaza tura oponentului
                            current_state.multi_move = False
                            mutat = True
                            current_state.current_player = current_state.opponent()
                            break

                    # cere utilizatorului mutarea
                    if not wrong_direction:
                        linie, col = request_user_move()

                        if col == -1:
                            print("Jocul a fost inchis de user")
                            print("SCOR: USER-" + str(current_state.countDisks(current_state.matrix,
                                                                               current_state.current_player)) + '   SCOR AI- ' + str(
                                current_state.countDisks(current_state.matrix, current_state.opponent())))
                            return

                    print("Piesa selectata", current_state.matrix[linie][col])
                    d = request_user_direction(current_state.multi_move, current_state.matrix[linie][col])

                    # daca aleg o piesa de a mea atunci aflu mutarile posibile
                    if current_state.matrix[linie][col] in [current_state.current_player,
                                                            current_state.current_player.upper()]:
                        mutari_curente, start_move, _ = show_moves(current_state, None, linie,
                                                                   col, interface=False)
                    # print("ASTEA MOVES", mutari_curente)
                    vecx, vecy = linie + directions[d][0], col + directions[d][1]
                    next_x, next_y = vecx + directions[d][0], vecy + directions[d][1]

                    # daca directia in care am ales sa merg este valida
                    # altfel reia bucla si intreaba userul din nou
                    if [next_x, next_y, 1] in mutari_curente or [vecx, vecy, 0] in mutari_curente:

                        # verific daca am ajuns in baza, in caz afirmativ , fac piesa rege
                        baseline = 0 if current_state.current_player == 'n' else 7

                        piesa = current_state.matrix[start_move[0]][start_move[1]]

                        # muta piesa mea din locul curent
                        current_state.matrix[start_move[0]][start_move[1]] = '.'

                        # daca am o mutare in care capturez o piesa
                        if [next_x, next_y, 1] in mutari_curente:
                            # determin directia mutarii
                            # dx, dy = (linie - start_move[0]) // 2, (col - start_move[1]) // 2
                            # # gasesc vecinul direct din directia mutarii
                            # vx, vy = start_move[0] + dx, start_move[1] + dy
                            if next_x == baseline:
                                piesa = piesa.upper()

                            # elimin piesa oponentului
                            current_state.matrix[vecx][vecy] = '.'

                            # mut piesa mea peste piesa oponentului
                            current_state.matrix[next_x][next_y] = piesa

                            # salvez pozitia unde mi-a ramas piesa pentru a continua de acolo
                            # pentru ca am o mutare multipla
                            current_state.move = [next_x, next_y]

                            # marchez ca este o mutare multipla
                            # pentru a nu da tura oponentului si a-mi continua tura cu piesa
                            # cu care am facut mutarea precedenta
                            current_state.multi_move = True


                        # daca este o mutare simpla
                        else:
                            if vecx == baseline:
                                piesa = piesa.upper()

                            # deplasez piesa cu o patratica in diagonala aleasa
                            current_state.matrix[vecx][vecy] = piesa

                            # dau tura oponentului
                            current_state.current_player = current_state.opponent()
                            mutat = True
                            # redeseaza tabla dupa mutare
                            user_turn_end = int(round(time.time() * 1000))

                            print_board(current_state.matrix)

                            print("Mutarea userului a durat " + str(
                                user_turn_end - user_turn_start) + ' milisecunde')
                            break

                        # redeseaza tabla dupa mutare
                        user_turn_end = int(round(time.time() * 1000))

                        print_board(current_state.matrix)

                        print("Mutarea userului a durat " + str(
                            user_turn_end - user_turn_start) + ' milisecunde')

                    else:
                        wrong_direction = True

        # mutarea AI-ului
        else:
            print("Este randul ai-ului")
            ai_turn_start = int(round(time.time() * 1000))

            # daca mai are mutari AI-ul
            if len(current_state.moves(current_state.current_player)) > 0:

                # daca aleg algoritmul minimax
                if algo == 1:
                    stare_aleasa = minimax(current_state)
                    ai_turn_end = int(round(time.time() * 1000))
                    current_state.matrix = deepcopy(current_state.selected_state.matrix)
                    # redesenez tabla cu mutarea noua

                    # copiez mutarea facuta in cazul in care el poate face o mutare mutipla
                    current_state.move = copy(current_state.selected_state.move)
                    current_state.multi_move = current_state.selected_state.multi_move
                    print_board(current_state.matrix)
                    print("Mutarea ai-ului a durat " + str(ai_turn_end - ai_turn_start) + ' milisecunde')

                    # numara mutarile facut de ai
                    ai_count += 1

                    # daca mutarea curenta nu e multipla atunci dau tura userului
                    if not current_state.multi_move or len(current_state.moves(current_state.current_player)) == 0:
                        current_state.multi_move = False
                        current_state.current_player = current_state.opponent()
                # daca a ales alpha-beta
                else:

                    stare_aleasa = alpha_beta(-5000, 5000, current_state)
                    ai_turn_end = int(round(time.time() * 1000))
                    # salvez mutarea aleasa de AI
                    current_state.matrix = deepcopy(current_state.selected_state.matrix)

                    # redesenez tabla cu mutarea noua

                    # copiez mutarea facuta in cazul in care el poate face o mutare mutipla
                    current_state.move = copy(current_state.selected_state.move)
                    current_state.multi_move = current_state.selected_state.multi_move
                    print("MOVE", current_state.move)

                    print_board(current_state.matrix)
                    print("Mutarea ai-ului a durat " + str(ai_turn_end - ai_turn_start) + ' milisecunde')

                    # numara mutarile facut de ai
                    ai_count += 1

                    # daca mutarea curenta nu e multipla atunci dau tura userului
                    if not current_state.multi_move or len(current_state.moves(current_state.current_player)) == 0:
                        current_state.multi_move = False
                        current_state.current_player = current_state.opponent()


def request_user_direction(multimove, player):
    # cere directiile de deplasare in functie de tipul piesei
    # valideaza directia, in caz negativ cere o noua directie
    msg = '0-Left , 1 - Right'
    if player in ['N', 'A']:
        msg = '0-LeftUp, 1-RightUp, 2 - RightDown, 3- LeftDown '

    while True:
        try:
            d = int(input('Ghoose a direction ' + msg))
            if player in ['N', 'A']:
                if 0 <= d < 4:
                    break
                else:
                    print("Please enter a valid direction")
            else:
                if 0 <= d <= 1:
                    break
                else:
                    print("Please enter a valid direction")
        except ValueError:
            print("Please enter a valid direction")
    return d


# functie pentru a putea juca cu interfata grafica
def play_UI():
    user_count, ai_count = 0, 0
    game, current_state, algo, directions = get_user_input()
    print('CURRENT PLAYER', current_state.current_player)
    pygame.init()
    screen = pygame.display.set_mode((408, 408))

    rectangles = deseneaza_grid(screen, current_state.matrix)

    while True:

        # daca am ajuns in stare finala opreste jocul si arata castigatorul
        if current_state.afis_final():
            print_board(current_state.matrix)
            game_end_time = int(round(time.time() * 1000))
            print(len(current_state.moves(current_state.current_player, True)))
            print(len(current_state.moves((current_state.opponent()), True)))
            print("Mutari user: " + str(user_count) + ' ' + 'Mutari AI: ' + str(ai_count))
            print_time(game_start_time, game_end_time, 'Jocul a durat ')
            return
        print()
        if current_state.current_player == Game.JMIN:

            print("Este randul userului")

            user_turn_start = int(round(time.time() * 1000))

            mutat = False
            mutari_curente = []
            while not mutat:
                # daca imi continui tura
                if current_state.multi_move:

                    # gasesc mutarile posibile
                    mutari_curente, start_move, hasEliminationMove = show_moves(current_state, screen,
                                                                                current_state.move[0],
                                                                                current_state.move[1])
                    # daca nu pot continua mutarea( nu pot capura o piesa = hasEliminationMove)
                    if not hasEliminationMove:
                        # ma opresc,am mutat pe tura mea, urmeaza tura oponentului
                        current_state.multi_move = False
                        mutat = True
                        current_state.current_player = current_state.opponent()

                        break

                    # mai pot continua tura mea
                    else:
                        for move in mutari_curente:
                            # daca este mutare in care elimin atunci pot sa o execut
                            if move[2] == 1:
                                # desenez mutarea posibila
                                draw_possible_move(screen, move[0], move[1])
                            else:
                                pygame.draw.circle(screen, (0, 0, 0),
                                                   (move[1] * (50 + 1) + 25, move[0] * (50 + 1) + 25), 20)
                        # update UI
                        pygame.display.update()

                for event in pygame.event.get():
                    # daca ies din joc atunci afisez durata jocului
                    # scorul lui si scorul calculatorului
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        game_end_time = int(round(time.time() * 1000))
                        print_time(game_start_time, game_end_time, 'Jocul a durat')
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()

                        if len(current_state.moves(Game.JMIN)) > 0:

                            # numara mutarile facut de user
                            user_count += 1

                            for linie in range(8):
                                for col in range(8):

                                    if rectangles[linie][col].collidepoint(pos):

                                        # daca apas pe o piesa de a mea arata mutarile posibile
                                        if current_state.matrix[linie][col] in [current_state.current_player,
                                                                                current_state.current_player.upper()]:
                                            rectangles = deseneaza_grid(screen, current_state.matrix)
                                            mutari_curente, start_move, _ = show_moves(current_state, screen, linie,
                                                                                       col)
                                            pygame.display.update()
                                        # altfel daca apasa pe una din mutarile sugerate
                                        elif [linie, col, 1] in mutari_curente or [linie, col, 0] in mutari_curente:

                                            # verific daca am ajuns in baza, in caz afirmativ , fac piesa rege
                                            baseline = 0 if current_state.current_player == 'n' else 7

                                            piesa = current_state.matrix[start_move[0]][start_move[1]]
                                            if linie == baseline:
                                                piesa = piesa.upper()

                                            # muta piesa mea din locul curent
                                            current_state.matrix[start_move[0]][start_move[1]] = '.'

                                            # daca am o mutare in care capturez o piesa
                                            if [linie, col, 1] in mutari_curente:
                                                # determin directia mutarii
                                                dx, dy = (linie - start_move[0]) // 2, (col - start_move[1]) // 2
                                                # gasesc vecinul direct din directia mutarii
                                                vx, vy = start_move[0] + dx, start_move[1] + dy

                                                # elimin piesa oponentului
                                                current_state.matrix[vx][vy] = '.'

                                                # mut piesa mea peste piesa oponentului
                                                current_state.matrix[linie][col] = piesa

                                                # salvez pozitia unde mi-a ramas piesa pentru a continua de acolo
                                                # pentru ca am o mutare multipla
                                                current_state.move = [linie, col]

                                                # marchez ca este o mutare multipla
                                                # pentru a nu da tura oponentului si a-mi continua tura cu piesa
                                                # cu care am facut mutarea precedenta
                                                current_state.multi_move = True
                                                rectangles = deseneaza_grid(screen, current_state.matrix)


                                            # daca este o mutare simpla
                                            else:

                                                # deplasez piesa cu o patratica in diagonala aleasa
                                                current_state.matrix[linie][col] = piesa
                                                rectangles = deseneaza_grid(screen, current_state.matrix)

                                                # dau tura oponentului
                                                current_state.current_player = current_state.opponent()
                                                mutat = True
                                                # redeseaza tabla dupa mutare
                                                user_turn_end = int(round(time.time() * 1000))

                                                print_board(current_state.matrix)

                                                print("Mutarea userului a durat " + str(
                                                    user_turn_end - user_turn_start) + ' milisecunde')
                                                break

                                            # redeseaza tabla dupa mutare
                                            user_turn_end = int(round(time.time() * 1000))

                                            print_board(current_state.matrix)

                                            print("Mutarea userului a durat " + str(
                                                user_turn_end - user_turn_start) + ' milisecunde')


        # mutarea AI-ului
        else:
            print("Este randul ai-ului")
            ai_turn_start = int(round(time.time() * 1000))

            # daca mai are mutari AI-ul
            if len(current_state.moves(current_state.current_player)) > 0:

                # daca aleg algoritmul minimax
                if algo == 1:
                    stare_aleasa = minimax(current_state)
                    ai_turn_end = int(round(time.time() * 1000))
                    current_state.matrix = deepcopy(current_state.selected_state.matrix)
                    # redesenez tabla cu mutarea noua

                    rectangles = deseneaza_grid(screen, current_state.matrix)

                    # copiez mutarea facuta in cazul in care el poate face o mutare mutipla
                    current_state.move = copy(current_state.selected_state.move)
                    current_state.multi_move = current_state.selected_state.multi_move
                    print_board(current_state.matrix)
                    print("Mutarea ai-ului a durat " + str(ai_turn_end - ai_turn_start) + ' milisecunde')

                    # numara mutarile facut de ai
                    ai_count += 1

                    # daca mutarea curenta nu e multipla atunci dau tura userului
                    if not current_state.multi_move or len(current_state.moves(current_state.current_player)) == 0:
                        current_state.multi_move = False
                        current_state.current_player = current_state.opponent()

                # daca a ales alpha-beta
                else:

                    stare_aleasa = alpha_beta(-5000, 5000, current_state)
                    ai_turn_end = int(round(time.time() * 1000))
                    # salvez mutarea aleasa de AI
                    current_state.matrix = deepcopy(current_state.selected_state.matrix)

                    # redesenez tabla cu mutarea noua
                    rectangles = deseneaza_grid(screen, current_state.matrix)

                    # copiez mutarea facuta in cazul in care el poate face o mutare mutipla
                    current_state.move = copy(current_state.selected_state.move)
                    current_state.multi_move = current_state.selected_state.multi_move
                    print("MOVE", current_state.move)

                    print_board(current_state.matrix)
                    print("Mutarea ai-ului a durat " + str(ai_turn_end - ai_turn_start) + ' milisecunde')

                    # numara mutarile facut de ai
                    ai_count += 1

                    # daca mutarea curenta nu e multipla atunci dau tura userului
                    if not current_state.multi_move or len(current_state.moves(current_state.current_player)) == 0:
                        current_state.multi_move = False
                        current_state.current_player = current_state.opponent()


def print_time(start_time, end_time, message):
    print(message + ' ' + str((end_time - start_time) // 60000) + ' minute si ' + str(
        round(((end_time - start_time) % 60000) / 1000)) + " secunde")


if __name__ == "__main__":
    game_start_time = int(round(time.time() * 1000))
    play()

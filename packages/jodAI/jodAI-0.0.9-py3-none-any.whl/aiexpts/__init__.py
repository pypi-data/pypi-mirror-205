print("""
################# Expt 3 ############
 
# Using a Python dictionary to act as an adjacency list \
      graph={
          'A': ['B', 'C'],
          'B': ['D', 'E'],
          'C': ['F'],
          'D': [],
          'E': [],
          'F': []
      }
      def graph_display(graph):
      print("Graph \n\t")
      print(" A")
      print("/ \\")
      print("B  C")
      print("/\\ \\")
      print("D E F")
      visited=set()  # Set to keep track of visited nodes.

      def dfs(visited, graph, node):
      if node not in visited:
      print(node)
      visited.add(node)
      for neighbour in graph[node]:
      dfs(visited, graph, neighbour)

      # Driver Code
      graph_display(graph)
      print("\n\n")
      dfs(visited, graph, 'A')


## Expt 4 : ##################################################### 

from collections import deque
 
class Graph:
    def __init__(self, adjac_lis):
        self.adjac_lis = adjac_lis
 
    def get_neighbors(self, v):
        return self.adjac_lis[v]
 
    # This is heuristic function which is having equal values for all nodes
    def h(self, n):
        H = {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1
        }
 
        return H[n]
 
    def a_star_algorithm(self, start, stop):
        # In this open_lst is a lisy of nodes which have been visited, but who's 
        # neighbours haven't all been always inspected, It starts off with the start 
  #node
        # And closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always inspected
        open_lst = set([start])
        closed_lst = set([])
 
        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo = {}
        poo[start] = 0
 
        # par contains an adjac mapping of all nodes
        par = {}
        par[start] = start
 
        while len(open_lst) > 0:
            n = None
 
            # it will find a node with the lowest value of f() -
            for v in open_lst:
                if n == None or poo[v] + self.h(v) < poo[n] + self.h(n):
                    n = v;
 
            if n == None:
                print('Path does not exist!')
                return None
 
            # if the current node is the stop
            # then we start again from start
            if n == stop:
                reconst_path = []
 
                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]
 
                reconst_path.append(start)
 
                reconst_path.reverse()
 
                print('Path found: {}'.format(reconst_path))
                return reconst_path
 
            # for all the neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
              # if the current node is not presentin both open_lst and closed_lst
                # add it to open_lst and note n as it's par
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    par[m] = n
                    poo[m] = poo[n] + weight
 
                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update par data and poo data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if poo[m] > poo[n] + weight:
                        poo[m] = poo[n] + weight
                        par[m] = n
 
                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)
 
            # remove n from the open_lst, and add it to closed_lst
            # because all of his neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)
 
        print('Path does not exist!')
        return None

adjac_lis = {
    'A': [('B', 1), ('C', 3), ('D', 7)],
    'B': [('D', 5)],
    'C': [('D', 12)]
}
graph1 = Graph(adjac_lis)
graph1.a_star_algorithm('A', 'D')




############################## EXPT 5 Tick tacktoe #################

import random


class TicTacToe:

    def __init__(self):
        self.board = []

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append('-')
            self.board.append(row)

    def get_random_first_player(self):
        return random.randint(0, 1)

    def fix_spot(self, row, col, player):
        self.board[row][col] = player

    def is_player_win(self, player):
        win = None

        n = len(self.board)

        # checking rows
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        # checking columns
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

        # checking diagonals
        win = True
        for i in range(n):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        win = True
        for i in range(n):
            if self.board[i][n - 1 - i] != player:
                win = False
                break
        if win:
            return win
        return False

        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def is_board_filled(self):
        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def swap_player_turn(self, player):
        return 'X' if player == 'O' else 'O'

    def show_board(self):
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

    def start(self):
        self.create_board()

        player = 'X' if self.get_random_first_player() == 1 else 'O'
        while True:
            print(f"Player {player} turn")

            self.show_board()

            # taking user input
            row, col = list(
                map(int, input("Enter row and column numbers to fix spot: ").split()))
            print()

            # fixing the spot
            self.fix_spot(row - 1, col - 1, player)

            # checking whether current player is won or not
            if self.is_player_win(player):
                print(f"Player {player} wins the game!")
                break

            # checking whether the game is draw or not
            if self.is_board_filled():
                print("Match Draw!")
                break

            # swapping the turn
            player = self.swap_player_turn(player)

        # showing the final view of board
        print()
        self.show_board()


# starting the game
tic_tac_toe = TicTacToe()
tic_tac_toe.start()



############################# EXPT 6 First order logic #################


import time

def input_file():
    f = open('/content/input.txt')
    noq = int(f.readline().strip())
    q = []
    for i in range(noq):
        q.append(f.readline().strip())
    nKB = int(f.readline().strip())
    KB = []
    for i in range(nKB):
        KB.append(f.readline().strip())
    return noq, q, nKB, KB


def addInKB(KB, query):
    if query in KB:
        return False
    return True


def resolvable(query, query1):
    part = query.split(' | ')
    part1 = query1.split(' | ')
    cntUnifiable = 0
    cntUnified = 0
    flag = 0
    for pt in range(len(part)):
        for pt1 in range(len(part1)):
            pred = part[pt][ : part[pt].index('(')].strip()
            pred1 = part1[pt1][ : part1[pt1].index('(')].strip()
            param = query.split(' | ')[pt][query.split(' | ')[pt].index('(') + 1 : query.split(' | ')[pt].index(')')].split(',')
            param1 = query1.split(' | ')[pt1][query1.split(' | ')[pt1].index('(') + 1 : query1.split(' | ')[pt1].index(')')].split(',')
            if pred.startswith('~') and not pred1.startswith('~') and pred[1:] == pred1:
                flag = 1
            elif not pred.startswith('~') and pred1.startswith('~') and pred == pred1[1:]:
                flag = 1

            if flag == 1:
                flag = 0
                cntUnifiable += 1
                stringg = []
                err = 0
                count = 0
                for p in range(len(param)):
                    if param[p][0].isupper() and param1[p][0].isupper() and param[p] == param1[p]:
                        count += 1
                    elif param[p][0].isupper() and param1[p][0].isupper() and param[p] != param1[p]:  # Both Const
                        err = 1
                        return False
                    elif param[p][0].isupper() and param1[p][0].islower():  # replace in 1
                        count += 1
                        query1 = query1.replace(("(" + param1[p]), ("(" + param[p]))
                        query1 = query1.replace((param1[p] + ")"), (param[p] + ")"))
                        query1 = query1.replace(("," + param1[p] + ","), ("," + param[p] + ","))
                        if p == len(param) - 1 and err == 0:
                            stringg.append(query1)
                    elif param[p][0].islower() and param1[p][0].isupper():  # replace in 0
                        count += 1
                        query = query.replace(("(" + param[p]), ("(" + param1[p]))
                        query = query.replace((param[p] + ")"), (param1[p] + ")"))
                        query = query.replace(("," + param[p] + ","), ("," + param1[p] + ","))
                        param[p] = param1[p]
                        if p == len(param) - 1 and err == 0:
                            stringg.append(query)
                    elif param[p][0].islower() and param1[p][0].islower():  # Both variable 0 -> 1
                        count += 1
                        query1 = query1.replace(("(" + param1[p]), ("(" + param[p]))
                        query1 = query1.replace((param1[p] + ")"), (param[p] + ")"))
                        query1 = query1.replace(("," + param1[p] + ","), ("," + param[p] + ","))
                        param[p] = param1[p]
                        if p == len(param) - 1 and err == 0:
                            stringg.append(query)
                if count == len(param):
                    cntUnified += 1
                    count = 0
    if cntUnifiable == cntUnified and cntUnified > 0:
        cntUnified = 0
        cntUnifiable = 0
        return True
    else:
        return False

    return False


def unify(query, query1, KBase):
    part = query.split(' | ')
    part1 = query1.split(' | ')
    for t in part:
        pred = t[:t.index('(')].strip()
        param = t[t.index('(')+1:t.index(')')].split(',')
        flag = 0
        for t1 in part1:
            # print "T1:" + t1
            pred1 = t1[:t1.index('(')].strip()
            param1 = t1[t1.index('(')+1:t1.index(')')].split(',')
            if pred.startswith('~') and not pred1.startswith('~') and pred[1:] == pred1:
                flag = 1
            elif not pred.startswith('~') and pred1.startswith('~') and pred == pred1[1:]:
                flag = 1

            if flag == 1:  # For Same Predicate unify
                stringg = []
                err = 0
                qr = query[:]
                qr1 = query1[:]
                count = 0
                for p in range(len(param)):
                    if param[p][0].isupper() and param1[p][0].isupper() and param[p] == param1[p]:
                        count += 1
                        if p == len(param)-1 and err == 0:
                            u = qr.split(' | ')
                            uf = []
                            for pi in u:
                                if pi != (pred + '('+(',').join(param)+')'):
                                    uf.append(pi)
                            u1 = qr1.split(' | ')
                            uf1 = []
                            for pi1 in u1:
                                if pi1 != (pred1 + '('+(',').join(param1)+')'):
                                    uf1.append(pi1)
                            unified = " | ".join(set(uf + uf1))
                            stringg.append(unified)
                    elif param[p][0].isupper() and param1[p][0].isupper() and param[p] != param1[p]:  # Both Const
                        err = 1
                    elif param[p][0].isupper() and param1[p][0].islower() and err == 0:  # replace in 1
                        count += 1
                        qr1 = qr1.replace(("("+param1[p]),("("+param[p]))
                        qr1 = qr1.replace((param1[p] + ")"), (param[p] + ")"))
                        qr1 = qr1.replace((","+param1[p] + ","), (","+param[p] + ","))

                        if p == len(param)-1 and err == 0:
                            param1 = param
                            u = qr.split(' | ')
                            uf = []
                            for pi in u:
                                if pi != (pred + '('+(',').join(param)+')'):
                                    uf.append(pi)
                            # print uf
                            u1 = qr1.split(' | ')
                            uf1 = []
                            for pi1 in u1:
                                if pi1 != (pred1 + '('+(',').join(param1)+')'):
                                    uf1.append(pi1)
                            unified = " | ".join(set(uf + uf1))
                            stringg.append(unified)
                    elif param[p][0].islower() and param1[p][0].isupper() and err == 0:  # replace in 0
                        count += 1
                        qr = qr.replace(("(" + param[p]), ("(" + param1[p]))
                        qr = qr.replace((param[p] + ")"), (param1[p] + ")"))
                        qr = qr.replace(("," + param[p] + ","), ("," + param1[p] + ","))
                        if p == len(param)-1 and err == 0:
                            param = param1
                            u = qr.split(' | ')
                            uf = []
                            for pi in u:
                                if pi != (pred + '('+(',').join(param)+')'):
                                    uf.append(pi)
                            # print uf
                            u1 = qr1.split(' | ')
                            uf1 = []
                            for pi1 in u1:
                                if pi1 != (pred1 + '('+(',').join(param1)+')'):
                                    uf1.append(pi1)
                                # print uf1
                            unified = " | ".join(set(uf + uf1))
                            stringg.append(unified)
                    elif param[p][0].islower() and param1[p][0].islower() and err == 0:  # Both variable 0 -> 1
                        count += 1
                        qr1 = qr1.replace(("(" + param1[p]), ("(" + param[p]))
                        qr1 = qr1.replace((param1[p] + ")"), (param[p] + ")"))
                        qr1 = qr1.replace(("," + param1[p] + ","), ("," + param[p] + ","))
                        if p == len(param) - 1 and err == 0:
                            param1 = param
                            u = qr.split(' | ')
                            uf = []
                            for pi in u:
                                if pi != (pred + '('+(',').join(param)+')'):
                                    uf.append(pi)
                            # print uf
                            u1 = qr1.split(' | ')
                            uf1 = []
                            for pi1 in u1:
                                if pi1 != (pred1 + '('+(',').join(param1)+')'):
                                    uf1.append(pi1)
                                # print uf1
                            unified = " | ".join(set(uf + uf1))
                            stringg.append(unified)

                if count == len(param):
                    count = 0
                    return unified
            flag = 0


def resolution(q1, KBase, t):
    if q1 == None or q1 == "":
        return True
    # if not str in KBase :
    if addInKB(KBase, q1):
        KBase.append(q1)
    else:
        return False
    ll = []
    for idx in range(len(KBase)):
        if resolvable(q1, b[idx]):
            ll.append(KBase[idx])
    for idx in range(len(ll)):
        if ((time.time() - t) > 200):
            return False
        ans = unify(q1, ll[idx], KBase)
        if resolution(ans, KBase, t):
            return True
    return False

def standardize(KB):
    for i in range(len(KB)):
        temp = KB[i].split(' | ')
        param = []
        for t in temp:
            param.extend(t[t.index('(') + 1:t.index(')')].split(','))
        param = list(set(param))
        for p in range(len(param)):
            if param[p][0].islower():
                KB[i] = KB[i].replace(("(" + param[p]), ("(" + param[p] + str(i)))
                KB[i] = KB[i].replace((param[p] + ")"), (param[p]+ str(i) + ")"))
                KB[i] = KB[i].replace(("," + param[p] + ","), ("," + param[p]+ str(i) + ","))


def write(ans):
    file = open("output.txt", "w")
    for a in ans:
        file.write(str(a).upper()+"\n")
    file.close()


def main():
    nq, q, nKB, KB = input_file()
    standardize(KB)
    ans = []
    for i in range(len(q)):
        if q[i].startswith('~'):
            q[i] = q[i][1:]
        else:
            q[i] = '~' + q[i]
        try:
            a = resolution(q[i], KB[:], time.time())
        except:
            a = "FALSE"
        ans.append(a)
    write(ans)
    # print KB

main()

######################## EXPT 7 Planning Programming #################


tab = []
result = []
goalList = ["a", "b", "c", "d", "e"]


def parSolution(N):
    for i in range(N):
        if goalList[i] != result[i]:
            return False
    return True


def Onblock(index, count):

    # break point of recursive call
    if count == len(goalList)+1:
        return True
    # copy tab of index value to result
    block = tab[index]
    # stack block
    result.append(block)
    print(result)
    if parSolution(count):
        print("Pushed a result solution ")
        # remove block from tab
        tab.remove(block)
        Onblock(0, count + 1)
    else:
        print("result solution not possible, back to the tab")
        # pop out if no partial solution
        result.pop()
        Onblock(index+1, count)


def Ontab(problem):
    # check if everything in stack is on the tab
    if len(problem) != 0:
        tab.append(problem.pop())
        Ontab(problem)
    # if everything is on the tab the we return true
    else:
        return True


def goal_stack_planing(problem):
    # pop problem and put in tab
    Ontab(problem)
    # print index and number of blocks on result stack
    if Onblock(0, 1):
        print(result)


if __name__ == "__main__":
    problem = ["c", "a", "e", "d", "b"]
    print("Goal Problem")
    for k, j in zip(goalList, problem):
        print(k+"    "+j)
    goal_stack_planing(problem)
    print("result Solution")
    print(result)

    
################################ EXPT 8 ###########



!pip install pgmpy

from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination


alarm_model = BayesianModel([('Burglary', 'Alarm'),
                              ('Earthquake', 'Alarm'),
                              ('Alarm', 'JohnCalls'),
                              ('Alarm', 'MaryCalls')])

from pgmpy.factors.discrete import TabularCPD

cpd_burglary = TabularCPD(variable='Burglary', variable_card=2,
                      values=[[.999], [0.001]])
cpd_earthquake = TabularCPD(variable='Earthquake', variable_card=2,
                       values=[[0.998], [0.002]])
cpd_alarm = TabularCPD(variable='Alarm', variable_card=2,
                        values=[[0.999, 0.71, 0.06, 0.05],
                                [0.001, 0.29, 0.94, 0.95]],
                        evidence=['Burglary', 'Earthquake'],
                        evidence_card=[2, 2])
cpd_johncalls = TabularCPD(variable='JohnCalls', variable_card=2,
                      values=[[0.95, 0.1], [0.05, 0.9]],
                      evidence=['Alarm'], evidence_card=[2])
cpd_marycalls = TabularCPD(variable='MaryCalls', variable_card=2,
                      values=[[0.1, 0.7], [0.9, 0.3]],
                      evidence=['Alarm'], evidence_card=[2])

alarm_model.add_cpds(cpd_burglary, cpd_earthquake, cpd_alarm, cpd_johncalls, cpd_marycalls)


alarm_model.check_model()


alarm_model.nodes()


alarm_model.edges()


alarm_model.local_independencies('Burglary')







""")

# -*- coding: utf-8 -*-
#
#    Towers of Hanoi with use of stacks and graph searching
#    Copyright (C) 2016 August 
#    1200 Web Development
#    http://1200wd.com/
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import copy
import sys
from stack import Stack

TOWERS = 'ABC'
TOWERSIZE = 4

# For more then 7 discs you probably need to increase the recursionlimit
#sys.setrecursionlimit(10000)

def initgame():
    return {'A': Stack(list(reversed(range(1,TOWERSIZE+1)))), 'B': Stack(), 'C': Stack()}

def getgoal():
    return {'A': Stack(), 'B': Stack(), 'C': Stack(list(reversed(range(1,TOWERSIZE+1))))}

def show(gamedomain):
    for tower in sorted(gamedomain):
        print('%s%s' % (tower, gamedomain[tower]))

# Get all possilbe moves fom a given startdomain. Return a list of tupples with format
# (move, newdomain, score), i.e. ('ab', {stack1, stack2, stack3}, 3)
def possiblemoves(startdomain):
    moves = []
    domain = startdomain[1]
    for tower, discs in domain.items():
        if len(discs):
            for tn in TOWERS:
                if not domain[tn].top() or domain[tower].top() < domain[tn].top():
                    newdomain =  movedisc(domain, (tower, tn))
                    moves.append((tower+tn, newdomain, score(newdomain)))
    moves = sorted(moves, key=lambda x: x[2], reverse=True)
    return moves

# Count the number of moves of the biggest disc. One or two moves should be enough to
# solve the puzzle, so it tells something about the quality of the solution path.
def bigdiscmoves(path):
    if not path: return 0
    bigdiscrow = None
    countmoves = 0
    for domain in [x[1] for x in path]:
        for tower in domain:
            if TOWERSIZE in domain[tower]:
                bitdiscrownew = tower
        if bigdiscrow != bitdiscrownew:
            bigdiscrow = bitdiscrownew
            countmoves += 1
    return countmoves

# Simple mechanism to get the score of the current domain, this increases speed dramatically.
def score(domain):
    st = TOWERSIZE
    score = 0
    while st:
        if st in domain['C']:
            score += st
            st -= 1
        else:
            break
    return score

# Generate possible solution paths, explore paths with the highest score first.
# Stop searching and return path when a solution is found.
def generate(startdomain, goaldomain, path=[]):
    path = path + [startdomain]
    if startdomain[1] == goaldomain[1]:
        return path
    newmoves = possiblemoves(startdomain)
    for move in newmoves:
        if move[1] not in [x[1] for x in path]:
            newpath = generate(move, goaldomain, path)
            if newpath: return newpath
    return None

# Move disc from one stack to another using pop() and push()
def movedisc(gamedomain, move):
    if gamedomain[move[0]].top() > gamedomain[move[1]].top() and gamedomain[move[1]].top():
        print("Smaller discs (numbers) on top only!")
    elif not gamedomain[move[0]].top():
        print("No discs on tower %s" % TOWERS[move[0]])
    else:
        gd = copy.deepcopy(gamedomain)
        gd[move[1]].push(gd[move[0]].pop())
        return gd
    return gamedomain

if __name__ == '__main__':
    gamedomain = initgame()
    goaldomain = getgoal()
    moves = 0

    print("Welcome to Towers of Hanoi Nerd Edition. Goal is to move all discs from tower A to C, without putting bigger discs on smaller discs.\n"
          "Type for example 'ab' to move disc from tower A to B.\n"
          "Or [l]azy, [r]estart, [q]uit.\n")
    instruction = ''
    while instruction not in ['Q', 'QUIT'] and not gamedomain == goaldomain:
        show(gamedomain)
        instruction = input("(%d) Instruction? " % moves).upper()
        if instruction in ['R', 'RESTART']:
            print("Game restarted")
            gamedomain = initgame()
            moves = 0
            continue
        if instruction in ['L', 'LAZY']:
            print("Trying to solve puzzle with 'Artificial Intelligence'...")
            path = generate(('Start', gamedomain), ('Goal', goaldomain))
            print("Path found: %s" % [x[0] for x in path])
            print("Number of moves %d and number of biggest disc moves %d" % (len(path), bigdiscmoves(path)))
            continue
        if instruction in ['Q', 'QUIT']:
            continue

        try:
            if not(instruction[0] in TOWERS and instruction[1] in TOWERS):
                print("What are you talking about? Type for example 'AB' to move disc from tower A to B. "
                      "Or [l]azy, [r]estart, [q]uit.\n")
                continue
        except IndexError:
            print("IndexError!")
            continue

        gamedomain = movedisc(gamedomain, (instruction[0], instruction[1]))
        moves += 1

        if gamedomain == goaldomain:
            if input("CONGRATULATIONS!!! You solved the Towers of Hanoi puzzle with %d discs in %d turns\n"
                  "Try again (y/n)?" % (TOWERSIZE, moves)).upper() == 'Y':
                moves = 0
                gamedomain = initgame()

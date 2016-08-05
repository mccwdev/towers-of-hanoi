# -*- coding: utf-8 -*-
#
#    Stack Class for Towers of Hanoi puzzle
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

class Stack:
    def __init__(self, start=[]):
        self.stack = []
        for i in start: self.push(i)

    def push(self, node):
        self.stack.append(node)

    def pop(self):
        if not self.stack: return False
        return self.stack.pop()

    def top(self):
        if not self.stack: return False
        return self.stack[-1]

    def __repr__(self):
        res = "|"
        for i in self.stack:
            res += str(i) + '-'
        return res

    def __len__(self):
        return len(self.stack)

    def __getitem__(self, offset):
        return self.stack[offset]

    def __eq__(self, other):
        return self.stack == other.stack

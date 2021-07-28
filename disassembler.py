#!/usr/bin/env python3

import sys
from PIL import Image
import numpy as np

class Stack(list):
    def push(self, x):
        self.append(x)

    def peek(self):
        return self[-1]

stack = Stack([])
program = []
register = 0
insn_pointer = 0

DEBUG = False

def robinify(im):
    tiles = [im[x:x+128,y:y+128,0:4] for x in range(0,im.shape[0],128) for y in range(0,im.shape[1],128)]
    R = np.asarray(Image.open("robin.roo"))
    O = np.asarray(Image.open("oreos.roo"))
    B = np.asarray(Image.open("blind.roo"))
    I = np.asarray(Image.open("imag.roo"))
    N = np.asarray(Image.open("nobooli.roo"))
    d = list(zip([R,O,B,I,N], "robin"))

    ret = ''
    for c in tiles:
        for pair in d:
            if np.all(pair[0]==c):
                ret += pair[1]
                break
    return ret

def step():
    global insn_pointer
    insn = c_insn()
    if DEBUG:
        print(insn, program[insn_pointer+1], "@", insn_pointer)
    eval(insn+"()")

def run(prog):
    global insn_pointer, program
    for ch in prog:
        if ch not in "robin":
            print("Syntax Error")
            exit(1)

    if len(prog) % 5 != 0:
        print("Syntax Error")

    program = [prog[i:i+5] for i in range(0, len(prog), 5)]
    try:
        while insn_pointer < len(program):
            step()
            insn_pointer += 1
            if DEBUG:
                print(stack)
    except Exception as e:
        print("Fatal Error.")
        raise e
    print()
    print(stack)

def c_insn():
    return program[insn_pointer]

def robin():            # ldi
    global insn_pointer
    insn_pointer += 1
    toPush = c_insn()
    if toPush == "rinin":
        print('push acc')
        #stack.push(register)
    else:
        words = parseDigit(toPush)
        toPush = 0
        for i in range(words):
            insn_pointer += 1
            toPush += parseDigit(c_insn())
            toPush *= 27
        #stack.push(toPush//27)
        print('push ' + str(toPush//27))

def parseDigit(s):
    return int(s.replace('o', '0').replace('b', '1').replace('i', '2')[1:-1], 3)

def rboin():            # pop from stack
    #stack.pop()
    print('pop')

def riobn():            # add two numbers
    #stack.push(stack.pop()+stack.pop())
    print('add')

def rooon():            # sub two numbers
    #stack.push(stack.pop()-stack.pop())
    print('sub')

def riibn():            # mul two numbers
    #stack.push(stack.pop()*stack.pop())
    print('mul')

def riion():            # div two numbers
    #stack.push(stack.pop()//stack.pop())
    print('div')

def ribon():            # mod two numbers
    #stack.push(stack.pop()%stack.pop())
    print('mod')

def ronon():            # and two numbers
    #stack.push(stack.pop()&stack.pop())
    print('and')

def roion():            # or two numbers
    #stack.push(stack.pop()|stack.pop())
    print('or')

def roibn():            # xor two numbers
    #stack.push(stack.pop()^stack.pop())
    print('xor')

def riiin():            # duplicate stack's top
    #x = stack.pop()
    #stack.push(x)
    #stack.push(x)
    print('dup')

def rioin():            # swap two upper elements
    #x = stack.pop()
    #y = stack.pop()
    #stack.push(x)
    #stack.push(y)
    print('swp')

def rinin():            # pop to register
    global register
    #register = stack.pop()
    print('pop acc')

def rbiin():            # print as char
    #print(chr(stack.pop()), end='', flush=True)
    print('pop out chr')

def rboon():            # print as number
    #print(stack.pop(), end='', flush=True)
    print('pop out')

def rnbon():            # label
    global insn_pointer
    insn_pointer += 1
    print(str(c_insn()) + ':')

def rioon():            # jump to label
    global insn_pointer
    insn_pointer += 1
    print('jmp ' + str(c_insn()))

    for i, word in enumerate(program):
        if word == "rnbon":
            if i != len(program)-1 and program[i+1] == c_insn():
                #insn_pointer = i+1
                return
    print("Label not found!")
    raise RuntimeError

def rbion():            # jump if top of stack to label
    global insn_pointer
    print('c', end='')
    #if stack.peek():
    rioon()
    #else:
    #    insn_pointer += 1

def ribbn():            # return ( w/ return value )
    global insn_pointer
    #retval = stack.pop()
    #insn_pointer = stack.pop()
    #if DEBUG:
    #    print("returning to", insn_pointer)
    #stack.push(retval)
    print('ret')

def roiin():            # call ( w/ single argument )
    global insn_pointer
    #arg = stack.pop()
    #stack.push(insn_pointer+1)
    #stack.push(arg)
    print('call', end='')
    rioon()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./roolang.py [filename.roo]")
        exit()

    if sys.argv[1].split('.')[-1] != "roo":
        print("Invalid file format!")
        exit()

    with Image.open(sys.argv[1]) as f:
        print("Parsing...")
        program = robinify(np.asarray(f))
        print("Running...")
        run(program)
        print("Finished execution.")

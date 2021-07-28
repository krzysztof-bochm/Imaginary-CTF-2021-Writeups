# ImaginaryCTF 2021: Roolang

![date](https://img.shields.io/badge/date-28.07.2021-brightgreen.svg)  ![solved in time of CTF](https://img.shields.io/badge/solved-in%20time%20of%20CTF-brightgreen.svg) 
![reversing category](https://img.shields.io/badge/category-reversing-lightgrey.svg) ![score](https://img.shields.io/badge/score-400-blue.svg) 

## Description

ELF files are sooooo last year :rooVoid:. Instead of making yet another ELF to reverse, I made a new type of executable binary for you to reverse :rooYay:! It uses my new language Roolang. Just execute flag.roo to get the flag :rooPuzzlerDevil:! It's dynamically linked, so make sure you have the provided roo library files in the same directory :rooCash:. It's not very optimized, so it might take a moment (sorry about that) :rooNobooli:...

Special shoutout to :rooRobin: and :rooOreos:, who have nothing to do with this challenge, but are both very cool people :rooHeart:. Good luck, and I hope you have fun :rooNervous:!

## Attached files

- [roolang.zip](https://imaginaryctf.org/r/82D9-roolang.zip)
- [disassembler.py](https://github.com/krzysztof-bochm/Imaginary-CTF-2021-Writeups/blob/main/disassembler.py)
- [disassembly.asm](https://github.com/krzysztof-bochm/Imaginary-CTF-2021-Writeups/blob/main/disassembly.asm)
- [program.c](https://github.com/krzysztof-bochm/Imaginary-CTF-2021-Writeups/blob/main/program.c)

## Summary

The flag is getting printed onto stdout but **very** slowly. We just need to de-obfuscate and RE the program and optimize it to get the flag.

## Flag
``` ictf{thr33_ch33r5_t0_r00r0bin_th3_b3st_0f_u5_a11_r00h3art_7d2e2642} ```

## Detailed solution

After unzipping challenge's archive we can see 7 files:

- roolang.py
- flag.roo
- blind.roo, imag.roo, nobooli.roo, oreos.roo, robin.roo

```.roo``` files are just PNG images. All of them except for ```flag.roo``` contain single ```128x128 px``` emote, while ``` flag.roo``` is ```67x55``` array of these emotes.

For each of ```flag.roo```'s emotes the first letter of their filename is taken and written to program's string
```
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
 ```

The string is divided into 5 character sections, which are opcodes for a CPU emulated by the program.
```
def step():
    global insn_pointer
    insn = c_insn()
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
    except Exception as e:
        print("Fatal Error.")
        raise e
```

each opcode is contained in separate function. I will list them bellow ( not all of them are used in the program ), I am not expecting you to read all of them
```
robin - loads immediate value onto the stack
rboin - pops value from stack, discarding it
riobn - adds two numbers on top of the stack, pushes result onto the stack
rooon - substracts two numbers on top of the stack, pushes result onto the stack
riibn - multiplies
riion - divides
ribon - modulo operation
ronon - bitwise and
roion - bitwise or
roibn - bitwise xor
riiin - duplicates stack's top
rioin - swaps two top most elements
rinin - pops top of the stack to register
rbiin - prints top of the stack as ascii character
rboon - prints top of the stack as number
rnbon - tells the CPU that the next word is a label
rioon - jumps to the label specified in the next word
rbion - jumps to the label if top of the stack is not zero
ribbn - returns from subroutine
roiin - calls subroutine
```
Knowing what each opcode does we could now rewrite the program in C ( because I am more comfortable with it than with python ) and try making sense of it. However all opcode names are a bit confusing, to make it easier we will modify CPU's code to write human readable disassembly of our program.

We can achieve it by removing any flow control and stack manipulations from instructions, and making all instructions print what they are doing, for example
```
def robin():            # loads immediate value ento the stack
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
```
other opcode disassemblies will be present in attached file.

The program now will give following output
```
rooon:
push 0
push 14472334024676096
push 8944394323791450
...
push 105
push 85

roobn:
push 0
pop acc

rooin:
cjmp robon
jmp robbn

robon:
push acc
calljmp robin
xor
pop out chr
push acc
push 1
add
pop acc
jmp rooin
jmp robbn
...
```

full disassembly is present in attached file.

Now it will be much easier to transform it into C code:
```
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int64_t* stack_ptr;

void push(int64_t a) {
	*stack_ptr++ = a;
}
...
void lab5() {
	if(stack_ptr[-1]) goto lab6;

	pop();
	push(1);
	return;
...
	add();
	swp();
	pop();
}

int main() {
	stack_ptr = calloc(100000, sizeof(int64_t));
	int64_t acc;
	
lab1:
	push(0);
	push(14472334024676096);
	push(8944394323791450);
	...
	push(103);
	push(105);
	push(85);

lab2:
	push(0);
	acc = pop();

lab3:
	if(stack_ptr[-1]) goto lab4;
	else goto exit;

lab4:
	push(acc);
	lab5();
	xor();
	putchar(pop());
	fflush(stdout);
	push(acc);
	push(1);
	add();
	acc = pop();
	goto lab3;

exit:
}
```
full C code will be present in attached file.

When we compile and run this program it will start printing our flag. It is much faster than just running it in attached CPU emulator, but still it chokes after couple of characters.

To better understand what this code does lets focus now on ```lab5``` subroutine. To call it with arguments from 0 to 10 we will use following code
```
for(int64_t i = 0; i < 10; i++) {
	push(i);
	lab5();
	printf("%lld -> %lld\n", i, pop());
}
```
Lets check what we get
```
0 -> 1   1 -> 1    2 -> 2
3 -> 3   4 -> 5    5 -> 8
6 -> 13  7 -> 21   8 -> 34
9 -> 55
```
```lab5``` function just returns terms of Fibonacci sequence, however it uses slow recursive approach in order to do so. We can simply optimize it
```
void lab5() {
	int64_t var = pop();

	int64_t a = 1;
	int64_t b = 1;
	int64_t c;

	while(var--) {
		c = a + b;
		a = b;
		b = c;
	}

	push(a);
	return;
}
```

When we run the program with optimized ```lab5``` function we get our flag immediately.
:rooYay:!

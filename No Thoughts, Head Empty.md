# ImaginaryCTF 2021: No Thoughts, Head Empty

![date](https://img.shields.io/badge/date-31.07.2021-brightgreen.svg)  ![solved in time of CTF](https://img.shields.io/badge/solved-in%20time%20of%20CTF-brightgreen.svg) 
![reversing category](https://img.shields.io/badge/category-reversing-lightgrey.svg) ![score](https://img.shields.io/badge/score-200-blue.svg)  ![solves](https://img.shields.io/badge/solves-101-brightgreen.svg) 

## Description

When I was making Roolang, of course I took a look at the mother of all esolangs! So, have some bf code. Run it here ([https://copy.sh/brainfuck/](https://copy.sh/brainfuck/)) with 32 bit cells and dynamic memory enabled. Run the program to get the flag, and then some.

## Attached files

- [flag_min.bf](https://imaginaryctf.org/r/8A7A-flag_min.bf)

## Summary

The flag is printed to stdout but each each character is printed twice as many times as previous one we need to either disable exponential growth of the number of printed characters or get the flag by other means.

## Flag
``` ictf{0n3_ch@r@ct3r_0f_d1f3r3nce} ```

## Detailed solution

When we paste our source to attached site and run the code we can see the flag being printed out:
```
iccttttffffffff{{{{{{{{{{{{{{{{00000000000000000000000000000000nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn3...
```

Fortunately when we dump the memory of the program using ```#``` ( remember to enable it in options ) just before print instruction (```.```) we can see that entire flag is already present in there
```
**dump 0 iteration 0 
line 17 char 20

** pointer = 0001 

00000: 0000000000 0000000105 0000000099 0000000116 .ict 
00004: 0000000102 0000000123 0000000048 0000000110 f{0n 
00008: 0000000051 0000000095 0000000099 0000000104 3_ch 
00012: 0000000064 0000000114 0000000064 0000000099 @r@c 
00016: 0000000116 0000000051 0000000114 0000000095 t3r_ 
00020: 0000000048 0000000102 0000000095 0000000100 0f_d 
00024: 0000000049 0000000102 0000000051 0000000114 1f3r 
00028: 0000000051 0000000110 0000000099 0000000101 3nce 
00032: 0000000125 0000000000 0000000032 0000000002 }... 
00036: 0000000001 0000000000 ..
```

We can just copy it to the flag input field. Note that when you set cell size to 8 bits, chunks of the flag would be bigger therefor faster to copy:
```
**dump 0 iteration 0 
line 17 char 20

** pointer = 0001 

00000: 000 105 099 116 102 123 048 110 051 095 099 104 .ictf{0n3_ch 
00012: 064 114 064 099 116 051 114 095 048 102 095 100 @r@ct3r_0f_d 
00024: 049 102 051 114 051 110 099 101 125 000 032 002 1f3r3nce}... 
00036: 001 000
```

## Another solution
We need to find part of code that multiplies the number of characters and delete it. This solution is probably the intended one, but due to the existence of above solution, it is unnecessarily *complicated*. And unless I knew that the flag was already in memory I would not extract printing loop from the code.

We can extract the final loop from the code
```
[>[->+>++<<]>>[-<<+>>]<[[<]<[<]>#.[>]>[>]<-][<]<[<]<[<]>[-]>[>]>-]
```
I have just checked when ```[``` corresponding to the last ```]``` of the file is, and copied entire loop.

The first sub-loop from our extracted code seams like it is doubling some cell in the memory, when we remove one of the ```+``` characters. When we run our code now the flag gets printed.
```
[>[->+>+<<]>>[-<<+>>]<[[<]<[<]>#.[>]>[>]<-][<]<[<]<[<]>[-]>[>]>-]
```   

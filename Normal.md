# ImaginaryCTF 2021: Normal

![date](https://img.shields.io/badge/date-31.07.2021-brightgreen.svg)  ![solved in time of CTF](https://img.shields.io/badge/solved-in%20time%20of%20CTF-brightgreen.svg) 
![reversing category](https://img.shields.io/badge/category-reversing-lightgrey.svg) ![score](https://img.shields.io/badge/score-150-blue.svg)  ![solves](https://img.shields.io/badge/solves-109-brightgreen.svg) 

## Description

Norse senor snorts spores, abhors non-nors, adores s'mores, and snores.

## Attached files

- [normal.v](https://imaginaryctf.org/r/70E7-normal.v)
- [Makefile](https://imaginaryctf.org/r/B484-Makefile)

## Summary

Circuit checks the flag using XOR like method. If all xored wires are low, then displays that the flag is correct.

## Flag
``` ictf{A11_ha!1_th3_n3w_n0rm_n0r!} ```

## Detailed solution

[![asciicast](https://asciinema.org/a/god5oTJWE6u7RO4ymax1e4sGI.svg)](https://asciinema.org/a/god5oTJWE6u7RO4ymax1e4sGI)

We can see that that the wire ( therefor bit ) at position N is only affected by flag's wire at the same position. Also if we change any wire of the flag, corresponding wire from wrong always changes. Therefor flagchecker acts like bitwise xor operation.

Note that:
```
Flag   	Password   	XOR
X	X		0
0	X		X
``` 
We can just zero the flag out to acquire the password.

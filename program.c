#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int64_t* stack_ptr;

void push(int64_t a) {
	*stack_ptr++ = a;
}

 int64_t pop() {
	return *--stack_ptr;
}

 void xor() {
	push(pop() ^ pop());
}

 void add() {
	push(pop() + pop());
}

 void dup() {
	int64_t a = pop();
	push(a); push(a);
}

 void sub() {
	push(pop() - pop());
}

 void swp() {
	int64_t x = pop();
	int64_t y = pop();
	push(x);
	push(y);
}


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

// ================================================

lab5:
	if(stack_ptr[-1]) goto lab6;

	pop();
	push(1);
	return;

lab6:
	dup();
	push(1);
	sub();
	if(stack_ptr[-1]) goto lab7;
	pop();
	return;

lab7:
	pop();
	dup();
	push(1);
	sub();
	push(0);
	sub();
	dup();
	push(1);
	sub();
	push(0);
	sub();

	lab5();
	swp();
	lab5();

	add();
	swp();
	pop();
}

int main() {
	stack_ptr = calloc(100000, sizeof(int64_t));
	int64_t acc;

/*
	for(int64_t i = 0; i < 1000; i++) {
		push(i);
		lab5();
		printf("%lld -> %lld\n", i, pop());
	}

	return 0;
*/

lab1:
	push(0);
	push(14472334024676096);
	push(8944394323791450);
	push(5527939700884769);
	push(3416454622906725);
	push(2111485077978096);
	push(1304969544928756);
	push(806515533049347);
	push(498454011879172);
	push(308061521170150);
	push(190392490709200);
	push(117669030460982);
	push(72723460248127);
	push(44945570212756);
	push(27777890035307);
	push(17167680177653);
	push(10610209857675);
	push(6557470319826);
	push(4052739537835);
	push(2504730782038);
	push(1548008755937);
	push(956722025992);
	push(591286729974);
	push(365435296253);
	push(225851433664);
	push(139583862488);
	push(86267571223);
	push(53316291075);
	push(32951280083);
	push(20365011165);
	push(12586268949);
	push(7778742098);
	push(4807527027);
	push(2971214979);
	push(1836311808);
	push(1134903217);
	push(701408693);
	push(433494481);
	push(267914343);
	push(165580035);
	push(102334114);
	push(63246016);
	push(39088153);
	push(24157707);
	push(14930304);
	push(9227513);
	push(5702805);
	push(3524541);
	push(2178357);
	push(1346217);
	push(832119);
	push(514176);
	push(317697);
	push(196465);
	push(121346);
	push(75129);
	push(46403);
	push(28590);
	push(17692);
	push(10993);
	push(6687);
	push(4157);
	push(2668);
	push(1606);
	push(957);
	push(534);
	push(282);
	push(128);
	push(176);
	push(42);
	push(94);
	push(2);
	push(114);
	push(108);
	push(100);
	push(99);
	push(35);
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

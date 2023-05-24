/*Nhóm 9 
1. Đoàn Quốc Trung 20133104
2. Vũ Trung Kiên   20133060
3. Phan Quốc Lưu   20133065
Ngay cap nhat cuoi: 06/03/2023
Cong dung: BigNum
*/
#include<iostream>
#include <conio.h>
#include<string.h>
using namespace std;
//Khai b�o hang
#define MAXDIGITS 100 	/* maximum length */
#define PLUS 1 			/* positive sign bit */
#define MINUS -1		 /* negative sign bit */

//Khai b�o c?u tr�c
typedef struct {
	char digits[MAXDIGITS]; /* the number */
	int signbit; 			/* PLUS or MINUS */
	int lastdigit; 			/*index of high-order digit*/
}bignum;
void initialize_bignum(bignum &n);
//Khai b�o h�m
//1. Nhap 1 so nguyen lon tu ban phim
void scan_bignum(bignum &n);
//2. In noi dung cua 1 so nguyen lon ra man hinh
void print_bignum(bignum n);
//3. Kiem tra 1 chuoi nhap vao co hop le
int kiemtra(char s[]);
//4.Cong 2 so bignum
void add_bignum(bignum a, bignum b, bignum &c);
//5.Tru 2 so bignum
void subtract_bignum(bignum a, bignum b, bignum &c);
//6.Tim max 2 so
int max(int a, int b);
//7. Cat bo nhung so 0 vo nghia trong 1 bignum
void zero_justify(bignum &n);
int compare_bignum(bignum a, bignum b);
//Neu a < b .PLUS
//Neu a> b . MINUS
//a=b . 0
void digit_shift(bignum &n,int d);
void multiply_bignum(bignum a, bignum b, bignum &c);
void divide_bignum(bignum a, bignum b, bignum &c);
void mode_bignum(bignum a,bignum b,bignum &c);
void tangtt_bignum(bignum &a);
void giamtt_bignum(bignum &a);
int main()
{
	do{
	bignum a, b, c;
	cout <<"Nhap a:";
	scan_bignum(a);
	cout <<"Nhap b:";
	scan_bignum(b);
	add_bignum(a,b,c);
	cout <<"a+b=";
	print_bignum(c);
	cout <<endl;
	subtract_bignum(a,b,c);
	cout <<"a-b=";
	print_bignum(c);
	cout <<endl;
	multiply_bignum(a,b,c);
	cout <<"a*b=";
	print_bignum(c);
	cout <<endl;
	divide_bignum(a,b,c);
	cout <<"a/b=";
	print_bignum(c);
	cout <<endl;
	mode_bignum(a,b,c);
	cout <<"a%b=";
	print_bignum(c);
	cout <<endl;
	tangtt_bignum(a);
	cout <<"++a =";
	print_bignum(a);
	cout <<endl;
	giamtt_bignum(b);
	cout <<"--b =";
	print_bignum(b);
	cout <<endl;
	cout <<"Nhan phim ESC de thoat...\n";
	}while(getch()!=27);
}
//Mot so h�m xul�
void print_bignum(bignum n)
{
	int i;
	if (n.signbit == MINUS) cout <<"-";
	for (i=n.lastdigit; i>=0; i--)
		cout << int(n.digits[i]);
}
void initialize_bignum(bignum &n)
{
	n.signbit=PLUS;
	n.lastdigit=0;
	for(int i=0;i<MAXDIGITS;i++)
		n.digits[i]=0;
}
int kiemtra(char s[]){
	//ktra k� tu  dau
	if (s[0]!='-' && !isdigit(s[0]))
		return 0;
	//ktra c�c k� t? ti?p theo
	int len = strlen(s);
	for(int i=1; i<len; i++)
		if (!isdigit(s[i])) return 0;
	//kh�ng ph�t hi?n vi ph?m
	return 1;
}

void scan_bignum(bignum &n)
{
	//B1: Nh?p chu?i
	char temp[256];
	cin.getline(temp,256);
	//B2: Ki?m tra
	if (!kiemtra(temp)){	//kh�ng h?p l?
		//g�n bignum = 0
		n.signbit = PLUS;
		n.lastdigit = 0;
		n.digits[0] = 0;
	}
	else {		//h?p l?. B3: chuy?n th�nh s? bignum
		//x�t 2 tr??ng h?p
		if (temp[0]!='-'){	//s? d??ng
			n.signbit = PLUS;
			n.lastdigit = strlen(temp)-1;
			for(int i=0; i<=n.lastdigit; i++)
				n.digits[i] = temp[n.lastdigit-i]-48;
		}
		else {				//s? �m
			n.signbit = MINUS;
			n.lastdigit = strlen(temp)-2;
			for(int i=0; i<=n.lastdigit; i++)
				n.digits[i] = temp[n.lastdigit+1-i]-48;
		}
	}
}
void add_bignum(bignum a, bignum b, bignum &c)
{
	int carry; /* carry digit */
	int i; /* counter */
	initialize_bignum(c);
	if (a.signbit == b.signbit) 
		c.signbit = a.signbit;
	else {
			if (a.signbit == MINUS) {
			a.signbit = PLUS;
			subtract_bignum(b,a,c);
			a.signbit = MINUS;
		} else {
				b.signbit = PLUS;
				subtract_bignum(a,b,c);
				b.signbit = MINUS;	
		}
	return;
	}	
	c.lastdigit = max(a.lastdigit,b.lastdigit)+1;
	for(i=a.lastdigit+1;i<=c.lastdigit;i++)
		a.digits[i]=0;
	for(i=b.lastdigit+1;i<=c.lastdigit;i++)
		b.digits[i]=0;	
	carry = 0;
	for (i=0; i<=(c.lastdigit); i++) {
		c.digits[i] = (char)(carry+a.digits[i]+b.digits[i]) % 10;
		carry = (carry + a.digits[i] + b.digits[i]) / 10;
	}
	zero_justify(c);
}	
//5.Tru 2 so bignum
void subtract_bignum(bignum a, bignum b, bignum &c)
{
	int borrow; /* anything borrowed? */
	int v; /* placeholder digit */
	int i; /* counter */
	if ((a.signbit == MINUS) || (b.signbit == MINUS)) {
		b.signbit = -1 * b.signbit;
		add_bignum(a,b,c);
		b.signbit = -1 * b.signbit;
		return;
	}
	if (compare_bignum(a,b) == PLUS) {
		subtract_bignum(b,a,c);
		c.signbit = MINUS;
		return;
	}
	c.signbit=PLUS;
	c.lastdigit = max(a.lastdigit,b.lastdigit);
	for(i=a.lastdigit+1;i<=c.lastdigit;i++)
		a.digits[i]=0;
	for(i=b.lastdigit+1;i<=c.lastdigit;i++)
		b.digits[i]=0;	
	borrow = 0;
	for (i=0; i<=(c.lastdigit); i++) {
		v = (a.digits[i] - borrow - b.digits[i]);
		if (a.digits[i] > 0)
			borrow = 0;
		if (v < 0) {
			v = v + 10;
			borrow = 1;
		}	
		c.digits[i] = (char) v % 10;		
	}
	zero_justify(c);
}
//6.Tim max 2 so
int max(int a, int b)
{
	if(a>=b)
		return a;
	return b;
}
//7. Cat bo nhung so 0 vo nghia trong 1 bignum
void zero_justify(bignum &n)
{
	while ((n.lastdigit > 0) && (n.digits[n.lastdigit]==0))
		n.lastdigit --;
	if ((n.lastdigit == 0) && (n.digits[0] == 0))
		n.signbit = PLUS; /* hack to avoid -0 */
}
int compare_bignum(bignum a, bignum b)
{
	int i; /* counter */
	if ((a.signbit == MINUS) && (b.signbit == PLUS)) 
		return(PLUS);
	if ((a.signbit == PLUS) && (b.signbit == MINUS)) 
		return(MINUS);
	if (b.lastdigit > a.lastdigit) 
		return (PLUS * a.signbit);
	if (a.lastdigit > b.lastdigit) 
		return (MINUS * a.signbit);
	for (i = a.lastdigit; i >= 0; i--) {
		if (a.digits[i] > b.digits[i])
			return(MINUS * a.signbit);
		if (b.digits[i] > a.digits[i])
			return(PLUS * a.signbit);
	}
	return(0);
	
}
void digit_shift(bignum &n,int d)
{
	int i;
	if((n.lastdigit==0) && (n.digits[0]==0))	
		return;
	for(i = n.lastdigit; i>=0;i--)
		n.digits[i+d]=n.digits[i];
	for(int i=0;i<d;i++)
	{
		n.digits[i]=0;
		n.lastdigit=n.lastdigit+d;
	}
}
void multiply_bignum(bignum a, bignum b, bignum &c)
{
	bignum row; /* represent shifted row */
	bignum tmp; /* placeholder bignum */
	initialize_bignum(c);
	int i,j; /* counters */
	row = a;
	for (i=0; i<=b.lastdigit; i++) {
		for (j=1; j<=b.digits[i]; j++) {
			add_bignum(c,row,tmp);
			c = tmp;
		}
		digit_shift(row,1);
	}
	c.signbit = a.signbit * b.signbit;
	zero_justify(c);
}
void divide_bignum(bignum a, bignum b, bignum &c)	
{
	bignum row; /* represent shifted row */
	bignum tmp; /* placeholder bignum */
	int asign, bsign; /* temporary signs */
	int i,j; /* counters */
	initialize_bignum(c);
	c.signbit = a.signbit * b.signbit;
	asign = a.signbit;
	bsign = b.signbit;
	a.signbit = PLUS;
	b.signbit = PLUS;
	initialize_bignum(row);
	initialize_bignum(tmp);
	c.lastdigit = a.lastdigit;
	for (i=a.lastdigit; i>=0; i--) {
		digit_shift(row,1);
		row.digits[0] = a.digits[i];
		c.digits[i] = 0;
		while (compare_bignum(row,b) != PLUS) {
			c.digits[i] ++;
			subtract_bignum(row,b,tmp);
			row = tmp;
		}
	}
	zero_justify(c);
	a.signbit = asign;
	b.signbit = bsign;
}
void mode_bignum(bignum a,bignum b,bignum &c)
{
	bignum thuong;
	bignum sotru;
	initialize_bignum(c);
	initialize_bignum(thuong);
	initialize_bignum(sotru);
	divide_bignum(a,b,thuong);
	multiply_bignum(b,thuong,sotru);
	subtract_bignum(a,sotru,c);	
}
void tangtt_bignum(bignum &a)
{
    int carry = 1;
    a.lastdigit = a.lastdigit + 1;
    for (int i = 0; i < a.lastdigit; i++) {
        int tmp = (char)(a.digits[i] + carry);
        if (tmp < 10) {
            a.digits[i] = tmp;
            carry = 0;
            break;
        } else {
            a.digits[i] = tmp % 10;
            carry = tmp / 10;
        }
    }
    if (carry > 0) {
        a.digits[a.lastdigit] = carry;
        a.lastdigit++;
    }
    zero_justify(a);
}
void giamtt_bignum(bignum &a)
{
    int borrow = 1;
    for (int i = 0; i <= a.lastdigit; i++) {
        int tmp = (char)(a.digits[i] - borrow);
        if (tmp >= 0) {
            a.digits[i] = tmp;
            borrow = 0;
            break;
        } else {
            a.digits[i] = 9;
            borrow = 1;
        }
    }
    zero_justify(a);
}

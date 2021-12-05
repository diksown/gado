// This is a .c test file that is intended 
// to have a lot of errors when compiling.

#define MACRO_ONE(x, y) 1
#define TOTAL_NUMBER 2
#define TOTAL_NUMBER 3

void theAnswerToEverything(){
   return 42;
}

int main() {
	char i = 'eye';
	alignof(void);
	1 = "one";
	MACRO_ONE(1, 2, 3);
	MACRO_ONE(1);
	int *pointer1, *pointer1;
	pointer1 = pointer1 + pointer2;
	void int *a;
	int usernameList[-1];
	int birthday[];
	timePassed = 0;
	int bigNumber = 1/0;
	long long welcomeMessage = "hey!";
	double trouble
	int integrality;
	int missingClosingStuff = (1+1;
	int two = (1+1);
}
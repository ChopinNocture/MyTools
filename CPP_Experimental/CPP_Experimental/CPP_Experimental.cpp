//====================================================
//	For epic interview test
//		author by Yanfeng
//			84649807@qq.com
//====================================================

#include "stdafx.h"
#include <iostream>
#include <string>


//-----------------------------------------------------------------------------------------------------------
// itoa tool function int trans to string display   , only support from base 2 to base 16
const int BUFF_SIZE = sizeof(int) * 4 + 2;
char* itoa(int value, unsigned int base) {
	static char buffer[BUFF_SIZE] = { '\0' };

	if (base > 16 || base < 2) {
		throw "Invalid base: only support range from 2 to 16!";
	}

	if (value == 0) {
		buffer[BUFF_SIZE - 2] = '0';		// zero
		return &buffer[BUFF_SIZE - 2];
	}

	bool bNeg = value < 0;
	if (bNeg) {
		value = -value;
	}

	int i = BUFF_SIZE - 2;
	while (0 != value && i >= 1)
	{
		buffer[i--] = "0123456789ABCDEF"[value%base];
		value /= base;
	}
	if (bNeg) {
		buffer[i--] = '-';
	}
	return &buffer[i + 1];
}

//-----------------------------------------------------------------------------------------------------------
// a interesting matrix function 
void BuildStringFromMatrix(int* Matrix, int NumRows, int NumColumns, char* OutBuffer)
{
	//  matrix check
	if (NumRows <= 0 || NumColumns <= 0) {	
		throw "invalid matrix";
	}

	std::string str_out;		// string easy to use

	int loopNum = NumRows < NumColumns ? NumRows : NumColumns;
	int i = 0, j = 0;

	for (int iter = 0; iter << 1 < loopNum; ++iter) {
		i = j = iter;
		for (; j < NumColumns - iter - 1; ++j) {				// top row
			str_out.append(itoa(Matrix[i*NumColumns + j], 10)).append(",");
		}
		for (; i < NumRows - iter; ++i) {						// right col
			str_out.append(itoa(Matrix[i*NumColumns + j], 10)).append(",");
		}

		if (--i > iter && --j >= iter) {
			for (; j > iter; --j) {								// bottom row back
				str_out.append(itoa(Matrix[i*NumColumns + j], 10)).append(",");
			}

			for (; i > iter; --i) {								// left col back
				str_out.append(itoa(Matrix[i*NumColumns + j], 10)).append(",");
			}
		}
	}
	strcpy_s(OutBuffer, NumRows*NumColumns * 4, str_out.c_str());	// dangours, only for quick test
}

//-----------------------------------------------------------------------------------------------------------
int main()
{
	using namespace std;

	try
	{
		// itoa test part
		int i_to, iBase;

		cout << "itoa function test:" << endl << "Please input the number to transfer :";
		cin >> i_to;
		cout << "then input the transfer base(2-16):";
		cin >> iBase;
		cout << "Output string is:" << itoa(i_to, iBase) << endl << endl;


		// BuildStringFromMatrix test part
		cout << "now test function: BuildStringFromMatrix" << endl << endl;
		int iTestTime = 1;

		cout << "How many times want to test:";
		cin >> iTestTime;

		if (iTestTime < 0 || iTestTime>50) {
			cout << "Greedy boy! Bye bye!";
			return 0;
		}

		while(iTestTime-->0){
			int row, col;
			cout << "input matrix row number:";
			cin >> row;
			cout << "col number:";
			cin >> col;

			cout << "Random " << row << " * " << col << " matrix looks like:" << endl;

			int* matrix = new int[row*col];
			for (int i = 0; i < row; ++i) {
				for (int j = 0; j < col; ++j) {
					matrix[col*i + j] = rand() % 10;		// matrix element is less than 10, good for eyes, & easy for setting buffer size
					cout << matrix[col*i + j] << ' ';
				}
				cout << endl;
			}

			char* sorted_arr = new char[row*col * 4];		// enough buffer size
			BuildStringFromMatrix(matrix, row, col, sorted_arr);

			cout << "result of BuildStringFromMatrix is:" << endl << sorted_arr << endl << endl;
		}
	}
	catch (const char* ex)
	{
		cout << ex;
	}
}
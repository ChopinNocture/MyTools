// CPP_Experimental.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <iostream>

#include "pch.h"
#include <iostream>
#include <string>

const int BUFF_LEN = sizeof(int) * 4 + 2;
//====================================================
// itoa tool function int trans to string display   , only support from base 2 to base 16
char* itoa(int value, unsigned int base) {
	if (base > 16 || base < 2) {
		throw std::string("invalid itoa base:");
	}

	static char buffer[BUFF_LEN] = { '\0' };

	if (value == 0) {
		buffer[BUFF_LEN - 2] = '0';		// zero
		return &buffer[BUFF_LEN - 2];
	}

	bool bNeg = value < 0;
	if (bNeg) {
		value = -value;
	}

	int i = BUFF_LEN - 2;
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

void BuildStringFromMatrix(int* Matrix, int NumRows, int NumColumns, char* OutBuffer)
{
	if (NumRows <= 0 || NumColumns <= 0) {
		throw "invalid matrix";
	}

	std::string str_out;

	int loopNum = NumRows < NumColumns ? NumRows : NumColumns;
	int i = 0, j = 0;

	for (int iter = 0; iter << 1 < loopNum; ++iter) {
		i = j = iter;
		for (; j < NumColumns - iter - 1; ++j) {				// start row
			str_out.append(itoa(Matrix[i*NumColumns + j], 10)).append(",");
		}
		for (; i < NumRows - iter; ++i) {						// end col
			str_out.append(itoa(Matrix[i*NumColumns + j], 10)).append(",");
		}

		if (--i > iter && --j >= iter) {
			for (; j > iter; --j) {								// end row back
				str_out.append(itoa(Matrix[i*NumColumns + j], 10)).append(",");
			}

			for (; i > iter; --i) {								// start col back
				str_out.append(itoa(Matrix[i*NumColumns + j], 10)).append(",");
			}
		}
	}
	strcpy_s(OutBuffer, NumRows*NumColumns * 4, str_out.c_str());	// dangours, only for quick test
}

int main()
{
	try
	{
		int i_to;
		std::cout << "itoa:";
		std::cin >> i_to;
		std::cout << itoa(i_to, 1) << std::endl;

		for (int oo = 0; oo < 15; ++oo) {
			int row, col;
			row = 4;
			col = 3;
			std::cin >> row;
			std::cin >> col;
			std::cout << "row:" << row << " col:" << col << std::endl;

			int* mat = new int[row*col];
			for (int i = 0; i < row; ++i) {
				for (int j = 0; j < col; ++j) {
					mat[col*i + j] = rand() % 10;
					std::cout << mat[col*i + j] << ' ';
				}
				std::cout << std::endl;
			}
			char* sorted_arr = new char[row*col * 4];
			BuildStringFromMatrix(mat, row, col, sorted_arr);
			std::cout << sorted_arr << std::endl;
		}
	}
	catch (std::string ex)
	{
		std::cout << ex;
	}

}
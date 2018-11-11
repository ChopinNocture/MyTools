// CPP_Experimental.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <iostream>

class TestClass
{
public:
	TestClass();									// Constructor function
	~TestClass();									// Destructor function
	TestClass(const TestClass& src_obj);			// Copy constructor function
	TestClass& operator=(const TestClass& r_obj);	// assignment copy operator
	TestClass* operator&();							// address operator &
	const TestClass* operator&() const;				// address operator &
}; 

TestClass::TestClass()
{
}

TestClass::TestClass(const TestClass& src_obj)
{
}

TestClass::~TestClass()
{
}

TestClass & TestClass::operator=(const TestClass & r_obj)
{
	// TODO: 在此处插入 return 语句
	return *this;
}

TestClass* TestClass::operator&()
{
	// TODO: 在此处插入 return 语句
	return this;
}

const TestClass* TestClass::operator&() const
{
	return this;
	//return nullptr;
}

const int BUFF_LEN = sizeof(int) * 4 + 2;
char* itoa(int value, unsigned int base) {
	if (base > 16) throw base;

	static char buffer[BUFF_LEN] = { '\0' };

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
	// Your code goes here
	std::string str_out;

	int iter = 0;

	int i=0, j=0, char_iter=0;
	for (i = iter; j < NumColumns - iter - 1; ++j) {
		str_out.append(itoa(Matrix[i*NumColumns + j], 10));
	}
	for (; i < NumRows - iter - 1; ++i) {
		str_out.append(itoa(Matrix[i*NumColumns + j], 10));
	}
	for (; j > iter; --j) {
		str_out.append(itoa(Matrix[i*NumColumns + j], 10));
	}
	for (; i > iter; --i) {
		str_out.append(itoa(Matrix[i*NumColumns + j], 10));
	}
	++iter;

	i = 0;
	j = 0 ~ NumColumns;
	
	i = 1 ~NumRows;
	j = NumColumns;
	

	i = NumRows - 1;
	j = NumColumns - 2 ~ 0;

	i = NumRows - 1 ~1;
	j = 0;
	

	while () {
		

		for (int i = 0; i < NumRows; ++i) {
			Matrix[]
			NumColumns
		}
	}


	for (int i = 0; i < NumRows; ++i) {
		for (int j = 0; j < NumColumns; ++j) {
			str_out += Matrix[NumColumns*i + j];
		}	
	}

	Matrix[0] = 0;
}

int main()
{
	int i_to;
	std::cout << "itoa:";
	std::cin >> i_to;
	std::cout << itoa(i_to, 16) << std::endl;


	int row, col;
	row = 4;
	col = 3;
	std::cin >> row;
	std::cin >> col;
	std::cout << "row:" << row << " col:" << col << std::endl;

	int* mat = new int[row*col];
	for (int i = 0; i < row; ++i) {
		for (int j = 0; j < col; ++j) {
			mat[col*i + j] = rand()%10;
			std::cout << mat[col*i + j] << ' ';
		}
		std::cout << std::endl;
	}
	char* sorted_arr = new char[row*col*4];
	BuildStringFromMatrix(mat, row, col, sorted_arr);
}


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "atod.h"
int diff(int size, double *x, double *y)
{
	int ret =1;
	int i;

	for(i=0; i < size; i++)
	{
		if (x[i] != y[i])
		{
			ret = 0;
			break;
		}
	}

	return ret;
}

int main(int argc, char **argv)
{
	int i, j, count, nocount, ret;
	double 	*data, *ptr_d;
	double  *dataset, *ptr_ds;
	int 	size;
	int	input_size, output_size, numofdata, data_size;
	int key;
	data = (double*)malloc(sizeof(double)*1024*20000);
	ret = file_load(argv[1], data, &size);
	numofdata = (int)data[0];
	input_size = (int)data[1];
	output_size = (int)data[2];
	data_size = input_size + output_size;
	dataset = (double*)malloc(sizeof(double)*data_size*numofdata);
	ptr_d = &data[3];
	ptr_ds = dataset;
	memcpy(ptr_ds, ptr_d, sizeof(double)*data_size);
	ptr_d += data_size;
	ptr_ds += data_size;
	count = 1;
	nocount = 0;
	for(i = 1; i < numofdata; i++)
	{
		key = 1;
		for(j = 0; j < count; j++)
		{
			if(diff(data_size, ptr_d, dataset+data_size*j))
			{
				key = 0;
				nocount++;
			}
		}	
		if(key)
		{
			memcpy(ptr_ds, ptr_d, sizeof(double)*data_size);
			ptr_ds += data_size;
			count++;
		}
		ptr_d += data_size;
	}
	#if 1
	printf("%d %d %d\n",count, input_size, output_size);
	for(j=0; j < count; j++)
	{
		for(i=0; i < input_size; i++)
		{
			printf("%g ",dataset[j*data_size + i]);
		}	
			printf("\n%g\n",dataset[j*data_size + i]);
	}
#endif
	return 0;
}

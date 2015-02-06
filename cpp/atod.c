#include <stdlib.h>
#include <stdio.h>
#include <memory.h>

double atod(char *str)
{
        int i,e=0;
        double n=0, sign;
        double mul_flag=0.1;

        if(str[0]=='-')
        {
                sign = -1;
                i = 1;
        }
        else
        {
                sign = 1;
                i = 0;
        }
        for(; str[i] >= '0' && str[i] <= '9'; ++i)
        {
                n = 10*n + (str[i] - '0');
        }

        if(str[i]=='.')
                for(++i;str[i] >= '0' && str[i] <= '9';++i)
                {
                        n += mul_flag*(str[i]-'0');
                        mul_flag*=0.1;
                }
        if(str[i++]=='e')
        {
                if(str[i++]=='+')
                {
                        for(; str[i] >= '0' && str[i] <= '9'; ++i)
                                e = 10*e + (str[i]-'0');
                        for(i=0; i < e; i++)
                                n *= 10;
                }
                else
                {
                        for(; str[i] >= '0' && str[i] <= '9'; ++i)
                                e = 10*e + (str[i]-'0');
                        for(i=0; i < e; i++)
                                n *= 0.1;                
		}
        }
        return sign * n ;
}

int file_load(char* filename, double* data, int* size)
{
        int i=0, count = 0;
        FILE *fd;
        char ch;
        char str[100];

        fd = fopen(filename, "r");

        if( fd < 0)
        {
                printf("ERROR : input data file is not open!\n");
                return -1;
        }

        while(EOF != (ch = fgetc(fd)))
        {

                if( ch != ' ' && ch != '\n' && ch != '\t' && ch != '\r')
                {
                        str[i++] = ch;
                }
		else if( i != 0)
		{
			i = 0;
			data[count++] = (double)atod(str);
			memset(str, 0, sizeof(char)*100);
		}
	}
	*size = count;
	fclose(fd);
	return 0;
}

int file_loadf(char* filename, float* data, int* size)
{
        int i=0, count = 0;
        FILE *fd;
        char ch;
        char str[100];

        fd = fopen(filename, "r");

        if( fd < 0)
        {
                printf("ERROR : input data file is not open!\n");
                return -1;
        }
        while(EOF != (ch = fgetc(fd)))
        {

                if( ch != ' ' && ch != '\n' && ch != '\t' && ch != '\r')
                {
                        str[i++] = ch;
                }
        else if( i != 0)
        {
            i = 0;

            data[count++] = (float)atod(str);
            memset(str, 0, sizeof(char)*100);
        }
    }
    *size = count;
    fclose(fd);
    return 0;
}

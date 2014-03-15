CFLAGS=-Wall -g -DNDEBUG
CC=gcc
MACPORTS = /usr/local
CPPFLAGS = -I$(MACPORTS)/include
LDFLAGS = -L$(MACPORTS)/lib
#LOADLIBS = -lgsl
LDLIBS = -lgsl -lgslcblas -lm

%:%.o
	$(CC) $(LDFLAGS) $< -o $@  $(LOADLIBS) $(LDLIBS) 

%.o:%.c
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@

CC = g++
CFLAGS = -g -lGL -lglfw -lGLEW
SOURCES = $(wildcard *.cpp)
OBJ = $(SOURCES:.cpp=.o)


main : $(OBJ)
	$(CC) $(OBJ) -o $@ $(CFLAGS)

main.o : main.cpp
	$(CC) $< -c $(CFLAGS)

%.o : %.cpp %.hpp
	$(CC) $< -c $(CFLAGS)
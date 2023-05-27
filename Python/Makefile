# Windows version !
ifeq ($(OS),Windows_NT)

CXX = icx
CFX = ifx

OPT_COMP0F = 
OPT_COMPF = $(OPT_COMP0F)

debug=0

!IF "$(debug)" != "0"
OPT_COMPF = -Od $(OPT_COMP0F) -debug:full -traceback 
!ENDIF

default: dll

boid.dll: boid.cpp
	$(CXX) $(OPT_COMPF) boid.cpp /link /DLL /OUT:boid.dll

boid.lib: boid.cpp
	$(CXX) $(OPT_COMPF) boid.cpp /link /DLL /OUT:boid.dll

dll: boid.dll

clean:	
	if exist *.exe del *.exe
	if exist *.obj del *.obj
	if exist *.mod del *.mod
	if exist *.pdb del *.pdb
	if exist *.lib del *.lib
	if exist *.exp del *.exp
	if exist *.dll del *.dll

else #################################
# Linux Version !
CXX = gcc

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)

default: makelib

libboid.so: boid.cpp 
	$(CXX) -fpic -shared -o $@ boid.cpp

makelib: libboid.so
endif
endif
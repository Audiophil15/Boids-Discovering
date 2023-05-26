#include <unistd.h>
#include <stdio.h>
#include <GL/glew.h>
#include <GLFW/glfw3.h>

const char * readfile(char * path);
GLuint createShader(unsigned int type, char * shaderpath);
GLuint createProgram(char * vspath, char * fspath);
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <stdio.h>

#include "GLtools.hpp"

void error_callback( int error, const char *msg ) {
	fprintf(stderr, "[%d] %s\n", error, msg);
}

GLFWwindow * glInit(int width, int heigt, const char * title){
	GLFWwindow * win;
	if (!glfwInit()) {
		printf("Error initialising glfw !\n");
		return nullptr;
	}
	glfwSetErrorCallback( error_callback );
	win = glfwCreateWindow(width, heigt, title, NULL, NULL);
	if (!win) {
		printf("Error creating the glfw window !\n");
		return nullptr;
	}
	glfwMakeContextCurrent(win);
	if (glewInit()) {
		printf("Error initialising glew !\n");
		return nullptr;
	}
	return win;
}
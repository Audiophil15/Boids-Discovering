#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include "shader.hpp"

#define DEBUG 0

const char * readfile(char * path) {

	FILE * file = fopen(path, "r");
	fseek(file, 0, SEEK_END);
	int length = ftell(file);
	fseek(file, 0, SEEK_SET);
	char * str = (char*)malloc(length*sizeof(char));
	fread(str, sizeof(char), length, file);
	if (DEBUG) {
		printf("%s\n", str); //DEBUG
	}
	return str;
}

GLuint createShader(unsigned int type, char * shaderpath){

	GLuint shaderID = glCreateShader(type);
	const char* shader = readfile(shaderpath);
	glShaderSource(shaderID, 1, &shader, 0);
	glCompileShader(shaderID);
	if (DEBUG){
		int status;
		glGetShaderiv(shaderID, GL_COMPILE_STATUS, &status);
		if ( status == GL_TRUE ){
  		printf("Shader %d compiled\n", shaderID);
  		}
  	}
	return shaderID;
}

GLuint createProgram(char * vertexShaderPath, char * fragmentShaderPath){

	GLuint vsid, fsid, progid;
	vsid = createShader(GL_VERTEX_SHADER, vertexShaderPath);
	fsid = createShader(GL_FRAGMENT_SHADER, fragmentShaderPath);
	progid = glCreateProgram();
	glAttachShader(progid, vsid);
	glAttachShader(progid, fsid);
	glLinkProgram(progid);
	if (DEBUG) {
		int status;
		glGetProgramiv(progid, GL_LINK_STATUS, &status);
		if ( status == GL_TRUE ){
		printf("Program %d linked with vs %d and fs %d\n", progid, vsid, fsid);
		}
	}
	return progid;
}
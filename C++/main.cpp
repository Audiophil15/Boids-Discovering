#include <stdio.h>
#include <string.h>
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <eigen3/Eigen/Core>

#include "shader.hpp"
#include "GLtools.hpp"

int main(){

	/* Initialisation of GLFW and GLEW which will
	allow us to open a window*/

	GLFWwindow * win = glInit(500, 500, "Boids");

	glfwSetInputMode(win, GLFW_STICKY_KEYS, GL_TRUE);
	printf("%s\n", glGetString(GL_VERSION));

	/* The shaders IDs are created,
	associated, and shaders get compiled here.*/

	GLuint program = createProgram("vs.glsl", "fs.glsl");
	GLuint program2 = createProgram("vs2.glsl", "fs2.glsl");

	float vtx[6] = {0.0, 0.0, 0.5, 0.5, 0.5, 0.0};

	GLuint vbo, vao;
	glGenBuffers(1, &vbo);
	glGenBuffers(1, &vao);

	const GLuint VTX_ATT_POSITION = 0;

	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	glBufferData(GL_ARRAY_BUFFER, 6*sizeof(float), vtx, GL_STATIC_DRAW);
	glBindBuffer(GL_ARRAY_BUFFER, 0);

	glBindVertexArray(vao);
	glEnableVertexAttribArray(VTX_ATT_POSITION);

	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	glVertexAttribPointer(VTX_ATT_POSITION, 2, GL_FLOAT, GL_FALSE, 2*sizeof(float), 0);

	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindVertexArray(0);


	do {

		glClear( GL_COLOR_BUFFER_BIT );

		glUseProgram(program);

		glBindVertexArray(vao);
		glDrawArrays(GL_TRIANGLES, 0, 3);
		glBindVertexArray(0);


		glUseProgram(program2);

		glBindVertexArray(vao);
		glDrawArrays(GL_TRIANGLES, 0, 3);
		glBindVertexArray(0);


		glfwSwapBuffers(win);
		glfwPollEvents();

	} while( glfwGetKey(win, GLFW_KEY_ESCAPE ) != GLFW_PRESS && glfwWindowShouldClose(win) == 0 );


	glDeleteBuffers(1, &vbo);
	glDeleteVertexArrays(1, &vao);

}
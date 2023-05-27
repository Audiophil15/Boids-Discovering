#include <stdio.h>
#include <string.h>
#include <glm/glm.hpp>
#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include "shader.hpp"
#include "geometry.hpp"
#include "GLtools.hpp"
#include "Boid.hpp"

int main(){

	/* Initialisation of GLFW and GLEW which will
	allow us to open a window*/

	GLFWwindow * win = glInit(1000, 1000, "Boids");

	glfwSetInputMode(win, GLFW_STICKY_KEYS, GL_TRUE);
	printf("%s\n", glGetString(GL_VERSION));

	/* The shaders IDs are created,
	associated, and shaders get compiled here.*/

	GLuint program = createProgram("vs.glsl", "fs.glsl");
	GLint uTransform = glGetUniformLocation(program, "uTransform");

	std::vector<glm::vec2> vtx = circle(1,0);

	GLuint vbo, vao;
	const GLuint VTX_ATT_POSITION = 0;

	glGenBuffers(1, &vbo);
	glGenBuffers(1, &vao);

	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	glBufferData(GL_ARRAY_BUFFER, vtx.size()*sizeof(glm::vec2), vtx.data(), GL_STATIC_DRAW);
	glBindBuffer(GL_ARRAY_BUFFER, 0);

	glBindVertexArray(vao);
	glEnableVertexAttribArray(VTX_ATT_POSITION);

	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	glVertexAttribPointer(VTX_ATT_POSITION, 2, GL_FLOAT, GL_FALSE, 2*sizeof(float), 0);

	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindVertexArray(0);


	int nbBoids = 10;

	for (int i = 0; i < nbBoids; i++){
		Boid::boidsList.push_back(new Boid(glm::vec2(i/(float)(nbBoids/2)-1, i/(float)(nbBoids/2)*i/(float)(nbBoids/2)-1), glm::vec2(0), glm::vec2(0), 0.01));
		// Boid::boidsList.push_back(new Boid(glm::vec2(cos(i*2*M_PI/nbBoids+i/2.), sin(i*2*M_PI/nbBoids)), glm::vec2(0), glm::vec2(0), 0.01));
		// Boid::boidsList.push_back(new Boid(glm::vec2(-1+2*(i/5.f), -1+2*(i/5.f)), glm::vec2(0), glm::vec2(0), 0.01));
		// printf("%f %f\n", Boid::boidsList[i]->getPosition().x, Boid::boidsList[i]->getPosition().y);
	}

	glm::mat4 transformation(1);

	do {

		glClear( GL_COLOR_BUFFER_BIT );

		glUseProgram(program);


		for (Boid* bp : Boid::boidsList) {
			bp->computeNextVelocity();
		}
		for (Boid* bp : Boid::boidsList) {
			bp->update();
		}
		Boid::updateGroupMassCenter();
		printf("%f %f\n", Boid::groupMassCenter.x, Boid::groupMassCenter.y);


		transformation = transformMatrix(Boid::groupMassCenter, 0.02f);
		glUniformMatrix4fv(uTransform, 1, GL_FALSE, glm::value_ptr(transformation));
		glBindVertexArray(vao);
		glDrawArrays(GL_TRIANGLES, 0, vtx.size());
		glBindVertexArray(0);

		for (int i = 0; i < nbBoids; i++){

			transformation = transformMatrix(Boid::boidsList[i]->getPosition(), Boid::boidsList[i]->getRadius());
			glUniformMatrix4fv(uTransform, 1, GL_FALSE, glm::value_ptr(transformation));

			glBindVertexArray(vao);
			glDrawArrays(GL_TRIANGLES, 0, vtx.size());
			glBindVertexArray(0);

		}

		glfwSwapBuffers(win);
		glfwPollEvents();

	} while( glfwGetKey(win, GLFW_KEY_ESCAPE ) != GLFW_PRESS && glfwWindowShouldClose(win) == 0 );


	glDeleteBuffers(1, &vbo);
	glDeleteVertexArrays(1, &vao);

}

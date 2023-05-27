#include <iostream>

#include "geometry.hpp"

std::vector<glm::vec2>circle(float radius, float inner){
	int nbsides = 4*250;
	std::vector<glm::vec2> vertices;
	double current, next;

	for (int i=0; i<nbsides; i++){
		current = i*M_PI*2/nbsides;
		next = (i+1)%nbsides*M_PI*2/nbsides;
		vertices.push_back(glm::vec2{float(cos(current))*radius, float(sin(current))*radius});
		if (inner){
			vertices.push_back(glm::vec2{float(cos(current))*inner, float(sin(current))*inner});
		} else {
			vertices.push_back(glm::vec2{0,0});
		}
		vertices.push_back(glm::vec2{float(cos(next))*radius, float(sin(next))*radius});
		if (inner){
			vertices.push_back(glm::vec2{float(cos(next))*radius, float(sin(next))*radius});
			vertices.push_back(glm::vec2{float(cos(current))*inner, float(sin(current))*inner});
			vertices.push_back(glm::vec2{float(cos(next))*inner, float(sin(next))*inner});
		}
	}

	return vertices;
}

glm::mat4 transformMatrix(glm::vec2 position, float scale){
	glm::mat4 transformation(1);
	// transformation = glm::rotate(transformation, a, glm::vec3(0.,0.,1.));
	transformation = glm::translate(transformation, glm::vec3(position.x, position.y, 0));
	transformation = glm::scale(transformation, glm::vec3(scale, scale, 1.f));
	return transformation;
}

glm::vec2 massCenter(std::vector<glm::vec2> positions){
	glm::vec2 center(0);
	for (glm::vec2 p : positions){
		center += p;
	}
	center /= positions.size();
	return center;
}
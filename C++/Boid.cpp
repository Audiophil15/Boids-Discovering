#include "Boid.hpp"

std::vector<Boid*> Boid::boidsList = std::vector<Boid*>();
glm::vec2 Boid::groupMassCenter = glm::vec2(0);
GLuint Boid::vertexArrayObject = 0;

Boid::Boid(glm::vec2 position = glm::vec2(0), glm::vec2 velocity = glm::vec2(0), glm::vec2 acceleration = glm::vec2(0), float radius = 0.01): pos(position), vel(velocity), acc(acceleration), radius(radius){}

void Boid::updateGroupMassCenter(){
	Boid::groupMassCenter = glm::vec2(0);
	for (Boid* b : Boid::boidsList){
		groupMassCenter += b->pos;
	}
	Boid::groupMassCenter /= Boid::boidsList.size();
}

void Boid::computeNextVelocity(){
	this->nextvel = glm::vec2(0);
	this->nextvel += (Boid::groupMassCenter-this->pos);
	this->nextvel /= this->nextvel.length();
}

void Boid::update(){
	this->vel = this->nextvel;
	this->pos += this->vel*0.1f;
}

glm::vec2 Boid::getPosition(){
	return this->pos;
}

float Boid::getRadius(){
	return this->radius;
}

#if !defined(BOID_H)
#define BOID_H

#include <glm/glm.hpp>
#include <GL/glew.h>

#include "geometry.hpp"

class Boid {

private:

	glm::vec2 pos;
	glm::vec2 vel;
	glm::vec2 nextvel;
	glm::vec2 acc;
	float radius;

public:
	static glm::vec2 groupMassCenter;
	static std::vector<Boid*> boidsList;
	static GLuint vertexArrayObject;

	Boid(glm::vec2 position , glm::vec2 velocity , glm::vec2 acceleration , float radius);
	~Boid(){};

	static void updateGroupMassCenter();
	void computeNextVelocity();

	void update();

	glm::vec2 subjectiveGroupMassCenter();

	glm::vec2 getPosition();
	float getRadius();

};


#endif // BOID_H

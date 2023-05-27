#if !defined(GEOMETRY_HPP)
#define GEOMETRY_HPP

#include <vector>
#include <math.h>
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <glm/gtx/transform.hpp>
#include <glm/gtc/matrix_transform.hpp>

std::vector<glm::vec2>circle(float radius, float inner);
glm::mat4 transformMatrix(glm::vec2 position, float scale);
glm::vec2 massCenter(std::vector<glm::vec2> positions);


#endif // GEOMETRY_HPP

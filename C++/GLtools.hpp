#if !defined(GLTOOLS_HPP)
#define GLTOOLS_HPP

#include <GLFW/glfw3.h>

void error_callback( int error, const char *msg );
GLFWwindow * glInit(int width, int heigt, const char * title);

#endif // GLTOOLS_HPP

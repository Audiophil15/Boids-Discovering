#version 330

layout(location = 0) in vec2 aVertexPosition;

out vec2 vPosition;

uniform mat4 uTransform;

void main() {
	vPosition = aVertexPosition;
	vPosition = (uTransform*vec4(aVertexPosition,0.,1.)).xy;

	gl_Position = vec4(vPosition, 0., 1.);
}

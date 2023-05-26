#version 330

in vec2 vPosition;

out vec4 fFragColor;

void main() {
	fFragColor = vec4(0,vPosition,1);
//	fFragColor = vec4(0,1,0,1);
}
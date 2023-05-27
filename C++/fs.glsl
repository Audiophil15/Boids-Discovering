#version 330

in vec2 vPosition;

out vec4 fFragColor;

void main() {
	// fFragColor = vec4(0, vPosition/2+0.5, 1);

	fFragColor = vec4(0, vPosition.x/2+0.5, vPosition.y/2+0.5, 1);

	// fFragColor = vec4(0, 1,1, 1);
}
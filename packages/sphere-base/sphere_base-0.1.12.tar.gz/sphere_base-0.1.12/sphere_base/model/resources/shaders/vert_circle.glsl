#version 330 core

layout(location = 0) in vec3 aPos;

out vec4 v_color;

uniform vec4 a_color;

void main()
{

        gl_Position = vec4(aPos, 1.0);
        v_color = a_color;
}

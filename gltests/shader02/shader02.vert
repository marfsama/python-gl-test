uniform mat4 ModelMatrix;
uniform mat4 ProjectionMatrix;


void main()
{
	gl_Position = 	ProjectionMatrix * ModelMatrix * gl_Vertex;
}
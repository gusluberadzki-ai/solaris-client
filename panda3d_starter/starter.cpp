// starter.cpp
// C++ version of the Panda3D starter game prototype.
// This file is separate from main.py and does not modify or delete the Python version.
// It uses GLFW + GLAD + GLM for windowing, input, and rendering.

#ifdef __APPLE__
#include <OpenGL/gl3.h>
#else
#include <glad/glad.h>
#endif
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <iostream>
#include <vector>
#include "gun_mesh.h"

static const unsigned int SCR_WIDTH = 1280;
static const unsigned int SCR_HEIGHT = 720;

double lastX = SCR_WIDTH / 2.0;
double lastY = SCR_HEIGHT / 2.0;
bool firstMouse = true;

float yaw = 90.0f;
float pitch = 0.0f;

glm::vec3 cameraPos = glm::vec3(0.0f, -18.0f, 1.8f);
glm::vec3 cameraFront = glm::vec3(0.0f, 1.0f, 0.0f);
glm::vec3 cameraUp = glm::vec3(0.0f, 0.0f, 1.0f);

bool keys[1024] = { false };

float movementSpeed = 10.0f;
float sprintMultiplier = 1.6f;
float mouseSensitivity = 0.1f;

bool reloadTriggered = false;
float reloadTime = 0.0f;
const float reloadDuration = 1.0f;

void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}

void keyboard_callback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);

    bool pressed = action != GLFW_RELEASE;
    if (key >= 0 && key < 1024) {
        keys[key] = pressed;
    }

    if (key == GLFW_KEY_R && action == GLFW_PRESS) {
        reloadTriggered = true;
        reloadTime = 0.0f;
    }
}

void mouse_callback(GLFWwindow* window, double xpos, double ypos)
{
    if (firstMouse)
    {
        lastX = xpos;
        lastY = ypos;
        firstMouse = false;
    }

    float xoffset = static_cast<float>(xpos - lastX);
    float yoffset = static_cast<float>(ypos - lastY);
    lastX = xpos;
    lastY = ypos;

    xoffset *= mouseSensitivity;
    yoffset *= mouseSensitivity;

    yaw -= xoffset;
    pitch -= yoffset;

    if (pitch > 89.0f)
        pitch = 89.0f;
    if (pitch < -89.0f)
        pitch = -89.0f;

    glm::vec3 direction;
    direction.x = cos(glm::radians(yaw)) * cos(glm::radians(pitch));
    direction.y = sin(glm::radians(yaw)) * cos(glm::radians(pitch));
    direction.z = sin(glm::radians(pitch));
    cameraFront = glm::normalize(direction);
}

unsigned int compileShader(unsigned int type, const char* source)
{
    unsigned int shader = glCreateShader(type);
    glShaderSource(shader, 1, &source, NULL);
    glCompileShader(shader);
    int success;
    char infoLog[512];
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    if (!success)
    {
        glGetShaderInfoLog(shader, 512, NULL, infoLog);
        std::cerr << "Shader compilation failed: " << infoLog << std::endl;
    }
    return shader;
}

unsigned int createShaderProgram()
{
    const char* vertexShaderSource = R"glsl(
        #version 330 core
        layout(location = 0) in vec3 aPos;
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        void main()
        {
            gl_Position = projection * view * model * vec4(aPos, 1.0);
        }
    )glsl";

    const char* fragmentShaderSource = R"glsl(
        #version 330 core
        out vec4 FragColor;
        uniform vec4 color;
        void main()
        {
            FragColor = color;
        }
    )glsl";

    unsigned int vertexShader = compileShader(GL_VERTEX_SHADER, vertexShaderSource);
    unsigned int fragmentShader = compileShader(GL_FRAGMENT_SHADER, fragmentShaderSource);

    unsigned int shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);

    int success;
    char infoLog[512];
    glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
    if (!success)
    {
        glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
        std::cerr << "Program linking failed: " << infoLog << std::endl;
    }

    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);
    return shaderProgram;
}

void processMovement(float deltaTime)
{
    glm::vec3 forward = glm::normalize(glm::vec3(cameraFront.x, cameraFront.y, 0.0f));
    glm::vec3 right = glm::normalize(glm::cross(forward, cameraUp));
    float speed = movementSpeed * deltaTime;
    if (keys[GLFW_KEY_LEFT_SHIFT])
        speed *= sprintMultiplier;

    if (keys[GLFW_KEY_W]) cameraPos += forward * speed;
    if (keys[GLFW_KEY_S]) cameraPos -= forward * speed;
    if (keys[GLFW_KEY_A]) cameraPos -= right * speed;
    if (keys[GLFW_KEY_D]) cameraPos += right * speed;
}

int main()
{
    if (!glfwInit())
    {
        std::cerr << "Failed to initialize GLFW\n";
        return -1;
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "C++ FPS Starter", NULL, NULL);
    if (!window)
    {
        std::cerr << "Failed to create GLFW window\n";
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
    glfwSetCursorPosCallback(window, mouse_callback);
    glfwSetKeyCallback(window, keyboard_callback);
    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);

    #ifndef __APPLE__
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        std::cerr << "Failed to initialize GLAD\n";
        return -1;
    }
    #endif

    glEnable(GL_DEPTH_TEST);

    unsigned int shaderProgram = createShaderProgram();

    // Simple grid plane using line segments.
    std::vector<float> gridVertices;
    const int gridRadius = 80;
    const float tileSize = 1.0f;
    for (int i = -gridRadius; i <= gridRadius; ++i)
    {
        gridVertices.push_back(i * tileSize);
        gridVertices.push_back(-gridRadius * tileSize);
        gridVertices.push_back(0.0f);
        gridVertices.push_back(i * tileSize);
        gridVertices.push_back(gridRadius * tileSize);
        gridVertices.push_back(0.0f);

        gridVertices.push_back(-gridRadius * tileSize);
        gridVertices.push_back(i * tileSize);
        gridVertices.push_back(0.0f);
        gridVertices.push_back(gridRadius * tileSize);
        gridVertices.push_back(i * tileSize);
        gridVertices.push_back(0.0f);
    }

    unsigned int gridVAO, gridVBO;
    glGenVertexArrays(1, &gridVAO);
    glGenBuffers(1, &gridVBO);
    glBindVertexArray(gridVAO);
    glBindBuffer(GL_ARRAY_BUFFER, gridVBO);
    glBufferData(GL_ARRAY_BUFFER, gridVertices.size() * sizeof(float), gridVertices.data(), GL_STATIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    unsigned int weaponVAO, weaponVBO, weaponEBO;
    glGenVertexArrays(1, &weaponVAO);
    glGenBuffers(1, &weaponVBO);
    glGenBuffers(1, &weaponEBO);
    glBindVertexArray(weaponVAO);
    glBindBuffer(GL_ARRAY_BUFFER, weaponVBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(gunVertices), gunVertices, GL_STATIC_DRAW);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, weaponEBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(gunIndices), gunIndices, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    float lastFrame = static_cast<float>(glfwGetTime());
    while (!glfwWindowShouldClose(window))
    {
        float currentFrame = static_cast<float>(glfwGetTime());
        float deltaTime = currentFrame - lastFrame;
        lastFrame = currentFrame;

        processMovement(deltaTime);

        if (reloadTriggered)
        {
            reloadTime += deltaTime;
            if (reloadTime >= reloadDuration)
            {
                reloadTriggered = false;
                reloadTime = 0.0f;
            }
        }

        glClearColor(0.10f, 0.12f, 0.15f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glUseProgram(shaderProgram);

        glm::mat4 projection = glm::perspective(glm::radians(60.0f), (float)SCR_WIDTH / (float)SCR_HEIGHT, 0.1f, 200.0f);
        glm::mat4 view = glm::lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
        glm::mat4 model = glm::mat4(1.0f);
        model = glm::translate(model, glm::vec3(-cameraPos.x, -cameraPos.y, 0.0f));

        int modelLoc = glGetUniformLocation(shaderProgram, "model");
        int viewLoc = glGetUniformLocation(shaderProgram, "view");
        int projLoc = glGetUniformLocation(shaderProgram, "projection");
        int colorLoc = glGetUniformLocation(shaderProgram, "color");

        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm::value_ptr(view));
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm::value_ptr(projection));

        // Draw grid
        glBindVertexArray(gridVAO);
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(model));
        glUniform4f(colorLoc, 0.35f, 0.38f, 0.32f, 1.0f);
        glDrawArrays(GL_LINES, 0, static_cast<GLsizei>(gridVertices.size() / 3));

        // Draw gun viewmodel in camera space
        glBindVertexArray(weaponVAO);
        glm::mat4 weaponView = glm::mat4(1.0f);
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm::value_ptr(weaponView));
        glm::mat4 weaponModel = glm::mat4(1.0f);
        float reloadEffect = reloadTriggered ? sin((reloadTime / reloadDuration) * 3.14159f) : 0.0f;
        weaponModel = glm::translate(weaponModel, glm::vec3(0.22f, 0.38f, -0.24f));
        weaponModel = glm::rotate(weaponModel, glm::radians(90.0f), glm::vec3(1.0f, 0.0f, 0.0f));
        weaponModel = glm::rotate(weaponModel, glm::radians(-5.0f + reloadEffect * 18.0f), glm::vec3(0.0f, 0.0f, 1.0f));
        weaponModel = glm::scale(weaponModel, glm::vec3(0.012f));
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(weaponModel));
        glUniform4f(colorLoc, 0.85f, 0.65f, 0.20f, 1.0f);
        glDrawElements(GL_TRIANGLES, gunIndexCount, GL_UNSIGNED_INT, 0);
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm::value_ptr(view));

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteVertexArrays(1, &gridVAO);
    glDeleteBuffers(1, &gridVBO);
    glDeleteVertexArrays(1, &weaponVAO);
    glDeleteBuffers(1, &weaponVBO);
    glDeleteBuffers(1, &weaponEBO);
    glDeleteProgram(shaderProgram);

    glfwTerminate();
    return 0;
}

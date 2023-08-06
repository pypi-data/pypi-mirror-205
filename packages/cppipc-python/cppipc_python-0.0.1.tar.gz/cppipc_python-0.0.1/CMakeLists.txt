cmake_minimum_required (VERSION 3.5)
project(cppipc_python)
# set(CMAKE_BUILD_TYPE Debug)

# Create the executable
add_subdirectory(pybind11)
# add_executable(${PROJECT_NAME} src/main_copy.cpp)
pybind11_add_module(${PROJECT_NAME} src/main.cpp)


add_subdirectory(src/cpp-ipc)
target_link_libraries(${PROJECT_NAME} PRIVATE ipc)



# ./cppipc_python recv 100
# ./cppipc_python send 100 120
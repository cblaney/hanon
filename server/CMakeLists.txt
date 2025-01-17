cmake_minimum_required(VERSION 3.5.0)

set(CMAKE_C_COMPILER "/usr/bin/gcc")
set(CMAKE_CXX_COMPILER "/usr/bin/g++")

project(server VERSION 0.1.0 LANGUAGES C CXX)

include_directories(inc)
link_directories(src)
add_executable(server 
    src/main.cpp
    src/server.cpp
)

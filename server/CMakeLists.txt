cmake_minimum_required(VERSION 3.5.0)

set(CMAKE_C_COMPILER "/usr/bin/gcc")
set(CMAKE_CXX_COMPILER "/usr/bin/g++")

project(hanon VERSION 0.1.0 LANGUAGES C CXX)

add_executable(hanon main.cpp)


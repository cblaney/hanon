cmake_minimum_required(VERSION 3.5.0)

set(CMAKE_C_COMPILER "/usr/bin/gcc")
set(CMAKE_CXX_COMPILER "/usr/bin/g++")

project(server VERSION 0.1.0 LANGUAGES C CXX)

find_package(Boost)

include_directories(inc
                    ${Boost_INCLUDE_DIRS}
                    )
link_directories(src)
add_executable(hanon
    src/main.cpp
)
target_link_libraries(hanon ${Boost_LIBRARIES})


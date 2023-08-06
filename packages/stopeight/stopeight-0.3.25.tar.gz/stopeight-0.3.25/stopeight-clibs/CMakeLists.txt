cmake_minimum_required (VERSION 3.2)

set(CMAKE_CXX_STANDARD 17)

project(stopeight-clibs)
include(${PROJECT_SOURCE_DIR}/Package.cmake)

add_subdirectory(matrix)
add_subdirectory(grapher)
add_subdirectory(analyzer)
add_subdirectory(legacy)

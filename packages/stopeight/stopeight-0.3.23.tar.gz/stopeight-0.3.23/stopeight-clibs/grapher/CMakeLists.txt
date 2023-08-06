cmake_minimum_required (VERSION 3.12)

project(stopeight-clibs-grapher)

aux_source_directory(. SRC_LIST)
#file(GLOB SOURCES "*.cpp")
set(${PROJECT_NAME}_sources
    containers.cpp
    algo.cpp
    grapher.cpp
    mean.cpp
    main.cpp
    ${POST_CONFIGURE_FILE}
)

#add_executable(${PROJECT_NAME} ${${PROJECT_NAME}_sources})
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
add_library(${PROJECT_NAME} SHARED ${${PROJECT_NAME}_sources})

#include_directories(${stopeight-clibs_INCLUDE_DIRS})
target_include_directories(${PROJECT_NAME}
    PRIVATE
    ${stopeight-clibs_INCLUDE_DIRS}
    ${GIT_HEADER_DIR}
)
target_link_libraries(${PROJECT_NAME} git)
install(TARGETS ${PROJECT_NAME} DESTINATION lib)

find_package(Python COMPONENTS Development)
if (Python_Development_FOUND)
#find_package(pybind11 CONFIG)
#if (pybind11_FOUND)
add_subdirectory(python)
#endif (pybind11_FOUND)
endif (Python_Development_FOUND)

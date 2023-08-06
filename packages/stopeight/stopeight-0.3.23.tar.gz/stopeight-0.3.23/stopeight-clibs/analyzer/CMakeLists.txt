cmake_minimum_required (VERSION 3.12)

project(stopeight-clibs-analyzer)
aux_source_directory(. SRC_LIST)
set(${PROJECT_NAME}_sources
    turns.cpp
    ${POST_CONFIGURE_FILE}
)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
add_library(${PROJECT_NAME} SHARED ${${PROJECT_NAME}_sources})

target_link_libraries(${PROJECT_NAME}
    PRIVATE
    stopeight-clibs-matrix
    git
)

target_include_directories(${PROJECT_NAME}
    PRIVATE
    ${stopeight-clibs_INCLUDE_DIRS}
    ${GIT_HEADER_DIR}
)
install(TARGETS ${PROJECT_NAME} DESTINATION lib)

find_package(Python COMPONENTS Development)
if (Python_Development_FOUND)
#find_package(pybind11 CONFIG)
#if (pybind11_FOUND)
add_subdirectory(python)
#endif (pybind11_FOUND)
endif (Python_Development_FOUND)

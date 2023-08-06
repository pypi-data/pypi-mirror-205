include(${PROJECT_SOURCE_DIR}/Includes.cmake)
include(${PROJECT_SOURCE_DIR}/Versioning.cmake)

find_package(Python COMPONENTS Interpreter Development)
if (Python_Interpreter_FOUND AND Python_Development_FOUND)
add_subdirectory(${PROJECT_SOURCE_DIR}/pybind11)
endif (Python_Interpreter_FOUND AND Python_Development_FOUND)

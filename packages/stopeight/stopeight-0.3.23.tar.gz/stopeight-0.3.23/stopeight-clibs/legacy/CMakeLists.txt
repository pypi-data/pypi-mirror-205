cmake_minimum_required (VERSION 3.12)

find_package(Qt5Core)
find_package(Qt5Gui)

if (Qt5Core_FOUND AND Qt5Gui_FOUND)

project(stopeight-clibs-legacy)
aux_source_directory(. SRC_LIST)
set(${PROJECT_NAME}_sources
    src/listcopyable.cpp
    src/listrotator.cpp
    src/listbase.cpp
    src/listswitchable.cpp
    src/dpoint.cpp
    src/myreal.cpp
    src/spiralscalculator.cpp
    src/spiralsanalyzer.cpp
    src/cliffscalculator.cpp
    src/cliffsanalyzer.cpp
    src/areaanalyzer.cpp
    src/areacalculator.cpp
    src/turnnormalizer.cpp
    src/turncalculator.cpp
    src/areanormalizer.cpp
    src/cornercalculator.cpp
    src/cornernormalizer.cpp
    src/calculator.cpp
    src/analyzer.cpp
    src/editorbase.cpp
    src/spirals.cpp
    src/editorspirals.cpp
    src/straightscalculator.cpp
    src/editorcliffs.cpp
    src/cliffs.cpp
    src/cliffsnormalizer.cpp
    src/turns.cpp
    src/turnanalyzer.cpp
    src/straightsanalyzer.cpp
    src/corneranalyzer.cpp
    src/straightsnormalizer.cpp
    src/corners.cpp
    src/render.cpp
    ${POST_CONFIGURE_FILE}
)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
add_library(${PROJECT_NAME} SHARED ${${PROJECT_NAME}_sources})

target_link_libraries(${PROJECT_NAME}
    PRIVATE
    Qt5::Core
    Qt5::Gui
    git
)

target_include_directories(${PROJECT_NAME}
    PRIVATE
    "include"
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
endif (Qt5Core_FOUND AND Qt5Gui_FOUND)

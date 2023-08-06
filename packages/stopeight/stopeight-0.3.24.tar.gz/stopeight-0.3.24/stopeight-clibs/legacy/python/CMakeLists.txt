cmake_minimum_required (VERSION 3.4.3)

find_package(Qt5Core)
find_package(Qt5Gui)
if (Qt5Core_FOUND AND Qt5Gui_FOUND)

#find_package(stopeight-clibs-legacy)
#if (stopeight-clibs-legacy_FOUND)
project(legacy)
pybind11_add_module(${PROJECT_NAME} 
    interfacepython.cpp
)
target_link_libraries(${PROJECT_NAME}
    PRIVATE
    stopeight-clibs-legacy
    Qt5::Core
)
target_include_directories(${PROJECT_NAME}
    PRIVATE
    "../include"
    "../../include"
    "../../cmake-git-version-tracking/better-example"
    ${Qt5Core_INCLUDE_DIRS}
#ubuntu includes/qt5/
)
#endif (stopeight-clibs-legacy_FOUND)

#find_package(stopeight-clibs-legacy)
#if (stopeight-clibs-legacy_FOUND)
project(finders)
pybind11_add_module(${PROJECT_NAME} 
    IFPyFinders.cpp
    IFPyShared.cpp
)
target_link_libraries(${PROJECT_NAME}
    PRIVATE
    stopeight-clibs-legacy
    stopeight-clibs-matrix
    Qt5::Core
#    Qt5::Gui
)
target_include_directories(${PROJECT_NAME}
    PRIVATE
    "../include"
    "../../include"
    "./"
    "../../cmake-git-version-tracking/better-example"
    ${Qt5Core_INCLUDE_DIRS}
)
#endif (stopeight-clibs-legacy_FOUND)

#find_package(stopeight-clibs-legacy)
#find_package(stopeight-clibs-matrix)
#if (stopeight-clibs-legacy_FOUND AND stopeight-clibs-matrix_FOUND)
project(getters)
pybind11_add_module(${PROJECT_NAME}
    IFPyGetters.cpp
    IFPyShared.cpp
)
target_link_libraries(${PROJECT_NAME}
    PRIVATE
    stopeight-clibs-legacy
    stopeight-clibs-matrix
    Qt5::Core
)
target_include_directories(${PROJECT_NAME}
    PRIVATE
    "../include"
    "../../include"
    "./"
    "../../cmake-git-version-tracking/better-example"
    ${Qt5Core_INCLUDE_DIRS}
)
#endif (stopeight-clibs-legacy_FOUND AND stopeight-clibs-matrix_FOUND)

endif (Qt5Core_FOUND AND Qt5Gui_FOUND)

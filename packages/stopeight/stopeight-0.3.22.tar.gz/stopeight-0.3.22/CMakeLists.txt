cmake_minimum_required(VERSION 3.2)

set(CMAKE_CXX_STANDARD 17)

project(stopeight)

#if (${EXT_NAME} MATCHES "STOPEIGHT.STOPEIGHT-CLIBS")
add_subdirectory(stopeight-clibs)
#elseif (${EXT_NAME} MATCHES "STOPEIGHT.MATRIX")
#add_subdirectory(stopeight-clibs/matrix)
#elseif (${EXT_NAME} MATCHES "STOPEIGHT.GRAPHER")
#add_subdirectory(stopeight-clibs/grapher)
#elseif (${EXT_NAME} MATCHES "STOPEIGHT.ANALYZER")
#add_subdirectory(stopeight-clibs/analyzer)
#elseif (${EXT_NAME} MATCHES "STOPEIGHT.LEGACY")
#add_subdirectory(stopeight-clibs/legacy)
#endif ()

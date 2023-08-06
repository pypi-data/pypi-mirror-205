cmake_minimum_required (VERSION 3.4.3)

#find_package(stopeight-clibs-analyzer)
#if (stopeight-clibs-analyzer_FOUND)

project(analyzer)

pybind11_add_module(${PROJECT_NAME} 
	IFPyAnalyzer.cpp
)

target_link_libraries(${PROJECT_NAME} PRIVATE stopeight-clibs-analyzer)

target_include_directories(${PROJECT_NAME}
    PRIVATE
    "../../include"
    "../"
    ${stopeight-clibs_INCLUDE_DIRS}
    "../../cmake-git-version-tracking/better-example"
)

#endif (stopeight-clibs-analyzer_FOUND)

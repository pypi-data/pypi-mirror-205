#############
# Variables needed in modules, auto-generated git.h file needed in wrappers
#############
set(PRE_CONFIGURE_FILE "${PROJECT_SOURCE_DIR}/cmake-git-version-tracking/better-example/git.cc.in")
set(POST_CONFIGURE_FILE "${CMAKE_CURRENT_BINARY_DIR}/git.cpp")
file(APPEND "${CMAKE_CURRENT_BINARY_DIR}/git.cpp" "")
include(${PROJECT_SOURCE_DIR}/cmake-git-version-tracking/git_watcher.cmake)
# Danger injection from submodule?
set(GIT_HEADER_DIR "${PROJECT_SOURCE_DIR}/cmake-git-version-tracking/better-example/")

# Create a library out of the compiled post-configure file.
add_library(git STATIC ${POST_CONFIGURE_FILE})
target_include_directories(git PUBLIC ${GIT_HEADER_DIR})
add_dependencies(git check_git)

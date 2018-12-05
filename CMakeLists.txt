cmake_minimum_required(VERSION 3.2)

project(SHORE_PY_BINDINGS)

include(libs/ShoreSDK/shore.cmake)

add_subdirectory(libs/pybind11-2.2.3)
add_subdirectory(src)
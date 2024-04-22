cmake_minimum_required(VERSION 3.2)

project(SHORE_PY_BINDINGS)

set(PYBIND_DIR libs/pybind11-2.12.0 CACHE PATH "relative path to pybind")

include(libs/ShoreSDK/shore.cmake)

add_subdirectory(${PYBIND_DIR})
add_subdirectory(src)

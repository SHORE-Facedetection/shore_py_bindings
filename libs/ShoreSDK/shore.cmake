set(SHORE_SDK_PATH ${CMAKE_SOURCE_DIR}/ShoreSDK CACHE PATH "Select path to SHORE SDK!")
set(SHORE_VERSION 161 CACHE STRING "Select required version of SHORE!" )
set(SHORE_LIB_PREFIX CACHE STRING 
    "Select Shore lib Prefix(e.g. Win32|Win64|Linux_x64|Linux_x86|Linux_armv7hf). Leave empty to autodetect")

file(GLOB_RECURSE SHORE_LIB_PATH_SHARED LIST_DIRECTORIES=false 
    ${SHORE_SDK_PATH}/Lib/${SHORE_LIB_PREFIX}*/${CMAKE_SHARED_LIBRARY_PREFIX}Shore${SHORE_VERSION}${CMAKE_SHARED_LIBRARY_SUFFIX}
)
# protected packages of shore can contain stub library which must be used for linking
foreach( _SHORE_LIB_PATH ${SHORE_LIB_PATH_SHARED})
    string(REGEX MATCH ".*_stub.*" item "${_SHORE_LIB_PATH}")
    if (item)
        message(STATUS "SHORE stub library found: ${item}")
        set (SHORE_STUB_LIB_PATH ${item})
        list (REMOVE_ITEM SHORE_LIB_PATH_SHARED ${item})
    endif()
endforeach()

file(GLOB_RECURSE SHORE_LIB_PATH_STATIC LIST_DIRECTORIES=false
    ${SHORE_SDK_PATH}/Lib/${SHORE_LIB_PREFIX}*/${CMAKE_STATIC_LIBRARY_PREFIX}Shore${SHORE_VERSION}${CMAKE_STATIC_LIBRARY_SUFFIX}
)
if (SHORE_LIB_PATH_SHARED AND NOT SHORE_LIB_PATH_STATIC)
    set (SHORE_LIB_TYPE SHARED)
    set (SHORE_LIB_PATH ${SHORE_LIB_PATH_SHARED})
elseif (SHORE_LIB_PATH_STATIC AND NOT SHORE_LIB_PATH_SHARED)
    set (SHORE_LIB_TYPE STATIC)
    set (SHORE_LIB_PATH ${SHORE_LIB_PATH_STATIC})
elseif (SHORE_LIB_PATH_SHARED AND SHORE_LIB_PATH_STATIC AND WIN32)
    set (SHORE_LIB_TYPE SHARED)
    set (SHORE_LIB_PATH ${SHORE_LIB_PATH_SHARED})
elseif( NOT SHORE_LIB_PATH_SHARED AND NOT SHORE_LIB_PATH_STATIC )
    message( FATAL_ERROR "SHORE library not found")
else()
    message(FATAL_ERROR "something wrong")
endif()
add_library(shore ${SHORE_LIB_TYPE} IMPORTED GLOBAL)
if( SHORE_LIB_PATH AND (NOT SHORE_LIB_PATH STREQUAL ""))
    message( STATUS "Found SHORE: ${SHORE_LIB_PATH}")
else()
    message(FATAL_ERROR "SHORE library not found")
endif()
get_filename_component(SHORE_LIB_DIR ${SHORE_LIB_PATH} DIRECTORY)
set_target_properties(shore PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${SHORE_LIB_DIR})
set_target_properties(shore PROPERTIES IMPORTED_LOCATION ${SHORE_LIB_PATH})
set_target_properties(shore PROPERTIES SHORE_VERSION ${SHORE_VERSION})
if (${SHORE_LIB_TYPE} STREQUAL STATIC)
    set_target_properties(shore PROPERTIES INTERFACE_COMPILE_DEFINITIONS SHORE_STATIC)
endif()
if (WIN32)
    set_target_properties(shore PROPERTIES IMPORTED_IMPLIB ${SHORE_LIB_PATH_STATIC})
endif()
set_target_properties(shore PROPERTIES INTERFACE_INCLUDE_DIRECTORIES ${SHORE_SDK_PATH}/Lib)
set(SHORE_MODEL_SOURCE 
    ${SHORE_SDK_PATH}/Model/Age_28x28_2009_09_17_131241.cpp
    ${SHORE_SDK_PATH}/Model/Angry_26x26_2008_10_21_152601.cpp
    ${SHORE_SDK_PATH}/Model/Face_24x24_2009_09_02_185611_48.cpp
    ${SHORE_SDK_PATH}/Model/FaceFront_24x24_2008_08_29_161712_7.cpp
    ${SHORE_SDK_PATH}/Model/FaceFrontId_36x44_2009_08_07_122105.cpp
    ${SHORE_SDK_PATH}/Model/FaceRotated_24x24_2008_10_15_180432_24.cpp
    ${SHORE_SDK_PATH}/Model/Gender_26x26_2008_09_04_174103.cpp
    ${SHORE_SDK_PATH}/Model/Happy_26x26_2008_09_08_124526.cpp
    ${SHORE_SDK_PATH}/Model/LeftEyeClosed_16x16_2008_10_23_185544.cpp
    ${SHORE_SDK_PATH}/Model/LeftEyeFront_16x16_2008_10_20_190938_4.cpp
    ${SHORE_SDK_PATH}/Model/MouthFront_16x14_2008_10_20_190419_4.cpp
    ${SHORE_SDK_PATH}/Model/MouthOpen_16x14_2008_10_23_185229.cpp
    ${SHORE_SDK_PATH}/Model/NoseFront_16x16_2008_10_17_134731_4.cpp
    ${SHORE_SDK_PATH}/Model/RightEyeClosed_16x16_2008_10_23_185544.cpp
    ${SHORE_SDK_PATH}/Model/RightEyeFront_16x16_2008_10_20_190953_4.cpp
    ${SHORE_SDK_PATH}/Model/Sad_26x26_2008_10_21_161703.cpp
    ${SHORE_SDK_PATH}/Model/Surprised_26x26_2008_09_11_175815.cpp
    ${SHORE_SDK_PATH}/Model/Tracking_36x36_2008_08_21_110315.cpp
)
set (SHORE_MODEL_CTM
    ${SHORE_SDK_PATH}/Model/ShapeLocator_68_2018_01_17_094200.ctm
)
set (SHORE_CREATE_FACE_ENGINE_CPP ${SHORE_SDK_PATH}/Lib/CreateFaceEngine.cpp)
set (SHORE_CREATE_DETECT_AND_TRACK_ENGINE_CPP ${SHORE_SDK_PATH}/Lib/CreateDetectAndTrackEngine.cpp)
set (SHORE_INCLUDE_DIR ${SHORE_SDK_PATH}/Lib)

set_property(TARGET shore PROPERTY SHORE_MODEL_SOURCE ${SHORE_MODEL_SOURCE})
if (${SHORE_VERSION} GREATER 161 )
    set_property(TARGET shore PROPERTY SHORE_MODEL_CTM ${SHORE_MODEL_CTM})
endif()
set_property(TARGET shore PROPERTY SHORE_CREATE_FACE_ENGINE_CPP ${SHORE_CREATE_FACE_ENGINE_CPP})
set_property(TARGET shore PROPERTY SHORE_CREATE_DETECT_AND_TRACK_ENGINE_CPP ${SHORE_CREATE_DETECT_AND_TRACK_ENGINE_CPP})
set_property(TARGET shore PROPERTY SHORE_SDK_DIR ${SHORE_SDK_PATH})

if (SHORE_STUB_LIB_PATH)
    # this library must be used for linking only, as long the protected 
    # shore library doesn't contain symbols
    add_library(shore_stub SHARED IMPORTED GLOBAL)
    set_target_properties(shore_stub
        PROPERTIES
            IMPORTED_LOCATION ${SHORE_STUB_LIB_PATH}
            INTERFACE_INCLUDE_DIRECTORIES $<TARGET_PROPERTY:shore,INTERFACE_INCLUDE_DIRECTORIES>
    )
endif()

set (SHORE_BINDINGS shore_bindings)

set (src 
    main.cpp
    $<TARGET_PROPERTY:shore,SHORE_CREATE_FACE_ENGINE_CPP>
    $<TARGET_PROPERTY:shore,SHORE_MODEL_SOURCE>
)
pybind11_add_module(${SHORE_BINDINGS} SHARED ${src})

set (SHORE_TARGET shore)

target_link_libraries(${SHORE_BINDINGS} PUBLIC ${SHORE_TARGET} PRIVATE pybind11::module)

set_target_properties(${SHORE_BINDINGS}
    PROPERTIES
        POSITION_INDEPENDENT_CODE ON
        CXX_STANDARD 11
        SUFFIX ${PYTHON_MODULE_EXTENSION}
        OUTPUT_NAME shore
        PREFIX ""
        INSTALL_RPATH "."
)
target_compile_definitions(${SHORE_BINDINGS}
    PUBLIC
        SHORE_REGISTER_MODELS
        SHORE_VERSION=$<TARGET_PROPERTY:shore,SHORE_VERSION>
)

###########################################################################
set (INSTALL_ROOT "${CMAKE_BINARY_DIR}/INSTALL")
install (TARGETS ${SHORE_BINDINGS}
         RUNTIME DESTINATION ${INSTALL_ROOT}
         LIBRARY DESTINATION ${INSTALL_ROOT}
         ARCHIVE DESTINATION ${INSTALL_ROOT}
)
install (
        FILES
            $<TARGET_PROPERTY:shore,SHORE_MODEL_CTM>
            $<TARGET_PROPERTY:shore,IMPORTED_LOCATION>
            ${CMAKE_SOURCE_DIR}/src/pyshore.py
            ${CMAKE_SOURCE_DIR}/test/video.py
            ${CMAKE_SOURCE_DIR}/test/run_shore.py
            ${CMAKE_SOURCE_DIR}/test/requirements.txt
            ${CMAKE_SOURCE_DIR}/Readme.md
        DESTINATION ${INSTALL_ROOT}
)
# License of pybind11
set (INSTALL_COPYRIGHT_DIR ${INSTALL_ROOT}/Copyright)
install (DIRECTORY DESTINATION ${INSTALL_COPYRIGHT_DIR})
install (
        FILES
            ${CMAKE_SOURCE_DIR}/libs/pybind11-2.8.1/LICENSE
        DESTINATION
            ${INSTALL_COPYRIGHT_DIR}/pybind11-2.8.1
)
# License of SHORE
get_target_property(SHORE_SDK_DIR shore SHORE_SDK_DIR)
install (
        DIRECTORY
            ${SHORE_SDK_DIR}/Copyright
        DESTINATION
            ${INSTALL_COPYRIGHT_DIR}/SHORE
)
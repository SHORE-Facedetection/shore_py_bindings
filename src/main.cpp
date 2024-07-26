/* Copyright (c) 2018 Fraunhofer IIS and shore_py_bindings contributors.
 *
 * This file is part of shore_py_bindings which is released under MIT license.
 * See file LICENSE for full license details.
 */

#include <CreateFaceEngine.h>
#include <Shore.h>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <iostream>
#include <tuple>
#include <cstdint>
#include <string>

namespace py = pybind11;

Shore::Content const* EngineProcess(Shore::Engine& eng,
    pybind11::array_t<unsigned char, py::array::c_style | py::array::forcecast> image,
    char const* colorSpace)
{
    const unsigned char* img = nullptr;
    Shore::Content const* content = nullptr;
    if (image.ndim() != 1)
    {
        unsigned long width = image.shape(1);
        unsigned long height = image.shape(0);
        unsigned long planes = 0;
        long pixelFeed = 0, lineFeed = 0, planeFeed = 0;
        if (!std::string(colorSpace).compare("GRAYSCALE")) 
        {
            if (image.ndim() != 2) 
            {
                throw std::runtime_error(
                    "Expected number of dimensions is 2, got " +
                    std::to_string(image.ndim()));
            }
            planes = 1;
            lineFeed = width;
            pixelFeed = 1;
            planeFeed = 0;
        }
        else if (!std::string(colorSpace).compare("RGB") ||
            !std::string(colorSpace).compare("BGR")) {
            if (image.ndim() != 3 && image.shape(2) != 3) 
            {
                std::string err =
                    "Expected number of dimensions is 3, got " +
                    std::to_string(image.ndim());
                err += ", expected number of color planes is 3, got " +
                    std::to_string(image.shape(2));
                throw std::runtime_error(err);
            }
            planes = 3;
            lineFeed = image.strides(0);
            pixelFeed = image.strides(1);
            planeFeed = image.strides(2);
        }
        else 
        {
            throw std::runtime_error("unsupported colorspace: " +
                std::string(colorSpace));
        }
        img = reinterpret_cast<const unsigned char*>(image.data());
        content = eng.Process(img, width, height, planes, pixelFeed,
            lineFeed, planeFeed, colorSpace);
        if (!content) 
        {
            throw std::runtime_error(
                "Failed to retrieve Shore content of image.");
        }
        return content;
    }
    else
    {
        throw std::runtime_error(
            "Image dimension is not supported. Not supported dimension is " +
            std::to_string(image.ndim()));
    }
}
/**
 * Initializes the Shore module.
 *
 */
PYBIND11_MODULE(shore, shoreModule) {

    shoreModule.doc() = "Shore", "Interface to access the Shore API.";
    shoreModule.def("CreateFaceEngine",
        &Shore::CreateFaceEngine,
        "Creates face engine",
        py::arg("timeBase") = 0,
        py::arg("updateTimeBase") = true,
        py::arg("threadCount") = 2,
        py::arg("modelType") = "Face.Front",
        py::arg("imageScale") = 1,
        py::arg("minFaceSize") = 0,
        py::arg("minFaceScore") = 0,
        py::arg("idMemoryLength") = 0,
        py::arg("idMemoryType") = "Spatial",
        py::arg("trackFaces") = true,
        py::arg("phantomTrap") = "Off",
        py::arg("searchParts") = "Off",
        py::arg("analyzeParts") = "Off",
        py::arg("analyzeDemography") = "Off",
        py::arg("analyzeExpression") = "Off",
        py::arg("analyzeValence") = "Off",
        py::arg("pointLocator") = "Off",
        py::arg("singleFaceMode") = false,
        py::arg("heartRate") = false,
        py::return_value_policy::reference
    );

    shoreModule.def("CreateEngine",
        &Shore::CreateEngine,
        "Creates a Shore engine with a Lua setup script",
        py::arg("setupScript"),
        py::arg("setupCall"),
        py::return_value_policy::reference
    );

    shoreModule.def("DeleteEngine",
        &Shore::DeleteEngine,
        "Deletes the Shore engine",
        py::arg("engine")
    );

    shoreModule.def("Version",
        &Shore::Version,
        "returns version of Shore library"
    );

    py::class_<Shore::Engine, std::unique_ptr<Shore::Engine, py::nodelete>> engine(shoreModule, "Engine");
    engine.def("Process", &EngineProcess,
        "Applies the Shore engine to the given image",
        pybind11::arg("image"),
        pybind11::arg("colorSpace") = "BGR",
        pybind11::return_value_policy::reference);

    // Bind Region class (need nodelete because of protected destructor).
    pybind11::class_<Shore::Region, std::unique_ptr<Shore::Region, pybind11::nodelete>>(shoreModule, "Region")
        .def("getLeft", &Shore::Region::GetLeft)
        .def("getTop", &Shore::Region::GetTop)
        .def("getRight", &Shore::Region::GetRight)
        .def("getBottom", &Shore::Region::GetBottom);

    // Bind Marker class (need nodelete because of protected destructor).
    pybind11::class_<Shore::Marker, std::unique_ptr<Shore::Marker, pybind11::nodelete>>(shoreModule, "Marker")
        .def("getX", &Shore::Marker::GetX)
        .def("getY", &Shore::Marker::GetY);

    // Bind Object class (need nodelete because of protected destructor).
    pybind11::class_<Shore::Object, std::unique_ptr<Shore::Object, pybind11::nodelete>>(shoreModule, "Object")
        .def("getType", &Shore::Object::GetType)
        .def("getRegion", &Shore::Object::GetRegion)
        .def("getMarkerCount", &Shore::Object::GetMarkerCount)
        .def("getMarkerKey", &Shore::Object::GetMarkerKey)
        .def("getMarker", &Shore::Object::GetMarker)
        .def("getMarkerOf", &Shore::Object::GetMarkerOf)
        .def("getAttributeCount", &Shore::Object::GetAttributeCount)
        .def("getAttributeKey", &Shore::Object::GetAttributeKey)
        .def("getAttribute", &Shore::Object::GetAttribute)
        .def("getAttributeOf", &Shore::Object::GetAttributeOf)
        .def("getRatingCount", &Shore::Object::GetRatingCount)
        .def("getRatingKey", &Shore::Object::GetRatingKey)
        .def("getRating", &Shore::Object::GetRating)
        .def("getRatingOf", &Shore::Object::GetRatingOf)
        .def("getPartCount", &Shore::Object::GetPartCount)
        .def("getPartKey", &Shore::Object::GetPartKey)
        .def("getPart", &Shore::Object::GetPart)
        .def("getPartOf", &Shore::Object::GetPartOf);

    // Bind Content class (need nodelete because of protected destructor).
    pybind11::class_<Shore::Content, std::unique_ptr<Shore::Content, pybind11::nodelete>>(shoreModule, "Content")
        .def("getObjectCount", &Shore::Content::GetObjectCount)
        .def("getObject", &Shore::Content::GetObject)
        .def("getInfoCount", &Shore::Content::GetInfoCount)
        .def("getInfoKey", &Shore::Content::GetInfoKey)
        .def("getInfo", &Shore::Content::GetInfo)
        .def("getInfoOf", &Shore::Content::GetInfoOf);
}

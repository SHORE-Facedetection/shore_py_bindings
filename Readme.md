## Summary
This package contains Python bindings for the [SHORE library](https://www.iis.fraunhofer.de/shore).
Please note that this is a supplementary addon package for the SHORE library for realtime face detection. 
The SHORE library is not included in this  project - please [contact us](mailto:facedetection@iis.fraunhofer.de) for a evaluation license. 
We do not offer any official support for the Python bindings. See the LICENSE file for details.

## Building
Please refer to the provided Dockerfile for a list of required packages. 
```
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DSHORE_SDK_PATH=${YOUR_SHORE_SDK_PATH} -DSHORE_VERSION=300 ../
cmake --build . --target install -- -j 4
```
## Usage

### Preparation
Make sure you have a Python version installed matching the provided
SHORE Python module.

For example, `shore.cpython-35m-x86_64-linux-gnu.so` is built for Python 3.5
(64 bit) on Linux, `shore.cp36-win_amd64.pyd` is built for Python 3.6 (64 bit)
on Windows.


### Linux/OSX
```
python3 -mvenv env
source env/bin/activate
pip install -r requirements.txt
```
### Windows
```
python3 -mvenv env
env\Scripts\activate.bat
pip install -r requirements.txt
```

### Pythonic API

`pyshore.py` contains an easy-to-use class-based interface to SHORE. Example usage:

```
engine = pyshore.create_face_engine()
content = engine(image, 'GRAYSCALE')
print(content.num_objects, content.num_infos)

for object in content.objects():
    print(object.type,
          object.region,
          object.num_markers, 
          object.num_attributes, 
          object.num_ratings, 
          object.num_parts)
    # `markers()` returns a dict-like object. 
    # The same is true for `attributes()`, `ratings()`, and `parts()`.
    markers = object.markers()
    print(markers['LeftEye'], markers['RightEye'])
    
    # Parts are themselves objects
    for part in object.parts().values():
        print(part.type, part.region)
```

## Sample code

The file `video.py` contains a simple application, which reads video frames
from a webcam using *OpenCV*, processes them with SHORE and shows the results
as overlayed text.
```
python video.py
```
Please refer to the SHORE-SDK documentation for details about the SHORE Engine
configuration.

The sample script `run_shore.py` reads image files from file system and process them with SHORE,and 
saves the same images with the detected faces to file system again. Additionally, the script 
demonstrates the use of the pythonic Shore API.

```
python run_shore.py -e <IMAGE_EXTENSION> -o <OUTPUT_DIR> <INPUT_IMAGE_OR_DIRECTORY>
```

### Troubleshooting

Please contact [facedetection@iis.fraunhofer.de](mailto:facedetection@iis.fraunhofer.de) to get support.

### Contributions
Please note that we only accept pull requests that are licensed under the MIT License.

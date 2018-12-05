## Summary
This package contains Python bindings for the [SHORE library](https://www.iis.fraunhofer.de/shore).
Please note that this is a supplementary addon package for the SHORE library for realtime face detection. 
The SHORE library is not included in this  project - please [contact us](mailto:facedetection@iis.fraunhofer.de) for a evaluation license. 
We do not offer any official support for the Python bindings. See the LICENSE file for details.

## Building
Please refer to the provided Dockerfile for a list of required packages. 
```
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DSHORE_SDK_PATH=${YOUR_SHORE_SDK_PATH} -DSHORE_VERSION=161 ../
cmake --build . --target install -- -j 4
```
## Usage

### Preparation
Make sure you have a Python version installed matching the provided
SHORE Python module.

For example, `shore.cpython-35m-x86_64-linux-gnu.so` is built for Python 3.5
(64 bit) on Linux, `shore.cp36-win_amd64.pyd` is built for Python 3.6 (64 bit)
on Windows.

*Note:* the Python modules built for Python 2.7 are not suffixed with the platform
information.

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

## Sample code

The file `video.py` contains a simple application, which reads video frames
from a webcam using *OpenCV*, processes them with SHORE and shows the results
as overlayed text.
```
python video.py
```
Please refer to the SHORE-SDK documentation for details about the SHORE Engine
configuration.

### Troubleshooting

#### Protected SHORE library
If you are using a protected version of the SHORE library you may get errors like the following 
if there are any licensing problems:
```
Sentinel LDK Protection System - Feature not found (32)
```

Make sure you have plugged in the provided USB key or installed the 
Sentinel Runtime package and activated the license.

Please contact [facedetection@iis.fraunhofer.de](mailto:facedetection@iis.fraunhofer.de) to get support.

### Contributions
Please note that we only accept pull requests that are licensed under the MIT License.

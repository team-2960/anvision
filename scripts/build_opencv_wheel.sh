#!/bin/sh

# Set repo variables
REPO_SRC="https://github.com/opencv/opencv-python.git"
REPO_LOCAL="./build/opencv-python"
REPO_LOCAL_DIR=$REPO_LOCAL/.git

# Ensure the repo is cloned
if [ ! -d $REPO_LOCAL_DIR ] ; then 
    git clone $REPO_SRC $REPO_LOCAL 
fi

# Set build arguments
export CMAKE_ARGS="-D ENABLE_NEON=ON -D WITH_OPENMP=ON -D WITH_OPENCL=OFF -D BUILD_TIFF=ON -D WITH_FFMPEG=ON -D WITH_TBB=ON -D BUILD_TBB=ON -D WITH_GSTREAMER=ON -D BUILD_TESTS=OFF -D WITH_EIGEN=OFF -D WITH_V4L=ON -D WITH_LIBV4L=ON -D WITH_VTK=OFF -D WITH_QT=OFF -D WITH_PROTOBUF=ON -D OPENCV_ENABLE_NONFREE=ON -D OPENCV_FORCE_LIBATOMIC_COMPILER_CHECK=1"
export ENABLE_CONTRIB=ON
export ENABLE_HEADLESS=ON

# Build wheel
cd build/opencv-python
pip wheel . --verbose
cd ../..
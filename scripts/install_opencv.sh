bash ./.venv/bin/activate

mkdir -p ./build

cd ./build

git clone https://github.com/opencv/opencv 
git clone https://github.com/opencv/opencv_contrib 

mkdir ./opencv/build
cd ./opencv/build

cmake -D CMAKE_BUILD_TYPE=Release \
      -D CMAKE_INSTALL_PREFIX=$(python -c "import sys; print(sys.prefix)") \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D PYTHON_EXECUTABLE=$(which python) \
      -D BUILD_opencv_python3=ON \
      -D BUILD_opencv_python2=OFF \
      -D ENABLE_NEON=ON \
      -D WITH_OPENMP=ON \
      -D WITH_OPENCL=OFF \
      -D BUILD_TIFF=ON \
      -D WITH_FFMPEG=ON \
      -D WITH_TBB=ON \
      -D BUILD_TBB=ON \
      -D WITH_GSTREAMER=ON \
      -D BUILD_TESTS=OFF \
      -D WITH_EIGEN=OFF \
      -D WITH_V4L=ON \
      -D WITH_LIBV4L=ON \
      -D WITH_VTK=OFF \
      -D WITH_QT=OFF \
      -D WITH_PROTOBUF=ON \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D INSTALL_C_EXAMPLES=OFF \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D OPENCV_FORCE_LIBATOMIC_COMPILER_CHECK=1 \
      -D OPENCV_GENERATE_PKGCONFIG=ON \
      -D BUILD_EXAMPLES=OFF ..

make -j2
make install

cd ../../../
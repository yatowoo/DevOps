#!/bin/bash -

DATADIR=~/GEANT4/downloads

G4_SOURCE=$(basename $(head -n1 G4DataList.txt))

SOURCE_DIR=~/GEANT4

tar xf $DATADIR/$G4_SOURCE -C $SOURCE_DIR/

SOURCE_DIR=$SOURCE_DIR/${G4_SOURCE%.tar.gz}
BUILD_DIR=$SOURCE_DIR-build
INSTALL_DIR=$SOURCE_DIR-install
mkdir -p $BUILD_DIR
cd -p $BUILD_DIR
cmake $SOURCE_DIR -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR -DGEANT4_BUILD_MULTITHREADED=OFF \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo -DGEANT4_INSTALL_DATA=OFF -DGEANT4_USE_G3TOG4=ON \
	-DGEANT4_USE_GDML=ON -DGEANT4_USE_OPENGL_X11=ON -DGEANT4_USE_QT=ON
make -j8
make install

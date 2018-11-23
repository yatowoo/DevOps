#!/bin/bash -

DATADIR=~/GEANT4/downloads
G4_SOURCE=$(basename $(head -n1 G4DataList.txt))
WORK_DIR=~/GEANT4
SOURCE_DIR=$WORK_DIR/${G4_SOURCE%.tar.gz}
BUILD_DIR=$SOURCE_DIR-build
INSTALL_DIR=$SOURCE_DIR-install

# Geant4 version info.
G4VER_MAJOR=$(echo $G4_SOURCE | cut -d'.' -f2)
G4VER_MINOR=$(echo $G4_SOURCE | cut -d'.' -f3)
let "G4VER_MINOR=$G4VER_MINOR"
G4VER_PATCH=$(echo $G4_SOURCE | cut -d'.' -f4 | cut -d'p' -f2)
let "G4VER_PATCH=$G4VER_PATCH"
G4SOURCE_VER=$G4VER_MAJOR.$G4VER_MINOR.$G4VER_PATCH 
if [ -e $INSTALL_DIR/bin/geant4.sh ];then
	G4VERION=$(bash -c cd;source $INSTALL_DIR/bin/geant4.sh;geant4-config --version)
	if [ $G4VERION = $G4SOURCE_VER ];then
		echo "[-] INFO - Geant4 latest version ($G4VERION) was installed in "$INSTALL_DIR
		exit
	else
	  echo "[-] INFO - Geant4 will be installed in"$INSTALL_DIR	
	fi
fi

if [ -e $DATADIR/$G4_SOURCE ];then
	echo "[-] INFO - Geant4 source file found : "$DATADIR/$G4_SOURCE
else
	echo "[X] ERROR - Source file not found. Please run geant4-download.sh before this."
	exit
fi

tar xvf $DATADIR/$G4_SOURCE -C $WORK_DIR/

mkdir -p $BUILD_DIR
cd $BUILD_DIR
cmake $SOURCE_DIR -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR -DGEANT4_BUILD_MULTITHREADED=OFF \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo -DGEANT4_INSTALL_DATA=OFF -DGEANT4_USE_G3TOG4=ON \
	-DGEANT4_USE_GDML=ON -DGEANT4_USE_OPENGL_X11=ON -DGEANT4_USE_QT=ON
make -j$(nproc) install

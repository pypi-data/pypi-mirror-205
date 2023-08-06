############################################################
# CMake config for the spatial_dyn library.
#
# Copyright 2018. All Rights Reserved.
#
# Created: September 16, 2018
# Authors: Toki Migimatsu
############################################################

include(CMakeFindDependencyMacro)

set(LIB_NAME spatial_dyn)
set(LIB_BINARY_DIR /Users/runner/work/spatial-dyn/spatial-dyn/build/temp.macosx-10.9-universal2-cpython-310)

if(NOT TARGET ${LIB_NAME}::${LIB_NAME})
    include("${LIB_BINARY_DIR}/${LIB_NAME}Targets.cmake")
endif()

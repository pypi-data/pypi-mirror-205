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
set(LIB_BINARY_DIR /project/build/temp.linux-x86_64-cpython-37)

if(NOT TARGET ${LIB_NAME}::${LIB_NAME})
    include("${LIB_BINARY_DIR}/${LIB_NAME}Targets.cmake")
endif()

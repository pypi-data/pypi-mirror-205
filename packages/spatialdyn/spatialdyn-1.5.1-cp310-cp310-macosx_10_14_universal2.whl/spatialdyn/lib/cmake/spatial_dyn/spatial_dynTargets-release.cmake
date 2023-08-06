#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "spatial_dyn::tinyxml2" for configuration "Release"
set_property(TARGET spatial_dyn::tinyxml2 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(spatial_dyn::tinyxml2 PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libtinyxml2.8.0.0.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libtinyxml2.8.dylib"
  )

list(APPEND _cmake_import_check_targets spatial_dyn::tinyxml2 )
list(APPEND _cmake_import_check_files_for_spatial_dyn::tinyxml2 "${_IMPORT_PREFIX}/lib/libtinyxml2.8.0.0.dylib" )

# Import target "spatial_dyn::spatial_dyn" for configuration "Release"
set_property(TARGET spatial_dyn::spatial_dyn APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(spatial_dyn::spatial_dyn PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libspatial_dyn.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libspatial_dyn.dylib"
  )

list(APPEND _cmake_import_check_targets spatial_dyn::spatial_dyn )
list(APPEND _cmake_import_check_files_for_spatial_dyn::spatial_dyn "${_IMPORT_PREFIX}/lib/libspatial_dyn.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

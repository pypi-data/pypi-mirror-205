#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "spatial_dyn::tinyxml2" for configuration "Release"
set_property(TARGET spatial_dyn::tinyxml2 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(spatial_dyn::tinyxml2 PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libtinyxml2.so.8.0.0"
  IMPORTED_SONAME_RELEASE "libtinyxml2.so.8"
  )

list(APPEND _IMPORT_CHECK_TARGETS spatial_dyn::tinyxml2 )
list(APPEND _IMPORT_CHECK_FILES_FOR_spatial_dyn::tinyxml2 "${_IMPORT_PREFIX}/lib64/libtinyxml2.so.8.0.0" )

# Import target "spatial_dyn::spatial_dyn" for configuration "Release"
set_property(TARGET spatial_dyn::spatial_dyn APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(spatial_dyn::spatial_dyn PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libspatial_dyn.so"
  IMPORTED_SONAME_RELEASE "libspatial_dyn.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS spatial_dyn::spatial_dyn )
list(APPEND _IMPORT_CHECK_FILES_FOR_spatial_dyn::spatial_dyn "${_IMPORT_PREFIX}/lib64/libspatial_dyn.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

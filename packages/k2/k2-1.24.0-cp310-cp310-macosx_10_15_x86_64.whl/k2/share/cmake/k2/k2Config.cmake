# Findk2
# ------
#
# Finds the k2 library
#
# This will define the following variables:
#
#   K2_FOUND        -- True if the system has the k2 library
#   K2_INCLUDE_DIRS -- The include directories for k2
#   K2_LIBRARIES    -- Libraries to link against
#   K2_CXX_FLAGS -- Additional (required) compiler flags
#   K2_CUDA_FLAGS -- CUDA flags used to build k2
#   K2_WITH_CUDA -- true if k2 was compiled with CUDA; false if k2 was compiled
#                   with CPU.
#   K2_CUDA_VERSION -- If set, it is the CUDA version that was used to compile k2
#   K2_TORCH_VERSION_MAJOR  -- The major version of PyTorch used to compile k2
#   K2_TORCH_VERSION_MINOR  -- The minor version of PyTorch used to compile k2
#   K2_VERSION -- The version of k2
#   K2_GIT_SHA1 -- git commit ID of this version
#   K2_GIT_DATE -- commit date of this version
#
# and the following imported targets:
#
#   k2_torch_api, k2_log, k2context, k2fsa

# This file is modified from pytorch/cmake/TorchConfig.cmake.in

set(K2_CXX_FLAGS "  -Wno-unused-variable  -Wno-strict-overflow ")
set(K2_CUDA_FLAGS "")
set(K2_WITH_CUDA OFF)
set(K2_CUDA_VERSION )
set(K2_TORCH_VERSION_MAJOR 1)
set(K2_TORCH_VERSION_MINOR 13)
set(K2_VERSION 1.24.0)
set(K2_GIT_SHA1 13675b4b5e299b6946941f8ca80698a485d2cf50)
set(K2_GIT_DATE "Thu Apr 27 04:12:03 2023")

if(DEFINED ENV{K2_INSTALL_PREFIX})
  set(K2_INSTALL_PREFIX $ENV{K2_INSTALL_PREFIX})
else()
  # Assume we are in <install-prefix>/share/cmake/k2/k2Config.cmake
  get_filename_component(CMAKE_CURRENT_LIST_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
  get_filename_component(K2_INSTALL_PREFIX "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)
endif()

set(K2_INCLUDE_DIRS ${K2_INSTALL_PREFIX}/include)

set(K2_LIBRARIES k2_torch_api k2_torch k2_log k2context k2fsa)

foreach(lib IN LISTS K2_LIBRARIES)
  find_library(location_${lib} ${lib}
    PATHS
    "${K2_INSTALL_PREFIX}/lib"
    "${K2_INSTALL_PREFIX}/lib64"
  )

  if(NOT MSVC)
    add_library(${lib} SHARED IMPORTED)
  else()
    add_library(${lib} STATIC IMPORTED)
  endif()

  set_target_properties(${lib} PROPERTIES
      INTERFACE_INCLUDE_DIRECTORIES "${K2_INCLUDE_DIRS}"
      IMPORTED_LOCATION "${location_${lib}}"
      CXX_STANDARD 14
  )

  set_property(TARGET ${lib} PROPERTY INTERFACE_COMPILE_OPTIONS   -Wno-unused-variable  -Wno-strict-overflow  -DHAVE_K2_TORCH_API_H=1)
endforeach()

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(k2 DEFAULT_MSG
  location_k2_torch_api
  location_k2_torch
  location_k2_log
  location_k2context
  location_k2fsa
)

#
# (C) Copyright 2011-2020 Johns Hopkins University (JHU), All Rights Reserved.
#
# --- begin cisst license - do not edit ---
#
# This software is provided "as is" under an open source license, with
# no warranty.  The complete license can be found in license.txt and
# http://www.cisst.org/cisst/license.txt.
#
# --- end cisst license ---

project (Amp1394Lib)

set (HEADERS
     BoardIO.h
     AmpIO.h
     Amp1394Time.h
     Amp1394BSwap.h
     BasePort.h
     EthBasePort.h
     EthUdpPort.h
     PortFactory.h)

set (SOURCE_FILES
     code/AmpIO.cpp
     code/Amp1394Time.cpp
     code/BasePort.cpp
     code/EthBasePort.cpp
     code/EthUdpPort.cpp
     code/PortFactory.cpp)


if (Amp1394_HAS_RAW1394)
  set (HEADERS ${HEADERS} FirewirePort.h)
  set (SOURCE_FILES ${SOURCE_FILES} code/FirewirePort.cpp)
endif (Amp1394_HAS_RAW1394)

if (Amp1394_HAS_PCAP)
  set (HEADERS ${HEADERS} EthRawPort.h)
  set (SOURCE_FILES ${SOURCE_FILES} code/EthRawPort.cpp)
endif (Amp1394_HAS_PCAP)

include_directories(${Amp1394_INCLUDE_DIR} ${Amp1394_EXTRA_INCLUDE_DIR})
link_directories(${Amp1394_LIBRARY_DIR} ${Amp1394_EXTRA_LIBRARY_DIR})

# Create Amp1394 library
add_library(Amp1394 STATIC
            ${HEADERS} ${SOURCE_FILES})

target_link_libraries(Amp1394 ${Amp1394_EXTRA_LIBRARIES})


option (Amp1394_BUILD_SWIG  "Build Amp1394 with Python wrapper" OFF)
if (Amp1394_BUILD_SWIG)
  find_package(SWIG REQUIRED)
  include(${SWIG_USE_FILE})

  find_package(PythonLibs)
  include_directories(${PYTHON_INCLUDE_PATH})

  find_package(PythonInterp)
  if (PYTHON_EXECUTABLE)
    execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import numpy; print(numpy.get_include())"
                    ERROR_QUIET
                    OUTPUT_VARIABLE Amp1394_NUMPY_INCLUDE_DIR
                    OUTPUT_STRIP_TRAILING_WHITESPACE)
    include_directories(${Amp1394_NUMPY_INCLUDE_DIR} "${Amp1394_BINARY_DIR}/Amp1394")
  endif()

  set_source_files_properties(Amp1394.i PROPERTIES CPLUSPLUS ON)
  swig_add_module(Amp1394Python python Amp1394.i ${HEADERS} ${SOURCE_FILES})
  swig_link_libraries(Amp1394Python ${PYTHON_LIBRARIES} ${Amp1394_EXTRA_LIBRARIES})

  if (WIN32)
    set_target_properties (_Amp1394Python PROPERTIES SUFFIX .pyd)
    set_target_properties (_Amp1394Python PROPERTIES DEBUG_POSTFIX "_d")
  endif (WIN32)

  # post build command
  add_custom_command(TARGET _Amp1394Python POST_BUILD
                     COMMAND ${CMAKE_COMMAND}
                     ARGS -E copy_if_different
                             ${CMAKE_CURRENT_BINARY_DIR}/Amp1394Python.py
                             ${LIBRARY_OUTPUT_PATH}/${CMAKE_CFG_INTDIR}/
                     COMMAND ${CMAKE_COMMAND}
                     ARGS -E copy_if_different
                             ${Amp1394_SOURCE_DIR}/python/test_eth1394.py
                             ${LIBRARY_OUTPUT_PATH}/${CMAKE_CFG_INTDIR}/
                     COMMAND ${CMAKE_COMMAND}
                     ARGS -E copy_if_different
                             ${Amp1394_SOURCE_DIR}/python/test_amp1394.py
                             ${LIBRARY_OUTPUT_PATH}/${CMAKE_CFG_INTDIR}/
                     COMMENT "Copying Python files to ${LIBRARY_OUTPUT_PATH}" )
endif (Amp1394_BUILD_SWIG)


# revision file
configure_file ("${CMAKE_CURRENT_SOURCE_DIR}/AmpIORevision.h.in"
                "${Amp1394_BINARY_DIR}/Amp1394/AmpIORevision.h")

# Install files
install (TARGETS Amp1394 COMPONENT Amp1394
         RUNTIME DESTINATION bin
         LIBRARY DESTINATION lib
         ARCHIVE DESTINATION lib)

install (FILES ${HEADERS}
         DESTINATION include/Amp1394
         COMPONENT Amp1394-dev)

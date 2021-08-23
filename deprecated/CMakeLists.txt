cmake_minimum_required(VERSION 3.13.4)
project(stockbot)

# Configure compiler properties
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "-g -Wall -Werror -pthread")

# Include the header files located in include
include_directories(include)

# Include the .cpp files using wildcard additions
file(GLOB SOURCES "src/*.cpp")

# Set stockbot to be built from source files
add_executable(stockbot ${SOURCES})

# Link the libraries to the executable
target_link_libraries(stockbot jsoncpp curl)
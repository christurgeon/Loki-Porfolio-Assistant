cmake_minimum_required(VERSION 3.13.4)
project(stockbot)

# Configure compiler properties
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "-g -Wall -Werror")

# Include the header files located in include
include_directories(include)

# Set the path to the folder including json and curl
link_directories(/usr/lib/x86_64-linux-gnu)

# Include the .cpp files using wildcard additions
file(GLOB SOURCES "src/*.cpp")

# Set stockbot to be built from source files
add_executable(stockbot ${SOURCES})

# Link the libraries to the executable
target_link_libraries(stockbot jsoncpp curl)
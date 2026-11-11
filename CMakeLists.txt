cmake_minimum_required(VERSION 3.16)
project(aed_dial LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Los ejecutables quedan directamente en build/ (tambien con Visual Studio).
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
foreach(cfg IN ITEMS Debug Release RelWithDebInfo MinSizeRel)
    string(TOUPPER ${cfg} CFG)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_${CFG} ${CMAKE_BINARY_DIR})
endforeach()

add_library(dial_core
    src/graph.cpp
    src/bucket_queue.cpp
    src/dial.cpp
    src/tracer.cpp)
target_include_directories(dial_core PUBLIC src)

add_executable(dial src/main.cpp)
target_link_libraries(dial PRIVATE dial_core)

enable_testing()
add_executable(test_dial tests/test_dial.cpp)
target_link_libraries(test_dial PRIVATE dial_core)
add_test(NAME test_dial COMMAND test_dial)

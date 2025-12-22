cmake_minimum_required(VERSION 3.16)
project(pwndoc-mcp-server VERSION 1.0.3 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Define version info
add_compile_definitions(
    PWNDOC_VERSION="${PROJECT_VERSION}"
    PWNDOC_AUTHOR="Walid Faour"
    PWNDOC_EMAIL="security@walidfaour.com"
)

# Windows: Prevent min/max macros from windows.h
if(WIN32)
    add_compile_definitions(NOMINMAX)
endif()

option(BUILD_STATIC "Build static binary" OFF)

# Find dependencies
find_package(CURL REQUIRED)
find_package(nlohmann_json 3.9 QUIET)

# If nlohmann_json not found, fetch it
if(NOT nlohmann_json_FOUND)
    include(FetchContent)
    FetchContent_Declare(
        json
        URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz
    )
    FetchContent_MakeAvailable(json)
endif()

# Source files
set(SOURCES
    src/main.cpp
    src/server.cpp
    src/client.cpp
    src/config.cpp
    src/tools.cpp
)

# Create executable
add_executable(pwndoc-mcp-server ${SOURCES})

# Include directories
target_include_directories(pwndoc-mcp-server PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Link libraries
target_link_libraries(pwndoc-mcp-server PRIVATE
    CURL::libcurl
    nlohmann_json::nlohmann_json
)

# Static linking
if(BUILD_STATIC)
    if(UNIX AND NOT APPLE)
        # Linux: static libgcc and libstdc++
        target_link_options(pwndoc-mcp-server PRIVATE -static-libgcc -static-libstdc++)
    elseif(WIN32)
        # Windows: link runtime statically
        set_property(TARGET pwndoc-mcp-server PROPERTY MSVC_RUNTIME_LIBRARY "MultiThreaded")
        # Use static CURL on Windows
        set(CURL_STATICLIB ON)
    endif()
endif()

# Install
install(TARGETS pwndoc-mcp-server DESTINATION bin)

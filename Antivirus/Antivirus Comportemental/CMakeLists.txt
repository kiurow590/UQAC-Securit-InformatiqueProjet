cmake_minimum_required(VERSION 3.30)
project(PIDChecker C)

set(CMAKE_C_STANDARD 11)

add_executable(PIDChecker main.c)
add_executable(PIDCheckerTest myDirectory/main.c)

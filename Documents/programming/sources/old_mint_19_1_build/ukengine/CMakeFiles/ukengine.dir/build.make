# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/htran/sources/ibus-unikey

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/htran/sources/ibus-unikey/build

# Include any dependencies generated for this target.
include ukengine/CMakeFiles/ukengine.dir/depend.make

# Include the progress variables for this target.
include ukengine/CMakeFiles/ukengine.dir/progress.make

# Include the compile flags for this target's objects.
include ukengine/CMakeFiles/ukengine.dir/flags.make

ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o: ukengine/CMakeFiles/ukengine.dir/flags.make
ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o: ../ukengine/byteio.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ukengine.dir/byteio.cpp.o -c /home/htran/sources/ibus-unikey/ukengine/byteio.cpp

ukengine/CMakeFiles/ukengine.dir/byteio.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ukengine.dir/byteio.cpp.i"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/htran/sources/ibus-unikey/ukengine/byteio.cpp > CMakeFiles/ukengine.dir/byteio.cpp.i

ukengine/CMakeFiles/ukengine.dir/byteio.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ukengine.dir/byteio.cpp.s"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/htran/sources/ibus-unikey/ukengine/byteio.cpp -o CMakeFiles/ukengine.dir/byteio.cpp.s

ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o.requires:

.PHONY : ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o.requires

ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o.provides: ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o.requires
	$(MAKE) -f ukengine/CMakeFiles/ukengine.dir/build.make ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o.provides.build
.PHONY : ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o.provides

ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o.provides.build: ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o


ukengine/CMakeFiles/ukengine.dir/charset.cpp.o: ukengine/CMakeFiles/ukengine.dir/flags.make
ukengine/CMakeFiles/ukengine.dir/charset.cpp.o: ../ukengine/charset.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object ukengine/CMakeFiles/ukengine.dir/charset.cpp.o"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ukengine.dir/charset.cpp.o -c /home/htran/sources/ibus-unikey/ukengine/charset.cpp

ukengine/CMakeFiles/ukengine.dir/charset.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ukengine.dir/charset.cpp.i"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/htran/sources/ibus-unikey/ukengine/charset.cpp > CMakeFiles/ukengine.dir/charset.cpp.i

ukengine/CMakeFiles/ukengine.dir/charset.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ukengine.dir/charset.cpp.s"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/htran/sources/ibus-unikey/ukengine/charset.cpp -o CMakeFiles/ukengine.dir/charset.cpp.s

ukengine/CMakeFiles/ukengine.dir/charset.cpp.o.requires:

.PHONY : ukengine/CMakeFiles/ukengine.dir/charset.cpp.o.requires

ukengine/CMakeFiles/ukengine.dir/charset.cpp.o.provides: ukengine/CMakeFiles/ukengine.dir/charset.cpp.o.requires
	$(MAKE) -f ukengine/CMakeFiles/ukengine.dir/build.make ukengine/CMakeFiles/ukengine.dir/charset.cpp.o.provides.build
.PHONY : ukengine/CMakeFiles/ukengine.dir/charset.cpp.o.provides

ukengine/CMakeFiles/ukengine.dir/charset.cpp.o.provides.build: ukengine/CMakeFiles/ukengine.dir/charset.cpp.o


ukengine/CMakeFiles/ukengine.dir/convert.cpp.o: ukengine/CMakeFiles/ukengine.dir/flags.make
ukengine/CMakeFiles/ukengine.dir/convert.cpp.o: ../ukengine/convert.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object ukengine/CMakeFiles/ukengine.dir/convert.cpp.o"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ukengine.dir/convert.cpp.o -c /home/htran/sources/ibus-unikey/ukengine/convert.cpp

ukengine/CMakeFiles/ukengine.dir/convert.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ukengine.dir/convert.cpp.i"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/htran/sources/ibus-unikey/ukengine/convert.cpp > CMakeFiles/ukengine.dir/convert.cpp.i

ukengine/CMakeFiles/ukengine.dir/convert.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ukengine.dir/convert.cpp.s"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/htran/sources/ibus-unikey/ukengine/convert.cpp -o CMakeFiles/ukengine.dir/convert.cpp.s

ukengine/CMakeFiles/ukengine.dir/convert.cpp.o.requires:

.PHONY : ukengine/CMakeFiles/ukengine.dir/convert.cpp.o.requires

ukengine/CMakeFiles/ukengine.dir/convert.cpp.o.provides: ukengine/CMakeFiles/ukengine.dir/convert.cpp.o.requires
	$(MAKE) -f ukengine/CMakeFiles/ukengine.dir/build.make ukengine/CMakeFiles/ukengine.dir/convert.cpp.o.provides.build
.PHONY : ukengine/CMakeFiles/ukengine.dir/convert.cpp.o.provides

ukengine/CMakeFiles/ukengine.dir/convert.cpp.o.provides.build: ukengine/CMakeFiles/ukengine.dir/convert.cpp.o


ukengine/CMakeFiles/ukengine.dir/data.cpp.o: ukengine/CMakeFiles/ukengine.dir/flags.make
ukengine/CMakeFiles/ukengine.dir/data.cpp.o: ../ukengine/data.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object ukengine/CMakeFiles/ukengine.dir/data.cpp.o"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ukengine.dir/data.cpp.o -c /home/htran/sources/ibus-unikey/ukengine/data.cpp

ukengine/CMakeFiles/ukengine.dir/data.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ukengine.dir/data.cpp.i"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/htran/sources/ibus-unikey/ukengine/data.cpp > CMakeFiles/ukengine.dir/data.cpp.i

ukengine/CMakeFiles/ukengine.dir/data.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ukengine.dir/data.cpp.s"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/htran/sources/ibus-unikey/ukengine/data.cpp -o CMakeFiles/ukengine.dir/data.cpp.s

ukengine/CMakeFiles/ukengine.dir/data.cpp.o.requires:

.PHONY : ukengine/CMakeFiles/ukengine.dir/data.cpp.o.requires

ukengine/CMakeFiles/ukengine.dir/data.cpp.o.provides: ukengine/CMakeFiles/ukengine.dir/data.cpp.o.requires
	$(MAKE) -f ukengine/CMakeFiles/ukengine.dir/build.make ukengine/CMakeFiles/ukengine.dir/data.cpp.o.provides.build
.PHONY : ukengine/CMakeFiles/ukengine.dir/data.cpp.o.provides

ukengine/CMakeFiles/ukengine.dir/data.cpp.o.provides.build: ukengine/CMakeFiles/ukengine.dir/data.cpp.o


ukengine/CMakeFiles/ukengine.dir/error.cpp.o: ukengine/CMakeFiles/ukengine.dir/flags.make
ukengine/CMakeFiles/ukengine.dir/error.cpp.o: ../ukengine/error.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building CXX object ukengine/CMakeFiles/ukengine.dir/error.cpp.o"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ukengine.dir/error.cpp.o -c /home/htran/sources/ibus-unikey/ukengine/error.cpp

ukengine/CMakeFiles/ukengine.dir/error.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ukengine.dir/error.cpp.i"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/htran/sources/ibus-unikey/ukengine/error.cpp > CMakeFiles/ukengine.dir/error.cpp.i

ukengine/CMakeFiles/ukengine.dir/error.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ukengine.dir/error.cpp.s"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/htran/sources/ibus-unikey/ukengine/error.cpp -o CMakeFiles/ukengine.dir/error.cpp.s

ukengine/CMakeFiles/ukengine.dir/error.cpp.o.requires:

.PHONY : ukengine/CMakeFiles/ukengine.dir/error.cpp.o.requires

ukengine/CMakeFiles/ukengine.dir/error.cpp.o.provides: ukengine/CMakeFiles/ukengine.dir/error.cpp.o.requires
	$(MAKE) -f ukengine/CMakeFiles/ukengine.dir/build.make ukengine/CMakeFiles/ukengine.dir/error.cpp.o.provides.build
.PHONY : ukengine/CMakeFiles/ukengine.dir/error.cpp.o.provides

ukengine/CMakeFiles/ukengine.dir/error.cpp.o.provides.build: ukengine/CMakeFiles/ukengine.dir/error.cpp.o


ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o: ukengine/CMakeFiles/ukengine.dir/flags.make
ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o: ../ukengine/inputproc.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building CXX object ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ukengine.dir/inputproc.cpp.o -c /home/htran/sources/ibus-unikey/ukengine/inputproc.cpp

ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ukengine.dir/inputproc.cpp.i"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/htran/sources/ibus-unikey/ukengine/inputproc.cpp > CMakeFiles/ukengine.dir/inputproc.cpp.i

ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ukengine.dir/inputproc.cpp.s"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/htran/sources/ibus-unikey/ukengine/inputproc.cpp -o CMakeFiles/ukengine.dir/inputproc.cpp.s

ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o.requires:

.PHONY : ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o.requires

ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o.provides: ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o.requires
	$(MAKE) -f ukengine/CMakeFiles/ukengine.dir/build.make ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o.provides.build
.PHONY : ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o.provides

ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o.provides.build: ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o


ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o: ukengine/CMakeFiles/ukengine.dir/flags.make
ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o: ../ukengine/mactab.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building CXX object ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ukengine.dir/mactab.cpp.o -c /home/htran/sources/ibus-unikey/ukengine/mactab.cpp

ukengine/CMakeFiles/ukengine.dir/mactab.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ukengine.dir/mactab.cpp.i"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/htran/sources/ibus-unikey/ukengine/mactab.cpp > CMakeFiles/ukengine.dir/mactab.cpp.i

ukengine/CMakeFiles/ukengine.dir/mactab.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ukengine.dir/mactab.cpp.s"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/htran/sources/ibus-unikey/ukengine/mactab.cpp -o CMakeFiles/ukengine.dir/mactab.cpp.s

ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o.requires:

.PHONY : ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o.requires

ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o.provides: ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o.requires
	$(MAKE) -f ukengine/CMakeFiles/ukengine.dir/build.make ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o.provides.build
.PHONY : ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o.provides

ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o.provides.build: ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o


ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o: ukengine/CMakeFiles/ukengine.dir/flags.make
ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o: ../ukengine/pattern.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building CXX object ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ukengine.dir/pattern.cpp.o -c /home/htran/sources/ibus-unikey/ukengine/pattern.cpp

ukengine/CMakeFiles/ukengine.dir/pattern.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ukengine.dir/pattern.cpp.i"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/htran/sources/ibus-unikey/ukengine/pattern.cpp > CMakeFiles/ukengine.dir/pattern.cpp.i

ukengine/CMakeFiles/ukengine.dir/pattern.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ukengine.dir/pattern.cpp.s"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/htran/sources/ibus-unikey/ukengine/pattern.cpp -o CMakeFiles/ukengine.dir/pattern.cpp.s

ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o.requires:

.PHONY : ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o.requires

ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o.provides: ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o.requires
	$(MAKE) -f ukengine/CMakeFiles/ukengine.dir/build.make ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o.provides.build
.PHONY : ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o.provides

ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o.provides.build: ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o


ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o: ukengine/CMakeFiles/ukengine.dir/flags.make
ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o: ../ukengine/ukengine.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Building CXX object ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ukengine.dir/ukengine.cpp.o -c /home/htran/sources/ibus-unikey/ukengine/ukengine.cpp

ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ukengine.dir/ukengine.cpp.i"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/htran/sources/ibus-unikey/ukengine/ukengine.cpp > CMakeFiles/ukengine.dir/ukengine.cpp.i

ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ukengine.dir/ukengine.cpp.s"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/htran/sources/ibus-unikey/ukengine/ukengine.cpp -o CMakeFiles/ukengine.dir/ukengine.cpp.s

ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o.requires:

.PHONY : ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o.requires

ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o.provides: ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o.requires
	$(MAKE) -f ukengine/CMakeFiles/ukengine.dir/build.make ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o.provides.build
.PHONY : ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o.provides

ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o.provides.build: ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o


ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o: ukengine/CMakeFiles/ukengine.dir/flags.make
ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o: ../ukengine/usrkeymap.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_10) "Building CXX object ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ukengine.dir/usrkeymap.cpp.o -c /home/htran/sources/ibus-unikey/ukengine/usrkeymap.cpp

ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ukengine.dir/usrkeymap.cpp.i"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/htran/sources/ibus-unikey/ukengine/usrkeymap.cpp > CMakeFiles/ukengine.dir/usrkeymap.cpp.i

ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ukengine.dir/usrkeymap.cpp.s"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/htran/sources/ibus-unikey/ukengine/usrkeymap.cpp -o CMakeFiles/ukengine.dir/usrkeymap.cpp.s

ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o.requires:

.PHONY : ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o.requires

ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o.provides: ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o.requires
	$(MAKE) -f ukengine/CMakeFiles/ukengine.dir/build.make ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o.provides.build
.PHONY : ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o.provides

ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o.provides.build: ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o


ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o: ukengine/CMakeFiles/ukengine.dir/flags.make
ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o: ../ukengine/unikey.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_11) "Building CXX object ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ukengine.dir/unikey.cpp.o -c /home/htran/sources/ibus-unikey/ukengine/unikey.cpp

ukengine/CMakeFiles/ukengine.dir/unikey.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ukengine.dir/unikey.cpp.i"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/htran/sources/ibus-unikey/ukengine/unikey.cpp > CMakeFiles/ukengine.dir/unikey.cpp.i

ukengine/CMakeFiles/ukengine.dir/unikey.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ukengine.dir/unikey.cpp.s"
	cd /home/htran/sources/ibus-unikey/build/ukengine && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/htran/sources/ibus-unikey/ukengine/unikey.cpp -o CMakeFiles/ukengine.dir/unikey.cpp.s

ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o.requires:

.PHONY : ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o.requires

ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o.provides: ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o.requires
	$(MAKE) -f ukengine/CMakeFiles/ukengine.dir/build.make ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o.provides.build
.PHONY : ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o.provides

ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o.provides.build: ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o


# Object files for target ukengine
ukengine_OBJECTS = \
"CMakeFiles/ukengine.dir/byteio.cpp.o" \
"CMakeFiles/ukengine.dir/charset.cpp.o" \
"CMakeFiles/ukengine.dir/convert.cpp.o" \
"CMakeFiles/ukengine.dir/data.cpp.o" \
"CMakeFiles/ukengine.dir/error.cpp.o" \
"CMakeFiles/ukengine.dir/inputproc.cpp.o" \
"CMakeFiles/ukengine.dir/mactab.cpp.o" \
"CMakeFiles/ukengine.dir/pattern.cpp.o" \
"CMakeFiles/ukengine.dir/ukengine.cpp.o" \
"CMakeFiles/ukengine.dir/usrkeymap.cpp.o" \
"CMakeFiles/ukengine.dir/unikey.cpp.o"

# External object files for target ukengine
ukengine_EXTERNAL_OBJECTS =

ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/charset.cpp.o
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/convert.cpp.o
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/data.cpp.o
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/error.cpp.o
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/build.make
ukengine/libukengine.a: ukengine/CMakeFiles/ukengine.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/htran/sources/ibus-unikey/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_12) "Linking CXX static library libukengine.a"
	cd /home/htran/sources/ibus-unikey/build/ukengine && $(CMAKE_COMMAND) -P CMakeFiles/ukengine.dir/cmake_clean_target.cmake
	cd /home/htran/sources/ibus-unikey/build/ukengine && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ukengine.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
ukengine/CMakeFiles/ukengine.dir/build: ukengine/libukengine.a

.PHONY : ukengine/CMakeFiles/ukengine.dir/build

ukengine/CMakeFiles/ukengine.dir/requires: ukengine/CMakeFiles/ukengine.dir/byteio.cpp.o.requires
ukengine/CMakeFiles/ukengine.dir/requires: ukengine/CMakeFiles/ukengine.dir/charset.cpp.o.requires
ukengine/CMakeFiles/ukengine.dir/requires: ukengine/CMakeFiles/ukengine.dir/convert.cpp.o.requires
ukengine/CMakeFiles/ukengine.dir/requires: ukengine/CMakeFiles/ukengine.dir/data.cpp.o.requires
ukengine/CMakeFiles/ukengine.dir/requires: ukengine/CMakeFiles/ukengine.dir/error.cpp.o.requires
ukengine/CMakeFiles/ukengine.dir/requires: ukengine/CMakeFiles/ukengine.dir/inputproc.cpp.o.requires
ukengine/CMakeFiles/ukengine.dir/requires: ukengine/CMakeFiles/ukengine.dir/mactab.cpp.o.requires
ukengine/CMakeFiles/ukengine.dir/requires: ukengine/CMakeFiles/ukengine.dir/pattern.cpp.o.requires
ukengine/CMakeFiles/ukengine.dir/requires: ukengine/CMakeFiles/ukengine.dir/ukengine.cpp.o.requires
ukengine/CMakeFiles/ukengine.dir/requires: ukengine/CMakeFiles/ukengine.dir/usrkeymap.cpp.o.requires
ukengine/CMakeFiles/ukengine.dir/requires: ukengine/CMakeFiles/ukengine.dir/unikey.cpp.o.requires

.PHONY : ukengine/CMakeFiles/ukengine.dir/requires

ukengine/CMakeFiles/ukengine.dir/clean:
	cd /home/htran/sources/ibus-unikey/build/ukengine && $(CMAKE_COMMAND) -P CMakeFiles/ukengine.dir/cmake_clean.cmake
.PHONY : ukengine/CMakeFiles/ukengine.dir/clean

ukengine/CMakeFiles/ukengine.dir/depend:
	cd /home/htran/sources/ibus-unikey/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/htran/sources/ibus-unikey /home/htran/sources/ibus-unikey/ukengine /home/htran/sources/ibus-unikey/build /home/htran/sources/ibus-unikey/build/ukengine /home/htran/sources/ibus-unikey/build/ukengine/CMakeFiles/ukengine.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : ukengine/CMakeFiles/ukengine.dir/depend


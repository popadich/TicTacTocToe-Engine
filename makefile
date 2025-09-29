# Compiler and flags
CC = gcc
CFLAGS = -g -O2 -Wall -c
LDFLAGS =
LIBS =

# Platform-specific settings for randomization
# Default: BSD systems (macOS, FreeBSD, etc.) use built-in arc4random
# Linux with libbsd: make linux-bsd (requires libbsd-dev package)
# Linux standard: make linux (uses rand())
# Windows/other: make standard (uses rand())
# Note: linux-bsd includes <bsd/stdlib.h> for arc4random declarations

# Source directory
SRC_DIR = TTTTengine

# Source files
SOURCES = $(SRC_DIR)/main.c $(SRC_DIR)/TTTT.c $(SRC_DIR)/TTTTapi.c

# Object files
OBJECTS = $(SOURCES:.c=.o)

# Executable name
EXECUTABLE = tttt

# Default target
all: $(EXECUTABLE)

# Linking rule
$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@ $(LIBS)

# Compilation rule
.c.o:
	$(CC) $(CFLAGS) $< -o $@

# Clean rule
clean:
	rm -f $(OBJECTS) $(EXECUTABLE)

# Platform-specific targets
linux-bsd: CFLAGS += -DHAVE_ARC4RANDOM
linux-bsd: LIBS += -lbsd
linux-bsd: all

linux: all

standard: all

# Testing targets
test: all
	python3 functional.py

integration-test: all
	python3 integration_test_suite.py

quick-test: all
	./quick_integration_test.sh

# Phony targets
.PHONY: all clean install linux-bsd linux standard test integration-test quick-test

# Install rule
install: all
	install -d -m 755 $(DESTDIR)/usr/local/bin
	install -m 755 $(EXECUTABLE) $(DESTDIR)/usr/local/bin
	install -d -m 755 $(DESTDIR)/usr/local/share/man/man1
	install -m 644 tttt.1 $(DESTDIR)/usr/local/share/man/man1
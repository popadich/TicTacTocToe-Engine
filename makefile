# Compiler and flags
CC = gcc
CFLAGS = -g -O2 -Wall -c
LDFLAGS =
LIBS =

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

# Phony targets
.PHONY: all clean install

# Install rule
install: all
	install -d -m 755 $(DESTDIR)/usr/local/bin
	install -m 755 $(EXECUTABLE) $(DESTDIR)/usr/local/bin
	install -d -m 755 $(DESTDIR)/usr/local/share/man/man1
	install -m 644 tttt.1 $(DESTDIR)/usr/local/share/man/man1
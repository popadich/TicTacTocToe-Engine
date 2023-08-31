CC      =  gcc
CFLAGS  =  -c -Wall 
LDFLAGS = 
LIBS = 
SOURCES =  main.c TTTT.c TTTTapi.c
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=tttt

all: $(SOURCES) $(EXECUTABLE)
	
$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@


clean:
	rm -rf *o tttt


relink:
	@echo "relinking ..."
	@$(CC)  $(CFLAGS)  -o $(EXECUTABLE)  $(OBJECTS)  $(LIBS)

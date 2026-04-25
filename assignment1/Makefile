CXX = g++
CXXFLAGS = -Wall -g -std=c++17

SRC_DIR = src
OBJ_DIR = build/obj
BIN_DIR = bin

PROGRAMS = quick insert merge bubble heap select tournament shaker comb intro library tim
TARGETS = $(addprefix $(BIN_DIR)/,$(PROGRAMS)) $(BIN_DIR)/monitor

all: $(TARGETS)

.SECONDARY: $(addprefix $(OBJ_DIR)/,$(addsuffix .o,$(PROGRAMS))) $(OBJ_DIR)/sort.o

$(BIN_DIR) $(OBJ_DIR):
	mkdir -p $@

$(BIN_DIR)/%: $(OBJ_DIR)/%.o $(OBJ_DIR)/sort.o | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $^ -o $@

$(BIN_DIR)/monitor: $(SRC_DIR)/monitor.cc | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $< -o $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cc $(SRC_DIR)/sort.h | $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf build bin

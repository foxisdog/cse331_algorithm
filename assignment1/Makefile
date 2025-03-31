CXX = g++
CXXFLAGS = -Wall -g
TARGETS = quick insert merge bubble heap select	tournament shaker comb intro library

all: $(TARGETS)

# 각 정렬 프로그램 빌드 규칙
quick: quick.o sort.o
	$(CXX) $(CXXFLAGS) $^ -o $@

insert: insert.o sort.o
	$(CXX) $(CXXFLAGS) $^ -o $@

merge: merge.o sort.o
	$(CXX) $(CXXFLAGS) $^ -o $@

bubble: bubble.o sort.o
	$(CXX) $(CXXFLAGS) $^ -o $@

heap: heap.o sort.o
	$(CXX) $(CXXFLAGS) $^ -o $@

select: select.o sort.o
	$(CXX) $(CXXFLAGS) $^ -o $@

tournament: tournament.o sort.o
	$(CXX) $(CXXFLAGS) $^ -o $@

shaker: shaker.o sort.o
	$(CXX) $(CXXFLAGS) $^ -o $@

comb: comb.o sort.o
	$(CXX) $(CXXFLAGS) $^ -o $@

intro: intro.o sort.o
	$(CXX) $(CXXFLAGS) $^ -o $@

library: library.o sort.o
	$(CXX) $(CXXFLAGS) $^ -o $@

# 오브젝트 파일 빌드 규칙
%.o: %.cc sort.h
	$(CXX) $(CXXFLAGS) -c $< -o $@

sort.o: sort.cc sort.h
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f *.o $(TARGETS)
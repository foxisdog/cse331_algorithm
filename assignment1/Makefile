CXX = g++
CXXFLAGS = -Wall -g

main:	main.o sort.o sort.h
	$(CXX) $(CXXFLAGS) -o main main.o sort.o
main.o:	main.cc
	$(CXX) $(CXXFLAGS) -c main.cc
sort.o:	sort.cc
	$(CXX) $(CXXFLAGS) -c sort.cc
clean:
	rm -f main *.o
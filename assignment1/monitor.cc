#include <iostream>
#include <fstream>
#include <chrono>
#include <unistd.h>
#include <sys/wait.h>
#include <string>
#include <vector>
#include <algorithm>
#include <iomanip>

struct RunResult {
    double time_ms; // 실행 시간 (밀리초 단위, 소수점 포함)
    long memory;    // 메모리 사용량 (바이트 단위)
};

long getMemoryUsage(pid_t pid) {
    std::string status_path = "/proc/" + std::to_string(pid) + "/status";
    std::ifstream status_file(status_path);
    std::string line;
    while (std::getline(status_file, line)) {
        if (line.find("VmRSS:") == 0) {
            long memory_kb = std::stol(line.substr(7));
            return memory_kb * 1024;
        }
    }
    return 0;
}

void execute(const char* program, const char* input_file, RunResult& result) {
    auto start = std::chrono::high_resolution_clock::now();
    
    pid_t pid = fork();
    if (pid == 0) { // Child process
        if (input_file) {
            freopen(input_file, "r", stdin);
        }
        execl(program, program, nullptr);
        exit(EXIT_FAILURE);
    } else { // Parent process
        int status;
        long max_memory = 0;
        while (waitpid(pid, &status, WNOHANG) == 0) {
            long current_memory = getMemoryUsage(pid);
            max_memory = std::max(max_memory, current_memory);
            usleep(1000); // Sleep for 1ms
        }
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> duration = end - start;
        result.time_ms = duration.count();
        result.memory = max_memory;
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <program> [input_file]\n";
        return 1;
    }

    const char* input_file = (argc >= 3) ? argv[2] : nullptr;
    std::ofstream log("perf_log.csv");
    log << std::fixed << std::setprecision(3);
    log << "Run,Time(ms),Memory(Bytes)\n";

    std::vector<RunResult> results;

    for (int i = 0; i < 100; ++i) {
        RunResult result{0.0, 0};
        execute(argv[1], input_file, result);
        results.push_back(result);
        
        log << i + 1 << "," 
            << result.time_ms << "," 
            << result.memory << "\n";
        
        std::cout << std::fixed << std::setprecision(3);
        std::cout << "Run " << i + 1 << ": Time = " 
                  << result.time_ms << " ms, Memory = " 
                  << result.memory / (1024.0 * 1024.0) 
                  << " MB\n";
    }

    // Calculate and print statistics
    double total_time_ms = 0.0;
    long total_memory_bytes = 0;
    double max_time_ms = 0.0;
    long max_memory_bytes = 0;

    for (const auto& result : results) {
        total_time_ms += result.time_ms;
        total_memory_bytes += result.memory;
        max_time_ms = std::max(max_time_ms, result.time_ms);
        max_memory_bytes = std::max(max_memory_bytes, result.memory);
    }

    double avg_time_ms = total_time_ms / results.size();
    double avg_memory_mb = static_cast<double>(total_memory_bytes) / results.size() / (1024 * 1024);

    std::cout << "\nStatistics:\n";
    std::cout << "Average Time: " << avg_time_ms << " ms\n";
    std::cout << "Max Time: " << max_time_ms << " ms\n";
    std::cout << "Average Memory: " << avg_memory_mb << " MB\n";
    std::cout << "Max Memory: " 
              << static_cast<double>(max_memory_bytes) / (1024 * 1024) 
              << " MB\n";

    std::cout << "\n100 runs completed. Results saved to perf_log.csv\n";
    return 0;
}

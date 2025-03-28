#include <iostream>
#include <fstream>
#include <chrono>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <string>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <filesystem>

namespace fs = std::filesystem;

struct RunResult {
    double time_ms;
    long memory;
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

void createDirectory(const std::string& path) {
    if (!fs::exists(path)) {
        fs::create_directory(path);
    }
}

void processInputFile(const std::string& program, const std::string& input_file, const std::string& output_dir) {
    fs::path input_path(input_file);
    std::string output_csv = output_dir + "/" + input_path.stem().string() + "_results.csv";
    std::ofstream log(output_csv);
    log << std::fixed << std::setprecision(3);
    log << "Run,Time(ms),Memory(Bytes)\n";

    std::vector<RunResult> results;

    for (int i = 0; i < 100; ++i) {
        RunResult result{0.0, 0};
        execute(program.c_str(), input_file.c_str(), result);
        results.push_back(result);
        
        log << i + 1 << "," 
            << result.time_ms << "," 
            << result.memory << "\n";
        
        std::cout << "Run " << i + 1 << " for " << input_file << ": Time = " 
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

    log << "\nStatistics:\n";
    log << "Average Time," << avg_time_ms << " ms\n";
    log << "Max Time," << max_time_ms << " ms\n";
    log << "Average Memory," << avg_memory_mb << " MB\n";
    log << "Max Memory," << static_cast<double>(max_memory_bytes) / (1024 * 1024) << " MB\n";

    std::cout << "Results for " << input_file << " saved to " << output_csv << "\n";
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <program> <input_file1> [input_file2] ...\n";
        return 1;
    }

    std::string program = argv[1];
    std::string output_dir = "results_" + std::to_string(std::chrono::system_clock::now().time_since_epoch().count());
    createDirectory(output_dir);

    for (int i = 2; i < argc; ++i) {
        std::string input_file = argv[i];
        std::cout << "Processing " << input_file << "...\n";
        processInputFile(program, input_file, output_dir);
    }

    std::cout << "All input files processed. Results saved in " << output_dir << "\n";
    return 0;
}

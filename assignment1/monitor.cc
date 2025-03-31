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
    int pipefd[2];
    pipe(pipefd);
    
    pid_t pid = fork();
    if (pid == 0) { // 자식 프로세스
        close(pipefd[0]);
        dup2(pipefd[1], STDOUT_FILENO);
        
        if (input_file) {
            freopen(input_file, "r", stdin);
        }
        execl(program, program, nullptr);
        exit(EXIT_FAILURE);
    } else { // 부모 프로세스
        close(pipefd[1]);
        
        // 메모리 측정 로직
        int status;
        long max_memory = 0;
        while (waitpid(pid, &status, WNOHANG) == 0) {
            long current_memory = getMemoryUsage(pid);
            max_memory = std::max(max_memory, current_memory);
            usleep(1000);
        }

        // 파이프 데이터 전체 읽기
        std::string output;
        char buffer[1024];
        ssize_t count;
        while ((count = read(pipefd[0], buffer, sizeof(buffer)-1)) > 0) {
            buffer[count] = '\0';
            output += buffer;
        }

        // 시간 데이터 파싱
        size_t pos = output.find("SORT_TIME:");
        if (pos != std::string::npos) {
            result.time_ms = std::stod(output.substr(pos + 10));
        }

        result.memory = max_memory;
        close(pipefd[0]);
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

    for (int i = 0; i < 5; ++i) { // 예열
        RunResult result{0.0, 0};
        execute(program.c_str(), input_file.c_str(), result);
    }

    for (int i = 0; i < 10; ++i) {
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

    // 프로그램 이름에서 경로 제거
    fs::path program_path(argv[1]);
    std::string program_name = program_path.stem().string(); // 확장자 제외 파일명 추출
    
    // 디렉토리 이름 생성
    std::string output_dir = program_name + "_results";
    
    // 중복 방지 처리
    int counter = 1;
    const std::string original_dir = output_dir;
    while (fs::exists(output_dir)) {
        output_dir = original_dir + "_" + std::to_string(counter++);
    }
    
    try {
        createDirectory(output_dir);
        if (!fs::exists(output_dir)) {
            throw std::runtime_error("Failed to create output directory: " + output_dir);
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }

    for (int i = 2; i < argc; ++i) {
        const std::string input_file = argv[i];
        std::cout << "Processing " << input_file << "...\n";
        
        try {
            processInputFile(program_path.string(), input_file, output_dir);
        } catch (const std::exception& e) {
            std::cerr << "Error processing file " << input_file << ": " << e.what() << "\n";
        }
    }

    std::cout << "All input files processed. Results saved in " << output_dir << "\n";
    return 0;
}

#pragma once
#include <map>
#include <string>
namespace commerce::runtime {
struct CommandResult {
    bool success{false};
    std::string status{"error"};
    std::string message;
    std::map<std::string, std::string> fields;
};
}

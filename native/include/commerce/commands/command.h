#pragma once
#include "commerce/action_policy.h"
#include <string>
#include <vector>
namespace commerce::commands {
struct CommandSpec {
    std::string name;
    RiskLevel risk{RiskLevel::ReadOnly};
    bool amount_required{false};
    std::string description;
};
struct ParsedCommand {
    std::string name;
    double amount_cad{0.0};
    std::vector<std::string> arguments;
    bool valid{false};
    std::string error;
};
}

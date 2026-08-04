#pragma once
#include "commerce/commands/command.h"
#include "commerce/commands/command_registry.h"
#include <string>
namespace commerce::commands {
class CommandParser final {
public:
    explicit CommandParser(const CommandRegistry& registry) : registry_(registry) {}
    [[nodiscard]] ParsedCommand parse(const std::string& line) const;
private:
    const CommandRegistry& registry_;
};
}

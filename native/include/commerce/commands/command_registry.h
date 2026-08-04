#pragma once
#include "commerce/commands/command.h"
#include <map>
#include <optional>
#include <string>
#include <vector>
namespace commerce::commands {
class CommandRegistry final {
public:
    CommandRegistry();
    void register_command(CommandSpec spec);
    [[nodiscard]] std::optional<CommandSpec> find(const std::string& name) const;
    [[nodiscard]] std::vector<CommandSpec> all() const;
private:
    std::map<std::string, CommandSpec> specs_;
};
}

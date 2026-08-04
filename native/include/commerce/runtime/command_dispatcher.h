#pragma once
#include "commerce/commands/command.h"
#include "commerce/runtime/command_result.h"
#include <functional>
#include <map>
#include <string>
namespace commerce::runtime {
class CommandDispatcher final {
public:
    using Handler = std::function<CommandResult(const commands::ParsedCommand&)>;
    void register_handler(std::string name, Handler handler);
    [[nodiscard]] CommandResult dispatch(const commands::ParsedCommand& command) const;
    [[nodiscard]] std::size_t size() const noexcept { return handlers_.size(); }
private:
    std::map<std::string, Handler> handlers_;
};
}

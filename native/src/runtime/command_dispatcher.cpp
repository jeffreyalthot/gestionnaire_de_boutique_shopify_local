#include "commerce/runtime/command_dispatcher.h"
#include <stdexcept>
#include <utility>
namespace commerce::runtime {
void CommandDispatcher::register_handler(std::string name, Handler handler) {
    if (name.empty() || !handler) throw std::invalid_argument("invalid command handler");
    if (!handlers_.emplace(std::move(name), std::move(handler)).second) throw std::invalid_argument("duplicate handler");
}
CommandResult CommandDispatcher::dispatch(const commands::ParsedCommand& command) const {
    if (!command.valid) return {false, "invalid", command.error, {}};
    const auto found = handlers_.find(command.name);
    if (found == handlers_.end()) return {false, "unsupported", "handler not registered", {}};
    return found->second(command);
}
}

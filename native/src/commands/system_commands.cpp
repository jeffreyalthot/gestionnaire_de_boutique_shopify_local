#include "commerce/commands/system_commands.h"
#include "commerce/commands/command_registry.h"
namespace commerce::commands {
namespace { void register_if_missing(CommandRegistry& registry, CommandSpec spec) { if (!registry.find(spec.name)) registry.register_command(std::move(spec)); } }
void register_system_commands(CommandRegistry& registry) {
    register_if_missing(registry, {"status", RiskLevel::ReadOnly, false, "Runtime status"});
    register_if_missing(registry, {"health", RiskLevel::ReadOnly, false, "Health snapshot"});
    register_if_missing(registry, {"shutdown", RiskLevel::Reversible, false, "Graceful shutdown"});
}
}

#include "commerce/commands/fulfillment_commands.h"
#include "commerce/commands/command_registry.h"
namespace commerce::commands {
namespace { void register_if_missing(CommandRegistry& registry, CommandSpec spec) { if (!registry.find(spec.name)) registry.register_command(std::move(spec)); } }
void register_fulfillment_commands(CommandRegistry& registry) {
    register_if_missing(registry, {"tracking-sync", RiskLevel::Reversible, false, "Synchronize tracking"});
    register_if_missing(registry, {"fulfillment-create", RiskLevel::Irreversible, false, "Create fulfillment"});
}
}

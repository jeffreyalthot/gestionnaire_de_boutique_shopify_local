#include "commerce/commands/procurement_commands.h"
#include "commerce/commands/command_registry.h"
namespace commerce::commands {
namespace { void register_if_missing(CommandRegistry& registry, CommandSpec spec) { if (!registry.find(spec.name)) registry.register_command(std::move(spec)); } }
void register_procurement_commands(CommandRegistry& registry) {
    register_if_missing(registry, {"supplier-compare", RiskLevel::ReadOnly, false, "Compare suppliers"});
    register_if_missing(registry, {"purchase-plan", RiskLevel::Reversible, true, "Prepare purchase"});
    register_if_missing(registry, {"purchase", RiskLevel::Financial, true, "Submit supplier purchase"});
}
}

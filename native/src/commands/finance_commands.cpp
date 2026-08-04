#include "commerce/commands/finance_commands.h"
#include "commerce/commands/command_registry.h"
namespace commerce::commands {
namespace { void register_if_missing(CommandRegistry& registry, CommandSpec spec) { if (!registry.find(spec.name)) registry.register_command(std::move(spec)); } }
void register_finance_commands(CommandRegistry& registry) {
    register_if_missing(registry, {"finance-close", RiskLevel::ReadOnly, false, "Prepare financial close"});
    register_if_missing(registry, {"reserve-review", RiskLevel::ReadOnly, false, "Review cash reserves"});
    register_if_missing(registry, {"refund", RiskLevel::Financial, true, "Plan customer refund"});
}
}

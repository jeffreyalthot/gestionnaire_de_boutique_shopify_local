#include "commerce/commands/order_commands.h"
#include "commerce/commands/command_registry.h"
namespace commerce::commands {
namespace { void register_if_missing(CommandRegistry& registry, CommandSpec spec) { if (!registry.find(spec.name)) registry.register_command(std::move(spec)); } }
void register_order_commands(CommandRegistry& registry) {
    register_if_missing(registry, {"order-review", RiskLevel::ReadOnly, false, "Review order"});
    register_if_missing(registry, {"order-hold", RiskLevel::Reversible, false, "Hold risky order"});
    register_if_missing(registry, {"order-cancel", RiskLevel::Irreversible, false, "Cancel an order"});
}
}

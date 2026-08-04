#include "commerce/commands/marketing_commands.h"
#include "commerce/commands/command_registry.h"
namespace commerce::commands {
namespace { void register_if_missing(CommandRegistry& registry, CommandSpec spec) { if (!registry.find(spec.name)) registry.register_command(std::move(spec)); } }
void register_marketing_commands(CommandRegistry& registry) {
    register_if_missing(registry, {"campaign-review", RiskLevel::ReadOnly, false, "Review campaigns"});
    register_if_missing(registry, {"discount-schedule", RiskLevel::Irreversible, false, "Schedule guarded discount"});
}
}

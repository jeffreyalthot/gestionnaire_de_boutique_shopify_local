#include "commerce/commands/compliance_commands.h"
#include "commerce/commands/command_registry.h"
namespace commerce::commands {
namespace { void register_if_missing(CommandRegistry& registry, CommandSpec spec) { if (!registry.find(spec.name)) registry.register_command(std::move(spec)); } }
void register_compliance_commands(CommandRegistry& registry) {
    register_if_missing(registry, {"compliance-scan", RiskLevel::ReadOnly, false, "Scan product compliance"});
    register_if_missing(registry, {"product-quarantine", RiskLevel::Reversible, false, "Quarantine a product"});
}
}

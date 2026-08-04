#include "commerce/commands/catalog_commands.h"
#include "commerce/commands/command_registry.h"
namespace commerce::commands {
namespace { void register_if_missing(CommandRegistry& registry, CommandSpec spec) { if (!registry.find(spec.name)) registry.register_command(std::move(spec)); } }
void register_catalog_commands(CommandRegistry& registry) {
    register_if_missing(registry, {"catalog-search", RiskLevel::ReadOnly, false, "Search Alibaba catalog"});
    register_if_missing(registry, {"catalog-score", RiskLevel::ReadOnly, false, "Score candidates"});
    register_if_missing(registry, {"catalog-publish", RiskLevel::Irreversible, false, "Publish eligible product"});
}
}

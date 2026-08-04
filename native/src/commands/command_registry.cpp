#include "commerce/commands/command_registry.h"
#include "commerce/commands/catalog_commands.h"
#include "commerce/commands/compliance_commands.h"
#include "commerce/commands/finance_commands.h"
#include "commerce/commands/fulfillment_commands.h"
#include "commerce/commands/marketing_commands.h"
#include "commerce/commands/order_commands.h"
#include "commerce/commands/procurement_commands.h"
#include "commerce/commands/system_commands.h"
#include <stdexcept>
#include <utility>
namespace commerce::commands {
CommandRegistry::CommandRegistry() {
    register_command({"status", RiskLevel::ReadOnly, false, "Show runtime status"});
    register_command({"catalog-sync", RiskLevel::Reversible, false, "Queue catalog synchronization"});
    register_command({"inventory-sync", RiskLevel::Reversible, false, "Queue inventory reconciliation"});
    register_command({"supplier-compare", RiskLevel::ReadOnly, false, "Compare supplier offers"});
    register_command({"order-review", RiskLevel::ReadOnly, false, "Review order risk"});
    register_command({"publish-catalog", RiskLevel::Irreversible, false, "Publish eligible catalog"});
    register_command({"purchase", RiskLevel::Financial, true, "Plan supplier purchase in CAD"});
    register_command({"refund", RiskLevel::Financial, true, "Plan customer refund in CAD"});
    register_command({"price-change", RiskLevel::Irreversible, false, "Plan guarded price change"});
    register_catalog_commands(*this);
    register_compliance_commands(*this);
    register_finance_commands(*this);
    register_fulfillment_commands(*this);
    register_marketing_commands(*this);
    register_order_commands(*this);
    register_procurement_commands(*this);
    register_system_commands(*this);

}
void CommandRegistry::register_command(CommandSpec spec) {
    if (spec.name.empty()) throw std::invalid_argument("command name is empty");
    const auto inserted = specs_.emplace(spec.name, std::move(spec));
    if (!inserted.second) throw std::invalid_argument("duplicate command");
}
std::optional<CommandSpec> CommandRegistry::find(const std::string& name) const {
    const auto it = specs_.find(name);
    return it == specs_.end() ? std::nullopt : std::optional<CommandSpec>(it->second);
}
std::vector<CommandSpec> CommandRegistry::all() const {
    std::vector<CommandSpec> result; result.reserve(specs_.size());
    for (const auto& pair : specs_) result.push_back(pair.second);
    return result;
}
}

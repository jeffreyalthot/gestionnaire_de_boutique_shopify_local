#include "commerce/action_policy.h"

#include <cmath>
#include <utility>

namespace commerce {

ActionPolicy::ActionPolicy(PolicyConfig config) : config_(std::move(config)) {
    if (!std::isfinite(config_.maximum_live_financial_amount_cad) ||
        config_.maximum_live_financial_amount_cad < 0.0) {
        config_.maximum_live_financial_amount_cad = 0.0;
    }
}

ActionDecision ActionPolicy::evaluate(const ActionRequest& request) const {
    if (request.name.empty()) {
        return {false, config_.dry_run, false, "action name is empty"};
    }
    if (!std::isfinite(request.amount_cad) || request.amount_cad < 0.0) {
        return {false, config_.dry_run, false, "financial amount is invalid"};
    }

    const bool sensitive =
        request.risk == RiskLevel::Irreversible || request.risk == RiskLevel::Financial;

    if (config_.dry_run || !request.live_requested) {
        return {
            true,
            true,
            sensitive,
            sensitive ? "simulation accepted; live execution requires explicit approval"
                      : "simulation accepted",
        };
    }

    if (sensitive && !request.explicitly_approved) {
        return {false, false, true, "explicit approval is required"};
    }

    if (request.risk == RiskLevel::Financial &&
        request.amount_cad > config_.maximum_live_financial_amount_cad) {
        return {
            false,
            false,
            true,
            "amount exceeds the configured live financial ceiling",
        };
    }

    return {true, false, sensitive, "live action accepted by policy"};
}

const PolicyConfig& ActionPolicy::config() const noexcept {
    return config_;
}

std::string_view risk_name(RiskLevel risk) noexcept {
    switch (risk) {
        case RiskLevel::ReadOnly:
            return "read-only";
        case RiskLevel::Reversible:
            return "reversible";
        case RiskLevel::Irreversible:
            return "irreversible";
        case RiskLevel::Financial:
            return "financial";
    }
    return "unknown";
}

}  // namespace commerce

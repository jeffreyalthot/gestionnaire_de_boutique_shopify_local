#pragma once

#include <string>
#include <string_view>

namespace commerce {

enum class RiskLevel {
    ReadOnly,
    Reversible,
    Irreversible,
    Financial,
};

struct ActionRequest {
    std::string name;
    RiskLevel risk{RiskLevel::ReadOnly};
    bool live_requested{false};
    bool explicitly_approved{false};
    double amount_cad{0.0};
};

struct ActionDecision {
    bool allowed{false};
    bool simulated{true};
    bool approval_required{false};
    std::string reason;
};

struct PolicyConfig {
    bool dry_run{true};
    double maximum_live_financial_amount_cad{1000.0};
};

class ActionPolicy final {
public:
    explicit ActionPolicy(PolicyConfig config);

    [[nodiscard]] ActionDecision evaluate(const ActionRequest& request) const;
    [[nodiscard]] const PolicyConfig& config() const noexcept;

private:
    PolicyConfig config_;
};

[[nodiscard]] std::string_view risk_name(RiskLevel risk) noexcept;

}  // namespace commerce

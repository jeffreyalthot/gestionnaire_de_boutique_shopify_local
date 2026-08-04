#pragma once

#include "commerce/action_policy.h"

#include <filesystem>
#include <mutex>
#include <string>

namespace commerce {

struct PersistResult {
    bool success{false};
    std::string plan_id;
    std::filesystem::path path;
    std::string error;
};

class DurablePlanStore final {
public:
    explicit DurablePlanStore(std::filesystem::path pending_directory);

    DurablePlanStore(const DurablePlanStore&) = delete;
    DurablePlanStore& operator=(const DurablePlanStore&) = delete;

    [[nodiscard]] PersistResult persist(const ActionRequest& request);
    [[nodiscard]] const std::filesystem::path& pending_directory() const noexcept;

private:
    [[nodiscard]] static bool safe_action_name(const std::string& name) noexcept;
    [[nodiscard]] static std::string utc_timestamp();
    [[nodiscard]] static std::string make_plan_id(const ActionRequest& request);
    [[nodiscard]] static std::string canonical_record(
        const std::string& plan_id,
        const ActionRequest& request,
        const std::string& created_at);

    std::filesystem::path pending_directory_;
    std::mutex write_mutex_;
};

}  // namespace commerce

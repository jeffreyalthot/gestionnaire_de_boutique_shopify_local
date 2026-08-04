#include "commerce/durable_plan_store.h"

#include "commerce/sha256.h"

#include <atomic>
#include <chrono>
#include <cctype>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <system_error>

namespace commerce {

namespace {
std::atomic<std::uint64_t> g_plan_sequence{0};
}

DurablePlanStore::DurablePlanStore(std::filesystem::path pending_directory)
    : pending_directory_(std::move(pending_directory)) {}

PersistResult DurablePlanStore::persist(const ActionRequest& request) {
    std::lock_guard<std::mutex> lock(write_mutex_);
    if (!safe_action_name(request.name)) {
        return {false, {}, {}, "action name contains unsupported characters"};
    }

    std::error_code error;
    std::filesystem::create_directories(pending_directory_, error);
    if (error) {
        return {false, {}, {}, "cannot create pending plan directory: " + error.message()};
    }

    const std::string created_at = utc_timestamp();
    const std::string plan_id = make_plan_id(request);
    const std::string canonical = canonical_record(plan_id, request, created_at);
    const std::string content = canonical + "checksum=" + sha256(canonical) + "\n";
    const std::filesystem::path temporary = pending_directory_ / (plan_id + ".tmp");
    const std::filesystem::path final = pending_directory_ / (plan_id + ".plan");

    {
        std::ofstream output(temporary, std::ios::binary | std::ios::trunc);
        if (!output) {
            return {false, plan_id, {}, "cannot open temporary plan file"};
        }
        output.write(content.data(), static_cast<std::streamsize>(content.size()));
        output.flush();
        if (!output) {
            output.close();
            std::filesystem::remove(temporary, error);
            return {false, plan_id, {}, "cannot durably write plan content"};
        }
    }

    std::filesystem::rename(temporary, final, error);
    if (error) {
        std::filesystem::remove(temporary, error);
        return {false, plan_id, {}, "cannot atomically publish plan file: " + error.message()};
    }
    return {true, plan_id, final, {}};
}

const std::filesystem::path& DurablePlanStore::pending_directory() const noexcept {
    return pending_directory_;
}

bool DurablePlanStore::safe_action_name(const std::string& name) noexcept {
    if (name.empty() || name.size() > 64U) {
        return false;
    }
    for (const unsigned char character : name) {
        if (!(std::islower(character) != 0 || std::isdigit(character) != 0 || character == '-')) {
            return false;
        }
    }
    return true;
}

std::string DurablePlanStore::utc_timestamp() {
    const auto now = std::chrono::system_clock::now();
    const std::time_t raw_time = std::chrono::system_clock::to_time_t(now);
    std::tm utc{};
#ifdef _WIN32
    gmtime_s(&utc, &raw_time);
#else
    gmtime_r(&raw_time, &utc);
#endif
    std::ostringstream output;
    output << std::put_time(&utc, "%Y-%m-%dT%H:%M:%SZ");
    return output.str();
}

std::string DurablePlanStore::make_plan_id(const ActionRequest& request) {
    const auto microseconds = std::chrono::duration_cast<std::chrono::microseconds>(
                                  std::chrono::system_clock::now().time_since_epoch())
                                  .count();
    const std::uint64_t sequence = g_plan_sequence.fetch_add(1U, std::memory_order_relaxed);
    const std::string material =
        request.name + ":" + std::to_string(microseconds) + ":" + std::to_string(sequence);
    return sha256(material).substr(0U, 32U);
}

std::string DurablePlanStore::canonical_record(
    const std::string& plan_id,
    const ActionRequest& request,
    const std::string& created_at) {
    std::ostringstream output;
    output << "version=1\n"
           << "id=" << plan_id << "\n"
           << "action=" << request.name << "\n"
           << "risk=" << risk_name(request.risk) << "\n"
           << "simulated=" << (request.live_requested ? "0" : "1") << "\n"
           << "approved=" << (request.explicitly_approved ? "1" : "0") << "\n"
           << "amount_cad=" << std::fixed << std::setprecision(2) << request.amount_cad << "\n"
           << "created_at_utc=" << created_at << "\n";
    return output.str();
}

}  // namespace commerce

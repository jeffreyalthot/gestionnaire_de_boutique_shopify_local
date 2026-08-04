#include "commerce/action_policy.h"
#include "commerce/bounded_queue.h"
#include "commerce/durable_plan_store.h"
#include "commerce/sha256.h"

#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

namespace {

void require(bool condition, const std::string& message) {
    if (!condition) {
        std::cerr << "[FAIL] " << message << '\n';
        std::exit(EXIT_FAILURE);
    }
    std::cout << "[OK] " << message << '\n';
}

}  // namespace

int main() {
    using commerce::ActionPolicy;
    using commerce::ActionRequest;
    using commerce::BoundedQueue;
    using commerce::PolicyConfig;
    using commerce::RiskLevel;

    ActionPolicy dry_policy(PolicyConfig{true, 1000.0});
    const auto dry_purchase =
        dry_policy.evaluate(ActionRequest{"purchase", RiskLevel::Financial, false, false, 250.0});
    require(dry_purchase.allowed, "dry-run financial plan is accepted");
    require(dry_purchase.simulated, "dry-run cannot become a live action");
    require(dry_purchase.approval_required, "financial action advertises approval requirement");

    ActionPolicy live_policy(PolicyConfig{false, 1000.0});
    const auto unapproved =
        live_policy.evaluate(ActionRequest{"refund", RiskLevel::Financial, true, false, 50.0});
    require(!unapproved.allowed, "unapproved live refund is rejected");

    const auto approved =
        live_policy.evaluate(ActionRequest{"refund", RiskLevel::Financial, true, true, 50.0});
    require(approved.allowed, "approved refund below ceiling is accepted");
    require(!approved.simulated, "approved live refund is marked live");

    const auto over_limit =
        live_policy.evaluate(ActionRequest{"purchase", RiskLevel::Financial, true, true, 1000.01});
    require(!over_limit.allowed, "financial ceiling cannot be bypassed by approval");

    const auto invalid =
        live_policy.evaluate(ActionRequest{"purchase", RiskLevel::Financial, true, true, -1.0});
    require(!invalid.allowed, "negative financial amount is rejected");

    BoundedQueue<int> queue(2);
    require(queue.try_push(1), "first bounded queue insertion succeeds");
    require(queue.try_push(2), "second bounded queue insertion succeeds");
    require(!queue.try_push(3), "bounded queue applies backpressure at capacity");
    require(queue.size() == 2, "bounded queue reports exact depth");
    require(queue.wait_pop().value_or(0) == 1, "bounded queue preserves FIFO order");
    require(queue.wait_pop().value_or(0) == 2, "bounded queue returns second item");
    queue.close();
    require(!queue.try_push(4), "closed queue rejects new work");
    require(!queue.wait_pop().has_value(), "closed empty queue terminates consumers");

    require(
        commerce::sha256("abc") ==
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        "SHA-256 matches the published abc test vector");
    require(
        commerce::sha256("") ==
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "SHA-256 matches the published empty-input test vector");

    const std::filesystem::path plan_root =
        std::filesystem::temp_directory_path() / "commerce_terminal_plan_store_test";
    std::error_code cleanup_error;
    std::filesystem::remove_all(plan_root, cleanup_error);
    commerce::DurablePlanStore plan_store(plan_root);
    const auto persisted = plan_store.persist(
        ActionRequest{"catalog-sync", RiskLevel::Reversible, false, false, 0.0});
    require(persisted.success, "accepted plan is persisted atomically");
    require(std::filesystem::exists(persisted.path), "published plan file exists");
    require(persisted.path.extension() == ".plan", "temporary extension is not exposed");

    std::ifstream plan_input(persisted.path, std::ios::binary);
    std::ostringstream plan_content;
    plan_content << plan_input.rdbuf();
    const std::string stored = plan_content.str();
    const std::size_t checksum_position = stored.rfind("checksum=");
    require(checksum_position != std::string::npos, "persisted plan contains an integrity checksum");
    const std::string canonical = stored.substr(0U, checksum_position);
    const std::string checksum =
        stored.substr(checksum_position + std::string("checksum=").size(), 64U);
    require(commerce::sha256(canonical) == checksum, "persisted plan checksum verifies");

    const auto unsafe = plan_store.persist(
        ActionRequest{"../purchase", RiskLevel::Financial, false, false, 10.0});
    require(!unsafe.success, "unsafe action name cannot escape the plan directory");
    std::filesystem::remove_all(plan_root, cleanup_error);

    return EXIT_SUCCESS;
}

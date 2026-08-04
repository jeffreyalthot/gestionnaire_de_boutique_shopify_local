#include "commerce/action_policy.h"
#include "commerce/bounded_queue.h"
#include "commerce/commands/command_parser.h"
#include "commerce/commands/command_registry.h"
#include "commerce/runtime/resource_monitor.h"
#include "commerce/durable_plan_store.h"
#include "commerce/terminal/diff_renderer.h"
#include "commerce/terminal/event_ring.h"
#include "commerce/terminal/fixed_line_registry.h"
#include "commerce/terminal_dashboard.h"

#include <filesystem>
#include <iostream>
#include <map>
#include <optional>
#include <sstream>
#include <string>
#include <string_view>
#include <thread>
#include <utility>
#include <vector>

namespace {

using commerce::ActionRequest;
using commerce::RiskLevel;

struct WorkItem {
    ActionRequest request;
};

bool exact_approval(commerce::TerminalDashboard& dashboard, const std::string& command) {
    dashboard.set_prompt("APPROVE " + command + " > ");
    std::string confirmation;
    const bool read = static_cast<bool>(std::getline(std::cin, confirmation));
    dashboard.set_prompt("commerce> ");
    dashboard.render();
    return read && confirmation == "APPROVE " + command;
}

int self_test() {
    commerce::ActionPolicy dry_policy({true, 1000.0});
    const auto simulated = dry_policy.evaluate({"purchase", RiskLevel::Financial, false, false, 500.0});
    if (!simulated.allowed || !simulated.simulated || !simulated.approval_required) {
        return 1;
    }
    commerce::ActionPolicy live_policy({false, 1000.0});
    const auto rejected = live_policy.evaluate({"refund", RiskLevel::Financial, true, false, 50.0});
    if (rejected.allowed || !rejected.approval_required) {
        return 2;
    }
    commerce::BoundedQueue<int> queue(1);
    if (!queue.try_push(7) || queue.try_push(8)) {
        return 3;
    }
    const auto value = queue.wait_pop();
    if (!value || *value != 7) {
        return 4;
    }
    queue.close();
    if (queue.wait_pop().has_value()) {
        return 5;
    }
    commerce::terminal::EventRing ring(2U);
    ring.push("one");
    ring.push("two");
    ring.push("three");
    if (ring.snapshot().size() != 2U || ring.snapshot().front() != "two") {
        return 6;
    }
    commerce::terminal::DiffRenderer renderer;
    const auto first = renderer.diff({{1U, "status"}}, 10U);
    const auto second = renderer.diff({{1U, "status"}}, 10U);
    if (first.size() != 1U || !second.empty()) {
        return 7;
    }
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    bool dry_run = true;
    bool run_self_test = false;
    std::filesystem::path plan_directory = "data/native_plans/pending";
    for (int index = 1; index < argc; ++index) {
        const std::string_view argument(argv[index]);
        if (argument == "--dry-run") {
            dry_run = true;
        } else if (argument == "--live") {
            dry_run = false;
        } else if (argument == "--self-test") {
            run_self_test = true;
        } else if (argument == "--plan-dir") {
            if (index + 1 >= argc) {
                std::cerr << "--plan-dir requires a directory\n";
                return 2;
            }
            plan_directory = argv[++index];
        } else if (argument == "--help") {
            std::cout << "Usage: shopify_alibaba_terminal [--dry-run|--live] "
                         "[--plan-dir PATH] [--self-test]\n";
            return 0;
        } else {
            std::cerr << "Unknown argument: " << argument << '\n';
            return 2;
        }
    }

    if (run_self_test) {
        return self_test();
    }

    commerce::ActionPolicy policy({dry_run, 1000.0});
    commerce::commands::CommandRegistry command_registry;
    commerce::commands::CommandParser command_parser(command_registry);
    commerce::runtime::ResourceMonitor resource_monitor;
    commerce::BoundedQueue<WorkItem> queue(64);
    commerce::DurablePlanStore plan_store(std::move(plan_directory));
    commerce::TerminalDashboard dashboard(dry_run);
    auto worker = [&] {
        while (true) {
            auto item = queue.wait_pop();
            if (!item) {
                break;
            }
            dashboard.set_worker_state("persisting " + item->request.name);
            const auto persisted = plan_store.persist(item->request);
            if (persisted.success) {
                dashboard.completed(item->request.name + " persisted as " + persisted.plan_id);
            } else {
                dashboard.rejected(item->request.name + ": " + persisted.error);
            }
            dashboard.set_queue_depth(queue.size());
            dashboard.set_worker_state("idle");
        }
    };

    std::vector<std::thread> workers;
    workers.reserve(2);
    workers.emplace_back(worker);
    workers.emplace_back(worker);

    dashboard.start();
    { const auto sample = resource_monitor.sample(); dashboard.set_resource_usage(sample.rss_mb, sample.cpu_percent, sample.hardware_threads); }
    dashboard.show_help();
    dashboard.set_prompt("commerce> ");

    std::string line;
    while (true) {
        if (!std::getline(std::cin, line)) {
            break;
        }
        dashboard.render();
        if (line == "quit" || line == "exit") { break; }
        if (line == "help") { dashboard.show_help(); continue; }
        const auto parsed = command_parser.parse(line);
        if (!parsed.valid) {
            dashboard.rejected((parsed.name.empty() ? line : parsed.name) + ": " + parsed.error);
            continue;
        }
        const auto spec = command_registry.find(parsed.name);
        if (!spec) { dashboard.rejected(parsed.name + ": registry lookup failed"); continue; }
        const std::string& command = parsed.name;
        const double amount = parsed.amount_cad;
        const bool sensitive = spec->risk == RiskLevel::Financial || spec->risk == RiskLevel::Irreversible;
        bool approved = false;
        if (!dry_run && sensitive) {
            approved = exact_approval(dashboard, command);
        }

        ActionRequest request{command, spec->risk, !dry_run, approved, amount};
        const auto decision = policy.evaluate(request);
        if (!decision.allowed) {
            dashboard.rejected(command + ": " + decision.reason);
            continue;
        }
        if (!queue.try_push({request})) {
            dashboard.rejected(command + ": bounded queue is full or closed");
            continue;
        }
        dashboard.accepted(command + " [" + std::string(commerce::risk_name(request.risk)) +
                           "]: " + decision.reason);
        dashboard.set_queue_depth(queue.size());
        const auto sample = resource_monitor.sample();
        dashboard.set_resource_usage(sample.rss_mb, sample.cpu_percent, sample.hardware_threads);
    }

    queue.close();
    for (auto& thread : workers) {
        if (thread.joinable()) {
            thread.join();
        }
    }
    dashboard.stop();
    return 0;
}

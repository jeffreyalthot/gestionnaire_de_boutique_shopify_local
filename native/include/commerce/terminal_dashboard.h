#pragma once

#include "commerce/terminal/diff_renderer.h"
#include "commerce/terminal/event_ring.h"
#include "commerce/terminal/fixed_line_registry.h"

#include <atomic>
#include <cstddef>
#include <mutex>
#include <string>

namespace commerce {

class TerminalDashboard final {
public:
    explicit TerminalDashboard(bool dry_run);
    ~TerminalDashboard();

    TerminalDashboard(const TerminalDashboard&) = delete;
    TerminalDashboard& operator=(const TerminalDashboard&) = delete;

    void start();
    void stop();
    void accepted(std::string event);
    void rejected(std::string event);
    void completed(std::string event);
    void retried(std::string event);
    void set_queue_depth(std::size_t depth);
    void set_worker_state(std::string state);
    void set_resource_usage(double rss_mb, double cpu_percent, std::size_t hardware_threads);
    void set_prompt(std::string prompt);
    void show_help();
    void render();

    [[nodiscard]] std::size_t accepted_count() const noexcept;
    [[nodiscard]] std::size_t rejected_count() const noexcept;
    [[nodiscard]] std::size_t completed_count() const noexcept;
    [[nodiscard]] std::size_t retried_count() const noexcept;

private:
    void enable_virtual_terminal();
    [[nodiscard]] std::map<std::size_t, std::string> build_lines_locked() const;
    void render_locked();

    static constexpr std::size_t kWidth = 96U;
    static constexpr std::size_t kPromptRow = 23U;

    const bool dry_run_;
    std::atomic<std::size_t> accepted_{0};
    std::atomic<std::size_t> rejected_{0};
    std::atomic<std::size_t> completed_{0};
    std::atomic<std::size_t> retried_{0};
    std::atomic<std::size_t> queue_depth_{0};
    mutable std::mutex output_mutex_;
    terminal::EventRing events_{5U};
    terminal::FixedLineRegistry registry_{kWidth};
    terminal::DiffRenderer renderer_;
    std::string worker_state_{"idle"};
    double rss_mb_{0.0};
    double cpu_percent_{0.0};
    std::size_t hardware_threads_{1U};
    std::string prompt_{"commerce> "};
    bool active_{false};
};

}  // namespace commerce

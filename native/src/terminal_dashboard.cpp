#include "commerce/terminal_dashboard.h"

#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <utility>

#ifdef _WIN32
#include <windows.h>
#endif

#ifndef COMMERCE_VERSION
#define COMMERCE_VERSION "dev"
#endif

namespace commerce {

namespace {
std::string metric_line(const std::string& label, std::size_t value) {
    std::ostringstream output;
    output << label << std::setw(10) << value;
    return output.str();
}
}  // namespace

TerminalDashboard::TerminalDashboard(bool dry_run) : dry_run_(dry_run) {
    registry_.register_line("title", 1U);
    registry_.register_line("separator1", 2U);
    registry_.register_line("mode", 3U);
    registry_.register_line("resources", 4U);
    registry_.register_line("workers", 5U);
    registry_.register_line("accepted", 6U);
    registry_.register_line("rejected", 7U);
    registry_.register_line("completed", 8U);
    registry_.register_line("retried", 9U);
    registry_.register_line("queue", 10U);
    registry_.register_line("separator2", 11U);
    registry_.register_line("event_title", 12U);
    for (std::size_t index = 0U; index < events_.capacity(); ++index) {
        registry_.register_line("event" + std::to_string(index), 13U + index);
    }
    registry_.register_line("separator3", 18U);
    registry_.register_line("commands1", 19U);
    registry_.register_line("commands2", 20U);
    registry_.register_line("policy", 21U);
    registry_.register_line("separator4", 22U);
    registry_.register_line("prompt", kPromptRow);
}

TerminalDashboard::~TerminalDashboard() {
    stop();
}

void TerminalDashboard::enable_virtual_terminal() {
#ifdef _WIN32
    const HANDLE output = GetStdHandle(STD_OUTPUT_HANDLE);
    if (output == INVALID_HANDLE_VALUE) {
        return;
    }
    DWORD mode = 0;
    if (GetConsoleMode(output, &mode) != 0) {
        SetConsoleMode(output, mode | ENABLE_VIRTUAL_TERMINAL_PROCESSING);
    }
#endif
}

void TerminalDashboard::start() {
    std::lock_guard<std::mutex> lock(output_mutex_);
    if (active_) {
        return;
    }
    enable_virtual_terminal();
    active_ = true;
    renderer_.reset();
    events_.push("READY: terminal manager initialized");
    std::cout << "\x1b[?1049h\x1b[2J\x1b[H\x1b[?25h";
    render_locked();
    std::cout.flush();
}

void TerminalDashboard::stop() {
    std::lock_guard<std::mutex> lock(output_mutex_);
    if (!active_) {
        return;
    }
    active_ = false;
    std::cout << "\x1b[?25h\x1b[?1049l";
    std::cout.flush();
}

void TerminalDashboard::accepted(std::string event) {
    accepted_.fetch_add(1U, std::memory_order_relaxed);
    events_.push("ACCEPTED: " + std::move(event));
    render();
}

void TerminalDashboard::rejected(std::string event) {
    rejected_.fetch_add(1U, std::memory_order_relaxed);
    events_.push("REJECTED: " + std::move(event));
    render();
}

void TerminalDashboard::completed(std::string event) {
    completed_.fetch_add(1U, std::memory_order_relaxed);
    events_.push("COMPLETED: " + std::move(event));
    render();
}

void TerminalDashboard::retried(std::string event) {
    retried_.fetch_add(1U, std::memory_order_relaxed);
    events_.push("RETRIED: " + std::move(event));
    render();
}

void TerminalDashboard::set_queue_depth(std::size_t depth) {
    queue_depth_.store(depth, std::memory_order_relaxed);
    render();
}

void TerminalDashboard::set_worker_state(std::string state) {
    std::lock_guard<std::mutex> lock(output_mutex_);
    worker_state_ = std::move(state);
    render_locked();
    std::cout.flush();
}


void TerminalDashboard::set_resource_usage(double rss_mb, double cpu_percent, std::size_t hardware_threads) {
    std::lock_guard<std::mutex> lock(output_mutex_);
    rss_mb_ = rss_mb;
    cpu_percent_ = cpu_percent;
    hardware_threads_ = hardware_threads;
    render_locked();
    std::cout.flush();
}

void TerminalDashboard::set_prompt(std::string prompt) {
    std::lock_guard<std::mutex> lock(output_mutex_);
    prompt_ = std::move(prompt);
    render_locked();
    std::cout.flush();
}

void TerminalDashboard::show_help() {
    events_.push("HELP: status catalog-sync inventory-sync supplier-compare order-review");
    events_.push("HELP: publish-catalog purchase <CAD> refund <CAD> price-change quit");
    render();
}

void TerminalDashboard::render() {
    std::lock_guard<std::mutex> lock(output_mutex_);
    if (!active_) {
        return;
    }
    render_locked();
    std::cout.flush();
}

std::map<std::size_t, std::string> TerminalDashboard::build_lines_locked() const {
    std::map<std::size_t, std::string> lines;
    lines[1U] = std::string("SHOPIFY - ALIBABA FIXED TERMINAL MANAGER ") + COMMERCE_VERSION;
    lines[2U] = std::string(kWidth, '=');
    lines[3U] = std::string("MODE        : ") +
                (dry_run_ ? "DRY-RUN / NO EXTERNAL MUTATION" : "SUPERVISED LIVE / APPROVAL GATED");
    std::ostringstream resource_line;
    resource_line << "RESOURCES   : RSS=" << std::fixed << std::setprecision(1) << rss_mb_
                  << " MB | CPU=" << cpu_percent_ << "% | host_threads=" << hardware_threads_;
    lines[4U] = resource_line.str();
    lines[5U] = "WORKERS     : 2 bounded workers | state=" + worker_state_;
    lines[6U] = metric_line("ACCEPTED    : ", accepted_.load(std::memory_order_relaxed));
    lines[7U] = metric_line("REJECTED    : ", rejected_.load(std::memory_order_relaxed));
    lines[8U] = metric_line("COMPLETED   : ", completed_.load(std::memory_order_relaxed));
    lines[9U] = metric_line("RETRIED     : ", retried_.load(std::memory_order_relaxed));
    lines[10U] = metric_line("QUEUE       : ", queue_depth_.load(std::memory_order_relaxed));
    lines[11U] = std::string(kWidth, '-');
    lines[12U] = "EVENT RING (fixed rows; oldest entries are replaced)";
    const auto events = events_.snapshot();
    for (std::size_t index = 0U; index < events_.capacity(); ++index) {
        lines[13U + index] = index < events.size() ? events[index] : "";
    }
    lines[18U] = std::string(kWidth, '-');
    lines[19U] = "COMMANDS    : status catalog-sync inventory-sync supplier-compare order-review";
    lines[20U] = "SENSITIVE   : publish-catalog purchase <CAD> refund <CAD> price-change";
    lines[21U] = "POLICY      : live financial/irreversible actions require exact explicit approval";
    lines[22U] = std::string(kWidth, '-');
    lines[kPromptRow] = prompt_;
    return lines;
}

void TerminalDashboard::render_locked() {
    const auto patches = renderer_.diff(build_lines_locked(), kWidth);
    for (const auto& patch : patches) {
        std::cout << "\x1b[" << patch.row << ";1H" << patch.text;
    }
    std::cout << "\x1b[" << kPromptRow << ";" << (prompt_.size() + 1U) << "H";
}

std::size_t TerminalDashboard::accepted_count() const noexcept {
    return accepted_.load(std::memory_order_relaxed);
}

std::size_t TerminalDashboard::rejected_count() const noexcept {
    return rejected_.load(std::memory_order_relaxed);
}

std::size_t TerminalDashboard::completed_count() const noexcept {
    return completed_.load(std::memory_order_relaxed);
}

std::size_t TerminalDashboard::retried_count() const noexcept {
    return retried_.load(std::memory_order_relaxed);
}

}  // namespace commerce

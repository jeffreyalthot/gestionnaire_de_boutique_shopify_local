#include "commerce/terminal/ascii_sanitizer.h"
#include "commerce/terminal/metric_widget.h"
#include "commerce/terminal/page_registry.h"
#include "commerce/terminal/progress_bar.h"
#include "commerce/terminal/screen_buffer.h"
#include "commerce/terminal/sparkline.h"
#include "commerce/terminal/status_widget.h"
#include "commerce/terminal/table_widget.h"
#include "commerce/terminal/terminal_size.h"

#include <cstdlib>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

namespace {
void require(bool value, const char* message) {
    if (!value) {
        std::cerr << "[FAIL] " << message << '\n';
        std::exit(EXIT_FAILURE);
    }
}

class TestPage final : public commerce::terminal::Page {
public:
    explicit TestPage(std::string value) : value_(std::move(value)) {}
    [[nodiscard]] std::string key() const override { return value_; }
    [[nodiscard]] std::string title() const override { return "Page " + value_; }
    [[nodiscard]] std::vector<std::string> render(std::size_t width, std::size_t height) const override {
        return std::vector<std::string>(height, std::string(width, value_.front()));
    }
private:
    std::string value_;
};
}

int main() {
    commerce::terminal::ScreenBuffer screen(2U, 8U);
    screen.set(0U, "abcdefghi");
    screen.set_cell(1U, 2U, 'X');
    require(screen.line(0U).size() == 8U && screen.line(1U)[2U] == 'X', "screen fixed width");
    screen.resize(3U, 5U, true);
    require(screen.rows() == 3U && screen.columns() == 5U && screen.line(0U) == "abcde", "screen resize");

    commerce::terminal::Sparkline spark({1.0, 2.0, 3.0}, 3U);
    spark.append(4.0);
    require(spark.values().size() == 3U && spark.render(3U).size() == 3U, "sparkline bounded");

    commerce::terminal::MetricWidget metric("RAM", "200", "Mio");
    metric.update("210", 5.0);
    require(metric.render(32U).find("+5.0%") != std::string::npos, "metric trend");

    commerce::terminal::StatusWidget status("Shopify", commerce::terminal::StatusLevel::Warning, "throttled");
    require(status.render(40U).find("WARNING") != std::string::npos, "status level");

    commerce::terminal::TableWidget table({{"a", "b"}, {"c", "d"}}, {"A", "B"});
    const auto rows = table.render_lines(20U, 3U);
    require(rows.size() == 3U && rows.front().size() == 20U, "table fixed region");

    commerce::terminal::PageRegistry pages;
    pages.register_page(std::make_shared<TestPage>("a"));
    pages.register_page(std::make_shared<TestPage>("b"));
    require(pages.active_key() == "a" && pages.activate_next() && pages.active_key() == "b", "page next");
    require(pages.activate_next() && pages.active_key() == "a", "page wrap");
    require(pages.remove("a") && pages.active_key() == "b", "page remove");

    require(commerce::terminal::ProgressBar::render_labeled(0.5, 24U, "SYNC").size() <= 24U, "labeled progress");
    require(commerce::terminal::AsciiSanitizer::strip_ansi("\x1b[31mRED\x1b[0m") == "RED", "strip ansi");
    require(commerce::terminal::TerminalSize{10U, 5U}.clamped(40U, 12U).usable(), "terminal clamp");
    return EXIT_SUCCESS;
}

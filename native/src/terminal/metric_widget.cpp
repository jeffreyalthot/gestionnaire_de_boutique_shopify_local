#include "commerce/terminal/metric_widget.h"
#include "commerce/terminal/diff_renderer.h"

#include <cmath>
#include <iomanip>
#include <sstream>
#include <utility>

namespace commerce::terminal {

MetricWidget::MetricWidget(std::string label, std::string value, std::string unit)
    : label_(std::move(label)), value_(std::move(value)), unit_(std::move(unit)) {}

void MetricWidget::update(std::string value, std::optional<double> trend) {
    value_ = std::move(value);
    trend_ = trend && std::isfinite(*trend) ? trend : std::nullopt;
}

std::string MetricWidget::render(std::size_t width) const {
    std::ostringstream output;
    output << label_ << ": " << value_;
    if (!unit_.empty()) {
        output << ' ' << unit_;
    }
    if (trend_) {
        output << " [" << (*trend_ > 0.0 ? '+' : ' ') << std::fixed << std::setprecision(1) << *trend_ << "%]";
    }
    return DiffRenderer::fit_ascii(output.str(), width);
}

}  // namespace commerce::terminal

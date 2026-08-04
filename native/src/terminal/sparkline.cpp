#include "commerce/terminal/sparkline.h"

#include <algorithm>
#include <cmath>
#include <limits>

namespace commerce::terminal {

Sparkline::Sparkline(std::vector<double> values, std::size_t capacity)
    : values_(std::move(values)), capacity_(std::max<std::size_t>(1U, capacity)) {
    if (values_.size() > capacity_) {
        values_.erase(values_.begin(), values_.end() - static_cast<std::ptrdiff_t>(capacity_));
    }
}

void Sparkline::append(double value) {
    if (!std::isfinite(value)) {
        return;
    }
    values_.push_back(value);
    if (values_.size() > capacity_) {
        values_.erase(values_.begin());
    }
}

void Sparkline::clear() noexcept { values_.clear(); }

std::string Sparkline::render(std::size_t width) const {
    if (values_.empty() || width == 0U) {
        return std::string(width, ' ');
    }
    std::vector<double> finite;
    finite.reserve(values_.size());
    for (double value : values_) {
        if (std::isfinite(value)) {
            finite.push_back(value);
        }
    }
    if (finite.empty()) {
        return std::string(width, ' ');
    }
    const auto [minimum, maximum] = std::minmax_element(finite.begin(), finite.end());
    static constexpr char levels[] = "._-:=+*#%@";
    std::string output;
    const std::size_t start = finite.size() > width ? finite.size() - width : 0U;
    output.reserve(width);
    for (std::size_t index = start; index < finite.size(); ++index) {
        const double ratio = *maximum == *minimum ? 0.0 : (finite[index] - *minimum) / (*maximum - *minimum);
        const auto level = std::min<std::size_t>(9U, static_cast<std::size_t>(std::clamp(ratio, 0.0, 1.0) * 9.0));
        output.push_back(levels[level]);
    }
    if (output.size() < width) {
        output.insert(output.begin(), width - output.size(), ' ');
    }
    return output;
}

}  // namespace commerce::terminal

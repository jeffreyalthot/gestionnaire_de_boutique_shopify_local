#include "commerce/terminal/progress_bar.h"

#include <algorithm>
#include <cmath>
#include <iomanip>
#include <sstream>

namespace commerce::terminal {

std::string ProgressBar::render(double fraction, std::size_t width) {
    if (!std::isfinite(fraction)) {
        fraction = 0.0;
    }
    fraction = std::clamp(fraction, 0.0, 1.0);
    const auto filled = static_cast<std::size_t>(std::round(fraction * static_cast<double>(width)));
    return "[" + std::string(std::min(filled, width), '#') + std::string(width - std::min(filled, width), '-') + "]";
}

std::string ProgressBar::render_labeled(double fraction, std::size_t width, const std::string& label) {
    std::ostringstream suffix;
    const double bounded = std::clamp(std::isfinite(fraction) ? fraction : 0.0, 0.0, 1.0);
    suffix << (label.empty() ? "" : label + " ") << std::fixed << std::setprecision(1) << bounded * 100.0 << '%';
    const std::string suffix_text = suffix.str();
    if (width <= suffix_text.size() + 3U) {
        return suffix_text.substr(0U, width);
    }
    const std::size_t bar_width = width - suffix_text.size() - 1U;
    return render(bounded, bar_width >= 2U ? bar_width - 2U : 0U) + " " + suffix_text;
}

}  // namespace commerce::terminal

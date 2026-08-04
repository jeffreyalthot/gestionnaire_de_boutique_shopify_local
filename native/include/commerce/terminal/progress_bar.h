#pragma once

#include <cstddef>
#include <string>

namespace commerce::terminal {

class ProgressBar final {
public:
    [[nodiscard]] static std::string render(double fraction, std::size_t width);
    [[nodiscard]] static std::string render_labeled(
        double fraction,
        std::size_t width,
        const std::string& label = "");
};

}  // namespace commerce::terminal

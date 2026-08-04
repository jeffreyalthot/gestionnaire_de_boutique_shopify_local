#pragma once

#include <cstddef>
#include <string>
#include <vector>

namespace commerce::terminal {

class Widget {
public:
    virtual ~Widget() = default;
    [[nodiscard]] virtual std::string render(std::size_t width) const = 0;
    [[nodiscard]] virtual std::vector<std::string> render_lines(
        std::size_t width,
        std::size_t height) const;
    [[nodiscard]] virtual std::size_t minimum_width() const noexcept { return 1U; }
};

}  // namespace commerce::terminal

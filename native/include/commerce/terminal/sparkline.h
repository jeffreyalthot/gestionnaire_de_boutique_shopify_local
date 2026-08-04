#pragma once

#include "commerce/terminal/widget.h"

#include <cstddef>
#include <vector>

namespace commerce::terminal {

class Sparkline final : public Widget {
public:
    explicit Sparkline(std::vector<double> values = {}, std::size_t capacity = 120U);
    void append(double value);
    void clear() noexcept;
    [[nodiscard]] const std::vector<double>& values() const noexcept { return values_; }
    [[nodiscard]] std::string render(std::size_t width) const override;

private:
    std::vector<double> values_;
    std::size_t capacity_;
};

}  // namespace commerce::terminal

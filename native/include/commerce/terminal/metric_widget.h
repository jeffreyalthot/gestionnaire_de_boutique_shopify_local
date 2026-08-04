#pragma once

#include "commerce/terminal/widget.h"

#include <optional>
#include <string>

namespace commerce::terminal {

class MetricWidget final : public Widget {
public:
    MetricWidget(std::string label, std::string value, std::string unit = "");
    void update(std::string value, std::optional<double> trend = std::nullopt);
    [[nodiscard]] std::string render(std::size_t width) const override;

private:
    std::string label_;
    std::string value_;
    std::string unit_;
    std::optional<double> trend_;
};

}  // namespace commerce::terminal

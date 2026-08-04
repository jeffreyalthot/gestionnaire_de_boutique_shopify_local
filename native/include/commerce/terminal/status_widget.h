#pragma once

#include "commerce/terminal/widget.h"

#include <string>

namespace commerce::terminal {

enum class StatusLevel { Ok, Info, Warning, Error, Disabled };

class StatusWidget final : public Widget {
public:
    StatusWidget(std::string name, bool ok, std::string detail = "");
    StatusWidget(std::string name, StatusLevel level, std::string detail = "");

    void update(StatusLevel level, std::string detail = "");
    [[nodiscard]] StatusLevel level() const noexcept { return level_; }
    [[nodiscard]] std::string render(std::size_t width) const override;

private:
    std::string name_;
    StatusLevel level_;
    std::string detail_;
};

}  // namespace commerce::terminal

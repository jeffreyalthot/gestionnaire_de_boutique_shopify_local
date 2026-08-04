#include "commerce/terminal/status_widget.h"
#include "commerce/terminal/diff_renderer.h"

#include <utility>

namespace commerce::terminal {
namespace {
const char* label(StatusLevel level) noexcept {
    switch (level) {
        case StatusLevel::Ok: return "OK";
        case StatusLevel::Info: return "INFO";
        case StatusLevel::Warning: return "WARNING";
        case StatusLevel::Error: return "ERROR";
        case StatusLevel::Disabled: return "DISABLED";
    }
    return "UNKNOWN";
}
}

StatusWidget::StatusWidget(std::string name, bool ok, std::string detail)
    : StatusWidget(std::move(name), ok ? StatusLevel::Ok : StatusLevel::Error, std::move(detail)) {}

StatusWidget::StatusWidget(std::string name, StatusLevel level_value, std::string detail)
    : name_(std::move(name)), level_(level_value), detail_(std::move(detail)) {}

void StatusWidget::update(StatusLevel level_value, std::string detail) {
    level_ = level_value;
    detail_ = std::move(detail);
}

std::string StatusWidget::render(std::size_t width) const {
    const std::string text = name_ + "=" + label(level_) + (detail_.empty() ? "" : " " + detail_);
    return DiffRenderer::fit_ascii(text, width);
}

}  // namespace commerce::terminal

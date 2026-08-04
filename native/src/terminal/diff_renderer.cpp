#include "commerce/terminal/diff_renderer.h"

namespace commerce::terminal {

std::vector<LinePatch> DiffRenderer::diff(
    const std::map<std::size_t, std::string>& lines,
    std::size_t width) {
    std::vector<LinePatch> patches;
    for (const auto& [row, raw] : lines) {
        const auto text = fit_ascii(raw, width);
        const auto iterator = previous_.find(row);
        if (iterator == previous_.end() || iterator->second != text) {
            patches.push_back(LinePatch{row, text});
            previous_[row] = text;
        }
    }
    return patches;
}

void DiffRenderer::reset() {
    previous_.clear();
}

std::string DiffRenderer::fit_ascii(std::string value, std::size_t width) {
    for (char& character : value) {
        const auto byte = static_cast<unsigned char>(character);
        if (byte < 32U || byte > 126U) {
            character = '?';
        }
    }
    if (value.size() > width) {
        value.resize(width);
    }
    value.append(width - value.size(), ' ');
    return value;
}

}  // namespace commerce::terminal

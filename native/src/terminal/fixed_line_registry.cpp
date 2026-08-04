#include "commerce/terminal/fixed_line_registry.h"

#include <algorithm>
#include <stdexcept>
#include <utility>

namespace commerce::terminal {

FixedLineRegistry::FixedLineRegistry(std::size_t default_width)
    : default_width_(std::max<std::size_t>(40U, default_width)) {}

const FixedLine& FixedLineRegistry::register_line(
    std::string key,
    std::size_t row,
    std::size_t width) {
    if (key.empty() || row == 0U) {
        throw std::invalid_argument("fixed line key and row are required");
    }
    for (const auto& [existing_key, line] : lines_) {
        (void)existing_key;
        if (line.row == row) {
            throw std::invalid_argument("fixed line row already registered");
        }
    }
    const std::string stored_key = key;
    const auto [iterator, inserted] = lines_.emplace(
        stored_key,
        FixedLine{stored_key, row, width == 0U ? default_width_ : width});
    if (!inserted) {
        throw std::invalid_argument("fixed line key already registered");
    }
    return iterator->second;
}

const FixedLine& FixedLineRegistry::at(const std::string& key) const {
    return lines_.at(key);
}

std::vector<FixedLine> FixedLineRegistry::rows() const {
    std::vector<FixedLine> output;
    output.reserve(lines_.size());
    for (const auto& [key, line] : lines_) {
        (void)key;
        output.push_back(line);
    }
    std::sort(output.begin(), output.end(), [](const FixedLine& left, const FixedLine& right) {
        return left.row < right.row;
    });
    return output;
}

std::size_t FixedLineRegistry::size() const noexcept {
    return lines_.size();
}

}  // namespace commerce::terminal

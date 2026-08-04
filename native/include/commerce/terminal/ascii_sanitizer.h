#pragma once

#include <cstddef>
#include <string>

namespace commerce::terminal {

class AsciiSanitizer final {
public:
    [[nodiscard]] static std::string sanitize(const std::string& text);
    [[nodiscard]] static std::string sanitize_line(
        const std::string& text,
        std::size_t maximum_width = 0U);
    [[nodiscard]] static std::string strip_ansi(const std::string& text);
};

}  // namespace commerce::terminal

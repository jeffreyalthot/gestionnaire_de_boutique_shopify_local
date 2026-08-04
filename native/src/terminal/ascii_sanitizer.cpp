#include "commerce/terminal/ascii_sanitizer.h"

#include <cctype>

namespace commerce::terminal {

std::string AsciiSanitizer::strip_ansi(const std::string& text) {
    std::string output;
    output.reserve(text.size());
    bool escape = false;
    bool control_sequence = false;
    for (unsigned char byte : text) {
        if (!escape && byte == 0x1BU) {
            escape = true;
            control_sequence = false;
            continue;
        }
        if (escape) {
            if (!control_sequence && byte == '[') {
                control_sequence = true;
                continue;
            }
            if (!control_sequence || (byte >= 0x40U && byte <= 0x7EU)) {
                escape = false;
                control_sequence = false;
            }
            continue;
        }
        output.push_back(static_cast<char>(byte));
    }
    return output;
}

std::string AsciiSanitizer::sanitize(const std::string& text) {
    const std::string stripped = strip_ansi(text);
    std::string output;
    output.reserve(stripped.size());
    for (unsigned char byte : stripped) {
        output.push_back(byte >= 32U && byte <= 126U ? static_cast<char>(byte) : '?');
    }
    return output;
}

std::string AsciiSanitizer::sanitize_line(const std::string& text, std::size_t maximum_width) {
    std::string output = sanitize(text);
    for (char& value : output) {
        if (value == '\r' || value == '\n' || value == '\t') {
            value = ' ';
        }
    }
    if (maximum_width != 0U && output.size() > maximum_width) {
        output.resize(maximum_width);
    }
    return output;
}

}  // namespace commerce::terminal

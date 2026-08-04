#pragma once
#include <cstddef>
#include <string>
namespace commerce::terminal {
class InputEditor final {
public:
    void insert(char c); void backspace(); void clear();
    [[nodiscard]] const std::string& text() const noexcept { return text_; }
    [[nodiscard]] std::size_t cursor() const noexcept { return cursor_; }
private: std::string text_; std::size_t cursor_{0U};
};
}

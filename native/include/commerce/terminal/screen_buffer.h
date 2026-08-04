#pragma once

#include <cstddef>
#include <string>
#include <vector>

namespace commerce::terminal {

class ScreenBuffer final {
public:
    ScreenBuffer(std::size_t rows, std::size_t columns);

    void set(std::size_t row, std::string text);
    void set_cell(std::size_t row, std::size_t column, char value);
    void clear(char fill = ' ');
    void resize(std::size_t rows, std::size_t columns, bool preserve = true);

    [[nodiscard]] const std::string& line(std::size_t row) const;
    [[nodiscard]] std::vector<std::string> snapshot() const;
    [[nodiscard]] std::string joined(char separator = '\n') const;
    [[nodiscard]] std::size_t rows() const noexcept { return lines_.size(); }
    [[nodiscard]] std::size_t columns() const noexcept { return columns_; }

private:
    void normalize_all();
    std::size_t columns_;
    std::vector<std::string> lines_;
};

}  // namespace commerce::terminal

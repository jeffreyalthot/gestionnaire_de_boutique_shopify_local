#include "commerce/terminal/screen_buffer.h"
#include "commerce/terminal/diff_renderer.h"

#include <algorithm>
#include <sstream>
#include <stdexcept>

namespace commerce::terminal {

ScreenBuffer::ScreenBuffer(std::size_t rows, std::size_t columns)
    : columns_(columns), lines_(rows, std::string(columns, ' ')) {
    if (rows == 0U || columns == 0U) {
        throw std::invalid_argument("empty screen");
    }
}

void ScreenBuffer::set(std::size_t row, std::string text) {
    if (row >= lines_.size()) {
        throw std::out_of_range("row");
    }
    lines_[row] = DiffRenderer::fit_ascii(std::move(text), columns_);
}

void ScreenBuffer::set_cell(std::size_t row, std::size_t column, char value) {
    if (row >= lines_.size() || column >= columns_) {
        throw std::out_of_range("screen cell");
    }
    const unsigned char byte = static_cast<unsigned char>(value);
    lines_[row][column] = byte >= 32U && byte <= 126U ? value : '?';
}

void ScreenBuffer::clear(char fill) {
    const unsigned char byte = static_cast<unsigned char>(fill);
    const char safe = byte >= 32U && byte <= 126U ? fill : ' ';
    for (auto& line_value : lines_) {
        line_value.assign(columns_, safe);
    }
}

void ScreenBuffer::resize(std::size_t rows, std::size_t columns, bool preserve) {
    if (rows == 0U || columns == 0U) {
        throw std::invalid_argument("empty screen");
    }
    if (!preserve) {
        columns_ = columns;
        lines_.assign(rows, std::string(columns, ' '));
        return;
    }
    lines_.resize(rows, std::string(columns_, ' '));
    columns_ = columns;
    normalize_all();
}

const std::string& ScreenBuffer::line(std::size_t row) const { return lines_.at(row); }

std::vector<std::string> ScreenBuffer::snapshot() const { return lines_; }

std::string ScreenBuffer::joined(char separator) const {
    std::ostringstream output;
    for (std::size_t index = 0U; index < lines_.size(); ++index) {
        if (index != 0U) {
            output << separator;
        }
        output << lines_[index];
    }
    return output.str();
}

void ScreenBuffer::normalize_all() {
    for (auto& line_value : lines_) {
        line_value = DiffRenderer::fit_ascii(std::move(line_value), columns_);
    }
}

}  // namespace commerce::terminal

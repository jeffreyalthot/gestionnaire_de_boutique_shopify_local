#pragma once

#include "commerce/terminal/widget.h"

#include <cstddef>
#include <string>
#include <vector>

namespace commerce::terminal {

class TableWidget final : public Widget {
public:
    explicit TableWidget(
        std::vector<std::vector<std::string>> rows = {},
        std::vector<std::string> headers = {});

    void set_rows(std::vector<std::vector<std::string>> rows);
    void set_headers(std::vector<std::string> headers);
    [[nodiscard]] std::string render(std::size_t width) const override;
    [[nodiscard]] std::vector<std::string> render_lines(
        std::size_t width,
        std::size_t height) const override;

private:
    [[nodiscard]] std::vector<std::size_t> column_widths(std::size_t width) const;
    [[nodiscard]] std::string render_row(
        const std::vector<std::string>& row,
        const std::vector<std::size_t>& widths,
        std::size_t width) const;

    std::vector<std::vector<std::string>> rows_;
    std::vector<std::string> headers_;
};

}  // namespace commerce::terminal

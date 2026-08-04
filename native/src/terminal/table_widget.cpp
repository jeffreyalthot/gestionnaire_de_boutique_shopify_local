#include "commerce/terminal/table_widget.h"
#include "commerce/terminal/diff_renderer.h"

#include <algorithm>
#include <numeric>
#include <sstream>
#include <utility>

namespace commerce::terminal {

TableWidget::TableWidget(std::vector<std::vector<std::string>> rows, std::vector<std::string> headers)
    : rows_(std::move(rows)), headers_(std::move(headers)) {}

void TableWidget::set_rows(std::vector<std::vector<std::string>> rows) { rows_ = std::move(rows); }
void TableWidget::set_headers(std::vector<std::string> headers) { headers_ = std::move(headers); }

std::vector<std::size_t> TableWidget::column_widths(std::size_t width) const {
    std::size_t columns = headers_.size();
    for (const auto& row : rows_) {
        columns = std::max(columns, row.size());
    }
    if (columns == 0U || width == 0U) {
        return {};
    }
    const std::size_t separators = columns > 1U ? (columns - 1U) * 3U : 0U;
    const std::size_t available = width > separators ? width - separators : columns;
    std::vector<std::size_t> widths(columns, std::max<std::size_t>(1U, available / columns));
    std::size_t used = std::accumulate(widths.begin(), widths.end(), std::size_t{0U});
    for (std::size_t index = 0U; used < available; ++index, ++used) {
        ++widths[index % columns];
    }
    return widths;
}

std::string TableWidget::render_row(const std::vector<std::string>& row,
                                    const std::vector<std::size_t>& widths,
                                    std::size_t width) const {
    std::ostringstream output;
    for (std::size_t column = 0U; column < widths.size(); ++column) {
        if (column != 0U) {
            output << " | ";
        }
        const std::string value = column < row.size() ? row[column] : "";
        output << DiffRenderer::fit_ascii(value, widths[column]);
    }
    return DiffRenderer::fit_ascii(output.str(), width);
}

std::vector<std::string> TableWidget::render_lines(std::size_t width, std::size_t height) const {
    std::vector<std::string> output;
    if (height == 0U) {
        return output;
    }
    const auto widths = column_widths(width);
    output.reserve(height);
    if (!headers_.empty() && output.size() < height) {
        output.push_back(render_row(headers_, widths, width));
    }
    for (const auto& row : rows_) {
        if (output.size() >= height) {
            break;
        }
        output.push_back(render_row(row, widths, width));
    }
    while (output.size() < height) {
        output.emplace_back(width, ' ');
    }
    return output;
}

std::string TableWidget::render(std::size_t width) const {
    const auto lines = render_lines(width, 1U);
    return lines.empty() ? std::string{} : lines.front();
}

}  // namespace commerce::terminal

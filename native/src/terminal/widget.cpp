#include "commerce/terminal/widget.h"
#include "commerce/terminal/diff_renderer.h"

namespace commerce::terminal {

std::vector<std::string> Widget::render_lines(std::size_t width, std::size_t height) const {
    std::vector<std::string> lines;
    if (height == 0U) {
        return lines;
    }
    lines.reserve(height);
    lines.push_back(DiffRenderer::fit_ascii(render(width), width));
    while (lines.size() < height) {
        lines.emplace_back(width, ' ');
    }
    return lines;
}

}  // namespace commerce::terminal

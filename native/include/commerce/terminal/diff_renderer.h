#pragma once

#include <cstddef>
#include <map>
#include <string>
#include <vector>

namespace commerce::terminal {

struct LinePatch {
    std::size_t row{0U};
    std::string text;
};

class DiffRenderer final {
public:
    [[nodiscard]] std::vector<LinePatch> diff(
        const std::map<std::size_t, std::string>& lines,
        std::size_t width);
    void reset();
    [[nodiscard]] static std::string fit_ascii(std::string value, std::size_t width);

private:
    std::map<std::size_t, std::string> previous_;
};

}  // namespace commerce::terminal

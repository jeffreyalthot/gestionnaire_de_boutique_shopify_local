#pragma once

#include <cstddef>
#include <map>
#include <string>
#include <vector>

namespace commerce::terminal {

struct FixedLine {
    std::string key;
    std::size_t row{0U};
    std::size_t width{0U};
};

class FixedLineRegistry final {
public:
    explicit FixedLineRegistry(std::size_t default_width = 96U);
    const FixedLine& register_line(std::string key, std::size_t row, std::size_t width = 0U);
    [[nodiscard]] const FixedLine& at(const std::string& key) const;
    [[nodiscard]] std::vector<FixedLine> rows() const;
    [[nodiscard]] std::size_t size() const noexcept;

private:
    std::size_t default_width_;
    std::map<std::string, FixedLine> lines_;
};

}  // namespace commerce::terminal

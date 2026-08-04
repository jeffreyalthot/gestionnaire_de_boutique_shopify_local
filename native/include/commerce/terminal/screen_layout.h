#pragma once
#include <cstddef>
#include <map>
#include <string>
namespace commerce::terminal {
class ScreenLayout final {
public:
    ScreenLayout(std::size_t width,std::size_t height);
    void reserve(std::string key,std::size_t row);
    [[nodiscard]] std::size_t row(const std::string& key) const;
    [[nodiscard]] std::size_t width() const noexcept { return width_; }
    [[nodiscard]] std::size_t height() const noexcept { return height_; }
private:
    std::size_t width_,height_; std::map<std::string,std::size_t> rows_;
};
}

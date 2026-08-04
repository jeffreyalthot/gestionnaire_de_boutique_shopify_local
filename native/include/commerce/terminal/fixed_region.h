#pragma once
#include <cstddef>
#include <string>
namespace commerce::terminal {
struct FixedRegion { std::string name; std::size_t row{0}; std::size_t column{0}; std::size_t height{1}; std::size_t width{1};
[[nodiscard]] bool contains(std::size_t r,std::size_t c) const noexcept{return r>=row&&r<row+height&&c>=column&&c<column+width;}
[[nodiscard]] bool overlaps(const FixedRegion& other) const noexcept{return !(row+height<=other.row||other.row+other.height<=row||column+width<=other.column||other.column+other.width<=column);} };
}

#include "commerce/terminal/screen_layout.h"
#include <stdexcept>
namespace commerce::terminal {
ScreenLayout::ScreenLayout(std::size_t width,std::size_t height):width_(width),height_(height){ if(width<40U||height<10U) throw std::invalid_argument("terminal too small"); }
void ScreenLayout::reserve(std::string key,std::size_t row_value){ if(key.empty()||row_value==0U||row_value>height_) throw std::invalid_argument("invalid region"); for(const auto& [_,row]:rows_) if(row==row_value) throw std::invalid_argument("duplicate row"); if(!rows_.emplace(std::move(key),row_value).second) throw std::invalid_argument("duplicate key"); }
std::size_t ScreenLayout::row(const std::string& key) const { return rows_.at(key); }
}

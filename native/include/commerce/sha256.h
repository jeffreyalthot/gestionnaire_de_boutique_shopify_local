#pragma once

#include <string>
#include <string_view>

namespace commerce {

[[nodiscard]] std::string sha256(std::string_view input);

}  // namespace commerce

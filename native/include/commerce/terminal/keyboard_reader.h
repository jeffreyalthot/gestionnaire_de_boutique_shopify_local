#pragma once
#include <optional>
#include <string>
namespace commerce::terminal { class KeyboardReader final { public:[[nodiscard]] std::optional<std::string> read_line(bool blocking=true) const; }; }

#pragma once

#include <cstddef>

namespace commerce::terminal {

struct TerminalSize {
    std::size_t columns{96U};
    std::size_t rows{30U};

    [[nodiscard]] bool usable(std::size_t minimum_columns = 40U,
                              std::size_t minimum_rows = 12U) const noexcept;
    [[nodiscard]] TerminalSize clamped(std::size_t minimum_columns,
                                       std::size_t minimum_rows,
                                       std::size_t maximum_columns = 240U,
                                       std::size_t maximum_rows = 120U) const noexcept;
};

[[nodiscard]] TerminalSize current_terminal_size() noexcept;

}  // namespace commerce::terminal

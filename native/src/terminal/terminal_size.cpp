#include "commerce/terminal/terminal_size.h"

#include <algorithm>

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#else
#include <sys/ioctl.h>
#include <unistd.h>
#endif

namespace commerce::terminal {

bool TerminalSize::usable(std::size_t minimum_columns, std::size_t minimum_rows) const noexcept {
    return columns >= minimum_columns && rows >= minimum_rows;
}

TerminalSize TerminalSize::clamped(std::size_t minimum_columns,
                                   std::size_t minimum_rows,
                                   std::size_t maximum_columns,
                                   std::size_t maximum_rows) const noexcept {
    const std::size_t max_columns = std::max(minimum_columns, maximum_columns);
    const std::size_t max_rows = std::max(minimum_rows, maximum_rows);
    return {
        std::clamp(columns, minimum_columns, max_columns),
        std::clamp(rows, minimum_rows, max_rows),
    };
}

TerminalSize current_terminal_size() noexcept {
    TerminalSize size;
#ifdef _WIN32
    CONSOLE_SCREEN_BUFFER_INFO info{};
    if (GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &info)) {
        size.columns = static_cast<std::size_t>(info.srWindow.Right - info.srWindow.Left + 1);
        size.rows = static_cast<std::size_t>(info.srWindow.Bottom - info.srWindow.Top + 1);
    }
#else
    winsize value{};
    if (ioctl(STDOUT_FILENO, TIOCGWINSZ, &value) == 0) {
        if (value.ws_col != 0U) size.columns = value.ws_col;
        if (value.ws_row != 0U) size.rows = value.ws_row;
    }
#endif
    return size.clamped(20U, 8U, 500U, 300U);
}

}  // namespace commerce::terminal

#pragma once
#include <cstddef>
#include <string>
namespace commerce::terminal {
class ConsoleBackend {
public:
    virtual ~ConsoleBackend() = default;
    virtual void enter_alternate_screen() = 0;
    virtual void leave_alternate_screen() = 0;
    virtual void hide_cursor() = 0;
    virtual void show_cursor() = 0;
    virtual void write_at(std::size_t row, std::size_t column, const std::string& text) = 0;
    virtual void flush() = 0;
};
}

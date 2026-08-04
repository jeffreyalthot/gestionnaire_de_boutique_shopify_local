#pragma once
#include "commerce/terminal/console_backend.h"
namespace commerce::terminal {
class Win32ConsoleBackend final : public ConsoleBackend {
public:
    void enter_alternate_screen() override; void leave_alternate_screen() override;
    void hide_cursor() override; void show_cursor() override;
    void write_at(std::size_t row,std::size_t column,const std::string& text) override; void flush() override;
};
}

#pragma once
#include "commerce/terminal/console_backend.h"
#include <ostream>
namespace commerce::terminal {
class AnsiConsoleBackend final : public ConsoleBackend {
public:
    explicit AnsiConsoleBackend(std::ostream& output) : output_(output) {}
    void enter_alternate_screen() override; void leave_alternate_screen() override;
    void hide_cursor() override; void show_cursor() override;
    void write_at(std::size_t row,std::size_t column,const std::string& text) override; void flush() override;
private: std::ostream& output_;
};
}

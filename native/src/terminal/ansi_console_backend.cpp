#include "commerce/terminal/ansi_console_backend.h"
#include <ostream>
namespace commerce::terminal {
void AnsiConsoleBackend::enter_alternate_screen(){output_<<"\x1b[?1049h\x1b[2J";}
void AnsiConsoleBackend::leave_alternate_screen(){output_<<"\x1b[?1049l";}
void AnsiConsoleBackend::hide_cursor(){output_<<"\x1b[?25l";}
void AnsiConsoleBackend::show_cursor(){output_<<"\x1b[?25h";}
void AnsiConsoleBackend::write_at(std::size_t row,std::size_t column,const std::string& text){output_<<"\x1b["<<(row+1)<<';'<<(column+1)<<'H'<<text;}
void AnsiConsoleBackend::flush(){output_.flush();}
}

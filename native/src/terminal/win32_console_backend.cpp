#include "commerce/terminal/win32_console_backend.h"
#include <iostream>
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif
namespace commerce::terminal {
void Win32ConsoleBackend::enter_alternate_screen(){std::cout<<"\x1b[?1049h\x1b[2J";}
void Win32ConsoleBackend::leave_alternate_screen(){std::cout<<"\x1b[?1049l";}
void Win32ConsoleBackend::hide_cursor(){std::cout<<"\x1b[?25l";}
void Win32ConsoleBackend::show_cursor(){std::cout<<"\x1b[?25h";}
void Win32ConsoleBackend::write_at(std::size_t row,std::size_t column,const std::string& text){
#ifdef _WIN32
    const HANDLE handle=GetStdHandle(STD_OUTPUT_HANDLE); const COORD position{static_cast<SHORT>(column),static_cast<SHORT>(row)}; SetConsoleCursorPosition(handle,position); DWORD written=0; WriteConsoleA(handle,text.data(),static_cast<DWORD>(text.size()),&written,nullptr);
#else
    std::cout<<"\x1b["<<(row+1)<<';'<<(column+1)<<'H'<<text;
#endif
}
void Win32ConsoleBackend::flush(){std::cout.flush();}
}

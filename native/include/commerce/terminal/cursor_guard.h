#pragma once
#include "commerce/terminal/console_backend.h"
namespace commerce::terminal {
class CursorGuard final {
public:
 explicit CursorGuard(ConsoleBackend& backend):backend_(backend){backend_.hide_cursor();}
 ~CursorGuard(){backend_.show_cursor();}
 CursorGuard(const CursorGuard&)=delete;CursorGuard& operator=(const CursorGuard&)=delete;
private:ConsoleBackend& backend_;
};
}

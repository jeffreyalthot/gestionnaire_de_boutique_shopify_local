#pragma once
#include "commerce/terminal/console_backend.h"
namespace commerce::terminal {
class AlternateScreen final {
public:
    explicit AlternateScreen(ConsoleBackend& backend):backend_(backend){backend_.enter_alternate_screen();active_=true;}
    ~AlternateScreen(){if(active_)backend_.leave_alternate_screen();}
    AlternateScreen(const AlternateScreen&)=delete; AlternateScreen& operator=(const AlternateScreen&)=delete;
    void close(){if(active_){backend_.leave_alternate_screen();active_=false;}}
private: ConsoleBackend& backend_; bool active_{false};
};
}

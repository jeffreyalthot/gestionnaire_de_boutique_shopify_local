#include "commerce/terminal/screen_layout.h"
#include <cassert>
int main(){commerce::terminal::ScreenLayout l(96,30);l.reserve("header",1);assert(l.width()==96&&l.height()==30&&l.row("header")==1);return 0;}

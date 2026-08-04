#include "commerce/terminal/screen_buffer.h"
#include <cassert>
int main(){commerce::terminal::ScreenBuffer b(23,80);for(std::size_t i=0;i<b.rows();++i)b.set(i,"line");assert(b.rows()==23&&b.line(22).size()==80);return 0;}

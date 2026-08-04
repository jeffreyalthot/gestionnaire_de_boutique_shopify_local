#include "commerce/terminal/input_editor.h"
#include <cassert>
int main(){commerce::terminal::InputEditor e;for(char c:std::string("abcde"))e.insert(c);assert(e.text()=="abcde");e.backspace();assert(e.text()=="abcd");return 0;}

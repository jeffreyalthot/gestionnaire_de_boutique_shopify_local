#include "commerce/terminal/fixed_line_registry.h"
#include <cassert>
int main(){commerce::terminal::FixedLineRegistry r;auto& line=r.register_line("x",2);assert(line.row==2&&r.size()==1);return 0;}

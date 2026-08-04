#include "commerce/terminal/diff_renderer.h"
#include <cassert>
int main(){commerce::terminal::DiffRenderer r;auto a=r.diff({{0,"A"}},5);auto b=r.diff({{0,"A"}},5);assert(a.size()==1&&b.empty());return 0;}

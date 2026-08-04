#include "commerce/terminal/event_ring.h"
#include <cassert>
int main(){commerce::terminal::EventRing r(2);r.push("a");r.push("b");r.push("c");auto v=r.snapshot();assert(v.size()==2&&v[0]=="b"&&v[1]=="c");return 0;}

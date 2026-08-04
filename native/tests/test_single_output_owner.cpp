#include "commerce/runtime/single_output_owner.h"
#include <cassert>
int main(){commerce::runtime::SingleOutputOwner o;assert(o.acquire());assert(!o.acquire());o.release();assert(o.acquire());return 0;}

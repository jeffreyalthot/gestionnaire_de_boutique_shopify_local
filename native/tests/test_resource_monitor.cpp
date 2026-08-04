#include "commerce/runtime/resource_monitor.h"
#include <cassert>
int main(){commerce::runtime::ResourceMonitor m;auto s=m.sample();assert(s.rss_mb>=0.0);return 0;}

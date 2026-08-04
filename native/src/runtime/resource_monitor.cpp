#include "commerce/runtime/resource_monitor.h"
#include <algorithm>
#include <chrono>
#include <ctime>
#include <thread>
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <psapi.h>
#else
#include <sys/resource.h>
#endif
namespace commerce::runtime {
namespace {
double wall_seconds() { using clock=std::chrono::steady_clock; return std::chrono::duration<double>(clock::now().time_since_epoch()).count(); }
double process_cpu_seconds() { return static_cast<double>(std::clock()) / static_cast<double>(CLOCKS_PER_SEC); }
double rss_mb() {
#ifdef _WIN32
    PROCESS_MEMORY_COUNTERS info{}; info.cb=sizeof(info);
    if (GetProcessMemoryInfo(GetCurrentProcess(), &info, sizeof(info)) == 0) return 0.0;
    return static_cast<double>(info.WorkingSetSize) / 1048576.0;
#else
    rusage usage{}; if (getrusage(RUSAGE_SELF,&usage)!=0) return 0.0;
#if defined(__APPLE__)
    return static_cast<double>(usage.ru_maxrss) / 1048576.0;
#else
    return static_cast<double>(usage.ru_maxrss) / 1024.0;
#endif
#endif
}
}
ResourceMonitor::ResourceMonitor() : previous_cpu_seconds_(process_cpu_seconds()), previous_wall_seconds_(wall_seconds()) {}
ResourceSample ResourceMonitor::sample() {
    const double now_cpu=process_cpu_seconds(), now_wall=wall_seconds();
    const double wall_delta=std::max(0.000001,now_wall-previous_wall_seconds_);
    const double cpu=std::clamp((now_cpu-previous_cpu_seconds_)/wall_delta*100.0,0.0,200.0);
    previous_cpu_seconds_=now_cpu; previous_wall_seconds_=now_wall;
    return {rss_mb(),cpu,std::max(1U,std::thread::hardware_concurrency())};
}
}

#pragma once
#include <cstddef>
namespace commerce::runtime {
struct ResourceSample { double rss_mb{0.0}; double cpu_percent{0.0}; std::size_t hardware_threads{1U}; };
class ResourceMonitor final {
public:
    ResourceMonitor();
    [[nodiscard]] ResourceSample sample();
private:
    double previous_cpu_seconds_{0.0};
    double previous_wall_seconds_{0.0};
};
}

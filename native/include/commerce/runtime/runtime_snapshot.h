#pragma once
#include <map>
#include <string>
namespace commerce::runtime {
struct RuntimeSnapshot {
    std::string captured_at;
    std::string mode{"dry_run"};
    double rss_mb{0.0};
    double cpu_percent{0.0};
    std::map<std::string, std::string> metrics;
};
}

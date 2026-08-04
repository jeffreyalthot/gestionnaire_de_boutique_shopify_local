#pragma once
#include <atomic>
namespace commerce::runtime {
class ShutdownController final {
public:
    void request() noexcept { requested_.store(true); }
    void reset() noexcept { requested_.store(false); }
    [[nodiscard]] bool requested() const noexcept { return requested_.load(); }
private:
    std::atomic_bool requested_{false};
};
}

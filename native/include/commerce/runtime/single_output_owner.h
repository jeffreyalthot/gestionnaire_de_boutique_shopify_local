#pragma once
#include <atomic>
namespace commerce::runtime {
class SingleOutputOwner final {
public:
    bool acquire() noexcept;
    void release() noexcept;
    [[nodiscard]] bool owned() const noexcept;
private:
    std::atomic<bool> owned_{false};
};
}

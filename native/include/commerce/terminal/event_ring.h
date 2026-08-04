#pragma once

#include <cstddef>
#include <deque>
#include <mutex>
#include <string>
#include <vector>

namespace commerce::terminal {

class EventRing final {
public:
    explicit EventRing(std::size_t capacity = 6U);
    void push(std::string event);
    [[nodiscard]] std::vector<std::string> snapshot() const;
    [[nodiscard]] std::size_t capacity() const noexcept;

private:
    const std::size_t capacity_;
    mutable std::mutex mutex_;
    std::deque<std::string> events_;
};

}  // namespace commerce::terminal

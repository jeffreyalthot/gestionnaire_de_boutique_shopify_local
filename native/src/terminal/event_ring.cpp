#include "commerce/terminal/event_ring.h"

#include <algorithm>
#include <utility>

namespace commerce::terminal {

EventRing::EventRing(std::size_t capacity) : capacity_(std::max<std::size_t>(1U, capacity)) {}

void EventRing::push(std::string event) {
    std::lock_guard<std::mutex> lock(mutex_);
    if (event.size() > 300U) {
        event.resize(300U);
    }
    events_.push_back(std::move(event));
    while (events_.size() > capacity_) {
        events_.pop_front();
    }
}

std::vector<std::string> EventRing::snapshot() const {
    std::lock_guard<std::mutex> lock(mutex_);
    return {events_.begin(), events_.end()};
}

std::size_t EventRing::capacity() const noexcept {
    return capacity_;
}

}  // namespace commerce::terminal

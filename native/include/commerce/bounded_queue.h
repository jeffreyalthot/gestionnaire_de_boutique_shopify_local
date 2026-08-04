#pragma once

#include <condition_variable>
#include <cstddef>
#include <deque>
#include <mutex>
#include <optional>
#include <utility>

namespace commerce {

template <typename T>
class BoundedQueue final {
public:
    explicit BoundedQueue(std::size_t capacity) : capacity_(capacity == 0 ? 1 : capacity) {}

    BoundedQueue(const BoundedQueue&) = delete;
    BoundedQueue& operator=(const BoundedQueue&) = delete;

    bool try_push(T value) {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            if (closed_ || queue_.size() >= capacity_) {
                return false;
            }
            queue_.push_back(std::move(value));
        }
        not_empty_.notify_one();
        return true;
    }

    std::optional<T> wait_pop() {
        std::unique_lock<std::mutex> lock(mutex_);
        not_empty_.wait(lock, [this] { return closed_ || !queue_.empty(); });
        if (queue_.empty()) {
            return std::nullopt;
        }
        T value = std::move(queue_.front());
        queue_.pop_front();
        return value;
    }

    void close() {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            closed_ = true;
        }
        not_empty_.notify_all();
    }

    [[nodiscard]] std::size_t size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return queue_.size();
    }

    [[nodiscard]] std::size_t capacity() const noexcept {
        return capacity_;
    }

    [[nodiscard]] bool closed() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return closed_;
    }

private:
    const std::size_t capacity_;
    mutable std::mutex mutex_;
    std::condition_variable not_empty_;
    std::deque<T> queue_;
    bool closed_{false};
};

}  // namespace commerce

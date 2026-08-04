#include "commerce/terminal/page_registry.h"

#include <algorithm>
#include <stdexcept>
#include <utility>

namespace commerce::terminal {

void PageRegistry::register_page(std::shared_ptr<Page> page) {
    if (!page || page->key().empty()) {
        throw std::invalid_argument("invalid page");
    }
    const std::string key = page->key();
    if (!pages_.emplace(key, std::move(page)).second) {
        throw std::invalid_argument("duplicate page");
    }
    if (active_key_.empty()) {
        active_key_ = key;
    }
}

bool PageRegistry::remove(const std::string& key) {
    const bool was_active = key == active_key_;
    const bool removed = pages_.erase(key) != 0U;
    if (removed && was_active) {
        active_key_ = pages_.empty() ? std::string{} : pages_.begin()->first;
    }
    return removed;
}

bool PageRegistry::activate(const std::string& key) {
    if (pages_.find(key) == pages_.end()) {
        return false;
    }
    active_key_ = key;
    return true;
}

bool PageRegistry::activate_relative(int direction) {
    if (pages_.empty()) {
        return false;
    }
    auto iterator = pages_.find(active_key_);
    if (iterator == pages_.end()) {
        active_key_ = pages_.begin()->first;
        return true;
    }
    if (direction > 0) {
        ++iterator;
        if (iterator == pages_.end()) {
            iterator = pages_.begin();
        }
    } else {
        if (iterator == pages_.begin()) {
            iterator = pages_.end();
        }
        --iterator;
    }
    active_key_ = iterator->first;
    return true;
}

bool PageRegistry::activate_next() { return activate_relative(1); }
bool PageRegistry::activate_previous() { return activate_relative(-1); }

std::shared_ptr<const Page> PageRegistry::find(const std::string& key) const {
    const auto iterator = pages_.find(key);
    return iterator == pages_.end() ? nullptr : iterator->second;
}

std::shared_ptr<const Page> PageRegistry::active() const { return find(active_key_); }

std::vector<std::string> PageRegistry::keys() const {
    std::vector<std::string> output;
    output.reserve(pages_.size());
    for (const auto& item : pages_) {
        output.push_back(item.first);
    }
    return output;
}

}  // namespace commerce::terminal

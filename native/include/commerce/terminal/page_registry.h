#pragma once

#include "commerce/terminal/page.h"

#include <map>
#include <memory>
#include <string>
#include <vector>

namespace commerce::terminal {

class PageRegistry final {
public:
    void register_page(std::shared_ptr<Page> page);
    bool remove(const std::string& key);
    bool activate(const std::string& key);
    bool activate_next();
    bool activate_previous();

    [[nodiscard]] std::shared_ptr<const Page> find(const std::string& key) const;
    [[nodiscard]] std::shared_ptr<const Page> active() const;
    [[nodiscard]] const std::string& active_key() const noexcept { return active_key_; }
    [[nodiscard]] std::vector<std::string> keys() const;
    [[nodiscard]] std::size_t size() const noexcept { return pages_.size(); }

private:
    bool activate_relative(int direction);
    std::map<std::string, std::shared_ptr<Page>> pages_;
    std::string active_key_;
};

}  // namespace commerce::terminal

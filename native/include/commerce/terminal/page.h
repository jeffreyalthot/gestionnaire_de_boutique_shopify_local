#pragma once
#include <cstddef>
#include <string>
#include <vector>
namespace commerce::terminal { class Page { public: virtual ~Page()=default; [[nodiscard]] virtual std::string key() const=0; [[nodiscard]] virtual std::string title() const=0; [[nodiscard]] virtual std::vector<std::string> render(std::size_t width,std::size_t height) const=0; }; }

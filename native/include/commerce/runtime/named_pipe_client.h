#pragma once
#include <string>
namespace commerce::runtime {
class NamedPipeClient final {
public:
    explicit NamedPipeClient(std::string path) : path_(std::move(path)) {}
    [[nodiscard]] bool send(const std::string& message) const;
    [[nodiscard]] const std::string& path() const noexcept { return path_; }
private:
    std::string path_;
};
}

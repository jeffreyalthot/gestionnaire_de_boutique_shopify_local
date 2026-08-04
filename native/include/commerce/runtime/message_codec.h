#pragma once
#include <map>
#include <string>
namespace commerce::runtime {
class MessageCodec final {
public:
    [[nodiscard]] static std::string encode(const std::map<std::string,std::string>& fields);
    [[nodiscard]] static std::map<std::string,std::string> decode(const std::string& line);
private:
    [[nodiscard]] static std::string escape(const std::string& value);
    [[nodiscard]] static std::string unescape(const std::string& value);
};
}

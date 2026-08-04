#include "commerce/runtime/message_codec.h"

#include <sstream>
#include <stdexcept>

namespace commerce::runtime {

std::string MessageCodec::escape(const std::string& value) {
    std::string out;
    out.reserve(value.size());
    for (const char character : value) {
        if (character == '\\' || character == '=' || character == ';') {
            out.push_back('\\');
        }
        out.push_back(character);
    }
    return out;
}

std::string MessageCodec::unescape(const std::string& value) {
    std::string out;
    bool escaped = false;
    for (const char character : value) {
        if (escaped) {
            out.push_back(character);
            escaped = false;
        } else if (character == '\\') {
            escaped = true;
        } else {
            out.push_back(character);
        }
    }
    if (escaped) {
        throw std::invalid_argument("dangling escape");
    }
    return out;
}

std::string MessageCodec::encode(const std::map<std::string, std::string>& fields) {
    std::ostringstream out;
    bool first = true;
    for (const auto& [key, value] : fields) {
        if (!first) {
            out << ';';
        }
        first = false;
        out << escape(key) << '=' << escape(value);
    }
    return out.str();
}

std::map<std::string, std::string> MessageCodec::decode(const std::string& line) {
    std::map<std::string, std::string> result;
    std::string token;
    bool escaped = false;

    const auto commit = [&]() {
        std::size_t position = std::string::npos;
        bool local_escaped = false;
        for (std::size_t index = 0; index < token.size(); ++index) {
            if (local_escaped) {
                local_escaped = false;
                continue;
            }
            if (token[index] == '\\') {
                local_escaped = true;
                continue;
            }
            if (token[index] == '=') {
                position = index;
                break;
            }
        }
        if (position == std::string::npos) {
            throw std::invalid_argument("missing separator");
        }
        result.emplace(unescape(token.substr(0, position)), unescape(token.substr(position + 1)));
        token.clear();
    };

    for (const char character : line) {
        if (!escaped && character == ';') {
            commit();
            continue;
        }
        token.push_back(character);
        if (escaped) {
            escaped = false;
        } else if (character == '\\') {
            escaped = true;
        }
    }
    if (!token.empty()) {
        commit();
    }
    return result;
}

}  // namespace commerce::runtime

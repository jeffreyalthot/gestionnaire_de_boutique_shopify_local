#include "commerce/commands/command_parser.h"
#include <sstream>
namespace commerce::commands {
ParsedCommand CommandParser::parse(const std::string& line) const {
    ParsedCommand result;
    std::istringstream input(line);
    if (!(input >> result.name)) { result.error = "empty command"; return result; }
    const auto spec = registry_.find(result.name);
    if (!spec) { result.error = "unknown command"; return result; }
    if (spec->amount_required) {
        if (!(input >> result.amount_cad) || result.amount_cad <= 0.0) {
            result.error = "positive CAD amount required"; return result;
        }
    }
    std::string argument;
    while (input >> argument) result.arguments.push_back(argument);
    if (spec->amount_required && !result.arguments.empty()) {
        result.error = "unexpected trailing arguments"; return result;
    }
    result.valid = true;
    return result;
}
}

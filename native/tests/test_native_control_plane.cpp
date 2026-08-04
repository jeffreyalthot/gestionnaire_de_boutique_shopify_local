#include "commerce/commands/command_parser.h"
#include "commerce/commands/command_registry.h"
#include "commerce/runtime/message_codec.h"
#include "commerce/runtime/resource_monitor.h"
#include "commerce/runtime/single_output_owner.h"
#include "commerce/terminal/ascii_sanitizer.h"
#include "commerce/terminal/input_editor.h"
#include "commerce/terminal/progress_bar.h"
#include "commerce/terminal/screen_layout.h"

#include <cstdlib>
#include <iostream>
#include <map>
#include <string>

namespace {
void require(bool value, const char* message) {
    if (!value) { std::cerr << "[FAIL] " << message << '\n'; std::exit(EXIT_FAILURE); }
}
}

int main() {
    commerce::commands::CommandRegistry registry;
    commerce::commands::CommandParser parser(registry);
    const auto purchase = parser.parse("purchase 25.50");
    require(purchase.valid && purchase.amount_cad == 25.50, "parse purchase");
    require(!parser.parse("purchase nope").valid, "reject malformed amount");
    require(!parser.parse("unknown").valid, "reject unknown command");

    const auto encoded = commerce::runtime::MessageCodec::encode({{"key", "a=b;c"}, {"state", "ok"}});
    const auto decoded = commerce::runtime::MessageCodec::decode(encoded);
    require(decoded.at("key") == "a=b;c" && decoded.at("state") == "ok", "message round trip");

    commerce::runtime::SingleOutputOwner owner;
    require(owner.acquire() && !owner.acquire() && owner.owned(), "single owner");
    owner.release(); require(!owner.owned(), "owner release");

    commerce::terminal::ScreenLayout layout(96U, 23U);
    layout.reserve("prompt", 23U);
    require(layout.row("prompt") == 23U, "screen fixed row");
    require(commerce::terminal::ProgressBar::render(0.5, 10U) == "[#####-----]", "progress bar");
    require(commerce::terminal::AsciiSanitizer::sanitize(std::string({'A', static_cast<char>(1), 'B'})) == "A?B", "ascii sanitizer");

    commerce::terminal::InputEditor editor;
    editor.insert('a'); editor.insert('b'); editor.backspace();
    require(editor.text() == "a" && editor.cursor() == 1U, "input editor");

    commerce::runtime::ResourceMonitor monitor;
    const auto sample = monitor.sample();
    require(sample.rss_mb >= 0.0 && sample.hardware_threads >= 1U, "resource sample");
    return EXIT_SUCCESS;
}

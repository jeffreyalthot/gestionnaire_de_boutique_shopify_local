#include "commerce/terminal/diff_renderer.h"
#include "commerce/terminal/event_ring.h"
#include "commerce/terminal/fixed_line_registry.h"

#include <cstdlib>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>

namespace {
void require(bool condition, const char* message) {
    if (!condition) {
        std::cerr << "[FAIL] " << message << '\n';
        std::exit(EXIT_FAILURE);
    }
}
}

int main() {
    commerce::terminal::FixedLineRegistry registry(20U);
    registry.register_line("a", 1U);
    registry.register_line("b", 2U, 10U);
    require(registry.size() == 2U, "registry size");
    require(registry.rows().front().key == "a", "registry row order");
    bool duplicate_rejected = false;
    try {
        registry.register_line("c", 2U);
    } catch (const std::invalid_argument&) {
        duplicate_rejected = true;
    }
    require(duplicate_rejected, "duplicate row rejected");

    commerce::terminal::EventRing ring(2U);
    ring.push("a"); ring.push("b"); ring.push("c");
    const auto events = ring.snapshot();
    require(events.size() == 2U && events[0] == "b" && events[1] == "c", "ring stays fixed");

    commerce::terminal::DiffRenderer renderer;
    auto patches = renderer.diff({{1U, "abc"}, {2U, "def"}}, 8U);
    require(patches.size() == 2U, "initial full render");
    patches = renderer.diff({{1U, "abc"}, {2U, "changed"}}, 8U);
    require(patches.size() == 1U && patches[0].row == 2U, "only changed row rendered");
    require(patches[0].text.size() == 8U, "fixed width maintained");
    return EXIT_SUCCESS;
}

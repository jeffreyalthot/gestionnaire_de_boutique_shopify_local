#include "commerce/runtime/runtime_bridge.h"
#include "commerce/runtime/message_codec.h"
#include <iomanip>
#include <sstream>
namespace commerce::runtime {
bool RuntimeBridge::publish_snapshot(const RuntimeSnapshot& snapshot) const {
    std::map<std::string, std::string> fields = snapshot.metrics;
    fields["type"] = "snapshot"; fields["at"] = snapshot.captured_at; fields["mode"] = snapshot.mode;
    std::ostringstream rss; rss << std::fixed << std::setprecision(2) << snapshot.rss_mb; fields["rss_mb"] = rss.str();
    std::ostringstream cpu; cpu << std::fixed << std::setprecision(2) << snapshot.cpu_percent; fields["cpu_percent"] = cpu.str();
    return client_.send(MessageCodec::encode(fields));
}
bool RuntimeBridge::send_command(const std::string& command, const std::string& payload) const {
    return client_.send(MessageCodec::encode({{"type","command"},{"command",command},{"payload",payload}}));
}
}

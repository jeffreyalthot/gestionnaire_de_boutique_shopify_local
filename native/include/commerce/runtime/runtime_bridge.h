#pragma once
#include "commerce/runtime/named_pipe_client.h"
#include "commerce/runtime/runtime_snapshot.h"
#include <string>
namespace commerce::runtime {
class RuntimeBridge final {
public:
    explicit RuntimeBridge(NamedPipeClient client) : client_(std::move(client)) {}
    [[nodiscard]] bool publish_snapshot(const RuntimeSnapshot& snapshot) const;
    [[nodiscard]] bool send_command(const std::string& command, const std::string& payload) const;
private:
    NamedPipeClient client_;
};
}

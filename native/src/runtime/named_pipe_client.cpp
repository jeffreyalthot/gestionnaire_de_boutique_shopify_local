#include "commerce/runtime/named_pipe_client.h"
#include <fstream>
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif
namespace commerce::runtime {
bool NamedPipeClient::send(const std::string& message) const {
    if (message.size() > 1024U * 1024U || path_.empty()) return false;
#ifdef _WIN32
    HANDLE handle = CreateFileA(path_.c_str(), GENERIC_WRITE, 0, nullptr, OPEN_EXISTING, 0, nullptr);
    if (handle != INVALID_HANDLE_VALUE) {
        DWORD written = 0;
        const BOOL ok = WriteFile(handle, message.data(), static_cast<DWORD>(message.size()), &written, nullptr);
        CloseHandle(handle);
        return ok != 0 && written == message.size();
    }
#endif
    std::ofstream output(path_, std::ios::binary | std::ios::app);
    output.write(message.data(), static_cast<std::streamsize>(message.size()));
    output.put('\n');
    return output.good();
}
}

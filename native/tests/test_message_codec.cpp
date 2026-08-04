#include "commerce/runtime/message_codec.h"
#include <cassert>
int main(){auto e=commerce::runtime::MessageCodec::encode({{"x","a|b"}});auto d=commerce::runtime::MessageCodec::decode(e);assert(d["x"]=="a|b");return 0;}

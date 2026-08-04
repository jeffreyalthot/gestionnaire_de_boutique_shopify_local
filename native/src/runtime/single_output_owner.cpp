#include "commerce/runtime/single_output_owner.h"
namespace commerce::runtime {
bool SingleOutputOwner::acquire() noexcept { bool expected=false; return owned_.compare_exchange_strong(expected,true); }
void SingleOutputOwner::release() noexcept { owned_.store(false); }
bool SingleOutputOwner::owned() const noexcept { return owned_.load(); }
}

#pragma once
#include "commerce/terminal/widget.h"
namespace commerce::terminal { class AlertWidget final:public Widget { public: AlertWidget(std::string level,std::string message):level_(std::move(level)),message_(std::move(message)){} [[nodiscard]] std::string render(std::size_t width) const override; private:std::string level_,message_; }; }

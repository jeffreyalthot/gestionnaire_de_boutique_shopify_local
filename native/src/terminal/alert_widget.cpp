#include "commerce/terminal/alert_widget.h"
#include "commerce/terminal/diff_renderer.h"
namespace commerce::terminal { std::string AlertWidget::render(std::size_t width) const{return DiffRenderer::fit_ascii("["+level_+"] "+message_,width);} }

#include "commerce/terminal/input_editor.h"
namespace commerce::terminal {
void InputEditor::insert(char c){ if(c>=32 && c<=126){ text_.insert(text_.begin()+static_cast<std::ptrdiff_t>(cursor_),c); ++cursor_; } }
void InputEditor::backspace(){ if(cursor_>0U){ text_.erase(cursor_-1U,1U); --cursor_; } }
void InputEditor::clear(){ text_.clear(); cursor_=0U; }
}

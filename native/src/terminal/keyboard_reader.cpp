#include "commerce/terminal/keyboard_reader.h"
#include <iostream>
namespace commerce::terminal {std::optional<std::string> KeyboardReader::read_line(bool blocking) const{if(!blocking&&std::cin.rdbuf()->in_avail()<=0)return std::nullopt;std::string line;if(std::getline(std::cin,line))return line;return std::nullopt;} }

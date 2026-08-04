#include "commerce/commands/command_parser.h"
#include <cassert>
int main(){commerce::commands::CommandRegistry r; commerce::commands::CommandParser p(r);auto c=p.parse("purchase 25");assert(c.valid&&c.amount_cad==25.0);return 0;}

/***************************************************************************\
 *
 *
 *            ___        ___           ___           ___
 *           /  /\      /  /\         /  /\         /  /\
 *          /  /:/     /  /::\       /  /::\       /  /::\
 *         /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
 *        /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
 *       /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
 *      /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
 *      \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
 *           \  \:\   \  \:\        \  \:\        \  \:\
 *            \  \ \   \  \:\        \  \:\        \  \:\
 *             \__\/    \__\/         \__\/         \__\/
 *
 *
 *
 *
 *   This file is part of TRAP.
 *
 *   TRAP is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU Lesser General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU Lesser General Public License for more details.
 *
 *   You should have received a copy of the GNU Lesser General Public License
 *   along with this program; if not, write to the
 *   Free Software Foundation, Inc.,
 *   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 *   or see <http://www.gnu.org/licenses/>.
 *
 *
 *
 *   (c) Luca Fossati, fossati@elet.polimi.it
 *
\***************************************************************************/

#ifndef INSTRUCTIONBASE_HPP
#define INSTRUCTIONBASE_HPP

#include <ostream>
#include <string>

#include <boost/lexical_cast.hpp>

namespace trap{

/// Base class for all instructions; it enables access to the instruction
/// fields from the tools
class InstructionBase{
    public:
        ///Returns the instruction name
        virtual std::string getInstructionName() const throw() = 0;
        ///Returns the instruction mnemonic, so how the current
        ///instruction translated to assebmly code
        virtual std::string getMnemonic() const throw() = 0;
        ///Gets the ID of the instruction as returned by the decoder
        virtual unsigned int getId() const throw() = 0;
};

///Type representing a single entry in the instruction history queue
struct HistoryInstrType{
    unsigned int address;
    std::string name;
    std::string mnemonic;
    unsigned int cycle;

    ///Creates a string representation of the current history element
    std::string toStr() const{
        return boost::lexical_cast<std::string>(this->address) + "\t" + this->name + "\t" + this->mnemonic + "\t" + boost::lexical_cast<std::string>(this->cycle);
    }

    ///Prints the string representation of the current instruction on a stream
    std::ostream & operator <<( std::ostream & other ) const{
        other << this->toStr();
        return other;
    }
};

}

#endif

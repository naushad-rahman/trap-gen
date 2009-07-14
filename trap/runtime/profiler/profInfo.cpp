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

#include "profInfo.hpp"

#include <systemc.h>

#include <string>

#include <boost/lexical_cast.hpp>

///Total number of instructions executed
unsigned long long trap::ProfInstruction::numTotalCalls = 0;
///dump these information to a string,  in the command separated values (CVS) format
std::string trap::ProfInstruction::printCsv(){
    double instrTime = (this->time.to_default_time_units())/(sc_time(1, SC_NS).to_default_time_units());
    std::string csvLine(this->name + ";");
    csvLine += boost::lexical_cast<std::string>(this->numCalls) + ";";
    csvLine += boost::lexical_cast<std::string>(((double)this->numCalls*100)/ProfInstruction::numTotalCalls) + ";";
    csvLine += boost::lexical_cast<std::string>(instrTime) + ";";
    csvLine += boost::lexical_cast<std::string>(instrTime/this->numCalls);
    return csvLine;
}
///Prints the description of the informations which describe an instruction,  in the command separated values (CVS) format
std::string trap::ProfInstruction::printCsvHeader(){
    return "name;numCalls;numCalls %;time;Time per call";
}
///Empty constructor, performs the initialization of the statistics
trap::ProfInstruction::ProfInstruction(){
    this->numCalls = 1;
    this->time = SC_ZERO_TIME;
}


///Total number of function calls
unsigned long long trap::ProfFunction::numTotalCalls = 0;
///dump these information to a string, in the command separated values (CVS) format
std::string trap::ProfFunction::printCsv(){
    double funTotTime = (this->totalTime.to_default_time_units())/(sc_time(1, SC_NS).to_default_time_units());
    double funExclTime = (this->exclTime.to_default_time_units())/(sc_time(1, SC_NS).to_default_time_units());
    std::string csvLine(this->name + ";");
    csvLine += boost::lexical_cast<std::string>(this->numCalls) + ";";
    csvLine += boost::lexical_cast<std::string>(((double)this->numCalls*100)/ProfFunction::numTotalCalls) + ";";
    csvLine += boost::lexical_cast<std::string>(this->totalNumInstr) + ";";
    csvLine += boost::lexical_cast<std::string>(this->exclNumInstr) + ";";
    csvLine += boost::lexical_cast<std::string>(((double)this->exclNumInstr)/this->numCalls) + ";";
    csvLine += boost::lexical_cast<std::string>(funTotTime) + ";";
    csvLine += boost::lexical_cast<std::string>(funExclTime) + ";";
    csvLine += boost::lexical_cast<std::string>(funExclTime/this->numCalls);
    return csvLine;
}
///Prints the description of the informations which describe a function, in the command separated values (CVS) format
std::string trap::ProfFunction::printCsvHeader(){
    return "name;numCalls;numCalls %;totalNumInstr;exclNumInstr;NumInstr per call;totalTime;exclTime;Time per call";
}
///Empty constructor, performs the initialization of the statistics
trap::ProfFunction::ProfFunction(){
    this->numCalls = 1;
    this->totalTime = SC_ZERO_TIME;
    this->exclTime = SC_ZERO_TIME;
    this->totalNumInstr = 0;
    this->exclNumInstr = 0;
}
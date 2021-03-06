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
 *   the Free Software Foundation; either version 3 of the License, or
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
 *   (c) Luca Fossati, fossati@elet.polimi.it, fossati.l@gmail.com
 *
\***************************************************************************/

#include <ctype.h>
#include <cstring>

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>

#include <boost/filesystem.hpp>

#include <boost/lexical_cast.hpp>

#include "trap_utils.hpp"

#include "memAccessType.hpp"
#include "analyzer.hpp"

///Given an array of chars (either in hex or decimal form) if converts it to the
///corresponding integer representation
unsigned int trap::MemAnalyzer::toIntNum(const std::string &numStr){
    if(numStr.size() > 2 && numStr[0] == '0' && tolower(numStr[1]) == 'x'){
        int result;
        std::stringstream converter(numStr);
        converter >> std::hex >> result;
        return result;
    }
    else{
        //It still might be the string does not start with 0x but it is still a hex number;
        //I also have to check that it is a valid string
        bool ishex = false;
        for(unsigned int i = 0; i < numStr.size(); i++){
            if(tolower(numStr[i]) >= 'a' && tolower(numStr[i]) <= 'f'){
                ishex = true;
            }else if (tolower(numStr[i]) > 'f' || (tolower(numStr[i]) < 'a' && tolower(numStr[i]) > '9')  || tolower(numStr[i]) < '0'){
                THROW_EXCEPTION(numStr << " is not a valid number");
            }
        }
        if(ishex){
            int result;
            std::stringstream converter(numStr);
            converter >> std::hex >> result;
            return result;
        }
        else
            return boost::lexical_cast<int>(numStr);
    }
    return 0;
}

trap::MemAnalyzer::MemAnalyzer(std::string fileName, std::string memSize){
    this->memSize = this->toIntNum(memSize);
    boost::filesystem::path memDumpPath = boost::filesystem::system_complete(boost::filesystem::path(fileName));
    if ( !boost::filesystem::exists( memDumpPath ) ){
        THROW_EXCEPTION("Path " << fileName << " specified for the memory dump does not exists");
    }
    else{
        this->dumpFile.open(fileName.c_str(), std::ifstream::in | std::ifstream::binary);
        if(!this->dumpFile.good())
            THROW_EXCEPTION("Error in opening file " << fileName);
    }
}

trap::MemAnalyzer::~MemAnalyzer(){
    if(this->dumpFile.is_open()){
        this->dumpFile.close();
    }
}

///Creates the image of the memory as it was at cycle procCycle
void trap::MemAnalyzer::createMemImage(boost::filesystem::path &outFile, double simTime){
    char * tempMemImage = new char[this->memSize];
    MemAccessType readVal;
    unsigned int maxAddress = 0;

    ::bzero(tempMemImage, this->memSize);

    while(this->dumpFile.good()){
        this->dumpFile.read((char *)&readVal, sizeof(MemAccessType));
        if(this->dumpFile.good()){
            if(readVal.simulationTime > simTime && simTime > 0) //I've reached the desired cycle
                break;
            if(readVal.address < this->memSize){
                tempMemImage[readVal.address] = readVal.val;
                if(readVal.address > maxAddress)
                    maxAddress = readVal.address;
            }
        }
    }
    this->dumpFile.seekg(std::ifstream::beg);

    //Now I print on the output file the memory image
    std::ofstream memImageFile(outFile.string().c_str());
    for(int i = 0; i < maxAddress; i+=sizeof(int)){
        memImageFile << "MEM[" << std::hex << std::showbase << i << "] = " << ((int *)tempMemImage)[i/sizeof(int)] << std::endl;
    }
    memImageFile.close();
    delete [] tempMemImage;
}

///Returns the first memory access that modifies the address addr after
///procCycle
std::map<unsigned int, trap::MemAccessType> trap::MemAnalyzer::getFirstModAfter(std::string addr, unsigned int width, double simTime){
    MemAccessType readVal;
    std::map<unsigned int, trap::MemAccessType> retVal;
    unsigned int address = this->toIntNum(addr);

    while(this->dumpFile.good()){
        this->dumpFile.read((char *)&readVal, sizeof(MemAccessType));
        if(this->dumpFile.good()){
            if(readVal.simulationTime >= simTime && readVal.address >= address && readVal.address < (address + width)){
                if(retVal.find(readVal.address) == retVal.end()){
                    retVal[readVal.address] = readVal;
                    if(retVal.size() == width){
                        this->dumpFile.seekg(std::ifstream::beg);
                        return retVal;
                    }
                }
            }
        }
    }

    THROW_EXCEPTION("No modifications performed to address " << std::hex << std::showbase << address);
    this->dumpFile.seekg(std::ifstream::beg);

    return retVal;
}

///Returns the last memory access that modified addr
std::map<unsigned int, trap::MemAccessType> trap::MemAnalyzer::getLastMod(std::string addr, unsigned int width){
    MemAccessType readVal;
    std::map<unsigned int, trap::MemAccessType> foundVal;
    bool found = false;
    unsigned int address = this->toIntNum(addr);

    while(this->dumpFile.good()){
        this->dumpFile.read((char *)&readVal, sizeof(MemAccessType));
        if(this->dumpFile.good()){
            if(readVal.address >= address && readVal.address < (address + width)){
                foundVal[readVal.address] = readVal;
            }
        }
    }

    if(foundVal.size() == 0)
        THROW_EXCEPTION("No modifications performed to address " << std::hex << std::showbase << address);

    this->dumpFile.seekg(std::ifstream::beg);
    return foundVal;
}

///Prints all the modifications done to address addr
void trap::MemAnalyzer::getAllModifications(std::string addr, boost::filesystem::path &outFile, unsigned int width, double initSimTime, double endSimTime){
    MemAccessType readVal;
    unsigned int address = this->toIntNum(addr);
    std::ofstream memImageFile(outFile.string().c_str());

    while(this->dumpFile.good()){
        this->dumpFile.read((char *)&readVal, sizeof(MemAccessType));
        if(this->dumpFile.good()){
            if(readVal.address >= address && readVal.address < (address + width) && readVal.simulationTime >= initSimTime && (endSimTime < 0 || readVal.simulationTime <= endSimTime)){
                memImageFile << "MEM[" << std::hex << std::showbase << readVal.address << "] = " << (int)readVal.val << " time " << std::dec << readVal.simulationTime << " program counter " << std::hex << std::showbase << readVal.programCounter << std::endl;
            }
        }
    }

    memImageFile.close();
    this->dumpFile.seekg(std::ifstream::beg);
}

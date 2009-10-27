# -*- coding: iso-8859-1 -*-
####################################################################################
#         ___        ___           ___           ___
#        /  /\      /  /\         /  /\         /  /\
#       /  /:/     /  /::\       /  /::\       /  /::\
#      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
#     /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
#    /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
#   /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
#   \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
#        \  \:\   \  \:\        \  \:\        \  \:\
#         \  \ \   \  \:\        \  \:\        \  \:\
#          \__\/    \__\/         \__\/         \__\/
#
#   This file is part of TRAP.
#
#   TRAP is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this TRAP; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA.
#   or see <http://www.gnu.org/licenses/>.
#
#   (c) Luca Fossati, fossati@elet.polimi.it
#
####################################################################################

import cxx_writer

readMethodNames = ['read_dword', 'read_word', 'read_half', 'read_byte']
readMethodNames_dbg = ['read_dword_dbg', 'read_word_dbg', 'read_half_dbg', 'read_byte_dbg']
writeMethodNames = ['write_dword', 'write_word', 'write_half', 'write_byte']
writeMethodNames_dbg = ['write_dword_dbg', 'write_word_dbg', 'write_half_dbg', 'write_byte_dbg']
genericMethodNames = ['lock', 'unlock']

methodTypes = None
methodTypeLen = None

def addMemoryMethods(self, memoryElements, methodsCode, methodsAttrs):
    archDWordType = self.bitSizes[0]
    archWordType = self.bitSizes[1]
    archHWordType = self.bitSizes[2]
    archByteType = self.bitSizes[3]

    addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
    for methName in readMethodNames + readMethodNames_dbg:
        if methName in methodsCode.keys() and methName in methodsAttrs.keys():
            readDecl = cxx_writer.writer_code.Method(methName, methodsCode[methName], methodTypes[methName], 'pu', [addressParam], inline = 'inline' in methodsAttrs[methName], pure = 'pure' in methodsAttrs[methName], virtual = 'virtual'  in methodsAttrs[methName], const = len(self.tlmPorts) == 0, noException = 'noexc'  in methodsAttrs[methName])
            memoryElements.append(readDecl)
    for methName in writeMethodNames + writeMethodNames_dbg:
        if methName in methodsCode.keys() and methName in methodsAttrs.keys():
            datumParam = cxx_writer.writer_code.Parameter('datum', methodTypes[methName])
            writeDecl = cxx_writer.writer_code.Method(methName, methodsCode[methName], cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], inline = 'inline' in methodsAttrs[methName], pure = 'pure' in methodsAttrs[methName], virtual = 'virtual'  in methodsAttrs[methName], noException = 'noexc'  in methodsAttrs[methName])
            memoryElements.append(writeDecl)

    for methName in genericMethodNames:
        if methName in methodsCode.keys() and methName in methodsAttrs.keys():
            lockDecl = cxx_writer.writer_code.Method(methName, methodsCode[methName], cxx_writer.writer_code.voidType, 'pu', inline = 'inline' in methodsAttrs[methName], pure = 'pure' in methodsAttrs[methName], virtual = 'virtual'  in methodsAttrs[methName], noException = 'noexc'  in methodsAttrs[methName])
            memoryElements.append(lockDecl)

def getCPPMemoryIf(self, model, namespace):
    # Creates the necessary structures for communicating with the memory; an
    # array in case of an internal memory, the TLM port for the use with TLM
    # etc.
    from procWriter import resourceType

    archDWordType = self.bitSizes[0]
    archWordType = self.bitSizes[1]
    archHWordType = self.bitSizes[2]
    archByteType = self.bitSizes[3]

    global methodTypes, methodTypeLen
    methodTypes = {'read_dword': archDWordType, 'read_word': archWordType, 'read_half': archHWordType, 'read_byte': archByteType,
                'read_dword_dbg': archDWordType, 'read_word_dbg': archWordType, 'read_half_dbg': archHWordType, 'read_byte_dbg': archByteType,
                'write_dword': archDWordType, 'write_word': archWordType, 'write_half': archHWordType, 'write_byte': archByteType,
                'write_dword_dbg': archDWordType, 'write_word_dbg': archWordType, 'write_half_dbg': archHWordType, 'write_byte_dbg': archByteType}
    methodTypeLen = {'read_dword': self.wordSize*2, 'read_word': self.wordSize, 'read_half': self.wordSize/2, 'read_byte': 1,
                    'read_dword_dbg': self.wordSize*2, 'read_word_dbg': self.wordSize, 'read_half_dbg': self.wordSize/2, 'read_byte_dbg': 1,
                    'write_dword': self.wordSize*2, 'write_word': self.wordSize, 'write_half': self.wordSize/2, 'write_byte': 1,
                    'write_dword_dbg': self.wordSize*2, 'write_word_dbg': self.wordSize, 'write_half_dbg': self.wordSize/2, 'write_byte_dbg': 1}

    classes = []
    memoryIfElements = []
    emptyBody = cxx_writer.writer_code.Code('')

    #############################################################
    # Creation of the memory base class
    #############################################################
    methodsCode = {}
    methodsAttrs = {}
    for methName in readMethodNames + writeMethodNames:
        methodsAttrs[methName] = ['pure', 'noexc']
        methodsCode[methName] = emptyBody
    for methName in readMethodNames_dbg:
        methodsAttrs[methName] = ['virtual']
        methodsCode[methName] = cxx_writer.writer_code.Code('return this->' + methName[:-4] + '(address);')
    for methName in writeMethodNames_dbg:
        methodsAttrs[methName] = ['virtual']
        methodsCode[methName] = cxx_writer.writer_code.Code('this->' + methName[:-4] + '(address, datum);')
    for methName in genericMethodNames:
        methodsAttrs[methName] = ['pure']
        methodsCode[methName] = emptyBody
    addMemoryMethods(self, memoryIfElements, methodsCode, methodsAttrs)

    for curType in [archWordType, archHWordType]:
        swapEndianessCode = str(archByteType) + """ helperByte = 0;
        for(int i = 0; i < sizeof(""" + str(curType) + """)/2; i++){
            helperByte = ((""" + str(archByteType) + """ *)&datum)[i];
            ((""" + str(archByteType) + """ *)&datum)[i] = ((""" + str(archByteType) + """ *)&datum)[sizeof(""" + str(curType) + """) -1 -i];
            ((""" + str(archByteType) + """ *)&datum)[sizeof(""" + str(curType) + """) -1 -i] = helperByte;
        }
        """
        swapEndianessBody = cxx_writer.writer_code.Code(swapEndianessCode)
        datumParam = cxx_writer.writer_code.Parameter('datum', curType.makeRef())
        swapEndianessDecl = cxx_writer.writer_code.Method('swapEndianess', swapEndianessBody, cxx_writer.writer_code.voidType, 'pu', [datumParam], inline = True, noException = True, const = True)
        memoryIfElements.append(swapEndianessDecl)

    memoryIfDecl = cxx_writer.writer_code.ClassDeclaration('MemoryInterface', memoryIfElements, namespaces = [namespace])
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    memoryIfDecl.addDestructor(publicDestr)
    classes.append(memoryIfDecl)

    ############################################################
    # Now I finally create an instance of the local memory
    ############################################################
    memoryElements = []
    readMemAliasCode = ''
    writeMemAliasCode = ''
    aliasAttrs = []
    aliasParams = []
    aliasInit = []
    MemoryToolsIfType = cxx_writer.writer_code.TemplateType('MemoryToolsIf', [str(archWordType)], 'ToolsIf.hpp')
    for alias in self.memAlias:
        aliasAttrs.append(cxx_writer.writer_code.Attribute(alias.alias, resourceType[alias.alias].makeRef(), 'pri'))
        aliasParams.append(cxx_writer.writer_code.Parameter(alias.alias, resourceType[alias.alias].makeRef()))
        aliasInit.append(alias.alias + '(' + alias.alias + ')')
        readMemAliasCode += 'if(address == ' + hex(long(alias.address)) + '){\nreturn this->' + alias.alias + ';\n}\n'
        writeMemAliasCode += 'if(address == ' + hex(long(alias.address)) + '){\n this->' + alias.alias + ' = datum;\nreturn;\n}\n'

    checkAddressCode = 'if(address >= this->size){\nTHROW_ERROR("Address " << std::hex << std::showbase << address << " out of memory");\n}\n'
    checkAddressCodeException = 'if(address >= this->size){\nTHROW_EXCEPTION("Address " << std::hex << std::showbase << address << " out of memory");\n}\n'

    if self.isBigEndian:
        swapEndianessCode = '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        swapEndianessCode = '#ifdef BIG_ENDIAN_BO\n'
    swapEndianessCode += 'this->swapEndianess(datum);\n#endif\n'
    if self.isBigEndian:
        swapDEndianessCode = '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        swapDEndianessCode = '#ifdef BIG_ENDIAN_BO\n'
    swapDEndianessCode += str(archWordType) + ' datum1 = (' + str(archWordType) + ')(datum);\nthis->swapEndianess(datum1);\n'
    swapDEndianessCode += str(archWordType) + ' datum2 = (' + str(archWordType) + ')(datum >> ' + str(self.wordSize*self.byteSize) + ');\nthis->swapEndianess(datum2);\n'
    swapDEndianessCode += 'datum = datum1 | (((' + str(archDWordType) + ')datum2) << ' + str(self.wordSize*self.byteSize) + ');\n#endif\n'

    memoryElements.append(cxx_writer.writer_code.Attribute('debugger', MemoryToolsIfType.makePointer(), 'pri'))
    setDebuggerBody = cxx_writer.writer_code.Code('this->debugger = debugger;')
    memoryElements.append(cxx_writer.writer_code.Method('setDebugger', setDebuggerBody, cxx_writer.writer_code.voidType, 'pu', [cxx_writer.writer_code.Parameter('debugger', MemoryToolsIfType.makePointer())]))
    checkWatchPointCode = """if(this->debugger != NULL){
        this->debugger->notifyAddress(address, sizeof(datum));
    }
    """
    endianessCode = {'read_dword': swapDEndianessCode, 'read_word': swapEndianessCode, 'read_half': swapEndianessCode, 'read_byte': '',
                'read_dword_dbg': swapDEndianessCode, 'read_word_dbg': swapEndianessCode, 'read_half_dbg': swapEndianessCode, 'read_byte_dbg': '',
                'write_dword': swapDEndianessCode, 'write_word': swapEndianessCode, 'write_half': swapEndianessCode, 'write_byte': '',
                'write_dword_dbg': swapDEndianessCode, 'write_word_dbg': swapEndianessCode, 'write_half_dbg': swapEndianessCode, 'write_byte_dbg': ''}

    # If there is no memory or there is a memory and this has debugging disabled
    if not self.memory or not self.memory[2]:
        methodsCode = {}
        methodsAttrs = {}
        for methName in readMethodNames + readMethodNames_dbg:
            methodsAttrs[methName] = []
            if methName.endswith('_gdb'):
                readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCodeException + '\n' + str(methodTypes[methName]) + ' datum = *(' + str(methodTypes[methName].makePointer()) + ')(this->memory + (unsigned long)address);\n' + endianessCode[methName] + '\nreturn datum;')
            else:
                methodsAttrs[methName].append('noexc')
                readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + '\n' + str(methodTypes[methName]) + ' datum = *(' + str(methodTypes[methName].makePointer()) + ')(this->memory + (unsigned long)address);\n' + endianessCode[methName] + '\nreturn datum;')
                if methName == 'read_word':
                    methodsAttrs[methName].append('inline')
            readBody.addInclude('trap_utils.hpp')
            methodsCode[methName] = readBody
        for methName in writeMethodNames + writeMethodNames_dbg:
            methodsAttrs[methName] = []
            if methName.endswith('_gdb'):
                methodsCode[methName] = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCodeException + checkWatchPointCode + '\n' + endianessCode[methName] + '\n*(' + str(methodTypes[methName].makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
            else:
                methodsAttrs[methName].append('noexc')
                methodsCode[methName] = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + checkWatchPointCode + '\n' + endianessCode[methName] + '\n*(' + str(methodTypes[methName].makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
                if methName == 'write_word':
                    methodsAttrs[methName].append('inline')
        for methName in genericMethodNames:
            methodsAttrs[methName] = []
            methodsCode[methName] = emptyBody
        addMemoryMethods(self, memoryElements, methodsCode, methodsAttrs)

        arrayAttribute = cxx_writer.writer_code.Attribute('memory', cxx_writer.writer_code.charPtrType, 'pri')
        memoryElements.append(arrayAttribute)
        sizeAttribute = cxx_writer.writer_code.Attribute('size', cxx_writer.writer_code.uintType, 'pri')
        memoryElements.append(sizeAttribute)
        memoryElements += aliasAttrs
        localMemDecl = cxx_writer.writer_code.ClassDeclaration('LocalMemory', memoryElements, [memoryIfDecl.getType()], namespaces = [namespace])
        constructorBody = cxx_writer.writer_code.Code('this->memory = new char[size];\nthis->debugger = NULL;')
        constructorParams = [cxx_writer.writer_code.Parameter('size', cxx_writer.writer_code.uintType)]
        publicMemConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams + aliasParams, ['size(size)'] + aliasInit)
        localMemDecl.addConstructor(publicMemConstr)
        destructorBody = cxx_writer.writer_code.Code('delete [] this->memory;')
        publicMemDestr = cxx_writer.writer_code.Destructor(destructorBody, 'pu', True)
        localMemDecl.addDestructor(publicMemDestr)
        classes.append(localMemDecl)
    else:
        # Here I have a local memory with debugging enabled.
        dumpCode1 = 'MemAccessType dumpInfo;\n'
        if not self.systemc and not model.startswith('acc')  and not model.endswith('AT'):
            dumpCode += 'dumpInfo.simulationTime = curCycle;\n'
        else:
            dumpCode += 'dumpInfo.simulationTime = sc_time_stamp().to_double();\n'
        if self.memory[3]:
            dumpCode += 'dumpInfo.programCounter = this->' + self.memory[3] + ';\n'
        else:
            dumpCode += 'dumpInfo.programCounter = 0;\n'
        dumpCode += 'for(int i = 0; i < '
        dumpCode2 = """; i++){
    dumpInfo.address = address + i;
    dumpInfo.val = (char)((datum & (0xFF << i*8)) >> i*8);
    this->dumpFile.write((char *)&dumpInfo, sizeof(MemAccessType));
}
"""

        methodsCode = {}
        methodsAttrs = {}
        for methName in readMethodNames + readMethodNames_dbg:
            methodsAttrs[methName] = ['noexc']
            if methName.endswith('_gdb'):
                readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCodeException + '\n' + str(methodTypes[methName]) + ' datum = *(' + str(methodTypes[methName].makePointer()) + ')(this->memory + (unsigned long)address);\n' + endianessCode[methName] + '\nreturn datum;')
            else:
                readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + '\n' + str(methodTypes[methName]) + ' datum = *(' + str(methodTypes[methName].makePointer()) + ')(this->memory + (unsigned long)address);\n' + endianessCode[methName] + '\nreturn datum;')
                if methName == 'read_word':
                    methodsAttrs[methName],append('inline')
            readBody.addInclude('trap_utils.hpp')
            methodsCode[methName] = readBody
        for methName in writeMethodNames + writeMethodNames_dbg:
            methodsAttrs[methName] = []
            if methName.endswith('_gdb'):
                methodsCode[methName] = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCodeException + checkWatchPointCode + '\n' + endianessCode[methName] + '\n*(' + str(methodTypes[methName].makePointer()) + ')(this->memory + (unsigned long)address) = datum;' + dumpCode1 + str(methodTypeLen[methName]) + dumpCode2)
            else:
                methodsAttrs[methName].append('noexc')
                methodsCode[methName] = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + checkWatchPointCode + '\n' + endianessCode[methName] + '\n*(' + str(methodTypes[methName].makePointer()) + ')(this->memory + (unsigned long)address) = datum;' + dumpCode1 + str(methodTypeLen[methName]) + dumpCode2)
                if methName == 'write_word':
                    methodsAttrs[methName].append('inline')
        for methName in genericMethodNames:
            methodsAttrs[methName] = []
            methodsCode[methName] = emptyBody
        addMemoryMethods(self, memoryElements, methodsCode, methodsAttrs)

        endOfSimBody = cxx_writer.writer_code.Code("""if(this->dumpFile){
           this->dumpFile.flush();
           this->dumpFile.close();
        }
        """)
        endOfSimDecl = cxx_writer.writer_code.Method('end_of_simulation', endOfSimBody, cxx_writer.writer_code.voidType, 'pu')
        memoryElements.append(endOfSimDecl)

        constructorParams = [cxx_writer.writer_code.Parameter('size', cxx_writer.writer_code.uintType)]
        constructorInit = ['size(size)']

        arrayAttribute = cxx_writer.writer_code.Attribute('memory', cxx_writer.writer_code.charPtrType, 'pri')
        memoryElements.append(arrayAttribute)

        if not self.systemc and not model.startswith('acc') and not model.endswith('AT'):
            cycleAttribute = cxx_writer.writer_code.Attribute('curCycle', cxx_writer.writer_code.uintType.makeRef(), 'pri')
            constructorParams.append(cxx_writer.writer_code.Parameter('curCycle', cxx_writer.writer_code.uintType.makeRef()))
            constructorInit.append('curCycle(curCycle)')
            memoryElements.append(cycleAttribute)

        sizeAttribute = cxx_writer.writer_code.Attribute('size', cxx_writer.writer_code.uintType, 'pri')
        memoryElements.append(sizeAttribute)
        dumpFileAttribute = cxx_writer.writer_code.Attribute('dumpFile', cxx_writer.writer_code.ofstreamType, 'pri')
        memoryElements.append(dumpFileAttribute)
        memoryElements += aliasAttrs
        if self.memory[3]:
            memoryElements.append(cxx_writer.writer_code.Attribute(self.memory[3], resourceType[self.memory[3]].makeRef(), 'pri'))
            pcRegParam = [cxx_writer.writer_code.Parameter(self.memory[3], resourceType[self.memory[3]].makeRef())]
            pcRegInit = [self.memory[3] + '(' + self.memory[3] + ')']
        localMemDecl = cxx_writer.writer_code.ClassDeclaration('LocalMemory', memoryElements, [memoryIfDecl.getType()], namespaces = [namespace])
        constructorBody = cxx_writer.writer_code.Code("""this->memory = new char[size];
            this->debugger = NULL;
            this->dumpFile.open("memoryDump.dmp", ios::out | ios::binary | ios::ate);
            if(!this->dumpFile){
                THROW_EXCEPTION("Error in opening file memoryDump.dmp for writing");
            }
        """)
        publicMemConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams + aliasParams + pcRegParam, constructorInit + aliasInit + pcRegInit)
        localMemDecl.addConstructor(publicMemConstr)
        destructorBody = cxx_writer.writer_code.Code("""delete [] this->memory;
        if(this->dumpFile){
           this->dumpFile.flush();
           this->dumpFile.close();
        }
        """)
        publicMemDestr = cxx_writer.writer_code.Destructor(destructorBody, 'pu', True)
        localMemDecl.addDestructor(publicMemDestr)
        classes.append(localMemDecl)

    return classes
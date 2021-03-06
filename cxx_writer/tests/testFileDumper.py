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
#   the Free Software Foundation; either version 3 of the License, or
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
#   (c) Luca Fossati, fossati@elet.polimi.it, fossati.l@gmail.com
#
####################################################################################


import unittest
import writer_code
import os

class TestFileDumper(unittest.TestCase):

    def testDumpVariablesImpl(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Variable('pippo', tempType)
        dumper = writer_code.FileDumper('prova.cpp', False)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 4 + 15)
        self.assertEqual(lines[14], '#include <map>\n')
        self.assertEqual(lines[15], '#include <string>\n')
        self.assertEqual(lines[17], 'std::map< int, std::string > pippo;\n')

    def testDumpVariablesHeader(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Variable('pippo', tempType)
        dumper = writer_code.FileDumper('prova.cpp', True)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 3 + 19)
        self.assertEqual(lines[16], '#include <map>\n')
        self.assertEqual(lines[17], '#include <string>\n')
        self.assertEqual(lines[18], '\n')
        self.assertEqual(lines[19], '\n')
        self.assertEqual(lines[20], '\n')

    def testDumpFunctionsHeader(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Function('pippo', writer_code.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType)
        dumper = writer_code.FileDumper('prova.cpp', True)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 4 + 19)
        self.assertEqual(lines[16], '#include <map>\n')
        self.assertEqual(lines[17], '#include <string>\n')
        self.assertEqual(lines[19], 'std::map< int, std::string > pippo();\n')

    def testDumpFunctionsImpl(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Function('pippo', writer_code.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType)
        dumper = writer_code.FileDumper('prova.cpp', False)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 8 + 15)
        self.assertEqual(lines[14], '#include <map>\n')
        self.assertEqual(lines[15], '#include <string>\n')
        self.assertEqual(lines[17], 'std::map< int, std::string > pippo(){\n')
        self.assertEqual(lines[18], '    std::map<int, std::string> myMap;\n')
        self.assertEqual(lines[19], '    myMap[5] = \"ccc\";\n')
        self.assertEqual(lines[20], '    return myMap;\n')
        self.assertEqual(lines[21], '}\n')

    def testTemplateFunctionsHeader(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Function('pippo', writer_code.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType, [], False, False, ['T'])
        dumper = writer_code.FileDumper('prova.cpp', True)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 8 + 19)
        self.assertEqual(lines[16], '#include <map>\n')
        self.assertEqual(lines[17], '#include <string>\n')
        self.assertEqual(lines[19], 'template < typename T > std::map< int, std::string > pippo(){\n')
        self.assertEqual(lines[20], '    std::map<int, std::string> myMap;\n')
        self.assertEqual(lines[21], '    myMap[5] = \"ccc\";\n')
        self.assertEqual(lines[22], '    return myMap;\n')
        self.assertEqual(lines[23], '}\n')

    def testTemplateFunctionsImpl(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Function('pippo', writer_code.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType, [], False, ['T'])
        dumper = writer_code.FileDumper('prova.cpp', False)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 3 + 15)
        self.assertEqual(lines[14], '#include <map>\n')
        self.assertEqual(lines[15], '#include <string>\n')

    def testDumpClassHeader(self):
        intDecl = writer_code.intType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu')
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        dumper = writer_code.FileDumper('prova.cpp', True)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 8 + 19)
        self.assertEqual(lines[16], 'class MyClass{\n')
        self.assertEqual(lines[17], '    private:\n')
        self.assertEqual(lines[18], '    int pippo;\n')
        self.assertEqual(lines[19], '\n')
        self.assertEqual(lines[20], '    public:\n')
        self.assertEqual(lines[21], '    MyClass();\n')
        self.assertEqual(lines[22], '};\n')


    def testDumpClassImpl(self):
        intDecl = writer_code.intType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu')
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        dumper = writer_code.FileDumper('prova.cpp', False)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 4 + 15)
        self.assertEqual(lines[14], 'MyClass::MyClass(){\n')
        self.assertEqual(lines[15], '\n')
        self.assertEqual(lines[16], '}\n')


    def testDumpTemplateClassHeader(self):
        intDecl = writer_code.intType
        stringDecl = writer_code.stringType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu', [], ['std::string()'])
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar], [stringDecl], ['T'])
        classDecl.addConstructor(publicConstr)
        dumper = writer_code.FileDumper('prova.cpp', True)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 12 + 20)
        self.assertEqual(lines[18], 'template < typename T > class MyClass : public std::string{\n')
        self.assertEqual(lines[19], '    private:\n')
        self.assertEqual(lines[20], '    int pippo;\n')
        self.assertEqual(lines[21], '\n')
        self.assertEqual(lines[22], '    public:\n')
        self.assertEqual(lines[23], '    MyClass() : std::string(){\n')
        self.assertEqual(lines[24], '\n')
        self.assertEqual(lines[25], '    }\n')
        self.assertEqual(lines[26], '\n')
        self.assertEqual(lines[27], '};\n')

    def testDumpTemplateClassImpl(self):
        intDecl = writer_code.intType
        stringDecl = writer_code.stringType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu', [], ['std::string()'])
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar], [stringDecl], ['T'])
        classDecl.addConstructor(publicConstr)
        dumper = writer_code.FileDumper('prova.cpp', False)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 1 + 16)

    def testEmptyFolder(self):
        folder = writer_code.Folder('')
        folder.create()
        os.remove('wscript')

    def testEmptyFolder(self):
        folder = writer_code.Folder('temp/try')
        folder.create()
        self.assert_(os.path.exists('temp/try/wscript'))
        os.remove('temp/try/wscript')
        import shutil
        shutil.rmtree('temp', True)

    def testDumpAll(self):
        folder = writer_code.Folder('temp')
        intDecl = writer_code.intType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu')
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        implFile = writer_code.FileDumper('prova.cpp', False)
        implFile.addMember(classDecl)
        headFile = writer_code.FileDumper('prova.hpp', True)
        headFile.addMember(classDecl)
        folder.addHeader(headFile)
        folder.addCode(implFile)
        folder.create()
        testImplFile = open('temp/prova.cpp', 'rt')
        lines = testImplFile.readlines()
        testImplFile.close()
        os.remove('temp/prova.cpp')
        self.assertEqual(len(lines), 19)
        self.assertEqual(lines[14], 'MyClass::MyClass(){\n')
        self.assertEqual(lines[15], '\n')
        self.assertEqual(lines[16], '}\n')
        testHeadFile = open('temp/prova.hpp', 'rt')
        lines = testHeadFile.readlines()
        testHeadFile.close()
        os.remove('temp/prova.hpp')
        self.assertEqual(len(lines), 27)
        self.assertEqual(lines[16], 'class MyClass{\n')
        self.assertEqual(lines[17], '    private:\n')
        self.assertEqual(lines[18], '    int pippo;\n')
        self.assertEqual(lines[19], '\n')
        self.assertEqual(lines[20], '    public:\n')
        self.assertEqual(lines[21], '    MyClass();\n')
        self.assertEqual(lines[22], '};\n')
        testWscriptFile = open('temp/wscript', 'rt')
        lines = testWscriptFile.readlines()
        testWscriptFile.close()
        os.remove('temp/wscript')
        self.assertEqual(len(lines), 16)
        self.assertEqual(lines[0], '#!/usr/bin/env python\n')
        self.assertEqual(lines[1], '# -*- coding: iso-8859-1 -*-\n')
        self.assertEqual(lines[2], '\n')
        self.assertEqual(lines[3], 'import os\n')
        self.assertEqual(lines[4], '\n')
        self.assertEqual(lines[5], '\n')
        self.assertEqual(lines[6], 'def build(bld):\n')
        self.assertEqual(lines[7], '    sources = \"\"\"\n')
        self.assertEqual(lines[8], '        prova.cpp\n')
        self.assertEqual(lines[9], '    \"\"\"\n')
        self.assertEqual(lines[10], '    uselib = \'BOOST BOOST_THREAD BOOST_FILESYSTEM BOOST_SYSTEM SYSTEMC TLM TRAP\'\n')
        self.assertEqual(lines[11], '    objects = \'\'\n')
        self.assertEqual(lines[12], '    includes = \'.\'\n')
        self.assertEqual(lines[13], '    target = \'temp\'\n')
        self.assertEqual(lines[15], '    bld.program(source = sources, target = target, use = uselib + \' \' + objects, includes = includes)\n')
        import shutil
        shutil.rmtree('temp', True)

    def testNestedDirs1(self):
        folder = writer_code.Folder('temp')
        nestFolder = writer_code.Folder('nested')
        folder.addSubFolder(nestFolder)
        folder.create()
        nestFolder.create()
        self.assert_(os.path.exists('temp/wscript'))
        self.assert_(os.path.exists('temp/nested/wscript'))
        os.remove('temp/wscript')
        os.remove('temp/nested/wscript')
        import shutil
        shutil.rmtree('temp', True)

    def testNestedDirs2(self):
        folder = writer_code.Folder('temp')
        nestFolder = writer_code.Folder('nested')
        folder.addSubFolder(nestFolder)
        nestFolder.create()
        folder.create()
        self.assert_(os.path.exists('temp/wscript'))
        self.assert_(os.path.exists('temp/nested/wscript'))
        os.remove('temp/wscript')
        os.remove('temp/nested/wscript')
        import shutil
        shutil.rmtree('temp', True)

    def testNestedDirsCommonPath(self):
        folder = writer_code.Folder('temp')
        nestFolder = writer_code.Folder('temp/nested')
        folder.addSubFolder(nestFolder)
        nestFolder.create()
        folder.create()
        os.remove('temp/wscript')
        os.remove('temp/nested/wscript')
        import shutil
        shutil.rmtree('temp', True)

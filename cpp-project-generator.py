import os
import json

cpp_version = '20'
compiler_path = 'C:\\msys64\\ucrt64\\bin\\g++.exe'
debugger_path = 'C:\\msys64\\ucrt64\\bin\\gdb.exe'

# Ex:
# 'C:\\mingw64\\bin\\g++.exe'
# 'C:\\mingw64\\bin\\gdb.exe'

def gerar_makefile():
    # Conteúdo do Makefile
    makefile_content = """#
# 'make'        build executable file 'main'
# 'make clean'  removes all .o and executable files
#

WORKSPACE_NAME := $(notdir $(CURDIR))

# Defina a versão padrão do C++ (ex: make CPP_VERSION=14, make CPP_VERSION=17)
CPP_VERSION ?= 20

# define the mode: Debug or Release (default: Debug) or make MODE=Release, make MODE=Debug
MODE ?= Debug

#########################################################################################

# Flags de compilação padrão
COMMON_FLAGS := -std=c++$(CPP_VERSION) -Wall -Wextra

# Flags de compilação específicas para Debug
DEBUG_FLAGS := -g -ggdb # Adicione aqui as flags específicas para debug

# Flags de compilação específicas para Release
RELEASE_FLAGS :=  -O2 -DNDEBUG

# Use a variável FLAGS para armazenar as flags a serem usadas
FLAGS := $(COMMON_FLAGS)

#########################################################################################

ifeq ($(MODE),Debug)
	FLAGS += $(DEBUG_FLAGS)
else
	FLAGS += $(RELEASE_FLAGS)
endif

# define the Cpp compiler to use
CXX = g++

# define any compile-time flags
# CXXFLAGS	:= -std=c++20 -Wall -Wextra #-g #ggdb   

CXXFLAGS := $(FLAGS)

# define library paths in addition to /usr/lib
#   if I wanted to include libraries not in /usr/lib I'd specify
#   their path using -Lpath, something like:
LFLAGS =

# define output directory
OUTPUT	:= bin

# define source directory
SRC		:= src

# define include directory
INCLUDE	:= include

# define lib directory
LIB		:= lib

ifeq ($(OS),Windows_NT)
OUTPUTMAIN	:= $(call FIXPATH,$(OUTPUT)/$(MODE)/$(MAIN))
MAIN	:= ${WORKSPACE_NAME}.exe
SOURCEDIRS	:= $(SRC)
INCLUDEDIRS	:= $(INCLUDE)
LIBDIRS		:= $(LIB)
FIXPATH = $(subst /,\,$1)
RM			:= del /q /f
MD	:= mkdir
else
OUTPUTMAIN	:= $(call FIXPATH,$(OUTPUT)/$(MODE)/$(MAIN))
MAIN	:= ${WORKSPACE_NAME}
SOURCEDIRS	:= $(shell find $(SRC) -type d)
INCLUDEDIRS	:= $(shell find $(INCLUDE) -type d)
LIBDIRS		:= $(shell find $(LIB) -type d)
FIXPATH = $1
RM = rm -f
MD	:= mkdir -p
endif

# define any directories containing header files other than /usr/include
INCLUDES	:= $(patsubst %,-I%, $(INCLUDEDIRS:%/=%))

# define the C libs
LIBS		:= $(patsubst %,-L%, $(LIBDIRS:%/=%))

# define the C source files
SOURCES		:= $(wildcard $(patsubst %,%/*.cpp, $(SOURCEDIRS)))

# define the C object files
OBJECTS		:= $(SOURCES:.cpp=.o)

# define the dependency output files
DEPS		:= $(OBJECTS:.o=.d)

#
# The following part of the makefile is generic; it can be used to
# build any executable just by changing the definitions above and by
# deleting dependencies appended to the file from 'make depend'
#
OUTPUTMAIN	:= $(call FIXPATH,$(OUTPUT)/$(MODE)/$(MAIN))

all: $(OUTPUT) $(MAIN)
	@echo Executing 'all' complete!

$(OUTPUT):
	$(MD) $(OUTPUT)

	$(MD) $(OUTPUT)/Debug
	$(MD) $(OUTPUT)/Release

$(MAIN): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $(OUTPUTMAIN) $(OBJECTS) $(LFLAGS) $(LIBS)

# include all .d files
-include $(DEPS)

# this is a suffix replacement rule for building .o's and .d's from .c's
# it uses automatic variables $<: the name of the prerequisite of
# the rule(a .c file) and $@: the name of the target of the rule (a .o file)
# -MMD generates dependency output files same name as the .o file
# (see the gnu make manual section about automatic variables)
.cpp.o:
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c -MMD $<  -o $@

.PHONY: clean
clean:
#	$(RM) $(OUTPUTMAIN)
#	$(RM) $(call FIXPATH,$(OBJECTS))
#	$(RM) $(call FIXPATH,$(DEPS))
#	@echo Cleanup complete!

	rm -f $(OUTPUTMAIN)

	rm -f $(OUTPUT)/Debug/$(MAIN)
	rm -f $(OUTPUT)/Release/$(MAIN)

	rm -f $(call FIXPATH,$(OBJECTS))
	rm -f $(call FIXPATH,$(DEPS))
	@echo Cleanup complete!

run: all
	./$(OUTPUTMAIN)
	@echo Executing 'run: all' complete!
    """
    # Escrever o conteúdo no arquivo Makefile
    with open("Makefile", "w") as makefile:
        makefile.write(makefile_content)

def criar_estrutura_projeto():
    diretorio_projeto = os.getcwd()  # Obtém o diretório de trabalho atual

    global cpp_version
    global compiler_path
    global debugger_path

    # Define a estrutura do projeto
    estrutura_projeto = {
        "src": ['main.cpp'],
        "include": [],
        "bin": ["Debug", "Release"],
        "lib": [],
        "docs": ['Additional Flags.txt'],
        ".vscode": {

            "c_cpp_properties.json": {

                "configurations": [
                    {
                        "name": "Debug",
                        "includePath": [
                            "${workspaceFolder}/**",
                            "${workspaceFolder}/include"
                        ],
                        "defines": [ 
                            "_DEBUG",
                            "UNICODE",
                            "_UNICODE"
                        ],
                        "compilerPath": f"{compiler_path}",
                        "cStandard": "c11",
                        "cppStandard": f"c++{cpp_version}",
                        "intelliSenseMode": "windows-gcc-x64",
                        "browse": {
                            "path": [
                                "${workspaceFolder}",
                                "${workspaceFolder}/include"
                            ],
                            "limitSymbolsToIncludedHeaders": True,
                            "databaseFilename": ""
                        }
                    }
                    # Adicione mais configurações conforme necessário
                ],
                "version": 4
            },

            "launch.json": {
                # Conteúdo do seu launch.json aqui
                "configurations": [
                    {
                        "name": "Debug",
                        "type": "cppdbg",
                        "request": "launch",
                        # "program": "${fileDirname}\\${fileBasenameNoExtension}.exe",
                        # "program": "${workspaceFolder}/bin/Debug/${fileBasenameNoExtension}.exe",
                        "program": "${workspaceFolder}/bin/Debug/${workspaceFolderBasename}.exe",
                        "args": [],
                        "stopAtEntry": False,
                        "cwd": "${fileDirname}",
                        "environment": [],
                        "externalConsole": True,
                        "MIMode": "gdb",
                        "miDebuggerPath": f"{debugger_path}",
                        "setupCommands": [
                            {
                                "description": "Enable pretty-printing for gdb",
                                "text": "-enable-pretty-printing",
                                "ignoreFailures": True
                            },
                            {
                                "description": "Set Disassembly Flavor to Intel",
                                "text": "-gdb-set disassembly-flavor intel",
                                "ignoreFailures": True
                            }
                        ],
                        "preLaunchTask": "Debug"
                    },

                    {
                        "name": "Release",
                        "type": "cppdbg",
                        "request": "launch",
                        # "program": "${fileDirname}\\${fileBasenameNoExtension}.exe",
                        # "program": "${workspaceFolder}\\bin\\Release\\${fileBasenameNoExtension}.exe",
                        "program": "${workspaceFolder}\\bin\\Release\\${workspaceFolderBasename}.exe",
                        "args": [],
                        "stopAtEntry": False,
                        "cwd": "${fileDirname}",
                        "environment": [],
                        "externalConsole": True,
                        "MIMode": "gdb",
                        "miDebuggerPath": f"{debugger_path}",
                        "setupCommands": [
                            {
                                "description": "Enable pretty-printing for gdb",
                                "text": "-enable-pretty-printing",
                                "ignoreFailures": True
                            },
                            {
                                "description": "Set Disassembly Flavor to Intel",
                                "text": "-gdb-set disassembly-flavor intel",
                                "ignoreFailures": True
                            }
                        ],
                        "preLaunchTask": "Release"
                    }
                ],
                "version": "2.0.0"

            },

            "settings.json": {
                # Conteúdo do seu settings.json aqui
                "C_Cpp.default.compilerPath": f"{compiler_path}",
                "files.associations": {
                    "array": "cpp",
                    "atomic": "cpp",
                    "bit": "cpp",
                    "*.tcc": "cpp",
                    "cctype": "cpp",
                    "charconv": "cpp",
                    "chrono": "cpp",
                    "clocale": "cpp",
                    "cmath": "cpp",
                    "compare": "cpp",
                    "concepts": "cpp",
                    "cstdarg": "cpp",
                    "cstddef": "cpp",
                    "cstdint": "cpp",
                    "cstdio": "cpp",
                    "cstdlib": "cpp",
                    "ctime": "cpp",
                    "cwchar": "cpp",
                    "cwctype": "cpp",
                    "deque": "cpp",
                    "string": "cpp",
                    "unordered_map": "cpp",
                    "vector": "cpp",
                    "exception": "cpp",
                    "algorithm": "cpp",
                    "functional": "cpp",
                    "iterator": "cpp",
                    "memory": "cpp",
                    "memory_resource": "cpp",
                    "numeric": "cpp",
                    "optional": "cpp",
                    "random": "cpp",
                    "ratio": "cpp",
                    "string_view": "cpp",
                    "system_error": "cpp",
                    "tuple": "cpp",
                    "type_traits": "cpp",
                    "utility": "cpp",
                    "format": "cpp",
                    "initializer_list": "cpp",
                    "iomanip": "cpp",
                    "iosfwd": "cpp",
                    "iostream": "cpp",
                    "istream": "cpp",
                    "limits": "cpp",
                    "new": "cpp",
                    "numbers": "cpp",
                    "ostream": "cpp",
                    "span": "cpp",
                    "sstream": "cpp",
                    "stdexcept": "cpp",
                    "streambuf": "cpp",
                    "cinttypes": "cpp",
                    "typeinfo": "cpp",
                    "variant": "cpp",
                    "map": "cpp",
                    "condition_variable": "cpp",
                    "forward_list": "cpp",
                    "list": "cpp",
                    "set": "cpp",
                    "executor": "cpp",
                    "io_context": "cpp",
                    "netfwd": "cpp",
                    "timer": "cpp",
                    "future": "cpp",
                    "mutex": "cpp",
                    "semaphore": "cpp",
                    "stop_token": "cpp",
                    "thread": "cpp"
                }
            },

            "tasks.json": {
                # Conteúdo do seu tasks.json aqui
                "tasks": [
                    {
                        "type": "cppbuild",
                        "label": "Debug",
                        "command": f"{compiler_path}",
                        "args": [
                            f"-std=c++{cpp_version}",
                            "-fdiagnostics-color=always",
                            "-g",


                            # "-Wall",        
                            # "-Weffc++",
                            # "-Wextra",
                            # "-Wconversion",
                            # "-Wsign-conversion",
                            # "-pedantic-errors",
                            # "-Werror",     


                            "-ggdb",


                            "-I${workspaceFolder}/include",
                            "-L${workspaceFolder}/lib",


                            # "-I./include",
                            # "-L./lib",


                            # "${file}",
                            "*.cpp",


                            "-o",

            
                            # "${fileDirname}\\${fileBasenameNoExtension}.exe",
                            # "${workspaceFolder}/bin/Debug/${fileBasenameNoExtension}.exe",
                            "${workspaceFolder}/bin/Debug/${workspaceFolderBasename}.exe",

                            # "-lglfw3",
                            # "-lopengl32",

                            # "-lsfml-graphics",
                            # "-lsfml-window",
                            # "-lsfml-system"
                        ],
                        "options": {
                            "cwd": "${fileDirname}"
                        },
                        "problemMatcher": [
                            "$gcc"
                        ],
                        "group": "build",
                        "detail": "Task generated by Debugger."
                    },
                    {
                        "type": "cppbuild",
                        "label": "Release",
                        "command": f"{compiler_path}",
                        "args": [
                            f"-std=c++{cpp_version}",
                            "-fdiagnostics-color=always",


                            "-I${workspaceFolder}/include",
                            "-L${workspaceFolder}/lib",


                            # "-I./include",
                            # "-L./lib",


                            "-O2",
                            "-DNDEBUG",


                            # "${file}",
                            "*.cpp",


                            "-o",


                            # "${fileDirname}\\${fileBasenameNoExtension}.exe",
                            # "${workspaceFolder}/bin/Release/${fileBasenameNoExtension}.exe",
                            "${workspaceFolder}/bin/Release/${workspaceFolderBasename}.exe",

                            # "-lglfw3",
                            # "-lopengl32",
                            
                            # "-lsfml-graphics",
                            # "-lsfml-window",
                            # "-lsfml-system"
                            
                        ],
                        "options": {
                            "cwd": "${fileDirname}"
                        },
                        "problemMatcher": [
                            "$gcc"
                        ],
                        "group": "build",
                        "detail": "Task generated by Debugger."
                    }

                ],
                "version": "2.0.0"
            }
        }
    }

    # Cria os diretórios e arquivos conforme a estrutura definida
    for pasta, conteudo in estrutura_projeto.items():
        caminho_pasta = os.path.join(diretorio_projeto, pasta)
        os.makedirs(caminho_pasta, exist_ok=True)

        if isinstance(conteudo, list):
            for item in conteudo:
                if os.path.splitext(item)[1] == '':
                    # Se o item da lista for uma pasta (sem extensão), cria a subpasta
                    caminho_subpasta = os.path.join(caminho_pasta, item)
                    os.makedirs(caminho_subpasta, exist_ok=True)
                else:
                    # Se o item da lista tiver uma extensão, cria o arquivo
                    caminho_arquivo = os.path.join(caminho_pasta, item)
                    with open(caminho_arquivo, 'w') as f:
                        if item == 'main.cpp':
                            f.write('#include <iostream>\n\n' 
                                    'int main(int argc, char* argv[])\n'
                                    '{\n\n\n'
                                    '   std::cin.get();\n'
                                    '}')
                        else:
                            f.write('Additional flags:\n\n'
                                    '   Warnings (in tasks.json):\n'
                                    '       "-Wall"\n'           
                                    '       "-Weffc++"\n'            
                                    '       "-Wextra"\n'           
                                    '       "-Wconversion"\n'            
                                    '       "-Wsign-conversion"\n'            
                                    '       "-pedantic-errors"\n'           
                                    '       "-Werror"\n\n'

                                    '   Single file compilation (needs to be changed for both Debug and Release) (in tasks.json):\n'
                                    '       "${file}" in place of: "*.cpp"\n'            
                                    '   Executable in the same source directory (needs to be changed for both Debug and Release) (in tasks.json):\n'
                                    '       "${fileDirname}\\${fileBasenameNoExtension}.exe" in place of: "${workspaceFolder}/bin/(Debug or Release)/${workspaceFolderBasename}.exe"\n\n'
                                    '       Extra: to change the executable name: {fileBasenameNoExtension}, {workspaceFolderBasename}\n'
                                    '              and (in launch.json): "program": "${workspaceFolder}\\bin\\(Debug or Release)\\${workspaceFolderBasename}.exe"\n\n'

                                    '   Glfw link flags:\n'
                                    '       "-lglfw3"\n'
                                    '       "-lopengl32"\n\n'
                                    '   SFML link flags:\n'
                                    '       "-lsfml-graphics"\n'
                                    '       "-lsfml-window"\n'
                                    '       "-lsfml-system"\n\n'
                                    'The same flags are commented in original Python file, so you can change them beforehand if needed.\n\n'
                                    'Make file:\n'
                                    '   You can change default configurations such as flags, similar to the ones above.\n'
                                    '   To use other settings: make MODE=(Debug or Release) or/and CPP_VERSION=(14, 17 etc)\n'
                                    '   Example:\n'
                                    '       make MODE=Release CPP_VERSION=17')            

        elif isinstance(conteudo, dict):
            for arquivo, conteudo_arquivo in conteudo.items():
                caminho_arquivo = os.path.join(caminho_pasta, arquivo)
                with open(caminho_arquivo, 'w') as f:
                    if arquivo.endswith(".json"):
                        json.dump(conteudo_arquivo, f, indent=4)
                    else:
                        f.write(conteudo_arquivo)

    gerar_makefile()                    

if __name__ == "__main__":
    # Executa a função para criar a estrutura no diretório atual
    criar_estrutura_projeto()

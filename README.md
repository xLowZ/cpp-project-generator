## Sobre

- Gera um template de um projeto C++ para o Visual Studio Code, pouco flexível.
- Para melhor utilização, deverão ser feitos ajustes manuais dos parâmetros no arquivo principal.
- Arquivo de texto adicional contém algumas informações extras após gerar o template.
- Por padrão, executáveis terão o nome da workspace em que se encontram (mesmo nome da pasta onde se encontra o seu `cpp-project-generator.py`).
- Portanto, basta trocar o nome da pasta ou copiar os arquivos para uma pasta com o nome de escolha.

## EN:
- Generates a template of a C++ project for Visual Studio Code, with limited flexibility.
- For better usage, manual adjustments of parameters in the main file are required.
- An additional text file contains some extra information after generating the template.
- By default, executables will have the name of the workspace they are in (same name as the folder where your `cpp-project-generator.py` is located).
- Therefore, simply change the name of the folder or copy the files to a folder with the desired name.

## Organização das pastas (exemplo):
```plaintext
.
├── .vscode
│   └── .json
├── bin
│   ├── Debug
│   │   └── executable_debug.exe
│   └── Release
│       └── executable_release.exe
├── docs
│   └── doc_files.txt
├── include
│   └── .h
├── lib
│   ├── .dll
│   ├── .lib
│   └── .a
├── src
│   └── .cpp
├── cpp-project-generator.py
└── Makefile
```

## Preview:
![image](https://github.com/xLowZ/cpp-project-generator/assets/132095310/16c2fcef-2cf6-4954-b5f3-0621f1889552)

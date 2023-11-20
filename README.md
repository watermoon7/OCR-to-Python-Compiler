# OCR-to-Python-Compiler
Translates OCR Reference Language into Python


## How to use
To use the compiler, navigate to the root directory and type the following command

  python ocrcompiler/testing.py
  
The file 'test2.ocr' will be translated and save in a file called 'test2.py'


## How it works
The lexer tokenises the code and appends each token to a token list. 
The parser affirms that each line is in accordance to the syntax rules. 
During this process, the method 'affirm_grammar' is called which:
- checks the current token is of the expected type
- generates the code for the token and adds the translated code to a string

Finally the translated code is written to a file


## TODO
  - implement classes (they're kind of broken)
  - fix nested do untils
  - add a gui
  - make it into a package
  - add comments
  - clean up the horendous code
  - write documentation
  - finish the writeup for the project
  - :( there is a lot to do 

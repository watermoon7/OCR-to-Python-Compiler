# OCR Compiler
This is a compiler which translates OCR reference language to Python. (OCR reference language is a type of pseudocode)

## How to use it
Navigate to the root directory. Then type

    python ocrcompiler/testing.py

This translates the code in the file test2.ocr and saves the result in test2.py if there are no errors.

## How it works
### Lexer
The Lexer increments through the inputted code character by character and classifies groups of characters into tokens.
It appends the tokens to a list called 'token_list'
### Parser
The Parser increments through the token list and checks the syntax rules of the language.
It does this by repeatedly calling the method statement which affirms the grammar of the line is correct.
If it is not, then the program outputs an error.

During parsing, the function 'affirm_grammar' is called. This does two things
- ensures the current token is of the expected type
- generates the translated token and adds it to the output string
### Generator
After parsing is complete, the Generator saves the translated code to a file.

## TODO
- Add GUI
- Add arrays, byRef, byVal (and possibly method checking)
- Make the project a package
- Allow passing a file/ directory as an argument when running the program (already done I just need to add it into this version)
- Fix the horrendous number of errors
- Make the code nicer
- Implement better ways of dealing with indentation
- Write tests
- Write documentation
- Project writeup
- Crustify the code

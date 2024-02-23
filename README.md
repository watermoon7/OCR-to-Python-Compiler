# OCR Compiler
This is a compiler which translates OCR reference language to Python. (OCR reference language is a type of pseudocode)

## How to use it
In a terminal or command prompt, navigate to the root directory. 
To compile a file type:

    python ocrcompiler input_file_path.ocr
Or

    python ocrcompiler input_file_path.txt

This translates the inputted code and saves the output to input_file_path.py (if there are no errors).

An alternative method: 
    
    chmod +x '/OCR-to-Python-Compiler/ocrcompiler/Compile.py'
    alias ocr = '/OCR-to-Python-Compiler/ocrcompiler/Compile.py'

Now you can use ocr as a command. For example:

    ocr input_file_path.ocr

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
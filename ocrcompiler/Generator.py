class Generator:
    def __init__(self):
        self.code = ""

    def generate(self, token):
        if isinstance(token, str):
            self.code += token
        elif isinstance(token, type):
            self.code += token().keyword
        else:
            self.code += token.keyword

    def write(self, output_path):
        with open(output_path, 'w') as outputFile:
            outputFile.write(self.code)
        print("Successfully finished generator.")

    def clear(self):
        self.code = None


generator = Generator()
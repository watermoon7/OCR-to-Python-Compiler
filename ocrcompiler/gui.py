import customtkinter, subprocess
import Lexer, Parser
from Generator import *

def change_theme(new_theme: str):
    customtkinter.set_appearance_mode(new_theme)

def change_font_size(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)

class OptionsMenu(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.appearance_mode_label = customtkinter.CTkLabel(self, text="Execution Mode:", anchor="w")
        self.appearance_mode_label.grid(row=0, column=0, padx=10, pady=10)
        self.mode_combobox = customtkinter.CTkOptionMenu(self, values = ["Interpret", "Compile"], command=self.get_mode)
        self.mode_combobox.grid(row=1, column=0, padx=10, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=2, column=0, padx=10, pady=10)
        self.theme_menu = customtkinter.CTkOptionMenu(self, values=["Light", "Dark", "System"], command=change_theme)
        self.theme_menu.grid(row=3, column=0, padx=10, pady=10)
        self.theme_menu.set("Dark")

        self.scaling_label = customtkinter.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=4, column=0, padx=10, pady=10)
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self, values=[str(i*10) + '%' for i in range(1, 21)], command=change_font_size)
        self.scaling_optionemenu.grid(row=5, column=0, padx=10, pady=10)
        self.scaling_optionemenu.set("100%")

        self.compile_label = customtkinter.CTkLabel(self, text="Run:", anchor="w")
        self.compile_label.grid(row=6, column=0, padx=10, pady=10)
        self.compile = customtkinter.CTkButton(self, text="Execute", anchor="w", command=self.execute)
        self.compile.grid(row=7, column=0, padx=10, pady=10)

    def get_mode(self, *args):
        return self.mode_combobox.get()

    def execute(self, *args):
        self.master.execute()


class Shell(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.shell_input = customtkinter.CTkTextbox(self)
        self.shell_input.grid(column=0, row=0, padx=10, pady=10, sticky="nesw")

        self.shell_output = customtkinter.CTkTextbox(self)
        self.shell_output.grid(column=0, row=1, padx=10, pady=10, sticky="nesw")
        self.shell_output.configure(state="disabled")




class App(customtkinter.CTk):

    def __init__(self, title_str = "OCR Reference Language Interpreter"):
        super().__init__()

        self.title_str = title_str
        self.title(self.title_str)
        self.geometry("1080x720")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.shell = Shell(self)
        self.shell.grid(row=0, column=0, padx=10, pady=20, sticky="nesw")

        self.options_menu = OptionsMenu(self)
        self.options_menu.grid(row=0, column=1, padx=10, pady=20, sticky="nesw")


    def clear(self):
        self.shell.shell_output.delete("0.0", customtkinter.END)


    def execute(self):
        code = self.shell.shell_input.get("0.0", customtkinter.END)[:-1]

        if code != '':
            lexer = Lexer.Lexer(code)
            tokens = lexer.Lex()
            parser = Parser.Parser(tokens, generator)

            parser.program()
            output = generator.code
            generator.code = ""
        else:
            output = ""
            
        if self.options_menu.get_mode() == "Interpret":
            output = subprocess.run(["python3", "-c", output], stdout=subprocess.PIPE, text=True).stdout.strip()
      
        self.shell.shell_output.configure(state=customtkinter.NORMAL)
        self.clear()
        self.shell.shell_output.insert("0.0", output)
        self.shell.shell_output.see(customtkinter.END)
        self.shell.shell_output.configure(state="disabled")

app = App()
app.mainloop()

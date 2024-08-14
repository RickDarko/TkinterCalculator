# Tkinter Calculator
# 2022/01/14
# https://github.com/BaseMax/TkinterCalculator
#changes 14/08/2024. Rick Darko
#added undo button, history window and minor improvments

import tkinter as tk  # Importa la librería Tkinter para crear la interfaz gráfica.

# Colores
WHITE = "#FFFFFF"
OFF_WHITE = "#F8FAFF"
LABEL_COLOR = "#25265E"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"

# Fuentes
DEFAULT_FONT_STYLE = ("Arial", 20)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)

class TkinterCalculator:
    def __init__(self):
        self.window = tk.Tk()  # Crea la ventana principal.
        self.window.geometry("375x667")  # Establece el tamaño de la ventana.
        self.window.resizable(0, 0)  # Desactiva la posibilidad de redimensionar la ventana.
        self.window.title("Calculator")  # Título de la ventana.

        # Variables para las expresiones matemáticas.
        self.total_expression = ""  # Expresión completa.
        self.current_expression = ""  # Expresión actual que se muestra en pantalla.

        # Crear los componentes de la interfaz.
        self.display_frame = self.create_display_frame()  # Crea el marco de la pantalla.
        self.total_label, self.label = self.create_display_labels()  # Crea las etiquetas de la pantalla.

        # Diccionarios para los botones de dígitos y operadores.
        self.digits = {
            7: (1,1), 8: (1,2), 9: (1,3),
            4: (2,1), 5: (2,2), 6: (2,3),
            1: (3,1), 2: (3,2), 3: (3,3),
            0: (4, 2), '.':(4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.buttons_frame = self.create_buttons_frame()  # Crea el marco para los botones.

        # Configuración de filas y columnas para los botones.
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        # Ajustar columnas para el nuevo botón de historial
        self.buttons_frame.columnconfigure(5, weight=1)  
        # Crear los botones de la calculadora.
        self.create_digit_buttons()  # Crea los botones numéricos.
        self.create_operator_buttons()  # Crea los botones de operadores.
        self.create_special_buttons()  # Crea botones especiales (como borrar y calcular).

        self.bind_keys()  # Asigna las teclas del teclado a las funciones de la calculadora.
        self.history = []  # Pila para almacenar el historial de expresiones.
        self.calculation_history = []  # Lista para almacenar el historial de cálculos.

    def run(self):
        self.window.mainloop()  # Inicia el bucle principal de la interfaz gráfica.

    # Crea el botón para calcular la raíz cuadrada.
    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221Ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    # Crea el botón de igual (=) para evaluar la expresión.
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    # Crea el marco donde se ubicarán todos los botones.
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    # Crea los botones especiales: borrar, igual, cuadrado y raíz cuadrada.
    def create_special_buttons(self):
        self.create_clear_button()  # Botón de borrar.
        self.create_equals_button()  # Botón de igual.
        self.create_square_button()  # Botón de cuadrado.
        self.create_sqrt_button()  # Botón de raíz cuadrada.
        self.create_undo_button()  # Botón de deshacer.
        self.create_history_button()  # Nuevo botón de historial

    # Crea las etiquetas para mostrar las expresiones y resultados.
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    # Crea el marco donde se muestra la expresión y el resultado.
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    # Crea los botones numéricos.
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    # Crea los botones de los operadores matemáticos (+, -, *, /).
    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    # Crea el botón de borrar (C).
    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    # Crea el botón de cuadrado (x²).
    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)
    
    #crear al boton de deshacer
    def create_undo_button(self):
        button = tk.Button(self.buttons_frame, text="Undo", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.undo)
        button.grid(row=0, column=0, sticky=tk.NSEW)

    def create_history_button(self):
        button = tk.Button(self.buttons_frame, text="Hist", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.show_history)
        button.grid(row=0, column=4, sticky=tk.NSEW)

    def undo(self):  #logica del boton deshacer.
        if self.history:
            self.total_expression, self.current_expression = self.history.pop()  # Restaurar el último estado guardado
            self.update_total_label()
            self.update_label()
    
    # Añade un valor (número o punto decimal) a la expresión actual.
    def add_to_expression(self, value):
        self.history.append((self.total_expression, self.current_expression))  # Guardar el estado actual
        self.current_expression += str(value)
        self.update_label()

    # Añade un operador a la expresión completa.
    def append_operator(self, operator):
        if self.current_expression == "":
            return  # Evita agregar un operador si no hay una expresión actual.
        self.history.append((self.total_expression, self.current_expression))  # Guardar el estado actual
        self.total_expression += self.current_expression + operator
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    # Asigna las teclas del teclado a las funciones de la calculadora.
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    # Limpia la expresión actual y la expresión completa.
    def clear(self):
        self.history.append((self.total_expression, self.current_expression))  # Guardar el estado actual
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    # Calcula el cuadrado de la expresión actual.
    def square(self):
        self.total_expression += self.current_expression
        self.history.append((self.total_expression, self.current_expression))  # Guardar el estado actual
        try:
            result = str(eval(f"{self.current_expression}**2"))
            self.current_expression = result
            self.calculation_history.append(self.total_expression + "² = " + result)  # Guardar en el historial
            self.total_expression = ""

        except Exception:
            self.current_expression = "Error"  # Muestra "Error" si la expresión no es válida.
        self.update_label()

    # Calcula la raíz cuadrada de la expresión actual.
    def sqrt(self):
        self.total_expression += self.current_expression
        self.history.append((self.total_expression, self.current_expression))  # Guardar el estado actual
        try:
            result = str(eval(f"{self.current_expression}**0.5"))
            self.current_expression = result
            self.calculation_history.append(self.total_expression + "√ = " + result)  # Guardar en el historial
            self.total_expression = ""
        except Exception:
            self.current_expression = "Error"  # Muestra "Error" si la expresión no es válida.
        self.update_label()

    # Actualiza la etiqueta que muestra la expresión completa.
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    # Actualiza la etiqueta que muestra la expresión actual.
    def update_label(self):
        self.label.config(text=self.current_expression[:11])  # Limita la longitud de la expresión mostrada.

    # Evalúa la expresión completa y muestra el resultado.
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            # Evaluamos la expresión total y guardamos el resultado en 'result'
            result = str(eval(self.total_expression))
            self.current_expression = result
            # Guardar la expresión completa junto con el resultado en el historial
            self.calculation_history.append(self.total_expression + " = " + result)
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def show_history(self):
        history_window = tk.Toplevel(self.window)
        history_window.title("Calculation History")
        history_window.geometry("300x400")
        
        history_text = tk.Text(history_window, font=SMALL_FONT_STYLE)
        history_text.pack(expand=True, fill='both')
        
        for entry in self.calculation_history:
            history_text.insert(tk.END, entry + "\n")

if __name__ == "__main__":
    tkinter_calculator = TkinterCalculator()  # Crea una instancia de la calculadora.
    tkinter_calculator.run()  # Ejecuta la calculadora.

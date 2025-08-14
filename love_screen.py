
import tkinter as tk
import random

# --- Configuración ---
MESSAGE = "Never forget that I'm always thinking of you"
CREDIT = "This app was made by Jc Rosas"
SYMBOLS = ['❤️', '🌹']
COLORS = ['red', 'pink', 'magenta', 'hot pink', 'white', 'violet red']
BACKGROUND_COLOR = 'black'
FONT_FAMILY = 'Arial'
MAIN_MESSAGE_SIZE = 40
MIN_SYMBOL_SIZE = 20
MAX_SYMBOL_SIZE = 50
GENERATION_SPEED_MS = 100  # Milisegundos para nuevos símbolos
LETTER_REVEAL_SPEED_MS = 120 # Milisegundos para revelar cada letra

# --- Aplicación ---
class LoveScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Para ti")
        self.root.attributes('-fullscreen', True)
        self.root.config(bg=BACKGROUND_COLOR, cursor="none")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Preparar el mensaje para aparecer letra por letra
        self.full_message = MESSAGE
        self.revealed_message = ""
        self.letter_index = 0

        # Crear la etiqueta del mensaje central (inicialmente vacía)
        self.message_label = tk.Label(
            self.root,
            text="",
            font=(FONT_FAMILY, MAIN_MESSAGE_SIZE, 'bold'),
            fg='white',
            bg=BACKGROUND_COLOR,
            wraplength=self.screen_width - 100 # Para que el texto se ajuste si es muy largo
        )
        self.message_label.place(relx=0.5, rely=0.5, anchor='center')

        # Crear la etiqueta de crédito en la esquina inferior derecha
        credit_label = tk.Label(
            self.root,
            text=CREDIT,
            font=(FONT_FAMILY, 10), # Letra pequeña
            fg='grey', # Color sutil
            bg=BACKGROUND_COLOR
        )
        # Usamos place con relx/rely para posicionar en la esquina
        credit_label.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor='se')

        self.root.bind('<Escape>', self.close_app)

        # Iniciar ambas animaciones
        self.animate_symbols()
        self.reveal_next_letter()

    def reveal_next_letter(self):
        """Añade la siguiente letra al mensaje y programa la próxima."""
        if self.letter_index < len(self.full_message):
            # Agrega el siguiente caracter a la cadena revelada
            self.revealed_message += self.full_message[self.letter_index]
            self.message_label.config(text=self.revealed_message)
            self.letter_index += 1
            self.root.after(LETTER_REVEAL_SPEED_MS, self.reveal_next_letter)

    def create_random_symbol(self):
        """Crea un corazón o una rosa en una posición y con un estilo aleatorio."""
        symbol = random.choice(SYMBOLS)
        color = random.choice(COLORS)
        size = random.randint(MIN_SYMBOL_SIZE, MAX_SYMBOL_SIZE)
        x_pos = random.randint(0, self.screen_width)
        y_pos = random.randint(0, self.screen_height)

        symbol_label = tk.Label(
            self.root,
            text=symbol,
            font=(FONT_FAMILY, size),
            fg=color,
            bg=BACKGROUND_COLOR
        )
        symbol_label.place(x=x_pos, y=y_pos)

    def animate_symbols(self):
        """Función que se llama repetidamente para generar nuevos símbolos."""
        self.create_random_symbol()
        self.root.after(GENERATION_SPEED_MS, self.animate_symbols)

    def close_app(self, event=None):
        """Cierra la aplicación."""
        self.root.destroy()

if __name__ == "__main__":
    main_window = tk.Tk()
    app = LoveScreen(main_window)
    main_window.mainloop()

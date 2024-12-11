#Autores: 
#Emiliano Juárez Márquez #348768
#Jesus Alejandro Rey Alvidrez #348545

import tkinter as tk
import tkinter.messagebox as messagebox
import random

class ScrabbleGame:
    def __init__(self):
        # Carga el diccionario y las fichas del juego
        self.dictionary = self.load_dictionary("palabras.txt")
        self.tiles = self.load_tiles("fichas.txt")
        self.trie = self.build_trie(self.dictionary)
        self.word_hash = {}

        # Variables de estado del juego
        self.current_player = 1
        self.player1_score = 0
        self.player2_score = 0
        self.player1_tiles = self.get_initial_tiles()
        self.player2_tiles = self.get_initial_tiles()

    def load_dictionary(self, filename):
        # Carga el diccionario de palabras desde un archivo de texto
        with open(filename, "r") as file:
            return [word.strip().lower() for word in file.readlines()]

    def load_tiles(self, filename):
        # Carga las fichas del juego desde un archivo de texto
        with open(filename, "r") as file:
            return [tile.strip().lower() for tile in file.readlines()]

    def build_trie(self, words):
        # Construye un Trie para buscar rápidamente palabras válidas
        trie = {}
        for word in words:
            node = trie
            for char in word:
                node = node.setdefault(char, {})
            node["_end"] = True
        return trie

    def get_initial_tiles(self):
        # Obtiene una muestra aleatoria de fichas iniciales para un jugador
        tiles = random.sample(self.tiles, 7)
        return tiles

    def is_valid_word(self, word):
        # Verifica si una palabra es válida consultando el Trie
        node = self.trie
        for char in word:
            if char not in node:
                return False
            node = node[char]
        return "_end" in node

    def is_repeated_word(self, word):
        # Verifica si una palabra ya ha sido jugada
        return word in self.word_hash

    def get_word_score(self, word):
        # Obtiene la puntuación de una palabra basada en los valores de las fichas
        scores = {
            "a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1,
            "j": 8, "k": 5, "l": 1, "m": 3, "n": 1, "o": 1, "p": 3, "q": 10, "r": 1,
            "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10
        }
        return sum(scores.get(char, 0) for char in word)

    def update_scores(self, word):
        # Actualiza la puntuación del jugador actual después de jugar una palabra
        score = self.get_word_score(word)
        if self.current_player == 1:
            self.player1_score += score
        else:
            self.player2_score += score

    def switch_player(self):
        # Cambia el turno al siguiente jugador
        self.current_player = 3 - self.current_player

    def play_word(self, word):
        # Juega una palabra y realiza las actualizaciones correspondientes
        self.word_hash[word] = True
        self.update_scores(word)
        if self.current_player == 1:
            self.player1_tiles = self.get_new_tiles(word)
        else:
            self.player2_tiles = self.get_new_tiles(word)
        self.switch_player()

    def get_new_tiles(self, word):
        # Obtiene las nuevas fichas para el jugador después de jugar una palabra
        new_tiles = []
        available_tiles = self.tiles + self.player1_tiles + self.player2_tiles
        tile_count = {tile: available_tiles.count(tile) for tile in available_tiles}
        for char in word:
            if char in tile_count and tile_count[char] > 0:
                tile_count[char] -= 1
            else:
                new_tile = random.choice(self.tiles)
                new_tiles.append(new_tile)
        return self.player1_tiles + new_tiles

class ScrabbleGUI:
    def __init__(self, root, game):
        # Configura la interfaz de usuario
        self.root = root
        self.game = game
        self.word_entry = None
        self.word_label = None
        self.player_label = None
        self.score_label = None
        self.tiles_label = None

        self.setup_ui()

    def setup_ui(self):
        # Configura la ventana principal y los elementos de la interfaz de usuario
        self.root.title("Scrabble")
        self.root.geometry("400x250")

        word_frame = tk.Frame(self.root)
        word_frame.pack(pady=10)

        self.word_label = tk.Label(word_frame, text="Introduce una palabra:")
        self.word_label.pack(side=tk.LEFT)

        self.word_entry = tk.Entry(word_frame)
        self.word_entry.pack(side=tk.LEFT)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        play_button = tk.Button(button_frame, text="Jugar", command=self.play_word)
        play_button.pack(side=tk.LEFT)

        self.player_label = tk.Label(self.root, text="Turno del Jugador 1")
        self.player_label.pack()

        self.score_label = tk.Label(self.root, text="Puntuación: Jugador 1: 0  Jugador 2: 0")
        self.score_label.pack()

        tiles_frame = tk.Frame(self.root)
        tiles_frame.pack(pady=10)

        tiles_label = tk.Label(tiles_frame, text="Fichas del Jugador:")
        tiles_label.pack(side=tk.LEFT)

        self.tiles_label = tk.Label(tiles_frame, text="")
        self.tiles_label.pack(side=tk.LEFT)

        self.update_tiles()

    def play_word(self):
        # Gestiona el evento de jugar una palabra desde la interfaz de usuario
        word = self.word_entry.get().strip().lower()
        if not word:
            return

        if not self.game.is_valid_word(word):
            messagebox.showerror("Palabra inválida", "La palabra no es válida.")
            return

        if self.game.is_repeated_word(word):
            messagebox.showerror("Palabra repetida", "La palabra ya ha sido jugada.")
            return

        tiles = self.game.player1_tiles if self.game.current_player == 1 else self.game.player2_tiles
        if not self.is_word_possible(word, tiles):
            messagebox.showerror("Fichas inválidas", "La palabra no se puede formar con tus fichas actuales.")
            return

        self.game.play_word(word)
        self.update_scores()
        self.update_tiles()
        self.word_entry.delete(0, tk.END)
        self.word_entry.focus_set()

    def is_word_possible(self, word, tiles):
        # Verifica si es posible formar una palabra con las fichas disponibles
        tile_count = {}
        for tile in tiles:
            tile_count[tile] = tile_count.get(tile, 0) + 1
        for char in word:
            if char not in tile_count or tile_count[char] == 0:
                return False
            tile_count[char] -= 1
        return True

    def update_scores(self):
        # Actualiza las etiquetas de puntuación y jugador actual en la interfaz de usuario
        player_text = f"Turno del Jugador {self.game.current_player}"
        score_text = f"Puntuación: Jugador 1: {self.game.player1_score}  Jugador 2: {self.game.player2_score}"
        self.player_label.config(text=player_text)
        self.score_label.config(text=score_text)

    def update_tiles(self):
        # Actualiza la etiqueta de las fichas del jugador actual en la interfaz de usuario
        tiles = self.game.player1_tiles if self.game.current_player == 1 else self.game.player2_tiles
        tiles_text = " ".join(tiles)
        self.tiles_label.config(text=tiles_text)

def main():
    root = tk.Tk()
    game = ScrabbleGame()
    gui = ScrabbleGUI(root, game)
    root.mainloop()

if __name__ == "__main__":
    main()

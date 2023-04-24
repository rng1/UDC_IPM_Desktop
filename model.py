import re
import requests


URL="https://cheat.sh/"


ANSI_ESCAPE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')


def escape_ansi(line: str):
    return ANSI_ESCAPE.sub('', line)


class Model(object):
    def search_command(self, command, fun):
        recipes = self.get_cheatsheet(command)
        fun(recipes)


    def parse_text(self, text: str):
            recipes = []
            # split("\n\n") splits on blank lines.
            # :warning: Doesn't work for two consecutive blank lines
            for chunk in text.split("\n\n"):
                entry = self.parse_chunk(chunk)
                recipes.append(entry)
            return recipes


    def parse_chunk(self, chunk: str):
        commands = ""
        description = ""
        for line in chunk.splitlines():
            if line.startswith("# "):
            	# Eliminar los dos puntos al final de las descripciones
                description = line[1:-1] 
            elif (line == "---"):
                # Asumimos que siempre es sintácticamente correcto
                # TODO: parsear esta especie the frontmatter
                pass
            else:
                commands = line

        return (commands, description)


    def get_cheatsheet(self, command: str):
        try:
            r = requests.get(URL + command)
        except requests.exceptions.ConnectionError:
            return ["ConnectionError"]

        text = escape_ansi(r.text)
        if text.startswith("Unknown topic."): # Comando no encontrado
            return []
        else:
            return self.parse_text(text)

    

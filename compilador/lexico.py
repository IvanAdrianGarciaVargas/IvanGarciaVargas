TOKENS = {
    'BOOL': 256,
    'CALL': 257,
    'CHAR': 258,
    'CONST_CHAR': 259,
    'CONST_STRING': 260,
    'DIF': 261,
    'DO': 262,
    'ELSE': 263,
    'FLOAT': 264,
    'FOR': 265,
    'FUNCTION': 266,
    'ID': 267,
    'IF': 268,
    'IGU': 269,
    'INT': 270,
    'MAI': 271,
    'MAIN': 272,
    'MAY': 273,
    'MEI': 274,
    'MEN': 275,
    'NUM': 276,
    'NUMF': 277,
    'READ': 278,
    'RETURN': 279,
    'STRING': 280,
    'THEN': 281,
    'TO': 282,
    'VOID': 283,
    'WHILE': 284,
    'WRITE': 285,
    'FALSE': 286,
    'TRUE': 287,
}

PALABRAS_RESERVADAS = ('bool', 'call', 'char', 'do', 'else', 'float', 'for',
    'function', 'if', 'int', 'main', 'read', 'return', 'string', 'then', 'to',
    'void', 'while', 'write', 'false', 'true',)

class Simbolo(object):
    def __init__(self, token=None, lexema=None):
        self.token = token
        self.lexema = lexema

    def __repr__(self):
        return f"{self.lexema} ({self.token})"


class Lexico(object):
    def __init__(self, codigo=""):
        self.codigo = codigo + " "
        self.tabla_de_simbolos = []
        self.indice = 0
        self.numero_de_linea = 1
        self.inicio = 0
        self.estado = 0
        self.caracter = self.codigo[0]
        self.lexema = ""
        self.token = None
        self.__cargar_palabras_reservadas()

    def inserta_simbolo(self, simbolo=None, token=None, lexema=None):
        """
        Inserta un simbolo en la tabla de simbolos. Puede aceptar un simbolo,
        o bien, un token y lexema.
        """
        if simbolo:
            self.tabla_de_simbolos.append(simbolo)

        elif token and lexema:
            self.tabla_de_simbolos.append(Simbolo(token=token, lexema=lexema))

        else:
            raise Exception("Debe proveer un Simbolo, o bien token y lexema!")

    def __cargar_palabras_reservadas(self):
        """
        Carga las palabras reservadas en la tabla de simbolos antes de iniciar
        el proceso de compilacion.
        """
        self.tabla_de_simbolos = list(map(lambda palabra:
                Simbolo(
                    token=TOKENS.get(palabra.upper()),
                    lexema=palabra
                ),
            PALABRAS_RESERVADAS)
        )
            
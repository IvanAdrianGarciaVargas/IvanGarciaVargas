CONSTANTES = ('BOOL', 'CALL','CHAR', 'CONST_CHAR', 'CONST_STRING', 'DIF', 'DO',
    'ELSE', 'FLOAT', 'FOR', 'FUNCTION', 'ID', 'IF', 'IGU', 'INT', 'MAI', 'MAIN',
    'MAY', 'MEI', 'MEN', 'NUM', 'NUMF', 'READ', 'RETURN', 'STRING', 'THEN', 'TO',
    'VOID', 'WHILE', 'WRITE', 'FALSE', 'TRUE',)

PALABRAS_RESERVADAS = ('bool', 'call', 'char', 'do', 'else', 'float', 'for',
    'function', 'if', 'int', 'main', 'read', 'return', 'string', 'then', 'to',
    'void', 'while', 'write', 'false', 'true',)

TOKENS = {constante: token for (token, constante) in enumerate(CONSTANTES, 256)}

SIMBOLOS_PERMITIDOS = r"(){}[],;+-*/\%&|!"

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
        self.indice = -1
        self.inicio_lexema = 0
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

    def __buscar_simbolo(self, lexema=''):
        """
        Recibe un lexema y busca un simbolo que coincida con el lexema en la
        tabla de simbolos.
        """
        return next((s for s in self.tabla_de_simbolos if s.lexema == lexema), None)

    def __siguiente_caracter(self):
        """
        Regresa el siguiente caracter en el codigo fuente.
        """
        try:
            self.indice += 1
            return self.codigo[self.indice]

        except IndexError:
            return None

    def __avanza_inicio_lexema(self):
        """
        Mueve el inicio del lexema una posicion hacia adelante.
        """
        self.inicio_lexema = self.indice + 1

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

    def siguiente_componente_lexico(self):
        """
        Regresa el siguiente componente lexico (Simbolo) encontrado en el codigo
        fuente.
        """
        while True:
            if self.estado == 0:
                caracter = self.__siguiente_caracter()
                if caracter in (' ', '\t', '\n'):
                    self.__avanza_inicio_lexema()
                    if caracter == '\n':
                        self.numero_de_linea += 1

                elif caracter is None:
                    return None

                elif caracter == '<':
                    self.estado = 1

                elif caracter == '=':
                    self.estado = 5

                elif caracter == '>':
                    self.estado = 6

                else:
                    self.estado = self.__fallo(self.inicio)

            elif self.estado == 1:
                caracter = self.__siguiente_caracter()
                if caracter == '=':
                    self.estado = 2

                elif caracter == '>':
                    self.estado = 3

                else:
                    self.estado = 4

            elif self.estado == 2:
                return Simbolo(token=TOKENS['MEI'], lexema=self.__leer_lexema())

            elif self.estado == 3:
                return Simbolo(token=TOKENS['DIF'], lexema=self.__leer_lexema())

            elif self.estado == 4:
                self.__retrocede_indice()
                return Simbolo(token=TOKENS['MEN'], lexema=self.__leer_lexema())

            elif self.estado == 5:
                return Simbolo(token=TOKENS['IGU'], lexema=self.__leer_lexema())

            elif self.estado == 6:
                caracter = self.__siguiente_caracter()
                if caracter == '=':
                    self.estado = 7

                else:
                    self.estado = 8

            elif self.estado == 7:
                return Simbolo(token=TOKENS['MAI'], lexema=self.__leer_lexema())

            elif self.estado == 8:
                self.__retrocede_indice()
                return Simbolo(token=TOKENS['MAY'], lexema=self.__leer_lexema())

            elif self.estado == 9:
                if caracter.isalpha():
                    self.estado = 10

                else:
                    self.estado = self.__fallo(self.inicio)

            elif self.estado == 10:
                caracter = self.__siguiente_caracter()
                if not caracter.isalnum():
                    self.estado = 11

            elif self.estado == 11:
                self.__retrocede_indice()
                lexema = self.__leer_lexema()
                simbolo = self.__buscar_simbolo(lexema=lexema)
                if simbolo is None:
                    simbolo = Simbolo(token=TOKENS['ID'], lexema=lexema)
                    self.inserta_simbolo(simbolo=simbolo)

                return simbolo

            elif self.estado == 12:
                if caracter.isdigit():
                    self.estado = 13

                else:
                    self.estado = self.__fallo(self.inicio)

            elif self.estado == 13:
                caracter = self.__siguiente_caracter()
                if caracter == '.':
                    self.estado = 14

                elif caracter in 'Ee':
                    self.estado = 16

                elif caracter.isdigit():
                    pass

                else:
                    self.estado = 20

            elif self.estado == 14:
                caracter = self.__siguiente_caracter()
                if caracter.isdigit():
                    self.estado = 15

                else:
                    self.estado = self.__fallo(self.inicio)

            elif self.estado == 15:
                caracter = self.__siguiente_caracter()
                if caracter in 'Ee':
                    self.estado = 16

                elif caracter.isdigit():
                    pass

                else:
                    self.estado = 21

            elif self.estado == 16:
                caracter = self.__siguiente_caracter()
                if caracter in '+-':
                    self.estado = 17

                elif caracter.isdigit():
                    self.estado = 18

                else:
                    self.estado = self.__fallo(self.inicio)

            elif self.estado == 17:
                caracter = self.__siguiente_caracter()
                if caracter.isdigit():
                    self.estado = 18

                else:
                    self.estado = self.__fallo(self.inicio)

            elif self.estado == 18:
                caracter = self.__siguiente_caracter()
                if caracter.isdigit():
                    pass

                else:
                    self.estado = 19

            elif self.estado == 19:
                self.__retrocede_indice()
                return Simbolo(token=TOKENS['NUMF'], lexema=self.__leer_lexema())

            elif self.estado == 20:
                self.__retrocede_indice()
                return Simbolo(token=TOKENS['NUM'], lexema=self.__leer_lexema())

            elif self.estado == 21:
                self.__retrocede_indice()
                return Simbolo(token=TOKENS['NUMF'], lexema=self.__leer_lexema())

            else:
                if caracter in SIMBOLOS_PERMITIDOS:
                    return Simbolo(token=ord(caracter), lexema=self.__leer_lexema())

                else:
                    # TODO generar objeto de error en vez de enviar un mensaje.
                    self.estado = 0
                    print("ln: %s. Error Lexico: Simbolo no permitido: '%s'" %
                        (self.numero_de_linea, self.__leer_lexema())
                    )

    def __leer_lexema(self):
        """
        Regresa la secuencia de caracteres entre el inicio_lexema y el indice,
        despues mueve el inicio_lexema a la siguiente posicion.
        """
        self.lexema = self.codigo[self.inicio_lexema: self.indice + 1]
        self.__avanza_inicio_lexema()
        self.inicio = 0
        self.estado = 0
        return self.lexema

    def __retrocede_indice(self):
        """
        Retrocede el indice una posicion hacia atras. Equivale al asterisco en
        los estados de aceptacion.
        """
        self.indice -= 1

    def __deshacer_automata(self):
        """
        Si un automata falla en un estado intermedio, regresa el indice al
        caracter previo al inicio_lexema, para procesar el primer caracter en
        el siguiente automata.
        """
        self.indice = self.inicio_lexema - 1

    def __fallo(self, inicio):
        """
        Regresa el valor del estado inicial del siguiente automata a probar
        cuando el automata anterior fallo.
        """
        if inicio == 0:
            self.inicio = 9

        elif inicio == 9:
            self.inicio = 12

        elif inicio == 12:
            self.inicio = 22

        return self.inicio
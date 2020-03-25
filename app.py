import json
from flask import Flask, render_template, request, jsonify
from compilador.lexico import Lexico

app = Flask(__name__)

@app.route('/tabla-de-simbolos/')
def tabla_de_simbolos(*args, **kwargs):
    lexico = Lexico()
    simbolos = [{'token': s.token, 'lexema': s.lexema} for s in lexico.tabla_de_simbolos]
    return ({'simbolos': simbolos}, 200)

@app.route('/compila/', methods=('post',))
def compila(*args, **kwargs):
    json_data = json.loads(request.data)
    lexico = Lexico(codigo=json_data.get('codigo', ''))
    componentes_lexicos = []
    while True:
        componente_lexico = lexico.siguiente_componente_lexico()
        if componente_lexico:
            componentes_lexicos.append(
                {
                    "token": componente_lexico.token,
                    "lexema": componente_lexico.lexema,
                }
            )

        else:
            break

    return ({'componentes_lexicos': componentes_lexicos}, 200)

if __name__ == '__main__':
    app.run(debug=True)
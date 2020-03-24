from flask import Flask, render_template, request, jsonify
from compilador.lexico import Lexico

app = Flask(__name__)

@app.route('/tabla-de-simbolos/')
def tabla_de_simbolos(*args, **kwargs):
    lexico = Lexico()
    simbolos = [{'token': s.token, 'lexema': s.lexema} for s in lexico.tabla_de_simbolos]
    return ({'simbolos': simbolos}, 200)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify, request
import util
app = Flask(__name__)

@app.route('/')
def all():
    return jsonify(database)

@app.route('/disciplinas', methods=['GET'])
def disciplinas():
    return jsonify(util.all_for_database('DISCIPLINA'))


@app.route('/disciplinas/<int:id_disciplina>', methods=['GET'])
def disciplina_pelo_id(id_disciplina):
    try: 
        disciplina = util.localiza(id_disciplina,'DISCIPLINA')
        return jsonify(disciplina)
    except util.NotFoundError:
        return jsonify({'erro':'disciplina nao encontrada'}),400
    

@app.route('/disciplinas', methods=['POST'])
def adiciona_disciplina():
    nova_disciplina = request.json
    try:
        disciplina = util.localiza(nova_disciplina['id'],'DISCIPLINA')
        return jsonify({'erro':'id ja utilizada'}),400
    except util.NotFoundError:
        pass
    util.adiciona(nova_disciplina, 'DISCIPLINA')
    return jsonify(util.all_for_database('DISCIPLINA'))



@app.route('/reseta', methods=['POST'])
def reseta_disciplinas():
    util.reseta()
    return 'banco resetado'


@app.route('/disciplinas/<int:id_disciplina>', methods=['DELETE'])
def deleta_disciplina(id_disciplina):
    try: 
        disciplina = util.localiza(id_disciplina,'DISCIPLINA')
        removido = util.remove(disciplina,'DISCIPLINA')
        return jsonify(removido)
    except util.NotFoundError:
        return jsonify({'erro':'disciplina nao encontrada'}),400

@app.route('/disciplinas/<int:id_disciplina>', methods=['PUT'])
def edita_disciplina(id_disciplina):
    try: 
        disciplina = util.localiza(id_disciplina,'DISCIPLINA')
        novo = request.json
        if 'nome' not in novo:
            return jsonify({'erro':'disciplina nao encontrada'}),400
        for key in disciplina:
            if key in novo:
                disciplina[key] = novo[key]
        return jsonify(disciplina)
    except util.NotFoundError:
        return jsonify({'erro':'disciplina nao encontrada'}),400

if __name__ == '__main__':
    app.run(host='localhost', port=5003, debug=True)

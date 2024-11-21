from flask import Flask, request, jsonify
from flask_cors import CORS
import scrape

app = Flask(__name__)
CORS(app)  # Para permitir requisições de outros domínios, como o localhost do Angular

@app.route('/api/dados', methods=['POST'])
def receber_dados():
    print('\n\n\n\ndados recebidos')
    dados = request.json  # Recebe os dados enviados pelo Angular no formato JSON
    # Exemplo de processamento dos dados recebidos
    
    u = dados['usuario']
    s = dados['senha']
    resposta = scrape.run_scraping(u, s)
    print('Scraping feito')
    
    return resposta

    # if resposta == 'Falha':
    #     return jsonify({'resultado': 'Falha'})
    # else:
    #     print(f'\n\n\n {resposta}')
    #     return resposta


if __name__ == '__main__':
    app.run(debug=True)
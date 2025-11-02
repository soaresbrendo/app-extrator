from flask import Flask, request, jsonify, send_file, render_template
import os
import io
from pdf_extractor import extrair_dados_pdf, mapear_paginas_por_pedido
from excel_generator import gerar_excel
import PyPDF2

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Armazenamento temporário de dados extraídos
dados_sessao = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/extract-pdf', methods=['POST'])
def extract_pdf():
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'Nenhum arquivo PDF fornecido'}), 400
        
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Arquivo deve ser um PDF'}), 400
        
        # Salvar PDF temporariamente
        pdf_bytes = file.read()
        session_id = os.urandom(16).hex()
        
        # Extrair dados usando a lógica fornecida
        dados_extraidos = extrair_dados_pdf(pdf_bytes)
        
        if not dados_extraidos:
            return jsonify({'error': 'Nenhum dado encontrado no PDF'}), 400
        
        mapa_paginas = mapear_paginas_por_pedido(pdf_bytes)
        
        # Armazenar dados e PDF na sessão
        dados_sessao[session_id] = {
            'dados': dados_extraidos,
            'pdf': pdf_bytes,
            'filename': file.filename,
            'mapa_paginas': mapa_paginas
        }
        
        # Preparar resposta com dados estruturados
        response_data = {
            'session_id': session_id,
            'filename': file.filename,
            'total_cnpjs': len(dados_extraidos),
            'dados': []
        }
        
        for cnpj, pedidos in dados_extraidos.items():
            for pedido, produtos in pedidos.items():
                response_data['dados'].append({
                    'cnpj': cnpj,
                    'pedido': pedido,
                    'total_produtos': len(produtos),
                    'produtos': produtos,
                    'paginas': mapa_paginas.get(pedido, [])
                })
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Erro na extração: {e}")
        return jsonify({'error': f'Erro ao processar PDF: {str(e)}'}), 500

@app.route('/api/add-product', methods=['POST'])
def add_product():
    try:
        data = request.json
        session_id = data.get('session_id')
        cnpj = data.get('cnpj')
        pedido = data.get('pedido')
        index = data.get('index', -1)  # Adicionar suporte a índice
        position = data.get('position', 'below')  # 'above' ou 'below'
        
        if session_id not in dados_sessao:
            return jsonify({'error': 'Sessão não encontrada'}), 404
        
        # Adicionar produto vazio
        novo_produto = {
            'SKU': '',
            'Descricao': '',
            'Quantidade': '',
            'Valor_Unitario': ''
        }
        
        produtos = dados_sessao[session_id]['dados'][cnpj][pedido]
        if index >= 0 and index < len(produtos):
            insert_index = index if position == 'above' else index + 1
            produtos.insert(insert_index, novo_produto)
        else:
            produtos.append(novo_produto)
        
        return jsonify({'success': True, 'produto': novo_produto, 'index': insert_index if index >= 0 else len(produtos) - 1})
        
    except Exception as e:
        print(f"Erro ao adicionar produto: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-product', methods=['POST'])
def delete_product():
    try:
        data = request.json
        session_id = data.get('session_id')
        cnpj = data.get('cnpj')
        pedido = data.get('pedido')
        index = data.get('index')
        
        if session_id not in dados_sessao:
            return jsonify({'error': 'Sessão não encontrada'}), 404
        
        if index is None or index < 0:
            return jsonify({'error': 'Índice inválido'}), 400
        
        produtos = dados_sessao[session_id]['dados'][cnpj][pedido]
        
        if index >= len(produtos):
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        # Remover produto
        produto_removido = produtos.pop(index)
        
        return jsonify({'success': True, 'produto_removido': produto_removido})
        
    except Exception as e:
        print(f"Erro ao excluir produto: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-data', methods=['POST'])
def update_data():
    try:
        data = request.json
        session_id = data.get('session_id')
        updated_data = data.get('dados')
        
        if session_id not in dados_sessao:
            return jsonify({'error': 'Sessão não encontrada'}), 404
        
        # Reorganizar dados atualizados
        novos_dados = {}
        for item in updated_data:
            cnpj = item['cnpj']
            pedido = item['pedido']
            
            if cnpj not in novos_dados:
                novos_dados[cnpj] = {}
            novos_dados[cnpj][pedido] = item['produtos']
        
        dados_sessao[session_id]['dados'] = novos_dados
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Erro ao atualizar dados: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-excel', methods=['POST'])
def generate_excel():
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id not in dados_sessao:
            return jsonify({'error': 'Sessão não encontrada'}), 404
        
        dados = dados_sessao[session_id]['dados']
        
        # Gerar Excel
        excel_file = gerar_excel(dados)
        
        if not excel_file:
            return jsonify({'error': 'Erro ao gerar arquivo Excel'}), 500
        
        filename = f"produtos_por_cnpj_pedido.xlsx"
        
        return send_file(
            excel_file,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        print(f"Erro ao gerar Excel: {e}")
        return jsonify({'error': 'Erro ao gerar arquivo Excel'}), 500

@app.route('/api/get-pdf-by-order', methods=['GET', 'POST'])
def get_pdf_by_order():
    try:
        if request.method == 'GET':
            session_id = request.args.get('session_id')
            pedido = request.args.get('pedido')
        else:
            data = request.json
            session_id = data.get('session_id')
            pedido = data.get('pedido')
        
        if session_id not in dados_sessao:
            return jsonify({'error': 'Sessão não encontrada'}), 404
        
        pdf_bytes = dados_sessao[session_id]['pdf']
        mapa_paginas = dados_sessao[session_id]['mapa_paginas']
        
        paginas = mapa_paginas.get(pedido, [])
        
        if not paginas:
            print(f"Páginas não encontradas para pedido {pedido}, retornando PDF completo")
            return send_file(
                io.BytesIO(pdf_bytes),
                as_attachment=False,
                download_name=f'pedido_{pedido}.pdf',
                mimetype='application/pdf'
            )
        
        # Criar novo PDF com apenas as páginas do pedido
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        pdf_writer = PyPDF2.PdfWriter()
        
        for num_pagina in paginas:
            if num_pagina < len(pdf_reader.pages):
                pdf_writer.add_page(pdf_reader.pages[num_pagina])
        
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        
        return send_file(
            output,
            as_attachment=False,
            download_name=f'pedido_{pedido}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Erro ao recuperar PDF: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Erro ao recuperar PDF'}), 500

@app.route('/api/get-pdf', methods=['POST'])
def get_pdf():
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id not in dados_sessao:
            return jsonify({'error': 'Sessão não encontrada'}), 404
        
        pdf_bytes = dados_sessao[session_id]['pdf']
        filename = dados_sessao[session_id]['filename']
        
        return send_file(
            io.BytesIO(pdf_bytes),
            as_attachment=False,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Erro ao recuperar PDF: {e}")
        return jsonify({'error': 'Erro ao recuperar PDF'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Extrator de Pedidos PDF")
    print("🌐 Acesse: http://localhost:5000")
    print("-" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

import PyPDF2
import re
import io

def extrair_cnpj(linhas_texto):
    """Extrai CNPJ do texto"""
    texto_completo = " ".join(linhas_texto)
    match = re.search(r"CNPJ\s+-?(\d{2})\s+(\d{2}\.\d{3}\.\d{3})/(\d{4})", texto_completo)
    if match:
        final = match.group(1)
        base = match.group(2)
        filial = match.group(3)
        return f"{base}/{filial}-{final}"
    return None

def extrair_pedido(linhas_texto):
    """Extrai número do pedido"""
    for linha in linhas_texto:
        match = re.search(r"PEDIDO DE COMPRAS\s+(\d+)", linha)
        if match:
            return match.group(1)
    return None

def mapear_paginas_por_pedido(pdf_bytes):
    """
    Mapeia quais páginas pertencem a cada pedido
    Retorna: {pedido: [lista_de_paginas]}
    """
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        total_paginas = len(pdf_reader.pages)
        
        mapa = {}
        pedido_atual = None
        
        for numero_pagina in range(total_paginas):
            pagina = pdf_reader.pages[numero_pagina]
            texto = pagina.extract_text()
            linhas = texto.split("\n")
            
            pedido = extrair_pedido(linhas)
            
            if pedido:
                pedido_atual = pedido
                if pedido_atual not in mapa:
                    mapa[pedido_atual] = []
            
            if pedido_atual:
                mapa[pedido_atual].append(numero_pagina)
        
        return mapa
        
    except Exception as e:
        print(f"Erro ao mapear páginas: {e}")
        return {}

def extrair_dados_pdf(pdf_bytes):
    """
    Extrai dados do PDF organizados por CNPJ e Pedido
    Retorna: {cnpj: {pedido: [produtos]}}
    """
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        total_paginas = len(pdf_reader.pages)
        
        print(f"Processando {total_paginas} páginas")
        
        dados_por_cnpj_pedido = {}
        
        for numero_pagina in range(total_paginas):
            pagina = pdf_reader.pages[numero_pagina]
            texto = pagina.extract_text()
            linhas = texto.split("\n")
            
            cnpj = extrair_cnpj(linhas)
            pedido = extrair_pedido(linhas)
            
            if not cnpj:
                print(f"CNPJ não localizado na página {numero_pagina + 1}")
                continue
            if not pedido:
                print(f"Pedido não localizado na página {numero_pagina + 1}")
                continue
            
            # Inicializa estrutura
            if cnpj not in dados_por_cnpj_pedido:
                dados_por_cnpj_pedido[cnpj] = {}
            if pedido not in dados_por_cnpj_pedido[cnpj]:
                dados_por_cnpj_pedido[cnpj][pedido] = []
            
            # Determina início da lista de produtos
            inicio_inicio = 0
            if numero_pagina == 0:
                for i, linha in enumerate(linhas):
                    if "Bruto Bonif." in linha:
                        inicio_inicio = i + 1
                        break
            
            # Extrai produtos
            for linha in linhas[inicio_inicio:]:
                match = re.search(
                    r"((?:\d{1,3}\.)*\d{1,3},\d{2})\s+[\w-]+\s+\d+\s+(.*?)\s+- REF:\s+(\d+)", 
                    linha
                )
                if match:
                    quantidade = match.group(1)
                    descricao = match.group(2).strip()
                    sku = match.group(3)
                    
                    valores = re.findall(r"(\d{1,3}(?:[.,]\d{3})*,\d{2})", linha)
                    valor_unitario = valores[-2] if len(valores) >= 2 else "N/A"
                    
                    produto = {
                        "SKU": sku,
                        "Descricao": descricao,
                        "Quantidade": quantidade,
                        "Valor_Unitario": valor_unitario
                    }
                    dados_por_cnpj_pedido[cnpj][pedido].append(produto)
        
        print(f"Extração concluída: {len(dados_por_cnpj_pedido)} CNPJs encontrados")
        return dados_por_cnpj_pedido
        
    except Exception as e:
        print(f"Erro ao extrair dados do PDF: {e}")
        return None

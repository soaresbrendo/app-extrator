import pandas as pd
import io

def gerar_excel(dados_por_cnpj_pedido):
    """
    Gera arquivo Excel com abas por CNPJ e Pedido
    Entrada: {cnpj: {pedido: [produtos]}}
    """
    try:
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for cnpj, pedidos in dados_por_cnpj_pedido.items():
                for pedido, produtos in pedidos.items():
                    df = pd.DataFrame(produtos)
                    
                    # Formato: 31838128000314-7202309
                    cnpj_limpo = cnpj.replace('.', '').replace('/', '').replace('-', '')
                    aba_nome = f"{cnpj_limpo}-{pedido}"
                    
                    # Limitar a 31 caracteres (limite do Excel)
                    aba_nome = aba_nome[:31]
                    
                    df.to_excel(writer, sheet_name=aba_nome, index=False)
                    
                    # Ajustar largura das colunas
                    worksheet = writer.sheets[aba_nome]
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 3, 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        return output
        
    except Exception as e:
        print(f"Erro ao criar Excel: {e}")
        return None

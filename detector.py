"""
Detector de Dados Pessoais - Desafio Participa DF
Autor: Lucas Boros
Data: Janeiro/2026

Solução híbrida: Regex + NLP (spaCy) para identificar dados pessoais
em solicitações de acesso à informação.
"""

import re
import pandas as pd
import spacy

# Carregar modelo spaCy
nlp = spacy.load('pt_core_news_sm')

# ==============
# CONFIGURAÇÃO
# ===============

FALSOS_POSITIVOS = [
    'caesb', 'detran', 'tcb', 'der', 'seduh', 'seec', 'pmdf', 'cbmdf', 
    'sicoob', 'terracap', 'adasa', 'cgdf', 'gdf', 'setor público',
    'sociedade de transportes coletivos de brasília', 'controladora-geral', 'distrito federal',
    # Tratamentos e saudações
    'vossa senhoria', 'vossas senhorias', 'excelência', 'encaminho',
    'certidão', 'ônus', 'atenciosamente', 'cordialmente', 'prezados',
    'prezado', 'prezada', 'ilustríssimo', 'ilustrissimo',
    # Termos técnicos/jurídicos
    'gestão de integridade', 'gestão de', 'governança de tic',
    'administração de banco de dados', 'letramento digital',
    'superior a15', 'inciso xxxiii', 'inciso ii', 'inciso xv',
    'advogados associados', 'setor público',
    'lei maria da penha', 'moro de aluguel',
    # Termos químicos/técnicos
    'coliformes termotolerantes', 'fósforo total', 'nitrogênio amoniacal',
    'nitrogênio total', 'oxigênio dissolvido', 'sólidos totais', 'letramento digital'
]

PALAVRAS_INVALIDAS = [
    'ltda', 'associados', 'advogados', 'inciso', 'gestão', 'administração', 
    'setor', 'lei', 'sociedade', 'coliformes', 'fósforo', 'nitrogênio',
    'oxigênio', 'sólidos', 'moro'
]

PADROES_REGEX = {
    'CPF': r'\d{3}\.\d{3}\.\d{3}-\d{1,2}|\d{11}',
    'E-mail': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'Telefone': r'\(\d{2}\)\s?\d{4,5}-\d{4}|\d{2}\s\d{4,5}-?\d{4}',
    'Matricula': r'[Mm]atr[ií]cula[:\s]+[\d.-]+|\d{2}\.\d{3}-\d{1}',
    'OAB': r'OAB[/-]?\w{2}[\s-]?\d{2,6}',
    'CNPJ': r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
}

# ============================================
# FUNÇÕES
# ============================================

def detectar_nomes_pessoas(texto):
    """
    Detecta nomes de pessoas usando NLP (spaCy).
    """
    doc = nlp(str(texto))
    nomes = []
    
    for ent in doc.ents:
        if ent.label_ == 'PER':
            nome_lower = ent.text.lower().strip()
            eh_falso_positivo = any(fp in nome_lower for fp in FALSOS_POSITIVOS)
            tem_tamanho_minimo = len(ent.text.split()) >= 2
            contem_palavra_invalida = any(p in nome_lower for p in PALAVRAS_INVALIDAS)
            
            if not eh_falso_positivo and tem_tamanho_minimo and not contem_palavra_invalida:
                nomes.append(ent.text)
    
    return nomes


def classificar_texto(texto):
    """
    Classifica um texto quanto à presença de dados pessoais.
    
    Returns:
        1 = Não Público (contém dados pessoais)
        0 = Público (não contém dados pessoais)
    """
    texto = str(texto)
    
    # Verifica padrões estruturados (regex)
    for padrao in PADROES_REGEX.values():
        if re.search(padrao, texto):
            return 1
    
    # Verifica nomes de pessoas (NLP)
    if len(detectar_nomes_pessoas(texto)) > 0:
        return 1
    
    return 0


def classificar_dataset(caminho_arquivo, coluna_texto='Texto Mascarado', coluna_id='ID'):
    """
    Classifica todos os textos de um arquivo Excel/CSV.
    
    Returns:
        DataFrame com ID e Classificacao
    """
    # Carregar arquivo
    if caminho_arquivo.endswith('.xlsx'):
        df = pd.read_excel(caminho_arquivo)
    else:
        df = pd.read_csv(caminho_arquivo)
    
    # Classificar
    df['Classificacao'] = df[coluna_texto].apply(classificar_texto)
    
    # Retornar resultado
    resultado = df[[coluna_id, 'Classificacao']].copy()
    resultado['Rotulo'] = resultado['Classificacao'].map({0: 'Público', 1: 'Não Público'})
    
    return resultado


# ============================================
# EXECUÇÃO DIRETA
# ============================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
        print(f"Processando: {arquivo}")
        resultado = classificar_dataset(arquivo)
        
        # Salvar resultado
        resultado.to_csv('resultado_classificacao.csv', index=False)
        print(f"Resultado salvo em: resultado_classificacao.csv")
        
        # Estatísticas
        total = len(resultado)
        nao_publicos = resultado['Classificacao'].sum()
        print(f"\nTotal: {total}")
        print(f"Público: {total - nao_publicos} ({(total-nao_publicos)/total:.1%})")
        print(f"Não Público: {nao_publicos} ({nao_publicos/total:.1%})")
    else:
        print("Uso: python detector.py <arquivo.xlsx>")
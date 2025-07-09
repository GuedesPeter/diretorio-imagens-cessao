import os
import pandas as pd
import subprocess
import platform

# Lista de termos a serem buscados (case-insensitive)
TERMO_BUSCA = [
    "RG_FRENTE", "CNH", "RG_VERSO", "SELFIE",
    "RG_FRENTE_TESTEMUNHA", "CNH_TESTEMUNHA", "RG_VERSO_TESTEMUNHA",
    "arqRG_FRENTE", "arqRG_VERSO", "arqSelfieIni", "arqCNH",
    "arqfotoDocumentoFrente", "arqfotoDocumentoVerso", "arqDECLARACAO_RESIDENCIA"
]

def verificar_arquivos_por_caminho(arquivo_excel):
    """
    Verifica se arquivos com determinados nomes estão presentes nos diretórios especificados no Excel.
    Cria um arquivo com duas abas: dados completos e resumo com colunas selecionadas (filtradas).
    """
    # Lê o Excel de entrada
    df = pd.read_excel(arquivo_excel)

    if 'Caminho' not in df.columns:
        raise ValueError("A coluna 'Caminho' não foi encontrada no arquivo Excel.")

    for index, row in df.iterrows():
        caminho = row['Caminho']
        encontrados = []

        if caminho and os.path.isdir(caminho):
            try:
                arquivos = os.listdir(caminho)
                arquivos_lower = [arquivo.lower() for arquivo in arquivos]
                for termo in TERMO_BUSCA:
                    if any(termo.lower() in arquivo for arquivo in arquivos_lower):
                        encontrados.append(termo)
            except Exception as e:
                encontrados = [f"Erro ao acessar pasta: {e}"]
        else:
            encontrados = ["Diretório inexistente"]

        df.at[index, 'Arquivos_Encontrados'] = ', '.join(encontrados) if encontrados else 'Nenhum'

    # Define o novo caminho de saída
    pasta_saida = os.path.dirname(arquivo_excel)
    novo_arquivo = os.path.join(pasta_saida, "docs_verificados.xlsx")

    # Criar DataFrame do resumo com colunas específicas
    colunas_resumo = ['codigos_af', 'Caminho', 'Arquivos_Encontrados']
    colunas_existentes = [col for col in colunas_resumo if col in df.columns]
    df_resumo = df[colunas_existentes]

    # Filtrar linhas que NÃO contenham "Diretório inexistente" nem "Nenhum"
    df_resumo = df_resumo[
        ~df_resumo['Arquivos_Encontrados'].isin(['Diretório inexistente', 'Nenhum'])
    ]

    # Salva o Excel com duas abas
    with pd.ExcelWriter(novo_arquivo, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Verificação Completa')
        df_resumo.to_excel(writer, index=False, sheet_name='Resumo')

    print(f"Verificação concluída. Resultado salvo em: {novo_arquivo}")

    # Abre o diretório no explorador de arquivos
    abrir_diretorio(pasta_saida)

def abrir_diretorio(pasta):
    """Abre o diretório no sistema operacional (somente localmente)."""
    sistema = platform.system()
    try:
        if sistema == "Windows":
            subprocess.run(['explorer', os.path.realpath(pasta)])
        elif sistema == "Darwin":  # macOS
            subprocess.run(['open', pasta])
        elif sistema == "Linux":
            subprocess.run(['xdg-open', pasta])
        else:
            print("Sistema operacional não reconhecido para abrir diretório.")
    except Exception as e:
        print(f"Erro ao tentar abrir o diretório: {e}")

if __name__ == "__main__":
    caminho_entrada = "ftp/dir/DIR_afs.xlsx"
    verificar_arquivos_por_caminho(caminho_entrada)

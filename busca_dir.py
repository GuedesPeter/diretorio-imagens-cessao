import pyodbc
import pandas as pd

def consulta_afs(afs, conn_str, output_excel):
    """
    Consulta o caminho para uma lista de AFs e salva o resultado em Excel.

    :param afs: lista de números AF (int)
    :param conn_str: string de conexão ODBC para o banco SQL Server com autenticação Windows
    :param output_excel: caminho do arquivo Excel de saída
    """
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    resultados = []

    query_template = """
    DECLARE @AF INT = ?;
    DECLARE @PATH NVARCHAR(MAX) = (SELECT [path] FROM ufnUrl_FTP(@AF));
    DECLARE @RESULTADO VARCHAR(MAX) = (
        SELECT 
            @PATH + '\\' + REPLICATE('0', 2 - LEN(DAY(af.data_cadastro))) + CAST(DAY(af.data_cadastro) AS VARCHAR) + '\\' + cast(af.codigo as varchar) + '\\'
        FROM
            AUXILIO_FINANCEIRO AF
        WHERE 
            AF.CODIGO = @AF
            AND AF.CONVENIO = 3
    );
    SELECT @RESULTADO AS DIR;
    """

    for af in afs:
        cursor.execute(query_template, af)
        row = cursor.fetchone()
        caminho = row.DIR if row else None
        resultados.append({'AF': af, 'Caminho': caminho})

    cursor.close()
    conn.close()

    df = pd.DataFrame(resultados)
    df.to_excel(output_excel, index=False)
    print(f"Arquivo salvo em {output_excel}")

if __name__ == "__main__":
    # Lê a lista de AFs do arquivo Excel
    arquivo_entrada = "ftp/lista/lista_afs.xlsx"  
    df_afs = pd.read_excel(arquivo_entrada)

    if 'CODIGO_AF' not in df_afs.columns:
        raise ValueError("A coluna 'CODIGO_AF' não foi encontrada no arquivo Excel.")

    lista_afs = df_afs['CODIGO_AF'].dropna().astype(int).tolist()

    conexao = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=FAC-DB53.facta.com.br;"
        "DATABASE=Facta_01_BaseDados;"
        "Trusted_Connection=yes;"
        "ApplicationIntent=ReadOnly;"
    )

    arquivo_saida = "ftp/dir/DIR_afs.xlsx"
    consulta_afs(lista_afs, conexao, arquivo_saida)

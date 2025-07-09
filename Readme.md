# 📘 Consulta e Verificação de Documentos de AFs

## 📌 Objetivo

Este projeto automatiza dois processos essenciais relacionados aos Auxílios Financeiros (AFs):

1. **Consulta dos diretórios de documentos** vinculados a cada AF diretamente do banco de dados.
2. **Verificação da presença de arquivos obrigatórios** dentro desses diretórios.

---

## 🚀 Scripts Disponíveis

| Script | Função |
|--------|--------|
| `consulta_afs.py` | Consulta os diretórios de documentos para cada AF via banco de dados SQL e gera um Excel com os caminhos. |
| `verificar_docs_afs.py` | Acessa cada caminho gerado e verifica a existência dos arquivos esperados como RG, CNH, Selfie, etc. |

---

## 🧱 Requisitos

- **Python 3.8+**
- **Bibliotecas Python:**

### 📦 Instalação das dependências

```bash
pip install pandas openpyxl pyodbc
```

## 📁 Estrutura de Pastas Esperada

```ftp/
├── lista/
│   └── lista_afs.xlsx          # Planilha de entrada com a coluna "CODIGO_AF"
├── dir/
│   ├── DIR_afs.xlsx            # Gerado pelo script consulta_afs.py
│   └── docs_verificados.xlsx   # Gerado pelo script verificar_docs_afs.py
```

### ⚙️ Como Usar

#### 1. Prepare a planilha de entrada
 - Local: ftp/lista/lista_afs.xlsx

- Deve conter a coluna: CODIGO_AF

#### 2. Execute o script de consulta SQL

```
python busca_dir.py
```

#### 3. Execute o script de verificação de arquivos
```
python verificar_arquivos.py
```

- Lê o Excel anterior e verifica se nos diretórios existem arquivos com os seguintes nomes parciais (ignora maiúsculas/minúsculas):

```
RG_FRENTE
CNH
RG_VERSO
SELFIE
RG_FRENTE_TESTEMUNHA
CNH_TESTEMUNHA
RG_VERSO_TESTEMUNHA
arqRG_FRENTE
arqRG_VERSO
arqSelfieIni
arqCNH
arqfotoDocumentoFrente
arqfotoDocumentoVerso
arqDECLARACAO_RESIDENCIA
```
- Gera o arquivo ftp/dir/docs_verificados.xlsx com os resultados.

- Abre automaticamente a pasta com o arquivo salvo.


## ✅ Resultado Final

O Excel docs_verificados.xlsx conterá:

- AF: Código do Auxílio Financeiro

- Caminho: Diretório consultado no FTP

- Arquivos_Encontrados: Lista dos arquivos identificados ou mensagem de erro

- Criação da aba "Resumo" no arquivo final, contendo apenas as AFs que possuem algum documento em seu diretório

## 🛠️ Possíveis Erros & Soluções

| Erro                    | Causa Possível                | Solução                                                                                                                           |
| ----------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `pyodbc.InterfaceError` | Driver ODBC ausente           | Instale o [ODBC Driver 17 for SQL Server](https://learn.microsoft.com/pt-br/sql/connect/odbc/download-odbc-driver-for-sql-server) |
| `Diretório inexistente` | Caminho consultado não existe | Verifique o caminho ou permissões de rede                                                                                         |
| `Erro ao acessar pasta` | Falha de permissão ou rede    | Certifique-se de que o caminho é acessível localmente                                                                             |

## 🤖 Extras e Dicas

 - A verificação é case-insensitive, ou seja, não importa se os arquivos estão em maiúsculas ou minúsculas.

- O script abre automaticamente a pasta ao final — ideal para produtividade.

- Pode ser estendido para enviar o relatório por e-mail, compactar arquivos ou realizar auditorias mais profundas.


## ✨ Contribuição

Sugestões, dúvidas ou melhorias? Fique à vontade para contribuir! Este projeto foi criado para facilitar processos repetitivos com confiabilidade.

## 📦 Disponível em:
Este projeto está disponível no GitHub:

🔗 [github.com/GuedesPeter/](https://github.com/GuedesPeter/diretorios_imagens_cessao)

⭐ Sinta-se à vontade para clonar, adaptar ou contribuir com melhorias!
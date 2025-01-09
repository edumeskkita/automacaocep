import pandas as pd
import requests
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF


# Configuração de envio de emails
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ORIGEM = "eduardomnabarro@gmail.com"
EMAIL_SENHA = "tjhdmawjkkbbgwdn"
EMAIL_DESTINATARIO = "eduardomnabarro@gmail.com"

# Função 1: Consulta CEPs via API e salva os resultados em um CSV
def consulta_ceps_api(arquivo_entrada, arquivo_saida):
    ceps_df = pd.read_csv(arquivo_entrada)  # Lê o CSV com Pandas
    resultados = []

    for cep in ceps_df["CEP"]:  # Supondo que a coluna de CEP no CSV se chama 'CEP'
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if response.status_code == 200:
            dados = response.json()
            if "erro" not in dados:
                resultados.append({
                    "CEP": cep,
                    "Logradouro": dados.get("logradouro", ""),
                    "Bairro": dados.get("bairro", ""),
                    "Cidade": dados.get("localidade", ""),
                    "Estado": dados.get("uf", "")
                })
            else:
                resultados.append({
                    "CEP": cep,
                    "Logradouro": "CEP inválido",
                    "Bairro": "",
                    "Cidade": "",
                    "Estado": ""
                })
        else:
            resultados.append({
                "CEP": cep,
                "Logradouro": "Erro na consulta",
                "Bairro": "",
                "Cidade": "",
                "Estado": ""
            })

    # Converte os resultados em um DataFrame e salva como CSV
    resultados_df = pd.DataFrame(resultados)
    resultados_df.to_csv(arquivo_saida, index=False, encoding='utf-8')

# Função 2: Envio de e-mails personalizados

def envia_emails(arquivo_dados):
    with open(arquivo_dados, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Pula o cabeçalho

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ORIGEM, EMAIL_SENHA)

            for linha in reader:
                # Tratamento de valores ausentes
                cep = linha[0] or "Não disponível"
                logradouro = linha[1] or "Não disponível"
                bairro = linha[2] or "Não disponível"
                cidade = linha[3] or "Não disponível"
                estado = linha[4] or "Não disponível"

                mensagem = MIMEMultipart()
                mensagem["From"] = EMAIL_ORIGEM
                mensagem["To"] = EMAIL_DESTINATARIO  # Substituir com o destinatário real
                mensagem["Subject"] = f"Trajetória Consultoria - Informações sobre o endereço do CEP {cep}"

                corpo_email = f"""
                Olá,

                Seguem os detalhes do endereço consultado para o CEP {cep}:
                - Logradouro: {logradouro}
                - Bairro: {bairro}
                - Cidade: {cidade}
                - Estado: {estado}

                Atenciosamente,
                Trajetória Consultoria
                """
                mensagem.attach(MIMEText(corpo_email, "plain"))
                server.send_message(mensagem)

# Função 3: Geração de relatório PDF
def gera_relatorio_pdf(arquivo_dados, arquivo_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Lê o arquivo CSV usando pandas
    df = pd.read_csv(arquivo_dados)
    df.fillna("", inplace=True)  # Preenche valores nulos com string vazia
    
    linhas_por_pagina = 20  # Define o número máximo de linhas por página
    total_linhas = len(df)
    total_paginas = (total_linhas // linhas_por_pagina) + (1 if total_linhas % linhas_por_pagina != 0 else 0)
    
    for pagina in range(total_paginas):
        pdf.add_page()
        
        # Cabeçalho
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(0, 10, txt="Trajetória Consultoria - Relatório de Endereços Consultados", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=10, style='B')
        pdf.cell(30, 10, "CEP", border=1, align='C')
        pdf.cell(60, 10, "Logradouro", border=1, align='C')
        pdf.cell(40, 10, "Bairro", border=1, align='C')
        pdf.cell(40, 10, "Cidade", border=1, align='C')
        pdf.cell(20, 10, "Estado", border=1, align='C')
        pdf.ln()
        
        # Conteúdo
        pdf.set_font("Arial", size=10)
        inicio = pagina * linhas_por_pagina
        fim = inicio + linhas_por_pagina
        for _, row in df.iloc[inicio:fim].iterrows():
            pdf.cell(30, 10, str(row["CEP"]), border=1)
            pdf.cell(60, 10, str(row["Logradouro"]), border=1)
            pdf.cell(40, 10, str(row["Bairro"]), border=1)
            pdf.cell(40, 10, str(row["Cidade"]), border=1)
            pdf.cell(20, 10, str(row["Estado"]), border=1)
            pdf.ln()
        
        # Rodapé
        pdf.set_y(260)
        pdf.set_font("Arial", size=8)
        pdf.cell(0, 10, txt="Trajetória Consultoria", ln=True, align='C')
        pdf.cell(0, 10, f"Página {pagina + 1} de {total_paginas}", align='C')
    
    # Salva o PDF
    pdf.output(arquivo_pdf)

# Chamando as funções em sequência
if __name__ == "__main__":
    arquivo_entrada = "ceps_lista_30.csv"  # Substituir pelo caminho do arquivo de entrada
    arquivo_saida = "enderecos.csv"
    arquivo_pdf = "relatorio.pdf"

    consulta_ceps_api(arquivo_entrada, arquivo_saida)
    #envia_emails(arquivo_saida)
    gera_relatorio_pdf(arquivo_saida, arquivo_pdf)

    print("Automação concluída com sucesso!")

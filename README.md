Automação de Consultas de CEP

Este projeto realiza consultas de CEP via API, gera um relatório em formato PDF e envia e-mails personalizados com os resultados. Ele foi desenvolvido em Python e utiliza bibliotecas amplamente usadas para automação de tarefas.

Requisitos
•	Python 3.10 ou superior
•	Bibliotecas Python: As seguintes bibliotecas são necessárias: 
o	pandas
o	requests
o	fpdf
o	smtplib (já incluída na biblioteca padrão do Python)
o	email (já incluída na biblioteca padrão do Python)
o	csv (já incluída na biblioteca padrão do Python)

Instalação

1. Instalar o Python
Faça o download e instale o Python 3.10 ou superior.
Durante a instalação, certifique-se de marcar a opção "Add Python to PATH".
2. Criar um ambiente virtual (opcional, mas recomendado)
Para evitar conflitos entre dependências, crie um ambiente virtual:
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
3. Instalar as dependências
Execute o seguinte comando no terminal para instalar as bibliotecas necessárias:
pip install pandas requests fpdf

Configuração

1. Configurar credenciais de e-mail
Edite as variáveis EMAIL_ORIGEM e EMAIL_SENHA no arquivo automacao.py para as suas credenciais de e-mail.

2. Configurar email de destinatário na variável EMAIL_DESTINATARIO no arquivo automacao.py.

3. Configurar os arquivos CSV
•	Prepare um arquivo CSV chamado ceps_lista_30.csv .
•	Certifique-se de que o arquivo contém uma coluna chamada CEP com os CEPs a serem consultados.
Exemplo de arquivo ceps_lista_30.csv:

CEP
01001-000
22041-001
30130-110

Como executar

1.	Execute o script principal no terminal:
python automacao.py
2.	O processo será executado em três etapas:
	Consulta dos CEPs via API e geração do arquivo enderecos.csv.
    Envio de e-mails com as informações obtidas.
	Geração de um relatório em PDF chamado relatorio.pdf.
3.	Os arquivos gerados (enderecos.csv e relatorio.pdf) estarão na mesma pasta do script.


Estrutura do Projeto

projeto/
	automacao.py  # Código principal
	ceps_lista_30.csv  # Arquivo de entrada com CEPs
	enderecos.csv  # Arquivo gerado com os resultados
	relatorio.pdf  # Relatório em PDF gerado
	README.md  # Este arquivo


Possíveis Melhorias

1.   Melhor tratamento de exceções: 
     Capturar e tratar erros específicos durante a consulta de CEPs e envio de e-mails.

2.   Variáveis sensíveis
     As credenciais do e-mail (EMAIL_ORIGEM e EMAIL_SENHA E EMAIL_DESTINO) estão no código. Recomendo usar variáveis de ambiente ou um arquivo .env para armazenar essas informações, utilizando bibliotecas como python-dotenv.

3.  Mensagens de log
    Adicionar mensagens de log para monitorar o progresso e possíveis erros seria útil, especialmente em tarefas longas como envio de e-mails
    Pode-se usar a biblioteca logging para registrar eventos importantes, como consultas bem-sucedidas ou falhas na API.

4.  Validação de CEP: 
    Antes de fazer a chamada à API, validar o formato do CEP. Isso pode evitar chamadas desnecessárias

5.  Tratamento de erros:
    Adicionar tratamento de erros para lidar com situações inesperadas, como falhas na API ou problemas de conexão.

________________________________________
Desenvolvido por Eduardo Nabarro
 


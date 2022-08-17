# face-analysis
Este projeto consiste em uma aplicação Serverless, em **AWS Lambda**, com o objetivo de realizar o reconhecimento facial em imagens. Para tanto, foi utilizado o serviço **AWS S3**, para armazenamento de imagens e Trigger da Lambda, bem como o **AWS Rekognition**, que realiza a detecção de faces nas imagens recebidas. Então, os resultados serão exibidos em um site estático, exibindo tudo o que foi encontrado em uma imagem, com seu respectivo grau de similaridade.

# Dependências

## Instalações

Atualmente, o projeto utiliza o Python em versão 3.9.  Para executá-lo, deve-se instalar as *libs* listadas em **requirements.txt.**, recomendando-se realizar o uso de ambiente virtual.

### Ambiente pela linha de comando

Inicie o virtual env dentro da pasta app

```bash
python -m venv .venv

```

Ative seu virtualenv

```bash
.venv\\Scripts\\activate

```

Instale os requirements

```bash
pip install -r requirements.txt

```

### Ambiente pela IDE PyCharm

- Menu **FIle > Settings > project: <nome_projeto> > Python interpreter**
- Ao lado do menu de seleção do interpretador, clique na roleta de configurações e em **add**.
- Marque a opção **New enviroment**, então define o **Base interpreter** (e.g. Python 3.9).
- Basta confirmar e será criado um diretório **venv** na raíz do projeto.

Para instalar as dependências:

- Pressione Ctrl+Alt+S para abrir as configurações e selecione **Tools > Python Integrated Tools**.
- No campo **Package requirements file,** selecione o arquivo ****requirements.txt
- Ao confirmar, aparecerá uma mensagem na IDE para instalar as dependências no arquivo, basta selecionar **Install requirements**

# Execução


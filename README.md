# face-analysis
Este projeto consiste em uma aplicação Serverless, em **AWS Lambda**, com o objetivo de realizar o reconhecimento facial em imagens. Para tanto, foi utilizado o serviço **AWS S3**, para armazenamento de imagens e Trigger da Lambda, bem como o **AWS Rekognition**, que realiza a detecção de faces nas imagens recebidas. Então, os resultados serão exibidos em um site estático, exibindo tudo o que foi encontrado em uma imagem, com seu respectivo grau de similaridade.

# Arquitetura

![application_architecture](https://user-images.githubusercontent.com/51297679/185242817-cd86ae23-1830-40e2-af48-057d7b52e301.png)

Como mostrado na arquitetura da solução, o fluxo da aplicação será:

1. O usuário faz o upload da imagem no site.
2. Essa ação no bucket dispara o Trigger da Lambda.
3. A Lambda transfere a imagem para o serviço do Rekognition.
4. Esse serviço realiza o reconhecimento facial.
5. Caso sejam identificadas faces, essas informações serão utilizadas para comparação com as imagens categorizadas, no bucket.
6. Então, poderá ser identificado alguém conhecido nessa nova imagem, sendo o resultado retornado ao Lambda.
7. O Lambda publica os resultados no bucket do site.
8. A página do site é atualizada com o resultado, via JavaScript, e então o usuário irá ver quem foi encontrado nas imagens, com o grau de similaridade.

O bucket de site servirá como uma página Web, contendo JavaScript, que permitirá o upload de imagens e exibição dos resultados, enquanto que o bucket de imagens será o como um banco de dados, contendo imagens já categorizadas, indicando quem está presente em cada foto. Ademais, o bocket de site está contido no diretório **face-analysis-site**, na raíz do repositório, bastando fazer seu upload no S3.

# Buckets

Para correto acesso aos recursos, deverão ser feitas algumas configurações nos buckets, pelo console AWS. Para aquele do site, na aba de propriedades, deve-se **habilitar a Hospedagem de site estático**, a fim de que fique disponível em um endpoint da região da AWS. Em seguida, em Permissões, deverá  ter acesso público liberado, para que possa ser acessado pelo navegador. Adicionalmente, em Política do bucket, deverá ser definida a permessão para recuperar objetos do bucket:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::face-analysis-site/*"
        }
    ]
}
```

Também é necessário definir o CORS para o endpoint do site estático:

```
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "http://face-analysis-site.s3-website-us-east-1.amazonaws.com/"
        ],
        "ExposeHeaders": [
            "Access-Control-Allow-Origin"
        ]
    }
]
```
Em AllowedOrigins, substituir pelo endpoint definido na hospedagem do bucket.

No bucket de imagens, deve-se também liberar acesso público e adicionar a permissão para que o endpoint do site possa fazer requisções GET e obter as imagens:

```
{
    "Version": "2012-10-17",
    "Id": "http referer policy get",
    "Statement": [
        {
            "Sid": "Allow get requests originating from face-analysis-site.s3-website-us-east-1.amazonaws.com.",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion"
            ],
            "Resource": "arn:aws:s3:::face-analysis-images/*",
            "Condition": {
                "StringLike": {
                    "aws:Referer": "http://face-analysis-site.s3-website-us-east-1.amazonaws.com/*"
                }
            }
        }
    ]
```
Em StringLike, substituir pelo endpoint definido na hospedagem do bucket.

Outro ponto é que, para o Bucket de imagens, devem ser criados os diretórios:
- **input/**: Irá conter as imagens a serem indexadas pelo Job, que serão a base para o match.
- **output/**: Conterá as imagens do upload para verificar o match com aquelas em input/, que servirão de Trigger para a Lambda.

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


## Variáveis de Ambiente

No momento, as variáveis de ambiente necessárias para execução do projeto são:

1. **COLLECTION_ID** - Nome da coleção a ser usada para indexação de imagens, pelo serviço do AWS Rekognition. Deverá ser criada ao executar o módulo do Job para indexação de imagens.
2. **FACES_BUCKET** - Nome do bucket que conterá as imagens para indexação pelo Rekognition, usadas na Lambda e Job. Deverá ser previamente criado no console AWS.
3. **SITE_BUCKET** - Nome do bucket que conterá a pagina web para exibir os resultados. Deverá ser previamente criado no console AWS.


## Logs

Foi implementado um módulo para geração de **Logs** da aplicação, de modo que são gerados arquivos de Log correspondentes ao dia em que a aplicação é executada. O módulo de Log é configurado para que, a cada dia, seja usado um arquivo diferente para o registro, mantendo melhor rastreabilidade. Isso foi feito pensando em como seria útil para um ambiente de produção e desenvolvimento.  

Assim sendo, tanto para o Job quanto para a Lambda, são garvados os possíveis erros, mantendo a pilha de exceção, a fim de facilitar o debug. Além disso, é feito registro dos resultados com sucesso. Adicionalmente, arquivos de log com duração de determinado período (Inicialmente 30 dias) são removidos, evitando acúmulo desnecessário.

## Organização

A arquitetura da aplicação está contida em **src**, dividida em módulos:

1. **common**: Módulos para uso comum no restante da aplicação, possuindo:
    
    1.1. **exceptions**: Classes de exceção personalizadas.
    
    1.2. **logger**: Classe para geração de log personalizado. 
2.**services**: Classes responsáveis pela conexão com serviços AWS S3 e Rekognition. Nesse, **image_index** é responsável pela indexação de imagens e comunicação com S3, enquanto que **face_analysis** irá receber eventos de upload no Bucket direcionados à Lambda.
3. **lambda_function**: Irá ser chamado pelo Lambda e direcionar os eventos para o módulo correspondente.
4. **job_index_collection**: Serám chamado pelo Job executado em EC2, a fim de indexar todas as imagens do Bucket.

## Testes

Separadamente dos módulos que definem as funcionalidades, foram criados os módulos de testes unitários, no diretório **tests**. Para sua estrutura, é recomendado definir o pacote:

- **features**: Conterá os arquivos de teste referentes a cada feature implementada, os quais foram separados por módulos, buscando ter a cobertura da maior parte do código. Deve-se definir as variáveis de ambiente antes da execução:

1. **COLLECTION_ID** - Nome da coleção usada nos teste, devendo ser definida com um nome diferente dquele usada no outro ambiente (e.g. faces-test). Deverá ser criada ao executar os testes.
2. **FACES_BUCKET** - Nome do bucket de teste que conterá as imagens, deverendo ser previamente criado no console AWS (e.g. face-analysis-images-test).
3. **SITE_BUCKET** - Nome do bucket de teste que conterá a pagina web. deverendo ser previamente criado no console AWS (e.g. face-analysis-site-test).

Para implementar os testes de cada funcionalidade:

- Criar um arquivo de teste, sempre iniciado com **test_**, seguido pelo nome da feature.
- No arquivo, criar a classe, sempre iniciando com **Test**, seguido pelo nome da funcionalidade.
- Dentro da classe, criar os métodos de teste, seguindo o padrão de nomeclatura, cobrindo os possíveis fluxos.

Para nomear os métodos de teste, baseou-se o padrão **test[Feature being tested],** definido no item 3 da referência:

[Estratégias populares para nomear testes](https://dzone.com/articles/7-popular-unit-test-naming)

Foi feita uma mudança para adaptação ao padrão do Python. Nesse caso, o nome sempre iniciará com o prefixo **test_**, seguido pelo nome da funcionalidade a ser testada, seguido por uma condição, indicada por um *if*.

A definição dos testes e sua execução são feitos com base na lib do *pytest*. Por assim ser, deve ser criado o módulo de conftest.py, o qual deve estar sempre em **tests/conftest.py**. Esse contém as configurações inicias para antes de executar os testes, tais como fixtures da própria lib, para outras configurações a serem feitas antes e/ou após certos testes.

Para execução de todos os testes, basta executar o comando do pytest apontando para o diretório tests. Automaticamente, a lib reconhece todos os testes pelo padrão de nomeclatura (todos os arquivos, classes e métodos iniciados com o prefixo test), sendo possível executar testes apenas em diretórios específicos. Deve-se também ter as variáveis de ambiente definidas em algum lugar, como em um arquivo *.env* ou nas opções da IDE.

Para gerar um relatório de cobertura em HTML, executar com os parâmetros:

```
pytest --cov --cov-report=html
```

Para conferir, abrir o **index.html** no dirtório **htmlcov** que for gerado.

O bucket do site pode ser criado vazio, sendo apenas para conter os dados de saída dos testes. Já o bucket de imagens pode ser criado com algumas poucas imagens em input/ e algumas em output/ que tenham match. Os testes devem ser alterados para refletir a quantidade de imagens e matches.

## Padrões e estilos de código.

Foram adicionados arquivos para configuração de **pre-commit**, **flake8** e **black**, a fim de realizar a verificação e manutenção da qualidade do código automaticamente. Assim sendo, ao realizar um commit, será executada a verificação do black, a qual irá, de forma automática, corrigir problemas de formatação e padronização de código, segundo boas práticas. Em seguida, será feita a verificação pelo flake8, a qual irá informar possíveis erros de padronização, segundo as recomendações do **PEP8**. Dessa forma, todos os erros devem ser corrigidos para possibilitar o commit, garantindo a qualidade do código.

Essas configurações foram definidas nos arquivos **.pre-commit-config.yaml, .flake8 e .pyproject.toml**, os quais devem estar sempre na raíz do projeto. Para instalar e atualizar o pre-commit, utilizar:

1. pre-commit install 
2. pip install --upgrade pre-commit
3. pre-commit autoupdate

Feito isso, todas as verificações serão executadas nos commits. Para executá-las manualmente, usar o comando:
 - pre-commit run --all-files
 
 No arquivo do flake8, foram informados alguns erros para serem ignorados, segundo os códigos de erro do PEP8, listado em: https://flake8.pycqa.org/en/2.5.5/warnings.html#error-codes
 
 # Build Automático

Foi utilizado o Git Actions para definição de um workflow para **Integração Contínua**. Esse foi configurado em .github/workflows/python-app.yml, de modo que sempre que for realizado um push ou Pull Request para a branch main, será feito o build definido nesse arquivo. O mesmo irá realizar a verificação de qualidade do código com flake8, bem como executar os testes unitários com Pytest, gerando o relatório de cobertura. Então, caso tudo seja executado com sucesso, é feita a integração.

As variáveis de ambiente necessárias para os testes foram definidas pela configuração de **Secrets** para uso nas Actions.

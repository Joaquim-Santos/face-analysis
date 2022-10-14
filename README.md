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

Assim sendo, tanto para o Job quanto para a Lambda, são garvados os possíveis erros, mantendo a pilha de exceção, a fim de facilitar o debug. Além disso, é feito registro dos resultados com sucesso. Além disso, após determinado período (Inicialmente 30 dias), os arquivos de log correspondentes gerados nesse tempo são removidos, evitando acúmulo desnecessário.

## Organização

A arquitetura da aplicação

# Cadastro Nacional de Endereços para Fins Estatísticos [CNEFE](https://www.ibge.gov.br/estatisticas/sociais/populacao/38734-cadastro-nacional-de-enderecos-para-fins-estatisticos.html?=&t=o-que-e)

![CI](https://github.com/maikereis/CNEFE-data/actions/workflows/ci.yml/badge.svg)
![Coverage Badge](https://raw.githubusercontent.com/maikereis/CNEFE-data/gh-pages/coverage.svg)
![Status](https://img.shields.io/badge/status-in%20refactoring-orange)
![Issues](https://img.shields.io/github/issues/maikereis/CNEFE-data)


---

Este projeto tem como objetivo **baixar, extrair, processar e consolidar** os dados do **Cadastro Nacional de Endereços para Fins Estatísticos (CNEFE)**, disponibilizados pelo [IBGE](https://www.ibge.gov.br/).
O pipeline integra informações do **Censo Demográfico 2022** com metadados territoriais, produzindo **arquivos CSV limpos e estruturados** para análise e utilização em pesquisas e aplicações georreferenciadas.

O CNEFE é uma base de dados de **endereços georreferenciados de domicílios brasileiros**, atualizada periodicamente a cada [censo demográfico](https://www.ibge.gov.br/estatisticas/sociais/saude/22827-censo-demografico-2022.html) e também de forma pontual conforme demandas de pesquisas como a [PNAD Contínua](https://www.ibge.gov.br/estatisticas/sociais/saude/17270-pnad-continua.html) e a [POF](https://www.ibge.gov.br/pof2024/).

## Visão Geral

O pipeline realiza as seguintes etapas principais:

1. **Download dos Dados**
   - Obtém os arquivos do CNEFE diretamente do FTP do IBGE.
   - Baixa também os arquivos de metadados territoriais (UF, municípios, distritos e subdistritos).

2. **Extração dos Arquivos**
   - Descompacta todos os arquivos ZIP dos endereços.

3. **Processamento dos Metadados**
   - Gera arquivos JSON com mapeamentos de códigos para nomes (UF, município, distrito e subdistrito).

4. **Processamento dos Endereços**
   - Processa os arquivos CSV em chunks para economizar memória.
   - Aplica os mapeamentos dos metadados.
   - Padroniza colunas e gera arquivos CSV consolidados e prontos para análise.


### Como Executar o Pipeline

O fluxo completo pode ser executado de forma automatizada usando o Makefile ou manualmente passo a passo.

Via Makefile (Recomendado)

    make all

Isso executará:

1. Download dos dados.

2. Extração dos arquivos.

3. Processamento dos metadados.

4. Processamento final dos endereços.


### Dicionário
As variáveis disponíveis no CNEFE:

| Variável                       | Descrição                                | LEGENDA                                                                                                                                                                                                                     |
|-------------------------------|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `COD_UNICO_ENDERECO`            | Código único do endereço               |                                                                                                                                                                                                                            |
| `COD_UF`                        | Código da UF                           |                                                                                                                                                                                                                            |
| `COD_MUNICIPIO`                | Código do município                    |                                                                                                                                                                                                                            |
| `COD_DISTRITO`                 | Código do distrito                     |                                                                                                                                                                                                                            |
| `COD_SUBDISTRITO`             | Código do subdistrito                  |                                                                                                                                                                                                                            |
| `COD_SETOR`                   | Código do setor                        |                                                                                                                                                                                                                            |
| `NUM_QUADRA`                  | Número da quadra                       | ¹                                                                                                                                                                                                                          |
| `NUM_FACE`                    | Número da face                         |                                                                                                                                                                                                                            |
| `CEP`                         | Código de Endereçamento Postal         |                                                                                                                                                                                                                            |
| `DSC_LOCALIDADE`             | Localidade                              |                                                                                                                                                                                                                            |
| `NOM_TIPO_SEGLOGR`           | Tipo do logradouro                     |                                                                                                                                                                                                                            |
| `NOM_TITULO_SEGLOGR`        | Título do logradouro                   |                                                                                                                                                                                                                            |
| `NOM_SEGLOGR`               | Nome do logradouro                     |                                                                                                                                                                                                                            |
| `NUM_ENDERECO`             | Número no logradouro                   |                                                                                                                                                                                                                            |
| `DSC_MODIFICADOR`         | Modificador do número                  |                                                                                                                                                                                                                            |
| `NOM_COMP_ELEM1`        | Complemento: Elemento 1                |                                                                                                                                                                                                                            |
| `VAL_COMP_ELEM1`       | Complemento: Valor 1                   |                                                                                                                                                                                                                            |
| `NOM_COMP_ELEM2`     | Complemento: Elemento 2                |                                                                                                                                                                                                                            |
| `VAL_COMP_ELEM2`    | Complemento: Valor 2                   |                                                                                                                                                                                                                            |
| `NOM_COMP_ELEM3`  | Complemento: Elemento 3                |                                                                                                                                                                                                                            |
| `VAL_COMP_ELEM3` | Complemento: Valor 3                   |                                                                                                                                                                                                                            |
| `NOM_COMP_ELEM4` | Complemento: Elemento 4                |                                                                                                                                                                                                                            |
| `VAL_COMP_ELEM4` | Complemento: Valor 4                   |                                                                                                                                                                                                                            |
| `NOM_COMP_ELEM5` | Complemento: Elemento 5                |                                                                                                                                                                                                                            |
| `VAL_COMP_ELEM5` | Complemento: Valor 5                   |                                                                                                                                                                                                                            |
| `LATITUDE`         | Latitude do Endereço                |                                                                                                                                                                                                                            |
| `LONGITUDE`       | Longitude do Endereço               |                                                                                                                                                                                                                            |
| `NV_GEO_COORD`   | Nível de geocodificação             | 1 = Endereço - coordenada original do Censo 2022<br>2 = Endereço - coordenada modificada (apartamentos em um mesmo número no logradouro)²<br>3 = Endereço - coordenada estimada (endereços sem coordenadas ou inválidas)³<br>4 = Face de quadra<br>5 = Localidade<br>6 = Setor censitário |
| `COD_ESPECIE`    | Espécie de endereço                | 1 = Domicílio particular<br>2 = Domicílio coletivo<br>3 = Estabelecimento agropecuário<br>4 = Estabelecimento de ensino<br>5 = Estabelecimento de saúde<br>6 = Estabelecimento de outras finalidades<br>7 = Edificação em construção ou reforma<br>8 = Estabelecimento religioso |
| `DSC_ESTABELECIMENTO` | Identificação do estabelecimento |                                                                                                                                                                                                                            |
| `COD_INDICADOR_ESTAB_ENDERECO` | Indicador de estabelecimento          | 1 = Único<br>2 = Múltiplo, até 10 estabelecimentos<br>3 = Múltiplo, mais de 10 estabelecimentos<br>4 = Múltiplo, quantidade desconhecida                                                                                       |
| `COD_INDICADOR_CONST_ENDERECO` | Indicador de construção ou reforma    | 1 = Único<br>2 = Múltiplo, até 10 unidades<br>3 = Múltiplo, mais de 10 unidades<br>4 = Múltiplo, quantidade desconhecida                                                                                                     |
| `COD_INDICADOR_FINALIDADE_CONST` | Indicador de finalidade de construção | 1 = Residencial<br>2 = Não residencial<br>3 = Misto<br>4 = Indeterminado                                                                                                                                                     |
| `COD_TIPO_ESPECIE` | Tipo da edificação dos domicílios | 101 = Casa<br>102 = Casa de vila ou condomínio<br>103 = Apartamento<br>104 = Outros                                                                                                                                          |


### **Notas**
¹ Cada registro representa uma espécie existente no endereço.
² O método utilizado para modificação de endereços de apartamentos em um mesmo número de logradouro está apresentado no documento metodológico da publicação.
³ Os critérios de coordenadas inválidas estão apresentados no documento metodológico da publicação.




## Estrutura de Saída

Após o processamento, o diretório `data/processed` conterá os arquivos CSV consolidados.
Cada linha representa um endereço único com as seguintes informações:

| Coluna          | Descrição                      |
|-----------------|--------------------------------|
| ID_ENDERECO     | Identificador único do endereço |
| ESTADO          | Nome da Unidade Federativa      |
| MUNICIPIO       | Nome do município              |
| DISTRITO        | Nome do distrito               |
| SUBDISTRITO     | Nome do subdistrito            |
| BAIRRO          | Nome do bairro                 |
| RUA             | Nome do logradouro             |
| TIPO_ARRUAMENTO | Tipo do logradouro             |
| NUM_ENDERECO    | Número do endereço             |
| COMPLEMENTO     | Complemento do endereço        |
| CEP             | Código postal                  |
| LATITUDE        | Latitude geográfica            |
| LONGITUDE       | Longitude geográfica          |



### Dicionário de Variáveis

O dicionário completo de variáveis originais pode ser encontrado no [CNEFE – IBGE](https://www.ibge.gov.br/estatisticas/sociais/populacao/38734-cadastro-nacional-de-enderecos-para-fins-estatisticos.html?=&t=downloads)
.
Parte da tabela original já está incluída no início deste repositório.

### Referencias:

* [CNEFE – Cadastro Nacional de Endereços para Fins Estatísticos](https://www.ibge.gov.br/estatisticas/sociais/saude/22827-censo-demografico-2022.html?=&t=o-que-e)

* [Censo Demográfico 2022](https://www.ibge.gov.br/estatisticas/sociais/saude/22827-censo-demografico-2022)

* [PNAD Contínua](https://www.ibge.gov.br/estatisticas/sociais/saude/17270-pnad-continua.html)

* [POF – Pesquisa de Orçamentos Familiares](https://www.ibge.gov.br/pof2024/)


### Documentação / Notas de Projeto
Este projeto está atualmente em refatoração. Alguns scripts ou interfaces podem mudar enquanto o trabalho está em andamento.
* [Comportamento Atual](docs/actual_behavior.md) – Informações sobre o comportamento do pipeline antes do refatoramento.
* [Antes do Refatoramento](docs/pre_refactoring.md) – Estado do código antes do início da refatoração.
* [Design de Domínio](docs/domain_design.md) – Modelo de domínio, agregados, entidades, value objects, serviços e eventos.

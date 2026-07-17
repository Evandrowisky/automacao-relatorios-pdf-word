# Automação de Relatórios PDF e Word

![Banner do projeto](docs/architecture.png)

Ferramenta em Python para extrair texto e dados estruturados de arquivos PDF, exportando os resultados para TXT, CSV, Excel, Word e PDF.

O projeto foi construído com foco em portfólio, organização profissional e evolução contínua. A arquitetura modular facilita a manutenção, a criação de novos exportadores e a adaptação dos padrões de extração para diferentes tipos de documentos.

## Problema resolvido

Empresas e profissionais frequentemente recebem relatórios em PDF e precisam transformar essas informações em formatos editáveis, auditáveis ou prontos para análise. Fazer isso manualmente consome tempo, dificulta padronização e aumenta o risco de erro.

## Solução

A aplicação processa um ou mais PDFs dentro de `input/pdf/`, extrai o texto por página, aplica Regex para obter campos estruturados e gera os formatos escolhidos pelo usuário.

| Formato | Finalidade |
| --- | --- |
| TXT | Texto integral extraído |
| CSV | Dados estruturados e leves |
| XLSX | Análise e filtros no Excel |
| DOCX | Relatório editável |
| PDF | Relatório final formatado |

## Arquitetura

![Arquitetura](docs/architecture.png)

Cada módulo possui uma responsabilidade clara:

- `main.py`: orquestra CLI, múltiplos PDFs e exportações.
- `config.py`: centraliza caminhos, Regex e formatos padrão.
- `pdf_reader.py`: extrai texto por página e texto completo.
- `regex_parser.py`: transforma texto em dados estruturados.
- `text_exporter.py`: gera TXT com o texto integral.
- `csv_exporter.py`: gera CSV consolidado.
- `excel_exporter.py`: gera XLSX formatado.
- `word_generator.py`: gera DOCX a partir de modelo.
- `pdf_converter.py`: converte DOCX para PDF.
- `image_handler.py`: valida imagens usadas no relatório Word.
- `validator.py`: valida entradas e saídas.
- `utils.py`: concentra utilidades reutilizáveis.

## Fluxograma

![Fluxograma](docs/workflow.png)

## Tecnologias utilizadas

- Python 3.11+
- pdfplumber
- python-docx
- docx2pdf
- Pillow
- openpyxl
- argparse
- logging
- unittest

## Estrutura do projeto

```text
automacao-relatorios-pdf-word/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── src/
│   ├── main.py
│   ├── config.py
│   ├── pdf_reader.py
│   ├── regex_parser.py
│   ├── text_exporter.py
│   ├── csv_exporter.py
│   ├── excel_exporter.py
│   ├── word_generator.py
│   ├── pdf_converter.py
│   ├── image_handler.py
│   ├── validator.py
│   └── utils.py
├── templates/
│   └── modelo_relatorio.docx
├── input/
│   ├── pdf/
│   └── images/
├── output/
├── docs/
│   ├── architecture.png
│   ├── workflow.png
│   └── demo.gif
├── examples/
│   ├── pdfs/
│   ├── resultados/
│   └── README.md
└── tests/
```

## Como instalar

Clone o repositório:

```bash
git clone https://github.com/Evandrowisky/automacao-relatorios-pdf-word.git
cd automacao-relatorios-pdf-word
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Adicione um ou mais arquivos PDF em:

```text
input/pdf/
```

Execute com os formatos desejados:

```bash
python src/main.py --txt
python src/main.py --xlsx
python src/main.py --csv --xlsx
python src/main.py --txt --csv --xlsx
python src/main.py --all
```

Também é possível executar sem argumentos. Nesse caso, a aplicação usa os formatos definidos em `src/config.py`.

Para ver todos os argumentos:

```bash
python src/main.py --help
```

## Saídas geradas

As saídas são organizadas por tipo:

```text
output/
├── txt/
├── csv/
├── excel/
├── docx/
└── pdf/
```

Exemplos:

```text
output/txt/relatorio_inspecao_01.txt
output/csv/dados_extraidos.csv
output/excel/dados_extraidos.xlsx
output/docx/relatorio_inspecao_01_relatorio.docx
output/pdf/relatorio_inspecao_01_relatorio.pdf
```

## Configuração dos formatos

Os formatos padrão ficam em `src/config.py`:

```python
output_formats = {
    "txt": True,
    "csv": True,
    "xlsx": True,
    "docx": False,
    "pdf": False,
}
```

Por padrão, TXT, CSV e Excel ficam ativos. DOCX e PDF final ficam desativados porque dependem do modelo Word e, para conversão PDF, do Microsoft Word disponível no ambiente.

## Extração por Regex

Os campos estruturados também ficam centralizados em `src/config.py`:

```python
DEFAULT_REGEX_PATTERNS = {
    "titulo": r"Título:\s*(?P<valor>.+)",
    "cliente": r"Cliente:\s*(?P<valor>.+)",
    "data": r"Data:\s*(?P<valor>.+)",
    "resumo": r"Resumo:\s*(?P<valor>[\s\S]+)",
}
```

Quando um campo não é encontrado, a aplicação preenche `Não encontrado`, registra aviso no log e continua processando os próximos arquivos.

## Exemplos

A pasta `examples/` contém PDFs fictícios e resultados demonstrativos sem dados reais:

```text
examples/
├── pdfs/
│   ├── relatorio_inspecao_01.pdf
│   ├── relatorio_inspecao_02.pdf
│   └── relatorio_inspecao_03.pdf
├── resultados/
│   ├── exemplo_saida.txt
│   ├── exemplo_saida.csv
│   └── exemplo_saida.xlsx
└── README.md
```

## Casos de uso

- Digitalização de relatórios.
- Consolidação de documentos.
- Preparação de dados para análise.
- Migração de informações.
- Criação de bases para Power BI.
- Geração de relatórios automatizados.
- Auditoria do texto extraído antes da estruturação.

## Testes

Execute:

```bash
python -m unittest discover tests
```

A suíte cobre:

- extração de texto;
- exportação para TXT;
- exportação para CSV;
- exportação para Excel;
- múltiplos PDFs;
- campos não encontrados;
- criação das pastas de saída;
- argumentos da linha de comando.

## Prints

![Fluxo da aplicação](docs/workflow.png)

## GIF demonstrativo

![Demonstração](docs/demo.gif)

## Roadmap

- Permitir configuração de Regex por arquivo externo.
- Criar perfis de extração por tipo de documento.
- Adicionar exportação para JSON.
- Criar relatório de erros em arquivo separado.
- Adicionar integração contínua com GitHub Actions.
- Criar interface gráfica simples.
- Adicionar suporte a OCR para PDFs escaneados.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

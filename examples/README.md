# Exemplos fictícios

Esta pasta contém arquivos criados apenas para demonstração do projeto.

Nenhum PDF possui dados reais ou confidenciais.

## PDFs de entrada

Os arquivos em `examples/pdfs/` simulam relatórios de inspeção com campos simples:

- `Título`
- `Cliente`
- `Data`
- `Resumo`

## Resultados esperados

Os arquivos em `examples/resultados/` mostram exemplos de saída:

- `exemplo_saida.txt`: texto integral separado por páginas.
- `exemplo_saida.csv`: dados estruturados consolidados.
- `exemplo_saida.xlsx`: planilha com os dados extraídos.

Para testar a aplicação com esses arquivos, copie os PDFs de `examples/pdfs/` para `input/pdf/` e execute:

```bash
python src/main.py --txt --csv --xlsx
```

# Auditoria final - Comparativo 54 x 54 ENEM 2025 Natal/RN

Gerado em: 2026-06-25T14:22:55-03:00

## Veredito

**Status:** APROVADO.

Os dados do estudo foram recalculados a partir do `RESULTADOS_2025.csv` local, que já bate CRC32 e tamanho com o ZIP oficial do INEP. Os códigos das escolas foram conferidos no Censo Escolar 2025/INEP. A amostra final tem 216 linhas, com 54 alunos por escola, e o CSV público não exporta identificador individual original.

## Fontes auditadas

- ENEM 2025: `/Volumes/KINGSTON/apps/microdados_enem_2025/DADOS/RESULTADOS_2025.csv`
- Verificação ENEM local x ZIP oficial: `/Volumes/KINGSTON/apps/microdados_enem_2025/analises_primi_2025_cop30/outputs/verificacao_crc_local_vs_zip_oficial_2025.json`
- Censo Escolar 2025: `/Volumes/KINGSTON/apps/microdados_enem_2025/analises_primi_2025_cop30/cache/microdados_censo_escolar_2025.zip`
- Resumo publicado: `/Volumes/KINGSTON/apps/microdados_enem_2025/analises_primi_2025_cop30/outputs/comparativo_escolas_natal_2025_resumo.csv`
- Amostra publicada: `/Volumes/KINGSTON/apps/microdados_enem_2025/analises_primi_2025_cop30/outputs/comparativo_escolas_natal_2025_amostra_54x54.csv`

## Códigos oficiais das escolas

| Código INEP | Nome no Censo Escolar 2025 | Município/UF | Usado? |
|---:|---|---|---|
| 24057134 | COLEGIO MARISTA DE NATAL | Natal/RN | sim |
| 24069191 | CENTRO DE EDUCACAO INTEGRADA S A - ROMUALDO | Natal/RN | sim |
| 24088846 | COLEGIO PORTO | Natal/RN | sim |
| 24097004 | COLEGIO CIENCIAS APLICADAS | Natal/RN | sim |
| 24350303 | CENTRO DE EDUCACAO INTEGRADA MAIS LTDA | Natal/RN | não |

## Contagens e filtros

| Escola | Bruto no ENEM | Excluídos | Pool 5 notas | Amostra | Critério | Top 54 OK? |
|---|---:|---:|---:|---:|---|---|
| CEI S/A Romualdo | 141 | 2 | 139 | 54 | top_54_media_5 | sim |
| Ciências Aplicadas | 56 | 2 | 54 | 54 | todos_5_notas | sim |
| Colégio Porto | 100 | 4 | 96 | 54 | top_54_media_5 | sim |
| Marista de Natal | 171 | 0 | 171 | 54 | top_54_media_5 | sim |

## Checagens automáticas

- Amostra final tem 216 linhas: `True`.
- Contagem 54 por escola confere: `True`.
- Médias do resumo conferem com recálculo: `True`.
- CSV público sem `NU_SEQUENCIAL`/`NU_INSCRICAO`: `True`.
- Código CEI Mais não usado: `Censo Escolar identifica como CENTRO DE EDUCACAO INTEGRADA MAIS LTDA, diferente do CEI S/A Romualdo pedido`.

## Hashes SHA-256

- `RESULTADOS_2025.csv`: `5df5ebed6395a3e69e3dc3b3c9731930312597318ff4dfc178b136514796803d`
- `microdados_censo_escolar_2025.zip`: `4dd0c065492ec379c217457188932742748f3734c24d6ca27a2aea44aa010a5a`
- `comparativo_escolas_natal_2025_resumo.csv`: `3d604953fcfefe15a64ae8901f9f00070441eec87327ceca31c7d59cc52d313f`
- `comparativo_escolas_natal_2025_amostra_54x54.csv`: `6c4e5642a060c60d3890bddd26e26c8176edef1f3d1f8b709f071e4b590a76c6`

## Observação metodológica

Este estudo não é média geral bruta das escolas. Ele compara N equalizado: todos os 54 alunos do Ciências Aplicadas com os 54 melhores de Porto, CEI S/A Romualdo e Marista de Natal, usando média simples das 5 notas como régua.

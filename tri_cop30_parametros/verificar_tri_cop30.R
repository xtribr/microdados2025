# =============================================================================
# verificar_tri_cop30.R
# PROVA REPRODUTÍVEL: os parâmetros TRI (a, b, c) da aplicação COP30/BAM do
# ENEM 2025 (Belém, Ananindeua e Marituba) ESTÃO publicados nos microdados,
# no arquivo ITENS_PROVA_2025.csv, sob os códigos de prova 1499-1538.
#
# O que este script mostra, usando SÓ os 2 arquivos públicos do INEP:
#   (1) Os códigos de prova dos candidatos da COP30 no RESULTADOS (1583-1634,
#       rótulo "BAM2" no Dicionário) têm 0 linhas no ITENS_PROVA;
#   (2) MAS o gabarito dos cadernos 1502-1532 do ITENS_PROVA é IDÊNTICO,
#       posição por posição, ao TX_GABARITO oficial gravado no RESULTADOS
#       para TODOS os candidatos BAM2 — logo são os mesmos cadernos;
#   (3) Esses cadernos não têm NENHUM item em comum com a prova Regular
#       (1447-1486) nem com a Reaplicação (1539-1582) — é uma prova própria,
#       com parâmetros próprios.
#
# Requisitos: R + pacote data.table (install.packages("data.table"))
# Dados: Microdados ENEM 2025 (gov.br/inep) — RESULTADOS_2025.csv e
#        ITENS_PROVA_2025.csv na pasta indicada abaixo.
# =============================================================================

library(data.table)

# >>> AJUSTE AQUI: pasta onde estão os CSVs dos microdados <<<
PASTA_DADOS <- "/Volumes/Kingston 1/microdados_enem_2025/DADOS"

# -----------------------------------------------------------------------------
# Passo 1 — ITENS_PROVA: os códigos "BAM2" não existem; 1499-1538 existem
# -----------------------------------------------------------------------------
itens <- fread(file.path(PASTA_DADOS, "ITENS_PROVA_2025.csv"),
               sep = ";", encoding = "Latin-1")

cat("\n== PASSO 1: o que existe no ITENS_PROVA ==\n")
cat("Linhas com CO_PROVA 1583-1634 (códigos BAM2 do RESULTADOS):",
    itens[CO_PROVA >= 1583 & CO_PROVA <= 1634, .N], " <- por isso 'ninguém achou'\n")
cat("Linhas com CO_PROVA 1499-1538 (família COP30/BAM):",
    itens[CO_PROVA >= 1499 & CO_PROVA <= 1538, .N], "\n")
cat("...com os 3 parâmetros preenchidos:",
    itens[CO_PROVA >= 1499 & CO_PROVA <= 1538 &
          !is.na(NU_PARAM_A) & !is.na(NU_PARAM_B) & !is.na(NU_PARAM_C), .N], "\n")

# -----------------------------------------------------------------------------
# Passo 2 — gabarito de ITENS (1502-1532) == TX_GABARITO dos alunos BAM2
# -----------------------------------------------------------------------------
# mapa dos 16 cadernos principais: código no RESULTADOS -> código no ITENS
mapa <- rbind(
  data.table(area = "CH", cod_res = c(1583, 1584, 1585, 1586), cod_itens = c(1520, 1521, 1522, 1523)),
  data.table(area = "LC", cod_res = c(1595, 1596, 1597, 1598), cod_itens = c(1529, 1530, 1531, 1532)),
  data.table(area = "MT", cod_res = c(1607, 1608, 1609, 1610), cod_itens = c(1502, 1503, 1504, 1505)),
  # atenção CN: Verde = 1621->1514 e Cinza = 1622->1513 (a ordem NÃO é crescente)
  data.table(area = "CN", cod_res = c(1619, 1620, 1621, 1622), cod_itens = c(1511, 1512, 1514, 1513))
)

# gabarito reconstruído a partir do ITENS_PROVA, na ordem das posições.
# LC no RESULTADOS tem 50 caracteres: 5 inglês + 5 espanhol + 40 comuns.
gab_itens <- function(cod, area) {
  it <- itens[CO_PROVA == cod][order(CO_POSICAO)]
  if (area == "LC") {
    ing <- it[TP_LINGUA == 0][order(CO_POSICAO), TX_GABARITO]
    esp <- it[TP_LINGUA == 1][order(CO_POSICAO), TX_GABARITO]
    com <- it[is.na(TP_LINGUA)][order(CO_POSICAO), TX_GABARITO]
    paste(c(ing, esp, com), collapse = "")
  } else {
    paste(it$TX_GABARITO, collapse = "")
  }
}

cat("\nLendo RESULTADOS_2025.csv (2,1 GB — só 9 colunas; aguarde ~1-3 min)...\n")
res <- fread(file.path(PASTA_DADOS, "RESULTADOS_2025.csv"), sep = ";", encoding = "Latin-1",
             select = c("CO_PROVA_CN", "CO_PROVA_CH", "CO_PROVA_LC", "CO_PROVA_MT",
                        "TX_GABARITO_CN", "TX_GABARITO_CH", "TX_GABARITO_LC", "TX_GABARITO_MT",
                        "CO_MUNICIPIO_PROVA"),
             showProgress = FALSE)

cat("\n== PASSO 2: gabarito do ITENS x gabarito oficial dos candidatos BAM2 ==\n")
verif <- mapa[, {
  col_cod <- paste0("CO_PROVA_", area)
  col_gab <- paste0("TX_GABARITO_", area)
  alunos  <- res[get(col_cod) == cod_res & get(col_gab) != ""]
  gab_oficial <- alunos[, unique(get(col_gab))]
  g_itens <- gab_itens(cod_itens, area)
  .(n_candidatos     = nrow(alunos),
    gabaritos_unicos = length(gab_oficial),
    confere          = length(gab_oficial) == 1 && gab_oficial == g_itens)
}, by = .(area, cod_res, cod_itens)]
print(verif)
cat("Cadernos conferidos:", nrow(verif), "| todos idênticos?", all(verif$confere), "\n")

# -----------------------------------------------------------------------------
# Passo 3 — três provas disjuntas (zero itens em comum)
# -----------------------------------------------------------------------------
cat("\n== PASSO 3: itens em comum entre as três provas (esperado: 0) ==\n")
it_bam <- itens[CO_PROVA >= 1499 & CO_PROVA <= 1538, unique(CO_ITEM)]
it_reg <- itens[CO_PROVA >= 1447 & CO_PROVA <= 1498, unique(CO_ITEM)]
it_rea <- itens[CO_PROVA >= 1539 & CO_PROVA <= 1582, unique(CO_ITEM)]
cat("COP30/BAM x Regular:     ", length(intersect(it_bam, it_reg)), "itens em comum\n")
cat("COP30/BAM x Reaplicação: ", length(intersect(it_bam, it_rea)), "itens em comum\n")
cat("Itens únicos da COP30/BAM:", length(it_bam), "\n")

# bônus: todo candidato BAM2 fez prova em Belém/Ananindeua/Marituba
cat("\nMunicípios de prova dos candidatos com código BAM2 (CH 1583-1586):\n")
print(res[CO_PROVA_CH %in% 1583:1586, .N, by = CO_MUNICIPIO_PROVA])
cat("(1501402 = Belém, 1500800 = Ananindeua, 1504422 = Marituba)\n")

cat("\nCONCLUSÃO: os parâmetros a/b/c da prova COP30/BAM são PÚBLICOS —\n")
cat("estão no ITENS_PROVA_2025.csv sob os códigos 1499-1538.\n")

#!/usr/bin/env Rscript
# Diferença entre as provas: Regular (1ª) × COP30/BAM × PPL/2ª aplicação.
# Comparação pela DIFICULDADE MÉDIA DO ITEM (parâmetro B) do caderno Azul de cada aplicação.
# Item-level (parâmetro intrínseco) — não usa notas de PPL (o INEP não separa PPL de reaplicação).
suppressMessages(library(ggplot2))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "palestra_2025/graficos")

# códigos do caderno AZUL de cada aplicação (ITENS_PROVA_2025 / scripts do projeto)
CODES <- list(
  Regular = c(LC = "1459", CH = "1447", CN = "1483", MT = "1471"),
  COP30   = c(LC = "1529", CH = "1520", CN = "1511", MT = "1502"),
  PPL     = c(LC = "1549", CH = "1539", CN = "1569", MT = "1559")
)
APP_LABEL <- c(Regular = "Regular (1ª aplicação)", COP30 = "COP30 / BAM",
               PPL = "PPL / 2ª aplicação")
APP_COL   <- c("Regular (1ª aplicação)" = "#1E6FB8", "COP30 / BAM" = "#FF7F0E",
               "PPL / 2ª aplicação" = "#2CA02C")
NOMES <- c(LC = "Linguagens", CH = "Humanas", CN = "Natureza", MT = "Matemática")

it <- read.csv(file.path(BASE, "DADOS/ITENS_PROVA_2025.csv"), sep = ";",
               fileEncoding = "latin1", stringsAsFactors = FALSE)
it$B    <- suppressWarnings(as.numeric(it$NU_PARAM_B))
it$aban <- as.character(it$IN_ITEM_ABAN)
it$lg   <- as.character(it$TP_LINGUA)
it <- it[!is.na(it$B), ]                                    # lógico limpo (sem NA)
it <- it[is.na(it$aban) | it$aban != "1", ]                 # tira anulados, NA-safe

rows <- list()
for (app in names(CODES)) {
  for (a in c("LC", "CH", "CN", "MT")) {
    code <- CODES[[app]][a]
    d <- it[it$SG_AREA == a & it$CO_PROVA == code, ]
    if (a == "LC") d <- d[is.na(d$lg) | d$lg != "1", ]      # tira Espanhol (lg=1); mantém Inglês(0)+comuns
    rows[[length(rows) + 1]] <- data.frame(
      app = APP_LABEL[app], area = a, nome = NOMES[a],
      b = mean(d$B), tri = mean(d$B) * 100 + 500, n = nrow(d))
  }
}
df <- do.call(rbind, rows)
df$app  <- factor(df$app, levels = APP_LABEL)
df$area <- factor(df$area, levels = c("LC", "CH", "CN", "MT"),
                  labels = paste0(c("LC", "CH", "CN", "MT"), "\n", NOMES[c("LC","CH","CN","MT")]))
print(df[, c("app", "area", "b", "tri", "n")])

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.minor = element_line(colour = "#ECECEE", linewidth = 0.3),
      plot.title    = element_text(face = "bold", size = 22, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 10)),
      plot.caption  = element_text(size = 9.5, colour = "#8C9298", hjust = 1),
      axis.title    = element_text(colour = "#1D1D20", size = 14),
      axis.text     = element_text(colour = "#6B7076", size = 12),
      legend.title  = element_blank(),
      legend.text   = element_text(colour = "#1D1D20", size = 12),
      legend.position = "top",
      plot.margin   = margin(18, 22, 14, 18))
}

p <- ggplot(df, aes(x = area, y = b, fill = app)) +
  geom_col(position = position_dodge(width = 0.8), width = 0.72) +
  geom_text(aes(label = gsub("\\.", ",", sprintf("%.2f", b))),
            position = position_dodge(width = 0.8), vjust = -0.5, size = 4.2,
            fontface = "bold", colour = "#1D1D20") +
  scale_fill_manual(values = APP_COL) +
  scale_y_continuous(limits = c(0, max(df$b) * 1.18), expand = expansion(mult = c(0, 0))) +
  labs(
    title = "As três provas têm a mesma dificuldade?",
    subtitle = "Dificuldade média do item (parâmetro B da TRI), caderno Azul de cada aplicação. Quanto maior o B, mais difícil.",
    x = NULL, y = "Dificuldade média do item (parâmetro B)",
    caption = paste0("Estudo XTRI — Prof. Alexandre Emerson Melo de Araújo  |  ITENS_PROVA (parâmetros intrínsecos; não usa notas de PPL — INEP não separa PPL de reaplicação)  |  Microdados ENEM 2025 / INEP")) +
  theme_xtri()
ggsave(file.path(OUT, "g06_comparacao_provas.png"), p, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: g06_comparacao_provas.png\n")

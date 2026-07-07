#!/usr/bin/env Rscript
# Dificuldade por posição + Taxa de erro por habilidade — estilo ggplot do deck, dado 2025.
suppressMessages(library(ggplot2))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "palestra_2025/graficos")

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.minor = element_line(colour = "#ECECEE", linewidth = 0.3),
      plot.title    = element_text(face = "bold", size = 22, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 10)),
      plot.caption  = element_text(size = 10, colour = "#8C9298", hjust = 1),
      axis.title    = element_text(colour = "#1D1D20", size = 14),
      axis.text     = element_text(colour = "#6B7076", size = 11),
      legend.title  = element_text(colour = "#1D1D20", size = 12),
      legend.text   = element_text(colour = "#6B7076", size = 10),
      legend.position = "top",
      plot.margin   = margin(18, 22, 14, 18)
    )
}
CAP <- "Estudo XTRI — Prof. Alexandre Emerson Melo de Araújo  |  Caderno Azul (P1)  |  Microdados ENEM 2025 / INEP"
DIF_COLS <- c("Fácil" = "#56C2F2", "Médio" = "#C7CBD0", "Difícil" = "#FB9276", "Muito difícil" = "#FA5230")
NOMES <- c(LC = "Linguagens e Códigos", CH = "Ciências Humanas",
           CN = "Ciências da Natureza", MT = "Matemática")

seq_df <- read.csv(file.path(BASE, "analises_primi_2025_cop30/outputs/itens_sequencia_dificuldade_2025.csv"),
                   stringsAsFactors = FALSE)
seq_df <- seq_df[seq_df$cor == "AZUL", ]
seq_df$categoria <- factor(seq_df$categoria, levels = names(DIF_COLS))
seq_df$hlabel <- gsub("^H", "", seq_df$habilidade)

# ---------- 1) DIFICULDADE POR POSIÇÃO ----------
for (a in c("LC", "CH", "CN", "MT")) {
  d <- seq_df[seq_df$area == a, ]
  if (a == "LC") d <- d[d$lingua_label != "ESP", ]   # mantém Inglês + comuns (1 linha/posição)
  d <- d[!is.na(d$B) & d$categoria %in% names(DIF_COLS), ]  # tira anulados (B vazio)
  d$categoria <- droplevels(d$categoria)
  d <- d[order(d$pos_area), ]

  p <- ggplot(d, aes(x = pos_area, y = B)) +
    geom_smooth(method = "loess", se = FALSE, colour = "#E8431F", linewidth = 1.4, span = 0.5) +
    geom_label(aes(label = hlabel, colour = categoria), fill = "white",
               label.size = 0, size = 4.1, fontface = "bold", label.padding = unit(0.1, "lines")) +
    scale_colour_manual(values = DIF_COLS, name = "Nível de dificuldade", drop = FALSE) +
    scale_x_continuous(breaks = seq(0, 45, 5)) +
    labs(
      title = sprintf("%s — dificuldade ao longo do caderno", NOMES[a]),
      subtitle = "Cada rótulo é a habilidade da questão naquela posição. Cor = nível de dificuldade; linha = tendência.",
      x = "Posição da questão no caderno", y = "Dificuldade do item (parâmetro B da TRI)",
      caption = CAP) +
    theme_xtri()
  ggsave(file.path(OUT, sprintf("g04_dificuldade_posicao_%s.png", a)), p,
         width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
  cat("ok: g04_dificuldade_posicao_", a, ".png\n", sep = "")
}

# ---------- 2) TAXA DE ERRO POR HABILIDADE ----------
hab <- read.csv(file.path(BASE, "analises_primi_2025_cop30/outputs/habilidades_dificuldade_2025.csv"),
                stringsAsFactors = FALSE)
hab$taxa_erro <- 100 - hab$pct_acerto_ponderado
AREA_COL <- c(LC = "#1FAFEF", CH = "#E84855", CN = "#2EC4B6", MT = "#3A86FF")
for (a in c("LC", "CH", "CN", "MT")) {
  d <- hab[hab$area == a, ]
  d <- d[order(d$taxa_erro), ]
  d$habilidade <- factor(d$habilidade, levels = d$habilidade)
  topo <- tail(d[order(d$taxa_erro), "habilidade"], 1)

  p <- ggplot(d, aes(x = taxa_erro, y = habilidade)) +
    geom_col(fill = AREA_COL[a], width = 0.72) +
    geom_text(aes(label = sprintf("%.0f%%", taxa_erro)), hjust = -0.15,
              size = 3.6, colour = "#1D1D20") +
    scale_x_continuous(limits = c(0, max(d$taxa_erro) * 1.12),
                       labels = function(v) paste0(v, "%")) +
    labs(
      title = sprintf("%s — taxa de erro por habilidade", NOMES[a]),
      subtitle = "% de erro nacional por habilidade (H), ordenada. Onde a turma mais erra = onde focar.",
      x = "Taxa de erro (% dos presentes)", y = "Habilidade ENEM",
      caption = CAP) +
    theme_xtri(13)
  ggsave(file.path(OUT, sprintf("g05_taxa_erro_%s.png", a)), p,
         width = 12, height = 8.5, dpi = 150, bg = "#F1F1F2")
  cat("ok: g05_taxa_erro_", a, ".png\n", sep = "")
}
cat("FIM dificuldade + taxa de erro\n")

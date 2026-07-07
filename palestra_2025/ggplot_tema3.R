#!/usr/bin/env Rscript
# Tema 3: "A redação prevê a prova objetiva?" — estilo ggplot original do deck.
# nota×nota na MESMA LINHA do RESULTADOS_2025 (permitido; não cruza PARTICIPANTES).
suppressMessages(library(ggplot2))

BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "palestra_2025/graficos")

# r / r² da base COMPLETA (n=3.067.856) — de correlacao_redacao.json
R  <- c(MT = 0.555, LC = 0.553, CH = 0.511, CN = 0.495)
R2 <- c(MT = 0.308, LC = 0.306, CH = 0.262, CN = 0.245)
NOME <- c(MT = "Matemática", LC = "Linguagens", CH = "Humanas", CN = "Natureza")
N_TOTAL <- 3067856

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.minor = element_line(colour = "#ECECEE", linewidth = 0.3),
      strip.text    = element_text(face = "bold", colour = "#1D1D20", size = 13),
      plot.title    = element_text(face = "bold", size = 22, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 10)),
      plot.caption  = element_text(size = 10, colour = "#8C9298", hjust = 1),
      axis.title    = element_text(colour = "#1D1D20", size = 14),
      axis.text     = element_text(colour = "#6B7076", size = 11),
      legend.title  = element_text(colour = "#1D1D20", size = 12),
      legend.text   = element_text(colour = "#6B7076", size = 10),
      plot.margin   = margin(18, 22, 14, 18)
    )
}
CAP <- "Estudo XTRI — Prof. Alexandre Emerson Melo de Araújo  |  nota × nota (mesma linha, RESULTADOS)  |  Microdados ENEM 2025 / INEP"

# ---------- g03a: barras de r² por área ----------
dfb <- data.frame(area = names(R2), r2 = as.numeric(R2) * 100, r = as.numeric(R),
                  nome = NOME[names(R2)])
dfb$area <- factor(dfb$area, levels = names(sort(R2, decreasing = TRUE)))
dfb$lab  <- sprintf("%.0f%%", dfb$r2)

pa <- ggplot(dfb, aes(x = area, y = r2)) +
  geom_col(width = 0.66, fill = "#E8431F") +
  geom_text(aes(label = lab), vjust = -0.5, size = 6, fontface = "bold", colour = "#1D1D20") +
  geom_text(aes(label = gsub("\\.", ",", sprintf("r = %.2f", r))), y = 3, size = 4.2, colour = "white") +
  scale_x_discrete(labels = function(x) paste0(x, "\n", NOME[x])) +
  scale_y_continuous(limits = c(0, 40), breaks = seq(0, 40, 10),
                     labels = function(v) paste0(v, "%")) +
  labs(
    title = "A redação prevê a prova objetiva? Só em parte.",
    subtitle = "Quanto da nota objetiva a redação \"explica\" (r², variância compartilhada). Repare: quase igual em Matemática e Linguagens.",
    x = NULL, y = "% da nota objetiva explicada pela redação",
    caption = paste0(CAP, "  |  n = 3.067.856")
  ) +
  theme_xtri()
ggsave(file.path(OUT, "g03a_ggplot_redacao_r2.png"), pa, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: g03a_ggplot_redacao_r2.png\n")

# ---------- g03b: densidade redação × objetiva (facet 2x2) ----------
df <- read.csv(file.path(BASE, "palestra_2025/amostra_redacao_objetiva.csv"), stringsAsFactors = FALSE)
long <- do.call(rbind, lapply(c("MT", "LC", "CH", "CN"), function(a) {
  data.frame(RED = df$RED, OBJ = df[[a]], area = a, stringsAsFactors = FALSE)
}))
long$face <- factor(sprintf("%s — %s", long$area, NOME[long$area]),
                    levels = sprintf("%s — %s", names(sort(R, decreasing = TRUE)),
                                     NOME[names(sort(R, decreasing = TRUE))]))
lab_df <- data.frame(
  face = factor(sprintf("%s — %s", names(R), NOME[names(R)]), levels = levels(long$face)),
  RED = 120, OBJ = 900, lab = gsub("\\.", ",", sprintf("r = %.2f", as.numeric(R)))
)

pb <- ggplot(long, aes(x = RED, y = OBJ)) +
  geom_bin2d(bins = 60) +
  scale_fill_gradientn(colours = c("#EAF4FB", "#9AD1F0", "#1FAFEF", "#1565A0", "#0B2E4F"),
                       trans = "sqrt", name = "candidatos") +
  geom_smooth(method = "lm", se = FALSE, colour = "#E8431F", linewidth = 1) +
  geom_text(data = lab_df, aes(label = lab), colour = "#1D1D20", fontface = "bold",
            size = 5, hjust = 0) +
  facet_wrap(~ face, ncol = 2) +
  labs(
    title = "Nuvem larga = previsão fraca: a redação não \"entrega\" a nota objetiva",
    subtitle = "Cada painel: nota de Redação (x) × nota TRI da área (y). Reta vermelha = tendência linear. r = correlação na base completa.",
    x = "Nota de Redação (0–1000)", y = "Nota TRI da área objetiva",
    caption = paste0(CAP, "  |  amostra n = 120.000")
  ) +
  theme_xtri(14)
ggsave(file.path(OUT, "g03b_ggplot_redacao_densidade.png"), pb, width = 13.33, height = 8.4, dpi = 150, bg = "#F1F1F2")
cat("ok: g03b_ggplot_redacao_densidade.png\n")
cat("FIM tema 3\n")

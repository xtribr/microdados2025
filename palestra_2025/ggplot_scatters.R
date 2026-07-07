#!/usr/bin/env Rscript
# Scatters "acerto não é nota" no estilo ggplot ORIGINAL do deck 2024, com dado 2025.
# acertos × NU_NOTA_TRI, cor = acrt_dif (proporção de itens difíceis acertados).
suppressMessages(library(ggplot2))

BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "palestra_2025/graficos")
dir.create(OUT, showWarnings = FALSE, recursive = TRUE)

# paleta rainbow igual à do deck: 0=vermelho -> 1=roxo
rainbow_cols <- c("#E8000B", "#FF7F0E", "#F5D800", "#2CA02C", "#17BECF", "#1F77E8", "#7A17E8")

areas <- list(
  LC = list(nome = "Linguagens e Códigos", iv = 45),
  CH = list(nome = "Ciências Humanas",       iv = 45),
  CN = list(nome = "Ciências da Natureza",   iv = 42),
  MT = list(nome = "Matemática",             iv = 43)
)

theme_xtri <- function() {
  theme_minimal(base_size = 15) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.minor = element_line(colour = "#ECECEE", linewidth = 0.3),
      plot.title    = element_text(face = "bold", size = 22, colour = "#1D1D20",
                                   margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 10)),
      plot.caption  = element_text(size = 10, colour = "#8C9298", hjust = 1),
      axis.title    = element_text(colour = "#1D1D20", size = 14),
      axis.text     = element_text(colour = "#6B7076", size = 11),
      legend.title  = element_text(colour = "#1D1D20", size = 12),
      legend.text   = element_text(colour = "#6B7076", size = 10),
      plot.margin   = margin(18, 22, 14, 18)
    )
}

for (a in names(areas)) {
  nome <- areas[[a]]$nome; iv <- areas[[a]]$iv
  df <- read.csv(file.path(BASE, sprintf("palestra_2025/plot_data/scatter_%s.csv", a)),
                 stringsAsFactors = FALSE)
  df$acrt_dif <- suppressWarnings(as.numeric(df$acert_dif))

  # subtítulo calculado do PRÓPRIO dado plotado -> x sempre casa com o texto
  mx    <- max(df$acertos)
  n_mx  <- sum(df$acertos == mx)
  notax <- max(df$nota[df$acertos == mx])
  sub <- sprintf("Mesmo nº de acertos → notas diferentes  |  %s candidatos fizeram %d acertos (nota máx. %s)",
                 format(n_mx, big.mark = "."), mx, format(notax, decimal.mark = ","))

  p <- ggplot(df, aes(x = acertos, y = nota, colour = acrt_dif)) +
    geom_jitter(width = 0.18, height = 0, size = 0.45, alpha = 0.35) +
    scale_colour_gradientn(colours = rainbow_cols, limits = c(0, 1), name = "acrt_dif") +
    scale_x_continuous(breaks = sort(unique(c(seq(0, iv, 5), iv))), limits = c(0, iv + 1)) +
    labs(
      title = sprintf("ENEM 2025 — %s: acerto não é nota", nome),
      subtitle = sub,
      x = sprintf("Número de Acertos (%s, de %d)", a, iv),
      y = "NU_NOTA_TRI",
      caption = "Estudo XTRI — Prof. Alexandre Emerson Melo de Araújo  |  amostra Regular P1 (~100 mil)  |  Microdados ENEM 2025 / INEP"
    ) +
    guides(colour = guide_colourbar(barheight = unit(4.2, "cm"), barwidth = unit(0.45, "cm"))) +
    theme_xtri()

  ggsave(file.path(OUT, sprintf("g01_ggplot_scatter_%s.png", a)),
         p, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
  cat("ok:", sprintf("g01_ggplot_scatter_%s.png", a), "\n")
}
cat("FIM scatters ggplot\n")

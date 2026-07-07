#!/usr/bin/env Rscript
# Barras: maior média TRI (4 objetivas) por estado, colorido por rede da escola do aluno.
suppressMessages(library(ggplot2))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "palestra_2025/graficos")
d <- read.csv(file.path(BASE, "palestra_2025/top_uf.csv"), stringsAsFactors = FALSE, fileEncoding = "UTF-8")
d <- d[order(d$media4), ]
d$uf <- factor(d$uf, levels = d$uf)
REDE <- c("Privada" = "#FA5230", "Federal" = "#1FAFEF", "Estadual" = "#2EC4B6", "Municipal" = "#8C9298")

theme_xtri <- function(base = 15) theme_minimal(base_size = base) + theme(
  plot.background = element_rect(fill = "#F1F1F2", colour = NA),
  panel.background = element_rect(fill = "white", colour = NA),
  panel.grid.major = element_line(colour = "#DEDEE1", linewidth = 0.4),
  panel.grid.minor = element_blank(),
  plot.title = element_text(face = "bold", size = 22, colour = "#1D1D20", margin = margin(b = 2)),
  plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 10)),
  plot.caption = element_text(size = 10, colour = "#8C9298", hjust = 1),
  axis.title = element_text(colour = "#1D1D20", size = 14),
  axis.text = element_text(colour = "#6B7076", size = 12),
  legend.title = element_blank(), legend.text = element_text(size = 12),
  legend.position = "top", plot.margin = margin(18, 22, 14, 18))

p <- ggplot(d, aes(x = media4, y = uf, fill = rede)) +
  geom_col(width = 0.72) +
  geom_text(aes(label = gsub("\\.", ",", sprintf("%.1f", media4))), hjust = -0.15, size = 4, colour = "#1D1D20") +
  scale_fill_manual(values = REDE) +
  scale_x_continuous(limits = c(0, max(d$media4) * 1.1), expand = expansion(mult = c(0, 0))) +
  labs(title = "Maior nota TRI por estado (média das 4 objetivas)",
       subtitle = "O melhor aluno de cada UF no ENEM 2025. A cor mostra a rede da escola — 26 de 27 são privadas; só RR é federal.",
       x = "Média das 4 provas objetivas (TRI)", y = NULL,
       caption = "Estudo XTRI — Prof. Alexandre Emerson Melo de Araújo  |  Microdados ENEM 2025 / INEP  |  escola: Censo Escolar 2025") +
  theme_xtri()
ggsave(file.path(OUT, "g10b_top_uf_barras.png"), p, width = 12, height = 9, dpi = 150, bg = "#F1F1F2")
cat("ok: g10b_top_uf_barras.png\n")

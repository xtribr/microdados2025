#!/usr/bin/env Rscript
# Gráfico ggplot — as questões mais fáceis de Linguagens + Humanas (ENEM 2025, caderno Azul)
suppressMessages(library(ggplot2))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025/posts_taticos/05_faceis_lc_ch"

CYAN <- "#1FAFEF"; CORAL <- "#FA5230"; INK <- "#1D1D20"; GRAY <- "#8C9298"
theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major.x = element_line(colour = "#E3E3E6", linewidth = 0.4),
      panel.grid.major.y = element_blank(), panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 23, colour = INK, margin = margin(b = 3)),
      plot.subtitle = element_text(size = 13.5, colour = GRAY, margin = margin(b = 12)),
      plot.caption  = element_text(size = 9.5, colour = GRAY, hjust = 0, margin = margin(t = 14)),
      axis.title    = element_text(colour = INK, size = 13),
      axis.text     = element_text(colour = INK, size = 12),
      legend.position = "top", legend.title = element_blank(), legend.text = element_text(size = 12.5),
      plot.title.position = "plot", plot.caption.position = "plot",
      plot.margin   = margin(18, 26, 14, 18)
    )
}

d <- read.csv(file.path(BASE, "faceis.csv"), encoding = "UTF-8")
d$area_f <- factor(ifelse(d$area == "LC", "Linguagens", "Ciências Humanas"),
                   levels = c("Linguagens", "Ciências Humanas"))
d$rot <- factor(paste0(d$q, "  ·  ", d$hab), levels = rev(paste0(d$q, "  ·  ", d$hab)))
vir <- function(x) gsub("\\.", ",", sprintf("%.1f", x))

p <- ggplot(d, aes(x = pct_acerto, y = rot, colour = area_f)) +
  geom_segment(aes(x = 0, xend = pct_acerto, yend = rot), linewidth = 1.1) +
  geom_point(size = 5.6) +
  geom_text(aes(label = paste0(vir(pct_acerto), "%")), hjust = -0.45, size = 4.1, fontface = "bold", show.legend = FALSE) +
  scale_colour_manual(values = c("Linguagens" = CYAN, "Ciências Humanas" = CORAL)) +
  scale_x_continuous(limits = c(0, 100), breaks = seq(0, 100, 20),
                     labels = function(v) paste0(v, "%"), expand = expansion(mult = c(0, 0.02))) +
  labs(title = "As questões mais fáceis de Linguagens e Humanas",
       subtitle = "ENEM 2025 (caderno Azul) — as 15 com maior % de acerto entre as duas áreas. Linguagens domina o topo:\n12 das 15 mais fáceis são de Linguagens; a mais fácil de Humanas (Q57) só aparece em 12º lugar.",
       x = "% de acerto observado", y = NULL,
       caption = "Fonte: Microdados ENEM 2025 / INEP · caderno Azul regular, itens não anulados · rótulo: nº da questão (dia 1) e habilidade · @xandaoxtri") +
  theme_xtri()
ggsave(file.path(BASE, "faceis_lc_ch.png"), p, width = 11, height = 8, dpi = 150, bg = "#F1F1F2")
cat("ok: faceis_lc_ch.png\n")

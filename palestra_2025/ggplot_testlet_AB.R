#!/usr/bin/env Rscript
# Plano A × B do testlet: discriminação (A) vs dificuldade (B) — "aliar os dois".
# Mostra que os 5 itens do testlet (Q6-10) são difíceis E discriminam muito bem.
suppressMessages(library(ggplot2))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "palestra_2025/graficos")

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 23, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 14)),
      plot.caption  = element_text(size = 10, colour = "#8C9298", hjust = 1, margin = margin(t = 12)),
      axis.title    = element_text(colour = "#1D1D20", size = 14),
      axis.text     = element_text(colour = "#6B7076", size = 12),
      legend.position = "none",
      plot.margin   = margin(20, 26, 14, 20)
    )
}
CAP <- "Estudo XTRI — Prof. Alexandre Emerson Melo de Araújo  |  Caderno Azul (P1)  |  Microdados ENEM 2025 / INEP"
DIF_DIFICIL <- "#FB9276"; DIF_MDIFICIL <- "#FA5230"

seq_df <- read.csv(file.path(BASE, "analises_primi_2025_cop30/outputs/itens_sequencia_dificuldade_2025.csv"),
                   stringsAsFactors = FALSE)
lc <- seq_df[seq_df$area == "LC" & seq_df$cor == "AZUL" & seq_df$pos_area >= 6 & seq_df$pos_area <= 45, ]
lc <- lc[!is.na(lc$A) & !is.na(lc$B), ]
lc$testlet <- lc$pos_area >= 6 & lc$pos_area <= 10
cloud <- lc[!lc$testlet, ]
t <- lc[lc$testlet, ]
t$fill <- ifelse(t$categoria == "Difícil", DIF_DIFICIL, DIF_MDIFICIL)
t$qlab <- sprintf("%d", t$pos_area)

medB <- median(lc$B)
A_HI <- 1.70   # Baker: discriminação "muito alta"

xr <- c(min(lc$B) - 0.05, max(lc$B) + 0.08)
yr <- c(min(lc$A) - 0.2, max(lc$A) + 0.35)

p <- ggplot() +
  # quadrante ideal (difícil + discrimina bem) levemente destacado
  annotate("rect", xmin = medB, xmax = xr[2], ymin = A_HI, ymax = yr[2],
           fill = "#FA5230", alpha = 0.05) +
  # linhas de referência
  geom_hline(yintercept = A_HI, linetype = "22", colour = "#8C9298", linewidth = 0.7) +
  geom_vline(xintercept = medB, linetype = "22", colour = "#8C9298", linewidth = 0.7) +
  # nuvem: demais itens de Linguagens
  geom_point(data = cloud, aes(x = B, y = A), colour = "#C7CBD0", size = 4.2, alpha = 0.9) +
  # testlet: bolhas grandes coloridas + número dentro
  geom_point(data = t, aes(x = B, y = A), fill = t$fill, colour = "white",
             shape = 21, size = 13, stroke = 1.4) +
  geom_text(data = t, aes(x = B, y = A, label = qlab), colour = "white",
            fontface = "bold", size = 4.7) +
  # rótulos das referências
  annotate("text", x = xr[1] + 0.02, y = A_HI + 0.12, hjust = 0,
           label = "discriminação muito alta (Baker: A > 1,70)", size = 3.9, colour = "#6B7076") +
  annotate("text", x = medB + 0.015, y = yr[1] + 0.05, hjust = 0,
           label = "→ mais difícil", size = 3.9, colour = "#6B7076") +
  # rótulo do quadrante ideal
  annotate("label", x = xr[2] - 0.02, y = yr[2] - 0.02, hjust = 1, vjust = 1,
           label = "difícil + discrimina bem\n= separa o topo",
           size = 4.1, colour = "#E8431F", fontface = "bold", fill = "#FFFFFF",
           label.size = 0, lineheight = 0.95) +
  scale_x_continuous(limits = xr, expand = c(0, 0)) +
  scale_y_continuous(limits = yr, expand = c(0, 0)) +
  labs(
    title = "Difícil e afiado: o testlet no plano discriminação × dificuldade",
    subtitle = "Cada ponto = uma questão de Linguagens (Azul). Os 5 do testlet (laranja) são difíceis E discriminam muito bem.",
    x = "Dificuldade — parâmetro B da TRI  (maior = mais difícil)",
    y = "Discriminação — parâmetro A da TRI  (maior = separa melhor quem sabe)",
    caption = CAP) +
  theme_xtri()

ggsave(file.path(OUT, "g11c_testlet_AxB.png"), p, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat(sprintf("ok: g11c_testlet_AxB.png  | medianaB=%.2f | testlet A: %.2f-%.2f\n", medB, min(t$A), max(t$A)))

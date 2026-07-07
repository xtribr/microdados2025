#!/usr/bin/env Rscript
# Testlet de Linguagens (Azul P1): Q6–Q10 derivam de UM texto (crônica "De próprio punho").
# Como a turma absorveu o formato? Taxa de erro por questão + escalada de dificuldade.
suppressMessages(library(ggplot2))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "palestra_2025/graficos")

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major.y = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 23, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 16)),
      plot.caption  = element_text(size = 10, colour = "#8C9298", hjust = 1, margin = margin(t = 14)),
      axis.title    = element_text(colour = "#1D1D20", size = 14),
      axis.text     = element_text(colour = "#6B7076", size = 12),
      legend.title  = element_text(colour = "#1D1D20", size = 12),
      legend.text   = element_text(colour = "#6B7076", size = 11),
      legend.position = "top",
      plot.margin   = margin(20, 26, 14, 20)
    )
}
CAP <- "Estudo XTRI — Prof. Alexandre Emerson Melo de Araújo  |  Caderno Azul (P1)  |  Microdados ENEM 2025 / INEP"
DIF_COLS <- c("Fácil" = "#56C2F2", "Médio" = "#C7CBD0", "Difícil" = "#FB9276", "Muito difícil" = "#FA5230")

seq_df <- read.csv(file.path(BASE, "analises_primi_2025_cop30/outputs/itens_sequencia_dificuldade_2025.csv"),
                   stringsAsFactors = FALSE)
lc <- seq_df[seq_df$area == "LC" & seq_df$cor == "AZUL", ]
lc$erro <- 100 - lc$pct_acerto

# Testlet = Q6 a Q10 (posições no caderno). Uma linha por posição (>=6 não tem língua dupla).
t <- lc[lc$pos_area >= 6 & lc$pos_area <= 10, ]
t <- t[order(t$pos_area), ]
t$q <- sprintf("Q%02d", t$pos_area)
t$q <- factor(t$q, levels = t$q)
t$categoria <- factor(t$categoria, levels = names(DIF_COLS))
t$hlabel <- paste0("H", gsub("^H", "", t$habilidade))

# Referência: resto de Linguagens (Q11–Q45) e média do próprio testlet.
resto <- round(mean(lc$erro[lc$pos_area >= 11]), 1)
media_testlet <- round(mean(t$erro), 1)
cat(sprintf("resto LC (Q11-45): %.1f%% | testlet (Q6-10): %.1f%%\n", resto, media_testlet))

vir <- function(x) gsub("\\.", ",", sprintf("%.1f", x))

p <- ggplot(t, aes(x = q, y = erro, fill = categoria)) +
  geom_col(width = 0.66) +
  # linha do resto da prova — DESENHADA ANTES dos rótulos (fica atrás dos números)
  geom_hline(yintercept = resto, linetype = "22", colour = "#1597D8", linewidth = 0.9) +
  # rótulo % de erro no topo
  geom_text(aes(label = paste0(vir(erro), "%")), vjust = -0.7,
            size = 5.2, fontface = "bold", colour = "#1D1D20") +
  # habilidade dentro da barra, base
  geom_text(aes(label = hlabel), y = 3.2, size = 3.9, colour = "white", fontface = "bold") +
  # etiqueta da linha de referência — na faixa vazia do topo-esquerdo, sem tocar barras/rótulos
  annotate("label", x = 0.5, y = 74, hjust = 0, vjust = 0.5,
           label = paste0("Resto de Linguagens (Q11–Q45): ", vir(resto), "%"),
           size = 4, colour = "#1597D8", fill = "#FFFFFF",
           label.size = 0.4, label.r = unit(0.12, "lines"), fontface = "bold") +
  scale_fill_manual(values = DIF_COLS, name = "Nível de dificuldade (TRI)", drop = TRUE) +
  scale_y_continuous(limits = c(0, 82), breaks = seq(0, 80, 20),
                     labels = function(v) paste0(v, "%"), expand = expansion(mult = c(0, 0.02))) +
  labs(
    title = "O “testlet” de Linguagens: um texto, cinco questões",
    subtitle = paste0("Azul (P1): Q6–Q10 saem todas da mesma crônica. Erro médio ", vir(media_testlet),
                      "% — 9 pontos acima do resto de Linguagens."),
    x = "Questão do testlet (posição no caderno)  ·  rótulo interno = habilidade ENEM",
    y = "Taxa de erro (% dos presentes)",
    caption = CAP) +
  theme_xtri()

ggsave(file.path(OUT, "g11_testlet_linguagens.png"), p,
       width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: g11_testlet_linguagens.png\n")

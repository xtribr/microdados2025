#!/usr/bin/env Rscript
suppressMessages(library(ggplot2))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "palestra_2025/graficos")
theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) + theme(
    plot.background = element_rect(fill = "#F1F1F2", colour = NA),
    panel.background = element_rect(fill = "white", colour = NA),
    panel.grid.major = element_line(colour = "#DEDEE1", linewidth = 0.4),
    panel.grid.minor = element_line(colour = "#ECECEE", linewidth = 0.3),
    plot.title = element_text(face = "bold", size = 22, colour = "#1D1D20", margin = margin(b = 2)),
    plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 10)),
    plot.caption = element_text(size = 10, colour = "#8C9298", hjust = 1),
    axis.title = element_text(colour = "#1D1D20", size = 14),
    axis.text = element_text(colour = "#6B7076", size = 11),
    legend.title = element_text(colour = "#1D1D20", size = 12),
    legend.text = element_text(colour = "#6B7076", size = 11),
    legend.position = "top", plot.margin = margin(18, 22, 14, 18))
}
CAPX <- "Estudo XTRI — Prof. Alexandre Emerson Melo de Araújo  |  Microdados ENEM 2025 / INEP"

# ===== g08a: scatter chutes × incoerência =====
sc <- read.csv(file.path(BASE, "palestra_2025/chutes_scatter.csv"), stringsAsFactors = FALSE)
sc$inc_c <- pmin(sc$incoer, 12)
p8a <- ggplot(sc, aes(x = acertos, y = nota_media, colour = inc_c)) +
  geom_point(size = 0.5, alpha = 0.35) +
  scale_colour_gradientn(colours = c("#1FAFEF", "#7FC97F", "#F5D800", "#FB9276", "#E8000B"),
                         name = "incoerências\n(errar fácil +\nacertar difícil)") +
  labs(title = "Chute deixa marca: mesmo acerto, nota menor",
       subtitle = "Cada ponto é um candidato. X = total de acertos (0–180); Y = média das 4 notas TRI. Cor = nº de incoerências.",
       x = "Total de acertos (4 áreas, 0–180)", y = "Média das notas TRI",
       caption = paste0(CAPX, "  |  amostra ~120 mil (Regular P1)")) +
  theme_xtri()
ggsave(file.path(OUT, "g08a_chutes_scatter.png"), p8a, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: g08a_chutes_scatter.png\n")

# ===== g08b: no mesmo acerto, mais incoerência = menos nota =====
ins <- read.csv(file.path(BASE, "palestra_2025/chutes_insight.csv"), stringsAsFactors = FALSE)
p8b <- ggplot(ins, aes(x = incoer, y = nota_med)) +
  geom_line(colour = "#E8431F", linewidth = 1.4) +
  geom_point(colour = "#E8431F", size = 3.2) +
  geom_text(aes(label = gsub("\\.", ",", sprintf("%.0f", nota_med))), vjust = -1, size = 4.3,
            fontface = "bold", colour = "#1D1D20") +
  scale_x_continuous(breaks = 1:12) +
  labs(title = "Dois alunos, 90 acertos cada: o que chuta tira menos",
       subtitle = "Entre candidatos com o MESMO total de acertos (~90/180): quanto mais incoerente o padrão (errar fácil + acertar difícil), menor a nota.",
       x = "Nº de incoerências (errou fácil e acertou difícil)", y = "Nota TRI média (mediana no grupo)",
       caption = paste0(CAPX, "  |  candidatos com 88–92 acertos")) +
  theme_xtri()
ggsave(file.path(OUT, "g08b_chutes_insight.png"), p8b, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: g08b_chutes_insight.png\n")

# ===== g09a: inglês × espanhol — nota por acertos =====
lc <- read.csv(file.path(BASE, "palestra_2025/lingua_curve.csv"), stringsAsFactors = FALSE,
               fileEncoding = "UTF-8")
lc$acertos <- as.integer(lc$acertos)
COL <- c("Inglês" = "#E8431F", "Espanhol" = "#1597D8")
p9 <- ggplot(lc[lc$acertos >= 3, ], aes(x = acertos, y = mediana, colour = lingua)) +
  geom_line(linewidth = 1.4) + geom_point(size = 1.6) +
  scale_colour_manual(values = COL, name = NULL) +
  scale_x_continuous(breaks = seq(0, 45, 5)) +
  labs(title = "Inglês × Espanhol: mesmo acerto, quem faz espanhol tira um pouco mais",
       subtitle = "Nota mediana de Linguagens por nº de acertos, por idioma. As curvas quase se sobrepõem — o espanhol fica levemente acima.",
       x = "Número de acertos (Linguagens, de 45)", y = "Nota TRI mediana (Linguagens)",
       caption = paste0(CAPX, "  |  Regular P1")) +
  theme_xtri()
ggsave(file.path(OUT, "g09a_ingles_espanhol_curva.png"), p9, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: g09a_ingles_espanhol_curva.png\n")
cat("FIM chutes+lingua ggplot\n")

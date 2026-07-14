#!/usr/bin/env Rscript
# CCI (Curva Característica do Item) 3PL — a questão mais difícil de cada área do ENEM 2025.
# Gráfico limpo, sem identidade visual de marca. P(θ)=c+(1-c)/(1+exp(-a(θ-b))), D=1 (convenção ENEM).
suppressMessages(library(ggplot2))
suppressMessages(library(jsonlite))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "estudo_cci_dificeis"); dir.create(OUT, showWarnings = FALSE)

it <- fromJSON(file.path(BASE, "estudo_cci_dificeis.json"))
nomes <- c(LC = "Linguagens", CH = "Ciências Humanas", CN = "Ciências da Natureza", MT = "Matemática")
cores <- c("Linguagens" = "#2C6FBB", "Ciências Humanas" = "#C0392B",
           "Ciências da Natureza" = "#1E8449", "Matemática" = "#6C3483")
it$area_f <- factor(nomes[it$area], levels = nomes)

# curva por item (nota = 500 + 100*theta)
th <- seq(-1.2, 5.2, length.out = 400)
curv <- do.call(rbind, lapply(seq_len(nrow(it)), function(i) {
  a <- it$a[i]; b <- it$b[i]; c <- it$c[i]
  P <- c + (1 - c) / (1 + exp(-a * (th - b)))
  data.frame(area_f = it$area_f[i], nota = 500 + 100 * th, P = P)
}))

it$nota_b <- 500 + 100 * it$b
it$lab <- sprintf("Q%d  ·  a=%.2f   b=%.2f   c=%.2f", it$n, it$a, it$b, it$c)
it$lab_dif <- sprintf("dificuldade TRI = %d\n%.0f%% acertaram", it$dif_tri, it$pct)

vir <- function(x) format(x, big.mark = ".", decimal.mark = ",")

p <- ggplot(curv, aes(nota, P, colour = area_f)) +
  # piso do chute (c)
  geom_hline(data = it, aes(yintercept = c), linetype = "dotted", colour = "#8C9298", linewidth = 0.5) +
  # dificuldade b
  geom_vline(data = it, aes(xintercept = nota_b), linetype = "dashed", colour = "#8C9298", linewidth = 0.5) +
  geom_line(linewidth = 1.5, show.legend = FALSE) +
  geom_text(data = it, aes(x = 320, y = c + 0.045, label = sprintf("piso do chute c = %.2f", c)),
            hjust = 0, size = 3.2, colour = "#6B7076", inherit.aes = FALSE) +
  geom_text(data = it, aes(x = nota_b - 10, y = 0.045, label = sprintf("b → nota %d", round(nota_b))),
            hjust = 1, size = 3.2, colour = "#6B7076", inherit.aes = FALSE) +
  geom_text(data = it, aes(x = 1000, y = 0.10, label = lab_dif), hjust = 1, vjust = 0,
            size = 3.4, colour = "#3A3A3D", fontface = "bold", inherit.aes = FALSE, lineheight = 0.95) +
  facet_wrap(~area_f, ncol = 2) +
  scale_colour_manual(values = cores) +
  scale_x_continuous(limits = c(300, 1000), breaks = seq(300, 1000, 100)) +
  scale_y_continuous(limits = c(0, 1), breaks = seq(0, 1, 0.25),
                     labels = function(v) paste0(v * 100, "%")) +
  labs(title = "As curvas das questões mais difíceis do ENEM 2025",
       subtitle = "Curva Característica do Item (modelo 3PL). Cada curva mostra a probabilidade de acerto conforme a proficiência (nota TRI)\ndo candidato, para o item de maior dificuldade (maior b) de cada área. Caderno Azul, 1ª aplicação.",
       x = "Proficiência do candidato — nota TRI (θ na escala 500 ± 100)",
       y = "Probabilidade de acerto",
       caption = "Dados: Microdados ENEM 2025 / INEP · parâmetros a (discriminação), b (dificuldade), c (acerto ao acaso) do modelo logístico de 3 parâmetros") +
  theme_minimal(base_size = 15) +
  theme(
    plot.background = element_rect(fill = "white", colour = NA),
    panel.background = element_rect(fill = "#FAFAFB", colour = NA),
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(colour = "#EAEAEC", linewidth = 0.4),
    panel.spacing = unit(1.1, "lines"),
    strip.text = element_text(face = "bold", size = 14, colour = "#1D1D20"),
    plot.title = element_text(face = "bold", size = 22, colour = "#1D1D20"),
    plot.subtitle = element_text(size = 12.5, colour = "#6B7076", margin = margin(t = 4, b = 12)),
    plot.caption = element_text(size = 9.5, colour = "#8C9298", hjust = 0, margin = margin(t = 12)),
    plot.title.position = "plot", plot.caption.position = "plot",
    axis.title = element_text(size = 12.5, colour = "#3A3A3D"),
    plot.margin = margin(18, 22, 14, 18)
  )
# rótulo do item (a,b,c) no topo de cada painel via strip? usa geom_text no rodapé de cada painel
p <- p + geom_text(data = it, aes(x = 300, y = 0.98, label = lab), hjust = 0, vjust = 1,
                   size = 3.4, colour = "#1D1D20", fontface = "bold", inherit.aes = FALSE)
ggsave(file.path(OUT, "cci_3pl_dificeis.png"), p, width = 11.5, height = 9, dpi = 150, bg = "white")
cat("ok: cci_3pl_dificeis.png\n")

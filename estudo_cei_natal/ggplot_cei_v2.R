#!/usr/bin/env Rscript
# v2: (1) Gráfico de incoerência por ÁREA (nuvem nacional + alunos CEI, tamanho = incoerência)
#     (2) Dificuldade e discriminação em formato didático: linhas de degrau com rótulos diretos.
suppressMessages(library(ggplot2))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025/estudo_cei_natal"
OUT  <- file.path(BASE, "graficos")

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 22, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 12)),
      plot.caption  = element_text(size = 9.5, colour = "#8C9298", hjust = 1, margin = margin(t = 12)),
      axis.title    = element_text(colour = "#1D1D20", size = 13.5),
      axis.text     = element_text(colour = "#6B7076", size = 12),
      legend.title  = element_text(size = 11.5, colour = "#1D1D20"),
      legend.text   = element_text(size = 11.5),
      legend.position = "top",
      strip.text    = element_text(face = "bold", size = 13.5, colour = "#1D1D20"),
      strip.background = element_rect(fill = "#E8E9EB", colour = NA),
      plot.margin   = margin(16, 22, 12, 16)
    )
}
ESC_COL <- c("CEI Romualdo" = "#FA5230", "CEI Roberto Freire" = "#1FAFEF", "Brasil" = "#8C9298")
NOMES <- c(LC = "Linguagens", CH = "Ciências Humanas", CN = "Ciências da Natureza", MT = "Matemática")
NITENS <- c(LC = 45, CH = 45, CN = 42, MT = 43)
CAP <- "Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2025 / INEP  |  CEI: 139 + 70 alunos"

al <- read.csv(file.path(BASE, "cei_alunos_area.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")

# ---------- 1) GRÁFICO DE INCOERÊNCIA — 1 por área ----------
for (a in names(NOMES)) {
  nac <- read.csv(file.path(BASE, "plot_data", sprintf("scatter_%s.csv", a)), stringsAsFactors = FALSE)
  d <- al[al$area == a, ]
  p <- ggplot() +
    geom_point(data = nac, aes(x = acertos, y = nota), colour = "#C9CBCE", size = 0.5, alpha = 0.22) +
    geom_point(data = d, aes(x = acertos, y = nota, colour = escola, size = incoer), alpha = 0.9) +
    scale_colour_manual(values = ESC_COL, name = NULL) +
    scale_size_continuous(range = c(1.6, 6), breaks = c(0, 2, 4, 6), name = "incoerências na área") +
    guides(colour = guide_legend(override.aes = list(size = 4))) +
    scale_x_continuous(limits = c(0, NITENS[a]), breaks = seq(0, NITENS[a], 5)) +
    labs(title = sprintf("Gráfico de incoerência — %s", NOMES[a]),
         subtitle = sprintf("Cinza = candidatos Brasil (Regular P1). Ponto = aluno CEI; tamanho = incoerência em %s (erros em itens fáceis × acertos em difíceis).", NOMES[a]),
         x = sprintf("Acertos em %s (de %d itens válidos)", NOMES[a], NITENS[a]),
         y = sprintf("Nota TRI — %s", NOMES[a]),
         caption = CAP) +
    theme_xtri()
  ggsave(file.path(OUT, sprintf("cei_incoerencia_%s.png", a)), p, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
  cat("ok: cei_incoerencia_", a, "\n", sep = "")
}

# ---------- helper: formato longo p/ degrau ----------
long3 <- function(df, cat_col, cat_levels) {
  esc <- df[, c("escola", "area", cat_col, "acerto_pct")]
  names(esc)[3] <- "cat"
  br <- unique(df[, c("area", cat_col, "acerto_nacional")])
  names(br)[2:3] <- c("cat", "acerto_pct")
  br$escola <- "Brasil"
  d <- rbind(esc, br[, names(esc)])
  d$cat <- factor(d$cat, levels = cat_levels)
  d$escola <- factor(d$escola, levels = c("CEI Romualdo", "CEI Roberto Freire", "Brasil"))
  d$area_lab <- factor(NOMES[d$area], levels = NOMES)
  d
}

degrau <- function(d, titulo, subtitulo, xlab, fname, ycap = 100) {
  p <- ggplot(d, aes(x = cat, y = acerto_pct, colour = escola, group = escola)) +
    geom_line(aes(linetype = escola), linewidth = 1.3) +
    geom_point(size = 3.4) +
    geom_text(data = d[d$escola == "CEI Romualdo", ],
              aes(label = sprintf("%.0f", acerto_pct)), vjust = -1.2, size = 3.9,
              fontface = "bold", show.legend = FALSE) +
    geom_text(data = d[d$escola == "CEI Roberto Freire", ],
              aes(label = sprintf("%.0f", acerto_pct)), vjust = 2.3, size = 3.9,
              fontface = "bold", show.legend = FALSE) +
    geom_text(data = d[d$escola == "Brasil", ],
              aes(label = sprintf("%.0f", acerto_pct)), vjust = 2.3, size = 3.7,
              show.legend = FALSE) +
    facet_wrap(~area_lab, ncol = 2) +
    scale_colour_manual(values = ESC_COL, name = NULL) +
    scale_linetype_manual(values = c("CEI Romualdo" = "solid", "CEI Roberto Freire" = "solid", "Brasil" = "22"), name = NULL) +
    scale_y_continuous(limits = c(0, ycap), labels = function(v) paste0(v, "%")) +
    labs(title = titulo, subtitle = subtitulo, x = xlab, y = "Acerto (% das respostas)", caption = CAP) +
    theme_xtri()
  ggsave(file.path(OUT, fname), p, width = 13.33, height = 8.4, dpi = 150, bg = "#F1F1F2")
  cat("ok:", fname, "\n")
}

# ---------- 2) DIFICULDADE (degrau) ----------
catd <- read.csv(file.path(BASE, "cei_categorias.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
d1 <- long3(catd, "categoria", c("Fácil", "Médio", "Difícil", "Muito difícil"))
# razão CEI/Brasil no 'Muito difícil' de MT p/ subtítulo
md <- d1[d1$area == "MT" & d1$cat == "Muito difícil", ]
razao <- mean(md$acerto_pct[md$escola != "Brasil"]) / md$acerto_pct[md$escola == "Brasil"]
degrau(d1,
       "O degrau da dificuldade: quem segura o item pesado?",
       sprintf("Todo mundo cai do Fácil ao Muito difícil — mas o Brasil (tracejado) despenca e as CEI caem devagar. Em Matemática 'Muito difícil': %sx o Brasil.",
               gsub("\\.", ",", sprintf("%.1f", razao))),
       "Nível de dificuldade do item (TRI, parâmetro B)",
       "cei_dificuldade.png")

# ---------- 3) DISCRIMINAÇÃO (degrau) ----------
dsc <- read.csv(file.path(BASE, "cei_disc.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
d2 <- long3(dsc, "faixa_disc", c("baixa/moderada (A<1,35)", "alta (1,35–1,69)", "muito alta (A≥1,70)"))
levels(d2$cat) <- c("baixa/moderada\n(A < 1,35)", "alta\n(1,35–1,69)", "muito alta\n(A > 1,70)")
degrau(d2,
       "Item que separa quem sabe: a distância cresce com o poder do item",
       "Quanto mais discriminativo o item (parâmetro A), mais a linha do Brasil (tracejado) se afasta das CEI — é o item 'navalha' premiando quem domina.",
       "Poder discriminatório do item (TRI, parâmetro A — escala de Baker)",
       "cei_discriminacao.png")

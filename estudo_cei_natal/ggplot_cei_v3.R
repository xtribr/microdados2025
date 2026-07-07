#!/usr/bin/env Rscript
# v3: Degrau da dificuldade POR ÁREA — 1 gráfico auto-explicativo por área.
# Anotações fazem a explicação: razão CEI/Brasil no Fácil e seta com a razão no Muito difícil.
suppressMessages(library(ggplot2))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025/estudo_cei_natal"
OUT  <- file.path(BASE, "graficos")

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major.y = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 23, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 8)),
      plot.caption  = element_text(size = 9.5, colour = "#8C9298", hjust = 1, margin = margin(t = 12)),
      axis.title    = element_text(colour = "#1D1D20", size = 14),
      axis.text.x   = element_text(colour = "#1D1D20", size = 14, face = "bold"),
      axis.text.y   = element_text(colour = "#6B7076", size = 12),
      legend.title  = element_blank(),
      legend.text   = element_text(size = 12.5),
      legend.position = "top",
      plot.margin   = margin(18, 26, 12, 18)
    )
}
ESC_COL <- c("CEI Romualdo" = "#FA5230", "CEI Roberto Freire" = "#1FAFEF", "Brasil" = "#8C9298")
NOMES <- c(LC = "Linguagens", CH = "Ciências Humanas", CN = "Ciências da Natureza", MT = "Matemática")
CAP <- "Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2025 / INEP  |  CEI: 139 + 70 alunos  |  categorias = classificação XTRI pelo parâmetro B (TRI)"
CATS <- c("Fácil", "Médio", "Difícil", "Muito difícil")
vir <- function(x, d = 1) gsub("\\.", ",", sprintf(paste0("%.", d, "f"), x))

catd <- read.csv(file.path(BASE, "cei_categorias.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")

for (a in names(NOMES)) {
  da <- catd[catd$area == a, ]
  esc <- da[, c("escola", "categoria", "acerto_pct")]
  br  <- unique(da[, c("categoria", "acerto_nacional")])
  names(br)[2] <- "acerto_pct"; br$escola <- "Brasil"
  d <- rbind(esc, br[, names(esc)])
  d$categoria <- factor(d$categoria, levels = CATS)
  d$escola <- factor(d$escola, levels = names(ESC_COL))
  d$xn <- as.numeric(d$categoria)

  # razões CEI médio / Brasil no Fácil e no Muito difícil
  rz <- function(cat) {
    ce <- mean(d$acerto_pct[d$categoria == cat & d$escola != "Brasil"])
    bb <- d$acerto_pct[d$categoria == cat & d$escola == "Brasil"]
    ce / bb
  }
  r_fac <- rz("Fácil"); r_md <- rz("Muito difícil")
  br_md  <- d$acerto_pct[d$categoria == "Muito difícil" & d$escola == "Brasil"]
  cei_md <- min(d$acerto_pct[d$categoria == "Muito difícil" & d$escola != "Brasil"])
  br_fac <- d$acerto_pct[d$categoria == "Fácil" & d$escola == "Brasil"]

  # rótulos das unidades: o de cima rotula ACIMA, o de baixo rotula ABAIXO (evita troca visual)
  lab <- d[d$escola != "Brasil", ]
  lab$vj <- NA_real_
  for (cc in CATS) {
    sub <- lab[lab$categoria == cc, ]
    hi <- sub$escola[which.max(sub$acerto_pct)]
    lab$vj[lab$categoria == cc] <- ifelse(lab$escola[lab$categoria == cc] == hi, -1.2, 2.4)
  }

  p <- ggplot(d, aes(x = xn, y = acerto_pct, colour = escola, group = escola)) +
    geom_line(aes(linetype = escola), linewidth = 1.4) +
    geom_point(size = 3.8) +
    geom_text(data = lab,
              aes(label = sprintf("%.0f%%", acerto_pct), vjust = vj), size = 4.6,
              fontface = "bold", show.legend = FALSE) +
    geom_text(data = d[d$escola == "Brasil", ],
              aes(label = sprintf("%.0f%%", acerto_pct)), vjust = 2.4, size = 4.2,
              show.legend = FALSE) +
    # callout 1: razão no Fácil (abaixo do ponto do Brasil)
    annotate("label", x = 1, y = br_fac - 14,
             label = sprintf("no fácil, as CEI acertam\n%sx a taxa do Brasil", vir(r_fac)),
             size = 4.1, colour = "#1D1D20", fill = "#FFFFFF", label.size = 0.3,
             lineheight = 0.95) +
    # callout 2: seta vertical Brasil -> CEI no Muito difícil + razão em destaque
    annotate("segment", x = 4.28, xend = 4.28, y = br_md + 1.5, yend = cei_md - 1.5,
             colour = "#E8431F", linewidth = 1.1,
             arrow = arrow(ends = "both", length = unit(0.16, "cm"), type = "closed")) +
    annotate("label", x = 4.36, y = (br_md + cei_md) / 2,
             label = sprintf("no item pesado:\n%sx o Brasil", vir(r_md)),
             hjust = 0, size = 4.7, fontface = "bold", colour = "#E8431F",
             fill = "#FFFFFF", label.size = 0.3, lineheight = 0.95) +
    scale_colour_manual(values = ESC_COL) +
    scale_linetype_manual(values = c("CEI Romualdo" = "solid", "CEI Roberto Freire" = "solid", "Brasil" = "22")) +
    scale_x_continuous(breaks = 1:4, labels = CATS, limits = c(0.6, 5.15)) +
    scale_y_continuous(limits = c(0, 100), breaks = seq(0, 100, 25), labels = function(v) paste0(v, "%")) +
    labs(title = sprintf("%s — o degrau da dificuldade", NOMES[a]),
         subtitle = "Como ler: toda linha cai — item difícil é difícil pra todos. A pergunta é quanto cada grupo segura em cada degrau.",
         x = "Dificuldade do item (parâmetro B da TRI)", y = "Acerto (% das respostas)",
         caption = CAP) +
    theme_xtri()
  ggsave(file.path(OUT, sprintf("cei_dificuldade_%s.png", a)), p, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
  cat("ok: cei_dificuldade_", a, "\n", sep = "")
}

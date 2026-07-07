#!/usr/bin/env Rscript
# Suíte por escola (lê config.json): habilidades, degrau de dificuldade por área,
# discriminação, incoerência por área, chutes e redação. Escola × Brasil.
suppressMessages(library(ggplot2))
suppressMessages(library(jsonlite))
args <- commandArgs(trailingOnly = FALSE)
sf <- sub("--file=", "", args[grep("--file=", args)])
BASE <- dirname(normalizePath(sf))
OUT <- file.path(BASE, "graficos")
CFG <- fromJSON(file.path(BASE, "config.json"))
ESC <- CFG$curto
COR <- CFG$cor
CORd <- CFG$cor_escura

theme_xtri <- function(base = 15, gridx = FALSE) {
  th <- theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major.y = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 22, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 10)),
      plot.caption  = element_text(size = 9.5, colour = "#8C9298", hjust = 1, margin = margin(t = 12)),
      axis.title    = element_text(colour = "#1D1D20", size = 13.5),
      axis.text     = element_text(colour = "#6B7076", size = 12),
      legend.title  = element_text(size = 11.5, colour = "#1D1D20"),
      legend.text   = element_text(size = 12),
      legend.position = "top",
      strip.text    = element_text(face = "bold", size = 13.5, colour = "#1D1D20"),
      strip.background = element_rect(fill = "#E8E9EB", colour = NA),
      plot.margin   = margin(16, 24, 12, 16)
    )
  if (gridx) th <- th + theme(panel.grid.major.x = element_line(colour = "#DEDEE1", linewidth = 0.4))
  else th <- th + theme(panel.grid.major.x = element_blank())
  th
}
SCOL <- c("#8C9298"); names(SCOL) <- "Brasil"
SCOL <- c(setNames(COR, ESC), SCOL)
NOMES <- c(LC = "Linguagens", CH = "Ciências Humanas", CN = "Ciências da Natureza", MT = "Matemática")
NITENS <- c(LC = 45, CH = 45, CN = 42, MT = 43)
res <- fromJSON(file.path(BASE, "resumo.json"))
CAP <- sprintf("Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2025 / INEP  |  %s: %d alunos (concluintes c/ escola declarada)",
               CFG$nome, res$processados)
CATS <- c("Fácil", "Médio", "Difícil", "Muito difícil")
vir <- function(x, d = 1) gsub("\\.", ",", sprintf(paste0("%.", d, "f"), x))

# ---------- 1) HABILIDADES ----------
hab <- read.csv(file.path(BASE, "habilidades.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
for (a in names(NOMES)) {
  d <- hab[hab$area == a, ]
  d <- d[order(d$erro_pct), ]
  d$habilidade <- factor(d$habilidade, levels = d$habilidade)
  dn <- d[!is.na(d$erro_nacional) & d$erro_nacional != "", ]
  dn$erro_nacional <- as.numeric(dn$erro_nacional)
  p <- ggplot(d, aes(x = erro_pct, y = habilidade)) +
    geom_col(fill = COR, width = 0.7) +
    geom_point(data = dn, aes(x = erro_nacional, y = habilidade),
               shape = 18, size = 3.4, colour = "#1D1D20") +
    geom_text(aes(label = sprintf("%.0f%%", erro_pct)), hjust = 1.18, size = 3.5, colour = "white", fontface = "bold") +
    scale_x_continuous(limits = c(0, 105), labels = function(v) paste0(v, "%"), expand = expansion(mult = c(0, 0))) +
    labs(title = sprintf("%s — onde o %s mais erra", NOMES[a], ESC),
         subtitle = "Barra = escola · losango preto = erro nacional. Barra passando do losango = erra mais que o Brasil.",
         x = "Taxa de erro (% das respostas dos alunos)", y = "Habilidade ENEM", caption = CAP) +
    theme_xtri(13, gridx = TRUE) + theme(panel.grid.major.y = element_blank())
  ggsave(file.path(OUT, sprintf("hab_%s.png", a)), p, width = 12, height = 9.5, dpi = 150, bg = "#F1F1F2")
  cat("ok: hab_", a, "\n", sep = "")
}

# ---------- 2) DEGRAU DA DIFICULDADE POR ÁREA ----------
catd <- read.csv(file.path(BASE, "categorias.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
for (a in names(NOMES)) {
  da <- catd[catd$area == a, ]
  e <- data.frame(escola = ESC, categoria = da$categoria, acerto = da$acerto_pct)
  b <- data.frame(escola = "Brasil", categoria = da$categoria, acerto = da$acerto_nacional)
  d <- rbind(e, b)
  d$categoria <- factor(d$categoria, levels = CATS)
  d$escola <- factor(d$escola, levels = names(SCOL))
  d$xn <- as.numeric(d$categoria)
  r_fac <- d$acerto[d$xn == 1 & d$escola == ESC] / d$acerto[d$xn == 1 & d$escola == "Brasil"]
  r_md  <- d$acerto[d$xn == 4 & d$escola == ESC] / d$acerto[d$xn == 4 & d$escola == "Brasil"]
  br_md <- d$acerto[d$xn == 4 & d$escola == "Brasil"]
  es_md <- d$acerto[d$xn == 4 & d$escola == ESC]
  br_fac <- d$acerto[d$xn == 1 & d$escola == "Brasil"]
  p <- ggplot(d, aes(x = xn, y = acerto, colour = escola, group = escola)) +
    geom_line(aes(linetype = escola), linewidth = 1.4) +
    geom_point(size = 3.8) +
    geom_text(data = d[d$escola == ESC, ], aes(label = sprintf("%.0f%%", acerto)),
              vjust = -1.2, size = 4.6, fontface = "bold", show.legend = FALSE) +
    geom_text(data = d[d$escola == "Brasil", ], aes(label = sprintf("%.0f%%", acerto)),
              vjust = 2.4, size = 4.2, show.legend = FALSE) +
    annotate("label", x = 1, y = br_fac - 16,
             label = sprintf("no fácil, o %s acerta\n%sx a taxa do Brasil", ESC, vir(r_fac)),
             size = 4.1, colour = "#1D1D20", fill = "#FFFFFF", lineheight = 0.95) +
    annotate("segment", x = 4.28, xend = 4.28, y = br_md + 1.5, yend = es_md - 1.5,
             colour = CORd, linewidth = 1.1,
             arrow = arrow(ends = "both", length = unit(0.16, "cm"), type = "closed")) +
    annotate("label", x = 4.36, y = (br_md + es_md) / 2,
             label = sprintf("no item pesado:\n%sx o Brasil", vir(r_md)),
             hjust = 0, size = 4.7, fontface = "bold", colour = CORd, fill = "#FFFFFF", lineheight = 0.95) +
    scale_colour_manual(values = SCOL, name = NULL) +
    scale_linetype_manual(values = setNames(c("solid", "22"), c(ESC, "Brasil")), name = NULL) +
    scale_x_continuous(breaks = 1:4, labels = CATS, limits = c(0.6, 5.15)) +
    scale_y_continuous(limits = c(0, 100), breaks = seq(0, 100, 25), labels = function(v) paste0(v, "%")) +
    labs(title = sprintf("%s — o degrau da dificuldade", NOMES[a]),
         subtitle = "Como ler: toda linha cai — item difícil é difícil pra todos. A pergunta é quanto cada grupo segura em cada degrau.",
         x = "Dificuldade do item (parâmetro B da TRI)", y = "Acerto (% das respostas)", caption = CAP) +
    theme_xtri() + theme(axis.text.x = element_text(face = "bold", size = 14, colour = "#1D1D20"))
  ggsave(file.path(OUT, sprintf("dificuldade_%s.png", a)), p, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
  cat("ok: dificuldade_", a, "\n", sep = "")
}

# ---------- 3) DISCRIMINAÇÃO (degrau, facet) ----------
dsc <- read.csv(file.path(BASE, "disc.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
e <- data.frame(escola = ESC, area = dsc$area, cat = dsc$faixa_disc, acerto = dsc$acerto_pct)
b <- data.frame(escola = "Brasil", area = dsc$area, cat = dsc$faixa_disc, acerto = dsc$acerto_nacional)
d2 <- rbind(e, b)
d2$cat <- factor(d2$cat, levels = c("baixa/moderada (A<1,35)", "alta (1,35–1,69)", "muito alta (A≥1,70)"))
levels(d2$cat) <- c("baixa/moderada\n(A < 1,35)", "alta\n(1,35–1,69)", "muito alta\n(A > 1,70)")
d2$escola <- factor(d2$escola, levels = names(SCOL))
d2$area_lab <- factor(NOMES[d2$area], levels = NOMES)
p3 <- ggplot(d2, aes(x = cat, y = acerto, colour = escola, group = escola)) +
  geom_line(aes(linetype = escola), linewidth = 1.3) +
  geom_point(size = 3.4) +
  geom_text(data = d2[d2$escola == ESC, ], aes(label = sprintf("%.0f", acerto)),
            vjust = -1.1, size = 3.9, fontface = "bold", show.legend = FALSE) +
  geom_text(data = d2[d2$escola == "Brasil", ], aes(label = sprintf("%.0f", acerto)),
            vjust = 2.3, size = 3.7, show.legend = FALSE) +
  facet_wrap(~area_lab, ncol = 2) +
  scale_colour_manual(values = SCOL, name = NULL) +
  scale_linetype_manual(values = setNames(c("solid", "22"), c(ESC, "Brasil")), name = NULL) +
  scale_y_continuous(limits = c(0, 100), labels = function(v) paste0(v, "%")) +
  labs(title = "Item que separa quem sabe: a distância cresce com o poder do item",
       subtitle = "Quanto mais discriminativo o item (parâmetro A), mais a linha do Brasil (tracejado) se afasta da escola.",
       x = "Poder discriminatório do item (TRI, parâmetro A — escala de Baker)",
       y = "Acerto (% das respostas)", caption = CAP) +
  theme_xtri()
ggsave(file.path(OUT, "discriminacao.png"), p3, width = 13.33, height = 8.4, dpi = 150, bg = "#F1F1F2")
cat("ok: discriminacao\n")

# ---------- 4) INCOERÊNCIA POR ÁREA ----------
al <- read.csv(file.path(BASE, "alunos_area.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
for (a in names(NOMES)) {
  nac <- read.csv(file.path(BASE, "plot_data", sprintf("scatter_%s.csv", a)), stringsAsFactors = FALSE)
  d <- al[al$area == a, ]
  p <- ggplot() +
    geom_point(data = nac, aes(x = acertos, y = nota), colour = "#C9CBCE", size = 0.5, alpha = 0.22) +
    geom_point(data = d, aes(x = acertos, y = nota, size = incoer), colour = COR, alpha = 0.85) +
    scale_size_continuous(range = c(1.6, 6), breaks = c(0, 2, 4, 6), name = "incoerências na área") +
    scale_x_continuous(limits = c(0, NITENS[a]), breaks = seq(0, NITENS[a], 5)) +
    labs(title = sprintf("Gráfico de incoerência — %s (%s)", NOMES[a], ESC),
         subtitle = sprintf("Cinza = candidatos Brasil (Regular P1). Ponto colorido = aluno; tamanho = incoerência em %s (erros em fáceis × acertos em difíceis).", NOMES[a]),
         x = sprintf("Acertos em %s (de %d itens válidos)", NOMES[a], NITENS[a]),
         y = sprintf("Nota TRI — %s", NOMES[a]), caption = CAP) +
    theme_xtri(gridx = TRUE)
  ggsave(file.path(OUT, sprintf("incoerencia_%s.png", a)), p, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
  cat("ok: incoerencia_", a, "\n", sep = "")
}

# ---------- 5) CHUTES (4 áreas juntas) ----------
alp <- read.csv(file.path(BASE, "alunos_proc.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
alp <- alp[alp$areas == 4, ]
nac <- read.csv(file.path(BASE, "chutes_scatter.csv"), stringsAsFactors = FALSE)
p5 <- ggplot() +
  geom_point(data = nac, aes(x = acertos, y = nota_media), colour = "#C7CBD0", size = 0.5, alpha = 0.25) +
  geom_point(data = alp, aes(x = acertos, y = nota_media, size = incoer), colour = COR, alpha = 0.85) +
  scale_size_continuous(range = c(1.6, 5.5), breaks = c(0, 3, 6, 9), name = "incoerências (4 áreas)") +
  labs(title = sprintf("Onde os alunos do %s caem na nuvem nacional", ESC),
       subtitle = "Cinza = 120 mil candidatos Brasil (Regular P1). Ponto colorido = aluno; tamanho = índice de incoerência.",
       x = "Acertos nas 4 provas objetivas (de 175 itens válidos)", y = "Nota TRI média (4 áreas)", caption = CAP) +
  theme_xtri(gridx = TRUE)
ggsave(file.path(OUT, "chutes.png"), p5, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: chutes\n")

# ---------- 6) REDAÇÃO ----------
CLAB <- c("C1\nnorma culta", "C2\ncompreender\no tema", "C3\nargumentação", "C4\ncoesão", "C5\nproposta de\nintervenção")
rc <- fromJSON(file.path(BASE, "redacao_comp.json"))[[ESC]]
nacr <- fromJSON(file.path(BASE, "redacao_2024_2025.json"))$`2025`$medias_comp
rows <- list()
for (i in 1:5) {
  rows[[length(rows) + 1]] <- data.frame(escola = ESC, comp = i, media = rc[[paste0("C", i)]]$media,
                                         p200 = rc[[paste0("C", i)]]$pct_200)
  rows[[length(rows) + 1]] <- data.frame(escola = "Brasil", comp = i,
                                         media = round(nacr[[paste0("NU_NOTA_COMP", i)]], 1), p200 = NA)
}
d6 <- do.call(rbind, rows)
d6$escola <- factor(d6$escola, levels = names(SCOL))
esc6 <- d6[d6$escola == ESC, ]
gg <- esc6$comp[which.min(esc6$media)]
gg_m <- min(esc6$media)
gg_p200 <- esc6$p200[esc6$comp == gg]
p6 <- ggplot(d6, aes(x = comp, y = media, colour = escola, group = escola)) +
  geom_hline(yintercept = 200, colour = "#C9CBCE", linewidth = 0.7, linetype = "12") +
  annotate("text", x = 0.62, y = 204, label = "nota máxima (200)", hjust = 0, size = 3.8, colour = "#8C9298") +
  geom_line(aes(linetype = escola), linewidth = 1.4) +
  geom_point(size = 3.8) +
  geom_text(data = d6[d6$escola == ESC, ], aes(label = vir(media, 0)), vjust = -1.2,
            size = 4.6, fontface = "bold", show.legend = FALSE) +
  geom_text(data = d6[d6$escola == "Brasil", ], aes(label = vir(media, 0)), vjust = 2.4,
            size = 4.2, show.legend = FALSE) +
  annotate("segment", x = gg - 0.22, xend = gg - 0.22, y = gg_m + 4, yend = 199,
           colour = CORd, linewidth = 1.1,
           arrow = arrow(ends = "both", length = unit(0.16, "cm"), type = "closed")) +
  annotate("label", x = 0.9, y = 190,
           label = sprintf("o gargalo: C%d — só %s%%\ndos alunos gabaritam (200)", gg, vir(gg_p200)),
           hjust = 0, size = 4.2, fontface = "bold", colour = CORd, fill = "#FFFFFF", lineheight = 0.98) +
  scale_colour_manual(values = SCOL, name = NULL) +
  scale_linetype_manual(values = setNames(c("solid", "22"), c(ESC, "Brasil")), name = NULL) +
  scale_x_continuous(breaks = 1:5, labels = CLAB, limits = c(0.6, 5.4)) +
  scale_y_continuous(limits = c(80, 215), breaks = seq(80, 200, 40)) +
  labs(title = sprintf("Redação — onde o %s ainda perde ponto", ESC),
       subtitle = "Média por competência (0–200), escola × Brasil (tracejado).",
       x = "Competência da redação", y = "Média na competência (0–200)", caption = CAP) +
  theme_xtri() + theme(axis.text.x = element_text(face = "bold", size = 13, colour = "#1D1D20", lineheight = 0.9))
ggsave(file.path(OUT, "redacao_competencias.png"), p6, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: redacao_competencias\n")

p7 <- ggplot(esc6, aes(x = comp, y = p200)) +
  geom_col(fill = COR, width = 0.55) +
  geom_text(aes(label = paste0(vir(p200, 0), "%")), vjust = -0.5, size = 4.6,
            fontface = "bold", colour = "#1D1D20") +
  scale_x_continuous(breaks = 1:5, labels = CLAB) +
  scale_y_continuous(limits = c(0, max(esc6$p200) * 1.18), labels = function(v) paste0(v, "%")) +
  labs(title = sprintf("Quem gabarita (nota 200) cada competência? — %s", ESC),
       subtitle = "% dos alunos com nota máxima em cada competência da redação.",
       x = "Competência da redação", y = "Alunos com nota 200 (%)", caption = CAP) +
  theme_xtri() + theme(axis.text.x = element_text(face = "bold", size = 13, colour = "#1D1D20", lineheight = 0.9))
ggsave(file.path(OUT, "redacao_200.png"), p7, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: redacao_200\n")

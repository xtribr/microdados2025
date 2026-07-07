#!/usr/bin/env Rscript
# Estudo CEI (Romualdo × Roberto Freire) — habilidades mais erradas, acerto por
# dificuldade e por discriminação, e chute (person-fit) sobre a nuvem nacional.
suppressMessages(library(ggplot2))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025/estudo_cei_natal"
OUT  <- file.path(BASE, "graficos")
dir.create(OUT, showWarnings = FALSE)

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 21, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13, colour = "#8C9298", margin = margin(b = 10)),
      plot.caption  = element_text(size = 9.5, colour = "#8C9298", hjust = 1, margin = margin(t = 12)),
      axis.title    = element_text(colour = "#1D1D20", size = 13.5),
      axis.text     = element_text(colour = "#6B7076", size = 11),
      legend.title  = element_blank(),
      legend.text   = element_text(size = 11.5),
      legend.position = "top",
      strip.text    = element_text(face = "bold", size = 13, colour = "#1D1D20"),
      strip.background = element_rect(fill = "#E8E9EB", colour = NA),
      plot.margin   = margin(16, 20, 12, 16)
    )
}
ESC_COL <- c("CEI Romualdo" = "#FA5230", "CEI Roberto Freire" = "#1FAFEF")
NOMES <- c(LC = "Linguagens", CH = "Ciências Humanas", CN = "Ciências da Natureza", MT = "Matemática")
CAP <- "Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2025 / INEP  |  CEI: 139 + 70 alunos (concluintes com escola declarada)"

hab <- read.csv(file.path(BASE, "cei_habilidades.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
cat <- read.csv(file.path(BASE, "cei_categorias.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
dsc <- read.csv(file.path(BASE, "cei_disc.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")

# ---------- 1) HABILIDADES MAIS ERRADAS (1 gráfico por área) ----------
for (a in names(NOMES)) {
  d <- hab[hab$area == a, ]
  ord <- aggregate(erro_pct ~ habilidade, d, mean)
  ord <- ord[order(ord$erro_pct), ]
  d$habilidade <- factor(d$habilidade, levels = ord$habilidade)
  dn <- unique(d[, c("habilidade", "erro_nacional")])
  dn <- dn[!is.na(dn$erro_nacional) & dn$erro_nacional != "", ]
  dn$erro_nacional <- as.numeric(dn$erro_nacional)

  p <- ggplot(d, aes(x = erro_pct, y = habilidade, fill = escola)) +
    geom_col(position = position_dodge(width = 0.8), width = 0.72) +
    geom_point(data = dn, aes(x = erro_nacional, y = habilidade),
               inherit.aes = FALSE, shape = 18, size = 3.2, colour = "#1D1D20") +
    scale_fill_manual(values = ESC_COL) +
    scale_x_continuous(limits = c(0, 102), labels = function(v) paste0(v, "%"),
                       expand = expansion(mult = c(0, 0))) +
    labs(title = sprintf("%s — onde cada unidade mais erra", NOMES[a]),
         subtitle = "Taxa de erro por habilidade ENEM (barras = unidades CEI; losango preto = erro nacional).",
         x = "Taxa de erro (% das respostas dos alunos)", y = "Habilidade ENEM",
         caption = CAP) +
    theme_xtri(13)
  ggsave(file.path(OUT, sprintf("cei_hab_%s.png", a)), p, width = 12, height = 9.5, dpi = 150, bg = "#F1F1F2")
  cat("ok: cei_hab_", a, "\n", sep = "")
}

# ---------- 2) ACERTO POR CATEGORIA DE DIFICULDADE ----------
cat$categoria <- factor(cat$categoria, levels = c("Fácil", "Médio", "Difícil", "Muito difícil"))
cat$area_lab <- factor(NOMES[cat$area], levels = NOMES)
catn <- unique(cat[, c("area_lab", "categoria", "acerto_nacional")])
p2 <- ggplot(cat, aes(x = categoria, y = acerto_pct, fill = escola)) +
  geom_col(position = position_dodge(width = 0.8), width = 0.72) +
  geom_point(data = catn, aes(x = categoria, y = acerto_nacional),
             inherit.aes = FALSE, shape = 18, size = 3.6, colour = "#1D1D20") +
  geom_text(aes(label = sprintf("%.0f", acerto_pct)),
            position = position_dodge(width = 0.8), vjust = -0.5, size = 3.4, colour = "#1D1D20") +
  facet_wrap(~area_lab, ncol = 2) +
  scale_fill_manual(values = ESC_COL) +
  scale_y_continuous(limits = c(0, 100), labels = function(v) paste0(v, "%")) +
  labs(title = "Acerto por nível de dificuldade do item (TRI, parâmetro B)",
       subtitle = "As duas unidades × Brasil (losango preto). O degrau Fácil→Muito difícil mostra o nível TRI da turma.",
       x = "Categoria de dificuldade do item (XTRI)", y = "Acerto (% das respostas)",
       caption = CAP) +
  theme_xtri()
ggsave(file.path(OUT, "cei_dificuldade.png"), p2, width = 13.33, height = 8.2, dpi = 150, bg = "#F1F1F2")
cat("ok: cei_dificuldade\n")

# ---------- 3) ACERTO POR FAIXA DE DISCRIMINAÇÃO (A, Baker) ----------
dsc$faixa_disc <- factor(dsc$faixa_disc, levels = c("baixa/moderada (A<1,35)", "alta (1,35–1,69)", "muito alta (A≥1,70)"))
dsc$area_lab <- factor(NOMES[dsc$area], levels = NOMES)
dscn <- unique(dsc[, c("area_lab", "faixa_disc", "acerto_nacional")])
p3 <- ggplot(dsc, aes(x = faixa_disc, y = acerto_pct, fill = escola)) +
  geom_col(position = position_dodge(width = 0.8), width = 0.72) +
  geom_point(data = dscn, aes(x = faixa_disc, y = acerto_nacional),
             inherit.aes = FALSE, shape = 18, size = 3.6, colour = "#1D1D20") +
  geom_text(aes(label = sprintf("%.0f", acerto_pct)),
            position = position_dodge(width = 0.8), vjust = -0.5, size = 3.4, colour = "#1D1D20") +
  facet_wrap(~area_lab, ncol = 2) +
  scale_fill_manual(values = ESC_COL) +
  scale_y_continuous(limits = c(0, 100), labels = function(v) paste0(v, "%")) +
  labs(title = "Acerto pelo poder discriminatório do item (TRI, parâmetro A)",
       subtitle = "Itens de A muito alto separam quem sabe: é onde a distância unidades × Brasil (losango) mais abre.",
       x = "Faixa de discriminação do item (escala de Baker)", y = "Acerto (% das respostas)",
       caption = CAP) +
  theme_xtri()
ggsave(file.path(OUT, "cei_discriminacao.png"), p3, width = 13.33, height = 8.2, dpi = 150, bg = "#F1F1F2")
cat("ok: cei_discriminacao\n")

# ---------- 4) CHUTE (person-fit) sobre a nuvem nacional ----------
al <- read.csv(file.path(BASE, "cei_alunos.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
al <- al[al$areas == 4, ]
nac <- read.csv(file.path(BASE, "chutes_scatter.csv"), stringsAsFactors = FALSE)
p4 <- ggplot() +
  geom_point(data = nac, aes(x = acertos, y = nota_media), colour = "#C7CBD0",
             size = 0.5, alpha = 0.25) +
  geom_point(data = al, aes(x = acertos, y = nota_media, colour = escola, size = incoer), alpha = 0.9) +
  scale_colour_manual(values = ESC_COL) +
  scale_size_continuous(range = c(1.6, 5.5), breaks = c(0, 3, 6, 9), name = "incoerências") +
  guides(colour = guide_legend(override.aes = list(size = 4))) +
  labs(title = "Onde os alunos CEI caem na nuvem nacional — e quanto 'chute' carregam",
       subtitle = "Cinza = 120 mil candidatos Brasil (Regular P1). Ponto = aluno CEI; tamanho = índice de incoerência (erros em fáceis × acertos em difíceis).",
       x = "Acertos nas 4 provas objetivas (de 175 itens válidos)", y = "Nota TRI média (4 áreas)",
       caption = CAP) +
  theme_xtri()
ggsave(file.path(OUT, "cei_chutes.png"), p4, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: cei_chutes\n")

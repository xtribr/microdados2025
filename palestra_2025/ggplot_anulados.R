#!/usr/bin/env Rscript
# AUTÓPSIA DOS ANULADOS (versão técnica) — curvas empíricas por alternativa + painel
# técnico explicando a psicometria (ICC, monotonicidade, convergência) embutido no gráfico.
# g13_*: anulados pela TRI (gabarito coral, rival cyan, ref saudável tracejada verde, acaso 20%).
# g14_*: previamente expostos (consenso dos fortes em coral; gabarito oficial apagado).
suppressMessages(library(ggplot2))
suppressMessages(library(gridExtra))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "palestra_2025/graficos")

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 22, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 10)),
      plot.caption  = element_text(size = 9.5, colour = "#8C9298", hjust = 1, margin = margin(t = 12)),
      axis.title    = element_text(colour = "#1D1D20", size = 13.5),
      axis.text     = element_text(colour = "#6B7076", size = 12),
      legend.position = "top",
      legend.title  = element_blank(),
      legend.text   = element_text(size = 12, colour = "#1D1D20"),
      plot.margin   = margin(16, 26, 8, 16)
    )
}
NOMES <- c(CH = "Ciências Humanas", CN = "Ciências da Natureza", MT = "Matemática")
CAP0 <- "Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2025 / INEP  |  Regular P1"
vir <- function(x, d = 0) gsub("\\.", ",", sprintf(paste0("%.", d, "f"), x))

# ---------- painel técnico (empilhado abaixo do gráfico via gridExtra) ----------
painel_tecnico <- function(titulo, linhas, largura_chars = 108) {
  linhas_q <- unlist(lapply(linhas, function(s) strwrap(s, width = largura_chars)))
  n <- length(linhas_q)
  y0 <- 0.74          # 1ª linha do corpo — bem abaixo do título (evita colisão)
  ymin_body <- 0.08   # margem inferior
  dy <- (y0 - ymin_body) / max(n - 1, 1)
  ys <- y0 - (seq_len(n) - 1) * dy
  df <- data.frame(y = ys, txt = linhas_q)
  ggplot() + theme_void() +
    scale_x_continuous(limits = c(0, 1), expand = c(0, 0)) +
    scale_y_continuous(limits = c(0, 1), expand = c(0, 0)) +
    annotate("rect", xmin = 0, xmax = 1, ymin = 0, ymax = 1, fill = "#FCEDE9") +
    annotate("rect", xmin = 0, xmax = 0.006, ymin = 0, ymax = 1, fill = "#FA5230") +
    annotate("text", x = 0.028, y = 0.94, label = titulo, hjust = 0, vjust = 1,
             fontface = "bold", colour = "#E8431F", size = 4.6) +
    geom_text(data = df, aes(x = 0.028, y = y, label = txt), hjust = 0, vjust = 1,
              size = 4.35, colour = "#1D1D20", lineheight = 1.05) +
    theme(plot.margin = margin(2, 2, 2, 2), plot.background = element_rect(fill = "#F1F1F2", colour = NA))
}

cur <- read.csv(file.path(BASE, "palestra_2025/anulados_curvas.csv"),
                stringsAsFactors = FALSE, encoding = "UTF-8",
                colClasses = c(co_item = "character"))
cur <- cur[cur$alt != "outros", ]
refs <- list(CH = "125735", CN = "141577", MT = "117856")

plot_item <- function(ci, fname, titulo, subtitulo, foco, rival, nota_lab, painel_titulo, painel_linhas,
                      heights = c(3.1, 1)) {
  d <- cur[cur$co_item == ci, ]
  a <- d$area[1]
  n_tot <- sum(unique(d[, c("banda_ini", "n_banda")])$n_banda)
  rci <- refs[[a]]
  rd <- cur[cur$co_item == rci, ]
  rgab <- rd$gab[1]
  rd <- rd[rd$alt == rgab, ]

  d$papel <- ifelse(d$alt == foco, "foco", ifelse(d$alt == rival, "rival", "outra"))
  all_d <- rbind(
    data.frame(banda_meio = d$banda_meio, pct = d$pct, alt = d$alt, papel = d$papel),
    data.frame(banda_meio = rd$banda_meio, pct = rd$pct, alt = rd$alt, papel = "referencia")
  )
  papel_levels <- c("foco", "rival", "outra", "referencia")
  all_d$papel <- factor(all_d$papel, levels = papel_levels)

  cols <- c(foco = "#FA5230", rival = "#1597D8", outra = "#C7CBD0", referencia = "#2EA84F")
  lws  <- c(foco = 1.9, rival = 1.3, outra = 0.7, referencia = 1.05)
  ltys <- c(foco = "solid", rival = "solid", outra = "solid", referencia = "22")
  labs_legenda <- c(
    foco = sprintf("Gabarito oficial (%s)", foco),
    rival = sprintf("Mais marcada pelos melhores (%s)", rival),
    outra = "Demais alternativas",
    referencia = "Item saudável — referência"
  )

  last_b <- max(d$banda_meio)
  xr <- c(320, last_b + 42)
  foco_d <- all_d[all_d$papel == "foco", ]
  rival_d <- all_d[all_d$papel == "rival", ]
  end_foco <- foco_d$pct[which.max(foco_d$banda_meio)]
  end_rival <- rival_d$pct[which.max(rival_d$banda_meio)]
  if (abs(end_foco - end_rival) < 4.5) {
    if (end_foco > end_rival) end_foco <- end_rival + 4.5 else end_rival <- end_foco + 4.5
  }

  p <- ggplot(all_d, aes(x = banda_meio, y = pct, colour = papel, group = interaction(alt, papel))) +
    geom_hline(yintercept = 20, linetype = "12", colour = "#8C9298", linewidth = 0.6) +
    annotate("text", x = xr[2] - 4, y = 23.2, label = "acaso (20%)", hjust = 1, size = 3.6, colour = "#8C9298") +
    geom_line(aes(linewidth = papel, linetype = papel)) +
    geom_point(data = foco_d, aes(x = banda_meio, y = pct), colour = "#FA5230", size = 2.4, inherit.aes = FALSE) +
    annotate("text", x = last_b + 14, y = end_foco, label = foco, hjust = 0, fontface = "bold",
             size = 4.8, colour = "#FA5230") +
    annotate("text", x = last_b + 14, y = end_rival, label = rival, hjust = 0, fontface = "bold",
             size = 4.8, colour = "#1597D8") +
    scale_colour_manual(values = cols, breaks = papel_levels, labels = labs_legenda) +
    scale_linewidth_manual(values = lws, guide = "none") +
    scale_linetype_manual(values = ltys, guide = "none") +
    scale_x_continuous(breaks = seq(300, 850, 100), limits = xr) +
    scale_y_continuous(limits = c(0, 102), breaks = seq(0, 100, 25), labels = function(v) paste0(v, "%")) +
    guides(colour = guide_legend(override.aes = list(linewidth = 2.4))) +
    labs(title = titulo, subtitle = subtitulo,
         x = sprintf("Nota TRI em %s (faixas de 50 pontos)", NOMES[a]),
         y = "Alunos que marcaram a alternativa (%)",
         caption = sprintf("%s  |  n = %s respostas ao item  |  %s", CAP0, format(n_tot, big.mark = "."), nota_lab)) +
    theme_xtri()

  tec <- painel_tecnico(painel_titulo, painel_linhas)
  g <- arrangeGrob(p, tec, ncol = 1, heights = heights)
  ggsave(file.path(OUT, fname), g, width = 13.33, height = 8.6, dpi = 150, bg = "#F1F1F2")
  cat("ok:", fname, "\n")
}

# ---------- MT — convergência (gabarito A cai, D sobe: discriminação negativa) ----------
plot_item(
  "97593", "g13_anulado_tri_MT.png",
  "O item que o modelo não explicou",
  "Matemática — anulada por 'problema de convergência'. Coral = gabarito oficial · verde = item saudável.",
  "A", "D", "gabarito oficial: A",
  "A LEITURA TÉCNICA",
  c("No modelo de 3 parâmetros (3PL), a Curva Característica do Item (ICC) do gabarito precisa CRESCER com a proficiência do candidato — isso é o parâmetro de discriminação (A) sendo positivo.",
    "Aqui ela faz o oposto: a marcação do gabarito A CAI de 14,8% (nota baixa) para 7,6% (nota alta) — discriminação negativa — enquanto a distratora D SOBE até 72,9% entre os melhores alunos.",
    "Sem um padrão monotônico, o algoritmo de calibração (máxima verossimilhança) não converge: A, B e C ficam instáveis. Sem parâmetros, o item não pode pontuar — motivo oficial: 'Problema de convergência'.")
)

# ---------- CN — convergência (curva em U do gabarito B) ----------
plot_item(
  "96748", "g13_anulado_tri_CN.png",
  "A curva em U que o 3PL não explica",
  "Ciências da Natureza — anulada por 'problema de convergência'. Coral = gabarito oficial · verde = item saudável.",
  "B", "E", "gabarito oficial: B",
  "A LEITURA TÉCNICA",
  c("A ICC do modelo de 3 parâmetros é monotônica por construção: a probabilidade de acertar o gabarito só pode SUBIR conforme a proficiência do candidato sobe — nunca cair e voltar a subir.",
    "O gabarito B desenha um U pela escala de nota: 26% (nota baixa) → 17% (meio da escala, ABAIXO do acaso de 20%) → 69% (nota alta) — um padrão que o 3PL proíbe.",
    "Esse formato é assinatura típica de item com dupla interpretação. Sem convergência não há A, B e C estáveis: o item saiu da régua e foi anulado.")
)
cat("FIM autópsia TRI (técnica)\n")

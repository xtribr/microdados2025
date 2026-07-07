#!/usr/bin/env Rscript
# LINKEDIN — Autópsia das questões anuladas do ENEM 2025 (quadrado 1200×1200).
# Small multiples: 5 itens anulados do Regular P1 (2 pela TRI + 3 vazadas) + painel-síntese.
# Coral = gabarito oficial (tri) ou resposta-consenso dos alunos fortes (vazadas, gabarito apagado).
# Base R + ggplot2 apenas (sem dplyr/readr).
suppressMessages(library(ggplot2))

BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "post_anulados/linkedin")

CORAL <- "#FA5230"; CINZA <- "#C7CBD0"; TINTA <- "#1D1D20"; GRIS <- "#8C9298"

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 21, colour = TINTA, margin = margin(b = 4)),
      plot.subtitle = element_text(size = 10.3, colour = GRIS, margin = margin(b = 12), lineheight = 1.2),
      plot.caption  = element_text(size = 8.2, colour = GRIS, hjust = 0, margin = margin(t = 14), lineheight = 1.25),
      axis.title    = element_text(colour = TINTA, size = 11),
      axis.text     = element_text(colour = "#6B7076", size = 9),
      strip.text    = element_text(face = "bold", size = 9.6, colour = TINTA,
                                   lineheight = 1.05, margin = margin(t = 4, b = 5)),
      panel.spacing.x = unit(16, "pt"),
      panel.spacing.y = unit(12, "pt"),
      legend.position = "none",
      plot.margin   = margin(18, 24, 14, 18)
    )
}
vir <- function(x, d = 1) gsub("\\.", ",", sprintf(paste0("%.", d, "f"), x))

cur <- read.csv(file.path(BASE, "palestra_2025/anulados_curvas.csv"),
                stringsAsFactors = FALSE, encoding = "UTF-8",
                colClasses = c(co_item = "character"))
cur <- cur[cur$alt != "outros" & cur$tipo %in% c("tri", "exposto"), ]

# foco: gabarito oficial (tri) ou consenso dos fortes (exposto — gabarito apagado pelo INEP)
foco_map <- c("97593" = "A", "96748" = "B", "141557" = "C", "141774" = "E", "31350" = "B")

rotulos <- c(
  "97593"  = "MT | anulada pela TRI (convergência)\ngabarito oficial A CAI com a nota",
  "96748"  = "CN | anulada pela TRI (convergência)\ngabarito oficial B faz curva em U",
  "141557" = "CN | vazada — curva saudável\ncoral = consenso dos fortes (C)",
  "141774" = "CN | vazada — curva saudável\ncoral = consenso dos fortes (E)",
  "31350"  = "MT | vazada — curva saudável\ncoral = consenso dos fortes (B)",
  "SINT"   = "As 3 vazadas: e a vantagem em massa?"
)
ordem <- c("97593", "96748", "141557", "141774", "31350", "SINT")

cur$foco  <- cur$alt == foco_map[cur$co_item]
cur$painel <- factor(rotulos[cur$co_item], levels = rotulos[ordem])

# linha do acaso (20%) só nos 5 painéis reais
acaso <- do.call(rbind, lapply(ordem[1:5], function(ci)
  data.frame(painel = rotulos[ci], x = c(325, 825), y = 20)))
acaso$painel <- factor(acaso$painel, levels = rotulos[ordem])

# letras no fim da curva (banda 825): só a coral (foco) e a cinza que termina mais alta
ult <- cur[cur$banda_meio == 825, ]
lab_fim <- do.call(rbind, lapply(split(ult, ult$co_item), function(d) {
  g <- d[!d$foco, ]
  d <- rbind(d[d$foco, ], g[which.max(g$pct), ])
  d$ylab <- d$pct
  if (abs(d$ylab[1] - d$ylab[2]) < 8)             # anti-colisão (não ocorre nos 5 itens)
    d$ylab[2] <- d$ylab[1] - sign(d$ylab[1] - d$ylab[2]) * 8
  d
}))

# painel-síntese (6º slot): pisos das vazadas ~ acaso
sint_txt <- paste0(
  "Nas 3 vazadas, o piso (nota 350-449)\n",
  "marcou o consenso perto do acaso:\n\n",
  "C: ", vir(26.7), "%    E: ", vir(9.4), "%    B: ", vir(23.2), "%\n\n",
  "Sem vantagem em massa.\n",
  "Anulação preventiva."
)
sint <- data.frame(painel = factor(rotulos["SINT"], levels = rotulos[ordem]),
                   x = 597, y = 49, lab = sint_txt)

p <- ggplot() +
  geom_line(data = acaso, aes(x = x, y = y, group = painel),
            linetype = "12", colour = GRIS, linewidth = 0.55) +
  geom_line(data = cur[!cur$foco, ],
            aes(x = banda_meio, y = pct, group = alt),
            colour = CINZA, linewidth = 0.65) +
  geom_line(data = cur[cur$foco, ],
            aes(x = banda_meio, y = pct, group = alt),
            colour = CORAL, linewidth = 1.6) +
  geom_point(data = cur[cur$foco, ],
             aes(x = banda_meio, y = pct),
             colour = CORAL, size = 1.7) +
  geom_text(data = lab_fim, aes(x = 845, y = ylab, label = alt, colour = foco),
            fontface = "bold", hjust = 0, size = 3.4) +
  geom_text(data = sint, aes(x = x, y = y, label = lab),
            size = 3.0, colour = TINTA, lineheight = 1.3, fontface = "bold") +
  scale_colour_manual(values = c("TRUE" = CORAL, "FALSE" = GRIS)) +
  facet_wrap(~painel, ncol = 2, drop = FALSE) +
  scale_x_continuous(breaks = c(400, 600, 800), limits = c(322, 872)) +
  scale_y_continuous(limits = c(-1, 95), breaks = seq(0, 75, 25),
                     labels = function(v) paste0(v, "%")) +
  labs(
    title = "Autópsia das questões anuladas do ENEM 2025",
    subtitle = paste0(
      "Cada linha = % dos alunos da faixa de nota que marcou a alternativa (Regular P1,\n",
      "~3,18 mi respostas por item). Coral = gabarito oficial (anuladas pela TRI) ou resposta-\n",
      "consenso dos alunos de nota alta (vazadas). Linha pontilhada = acaso (20%)."),
    x = "Nota TRI na área (faixas de 50 pontos)",
    y = "Alunos que marcaram a alternativa (%)",
    caption = paste0("Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2025 / INEP  |  Regular P1\n",
                     "curvas = % que marcou a alternativa, por faixa de 50 pts de nota")
  ) +
  theme_xtri()

ggsave(file.path(OUT, "xtri_anuladas_linkedin.png"), p,
       width = 8, height = 8, dpi = 150, bg = "#F1F1F2")
cat("ok: xtri_anuladas_linkedin.png\n")

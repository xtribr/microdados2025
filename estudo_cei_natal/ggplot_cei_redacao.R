#!/usr/bin/env Rscript
# Redação CEI por competência: média C1-C5 (vs Brasil) + % de nota 200 ("gabaritou").
suppressMessages(library(ggplot2))
suppressMessages(library(jsonlite))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025/estudo_cei_natal"
OUT  <- file.path(BASE, "graficos")

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major.y = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.major.x = element_blank(), panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 23, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 8)),
      plot.caption  = element_text(size = 9.5, colour = "#8C9298", hjust = 1, margin = margin(t = 12)),
      axis.title    = element_text(colour = "#1D1D20", size = 14),
      axis.text.x   = element_text(colour = "#1D1D20", size = 13, face = "bold", lineheight = 0.9),
      axis.text.y   = element_text(colour = "#6B7076", size = 12),
      legend.title  = element_blank(), legend.text = element_text(size = 12.5),
      legend.position = "top",
      plot.margin   = margin(18, 26, 12, 18)
    )
}
ESC_COL <- c("CEI Romualdo" = "#FA5230", "CEI Roberto Freire" = "#1FAFEF", "Brasil" = "#8C9298")
CAP <- "Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2025 / INEP  |  CEI: 139 + 70 redações válidas  |  Brasil = 3.245.696 redações válidas"
CLAB <- c("C1\nnorma culta", "C2\ncompreender\no tema", "C3\nargumentação", "C4\ncoesão", "C5\nproposta de\nintervenção")

cei <- fromJSON(file.path(BASE, "cei_redacao_comp.json"))
nac <- fromJSON(file.path(BASE, "redacao_2024_2025.json"))$`2025`$medias_comp
rows <- list()
for (esc in names(cei)) for (i in 1:5) {
  rows[[length(rows) + 1]] <- data.frame(escola = esc, comp = i,
                                         media = cei[[esc]][[paste0("C", i)]]$media,
                                         p200 = cei[[esc]][[paste0("C", i)]]$pct_200)
}
for (i in 1:5) rows[[length(rows) + 1]] <- data.frame(escola = "Brasil", comp = i,
                                                      media = round(nac[[paste0("NU_NOTA_COMP", i)]], 1), p200 = NA)
d <- do.call(rbind, rows)
d$escola <- factor(d$escola, levels = names(ESC_COL))

# rótulo dinâmico: unidade mais alta acima, mais baixa abaixo
lab <- d[d$escola != "Brasil", ]
lab$vj <- NA_real_
for (i in 1:5) {
  sub <- lab[lab$comp == i, ]
  hi <- as.character(sub$escola[which.max(sub$media)])
  lab$vj[lab$comp == i] <- ifelse(as.character(lab$escola[lab$comp == i]) == hi, -1.2, 2.4)
}

c1 <- d[d$comp == 1 & d$escola != "Brasil", "media"]
p <- ggplot(d, aes(x = comp, y = media, colour = escola, group = escola)) +
  geom_hline(yintercept = 200, colour = "#C9CBCE", linewidth = 0.7, linetype = "12") +
  annotate("text", x = 0.62, y = 204, label = "nota máxima (200)", hjust = 0, size = 3.8, colour = "#8C9298") +
  geom_line(aes(linetype = escola), linewidth = 1.4) +
  geom_point(size = 3.8) +
  geom_text(data = lab, aes(label = gsub("\\.", ",", sprintf("%.0f", media)), vjust = vj),
            size = 4.6, fontface = "bold", show.legend = FALSE) +
  geom_text(data = d[d$escola == "Brasil", ],
            aes(label = gsub("\\.", ",", sprintf("%.0f", media))), vjust = 2.4, size = 4.2, show.legend = FALSE) +
  # callout no C1 (gargalo): seta à esquerda do ponto, texto compacto na área livre
  annotate("segment", x = 0.78, xend = 0.78, y = max(c1) + 4, yend = 199,
           colour = "#E8431F", linewidth = 1.1,
           arrow = arrow(ends = "both", length = unit(0.16, "cm"), type = "closed")) +
  annotate("label", x = 0.9, y = 190,
           label = "o gargalo: C1, norma culta\nsó 1,4% (Rom) e 0% (RF)\ngabaritam (nota 200)",
           hjust = 0, size = 4.2, fontface = "bold", colour = "#E8431F", fill = "#FFFFFF", lineheight = 0.98) +
  scale_colour_manual(values = ESC_COL) +
  scale_linetype_manual(values = c("CEI Romualdo" = "solid", "CEI Roberto Freire" = "solid", "Brasil" = "22")) +
  scale_x_continuous(breaks = 1:5, labels = CLAB, limits = c(0.6, 5.4)) +
  scale_y_continuous(limits = c(80, 215), breaks = seq(80, 200, 40)) +
  labs(title = "Redação — onde as CEI ainda perdem ponto",
       subtitle = "Média por competência (0–200). As CEI dominam C4/C5, domaram a C2 (vilã nacional) — mas a C1 é a mais distante do teto.",
       x = "Competência da redação", y = "Média na competência (0–200)",
       caption = CAP) +
  theme_xtri()
ggsave(file.path(OUT, "cei_redacao_competencias.png"), p, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: cei_redacao_competencias\n")

# ---- % de nota 200 por competência ----
d2 <- d[d$escola != "Brasil", ]
p2 <- ggplot(d2, aes(x = comp, y = p200, fill = escola)) +
  geom_col(position = position_dodge(width = 0.7), width = 0.6) +
  geom_text(aes(label = gsub("\\.", ",", sprintf("%.0f%%", p200))),
            position = position_dodge(width = 0.7), vjust = -0.5, size = 4.4,
            fontface = "bold", colour = "#1D1D20") +
  scale_fill_manual(values = ESC_COL) +
  scale_x_continuous(breaks = 1:5, labels = CLAB) +
  scale_y_continuous(limits = c(0, 75), labels = function(v) paste0(v, "%")) +
  labs(title = "Quem gabarita (nota 200) cada competência?",
       subtitle = "% dos alunos CEI com nota máxima em cada competência. Na C5, 6 em 10 gabaritam; na C1, quase ninguém.",
       x = "Competência da redação", y = "Alunos com nota 200 (%)",
       caption = CAP) +
  theme_xtri()
ggsave(file.path(OUT, "cei_redacao_200.png"), p2, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: cei_redacao_200\n")

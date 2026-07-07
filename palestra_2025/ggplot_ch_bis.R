#!/usr/bin/env Rscript
# Item CH 152715 (2ª aplicação, Bis<0,01): com n=309, curva vira ruído — barras por tercil de nota.
# A assinatura do Bis~0: o gabarito (D) é marcado na MESMA proporção por fracos, médios e fortes.
# Versão técnica: painel de explicação psicométrica embutido (empilhado via gridExtra).
suppressMessages(library(ggplot2))
suppressMessages(library(jsonlite))
suppressMessages(library(gridExtra))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025"
OUT  <- file.path(BASE, "palestra_2025/graficos")

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major.y = element_line(colour = "#DEDEE1", linewidth = 0.4),
      panel.grid.major.x = element_blank(), panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 22, colour = "#1D1D20", margin = margin(b = 2)),
      plot.subtitle = element_text(size = 13.5, colour = "#8C9298", margin = margin(b = 10)),
      plot.caption  = element_text(size = 9.5, colour = "#8C9298", hjust = 1, margin = margin(t = 12)),
      axis.title    = element_text(colour = "#1D1D20", size = 13.5),
      axis.text     = element_text(colour = "#1D1D20", size = 12.5),
      legend.title  = element_blank(), legend.text = element_text(size = 12),
      legend.position = "top",
      strip.text    = element_text(face = "bold", size = 13, colour = "#1D1D20"),
      strip.background = element_rect(fill = "#E8E9EB", colour = NA),
      plot.margin   = margin(16, 24, 8, 16)
    )
}

painel_tecnico <- function(titulo, linhas, largura_chars = 108) {
  linhas_q <- unlist(lapply(linhas, function(s) strwrap(s, width = largura_chars)))
  n <- length(linhas_q)
  y0 <- 0.74
  ymin_body <- 0.08
  dy <- (y0 - ymin_body) / max(n - 1, 1)
  ys <- y0 - (seq_len(n) - 1) * dy
  df <- data.frame(y = ys, txt = linhas_q)
  ggplot() + theme_void() +
    scale_x_continuous(limits = c(0, 1), expand = c(0, 0)) +
    scale_y_continuous(limits = c(0, 1), expand = c(0, 0)) +
    annotate("rect", xmin = 0, xmax = 1, ymin = 0, ymax = 1, fill = "#FCEDE9") +
    annotate("rect", xmin = 0, xmax = 0.006, ymin = 0, ymax = 1, fill = "#FA5230") +
    annotate("text", x = 0.024, y = 0.94, label = titulo, hjust = 0, vjust = 1,
             fontface = "bold", colour = "#E8431F", size = 4.6) +
    geom_text(data = df, aes(x = 0.024, y = y, label = txt), hjust = 0, vjust = 1,
              size = 4.35, colour = "#1D1D20", lineheight = 1.05) +
    theme(plot.margin = margin(2, 2, 2, 2), plot.background = element_rect(fill = "#F1F1F2", colour = NA))
}

pares <- fromJSON(file.path(BASE, "palestra_2025/ch_bis_pares.json"))
df <- data.frame(nota = as.numeric(pares[, 1]), alt = pares[, 2], stringsAsFactors = FALSE)
df <- df[df$alt %in% c("A", "B", "C", "D", "E"), ]
q <- quantile(df$nota, c(1 / 3, 2 / 3))
df$grupo <- cut(df$nota, c(-Inf, q[1], q[2], Inf),
                labels = c(sprintf("nota até %d", round(q[1])),
                           sprintf("%d–%d", round(q[1]) + 1, round(q[2])),
                           sprintf("acima de %d", round(q[2]))))
tab <- as.data.frame(prop.table(table(df$grupo, df$alt), 1) * 100)
names(tab) <- c("grupo", "alt", "pct")
tab$gab <- tab$alt == "D"
ns <- table(df$grupo)
d_pct <- tab[tab$alt == "D", "pct"]

p <- ggplot(tab, aes(x = alt, y = pct, fill = gab)) +
  geom_hline(yintercept = 20, linetype = "12", colour = "#8C9298", linewidth = 0.6) +
  geom_col(width = 0.68) +
  geom_text(aes(label = sprintf("%.0f%%", pct)), vjust = -0.5, size = 4.0,
            fontface = "bold", colour = "#1D1D20") +
  facet_wrap(~grupo, ncol = 3) +
  scale_fill_manual(values = c("FALSE" = "#C7CBD0", "TRUE" = "#FA5230"),
                    labels = c("FALSE" = "Demais alternativas", "TRUE" = "Gabarito oficial (D)")) +
  scale_y_continuous(limits = c(0, max(tab$pct) * 1.18), labels = function(v) paste0(v, "%")) +
  labs(title = "O item que não media nada (Bis < 0,01)",
       subtitle = "Ciências Humanas, 2ª aplicação — três grupos de nota, mesmo padrão de marcação.",
       x = "Alternativa marcada", y = "Alunos do grupo que marcaram (%)",
       caption = sprintf("Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2025 / INEP  |  2ª aplicação, n = %d respondentes (%d por grupo)  |  linha pontilhada = acaso (20%%)",
                         nrow(df), round(mean(ns)))) +
  theme_xtri()

tec <- painel_tecnico("A LEITURA TÉCNICA", c(
  "A correlação bisserial mede a relação entre acertar o item e a proficiência total do candidato na prova — aqui ela é praticamente nula (Bis < 0,01).",
  sprintf("O gabarito D é marcado por %s%% dos alunos de nota baixa, %s%% dos de nota média e %s%% dos de nota alta — sem tendência de subida, e os fortes preferem a alternativa E (51%%).",
          gsub("\\.", ",", sprintf("%.0f", d_pct[1])),
          gsub("\\.", ",", sprintf("%.0f", d_pct[2])),
          gsub("\\.", ",", sprintf("%.0f", d_pct[3]))),
  "Sem correlação com a proficiência, o item não separa quem sabe de quem não sabe. Em amostra pequena (n=309, 2ª aplicação) o dano se amplia — a TRI cortou antes de distorcer a nota dos demais itens."
))

g <- arrangeGrob(p, tec, ncol = 1, heights = c(3.1, 1))
ggsave(file.path(OUT, "g13_anulado_tri_CH.png"), g, width = 13.33, height = 8.6, dpi = 150, bg = "#F1F1F2")
print(tab[tab$alt == "D", c("grupo", "pct")])
cat("ok: g13_anulado_tri_CH.png\n")

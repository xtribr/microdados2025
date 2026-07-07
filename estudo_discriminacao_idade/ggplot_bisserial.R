#!/usr/bin/env Rscript
# Comparação 2024×2025: discriminação por área via correlação ponto-bisserial (proxy do
# parâmetro A, calculado de forma idêntica nos dois anos a partir de TX_RESPOSTAS/TX_GABARITO).
suppressMessages(library(ggplot2))
suppressMessages(library(jsonlite))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025/estudo_discriminacao_idade"
OUT  <- file.path(BASE, "graficos")

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
      axis.text     = element_text(colour = "#1D1D20", size = 13),
      legend.position = "top", legend.title = element_blank(), legend.text = element_text(size = 12),
      plot.margin   = margin(16, 26, 12, 16)
    )
}
NOMES <- c(LC = "Linguagens", CH = "Ciências Humanas", CN = "Ciências da Natureza", MT = "Matemática")
vir <- function(x, d = 3) gsub("\\.", ",", sprintf(paste0("%.", d, "f"), x))

j <- fromJSON(file.path(BASE, "bisserial_2024_2025.json"))
rows <- list()
for (a in names(NOMES)) {
  rows[[length(rows) + 1]] <- data.frame(area = a, ano = "2024", r = j[["2024"]][[a]]$r_media)
  rows[[length(rows) + 1]] <- data.frame(area = a, ano = "2025", r = j[["2025"]][[a]]$r_media)
}
d <- do.call(rbind, rows)
d$area_lab <- factor(NOMES[d$area], levels = NOMES)
d$ano <- factor(d$ano, levels = c("2024", "2025"))

delta <- reshape(d[, c("area_lab", "ano", "r")], idvar = "area_lab", timevar = "ano", direction = "wide")
delta$dif <- delta$r.2025 - delta$r.2024
delta$lab <- sprintf("%s%s", ifelse(delta$dif >= 0, "+", ""), vir(delta$dif))

p <- ggplot(d, aes(x = area_lab, y = r, fill = ano)) +
  geom_col(position = position_dodge(width = 0.7), width = 0.6) +
  geom_text(aes(label = vir(r)), position = position_dodge(width = 0.7), vjust = -0.6, size = 4.3,
            fontface = "bold", colour = "#1D1D20") +
  geom_text(data = delta, aes(x = area_lab, y = pmax(r.2024, r.2025) + 0.05, label = lab),
            inherit.aes = FALSE, size = 4.0, fontface = "bold",
            colour = ifelse(delta$dif >= 0, "#2EA84F", "#E8431F")) +
  scale_fill_manual(values = c("2024" = "#C7CBD0", "2025" = "#FA5230")) +
  scale_y_continuous(limits = c(0, max(d$r) * 1.22), labels = function(v) vir(v, 2)) +
  labs(title = "A prova discrimina mais ou menos que em 2024?",
       subtitle = "Correlação ponto-bisserial média (acerto do item × nota da área) — proxy do parâmetro A, calculado de forma idêntica nos dois anos.",
       x = NULL, y = "Correlação ponto-bisserial (média por área)",
       caption = "Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2024 e 2025 / INEP  |  amostra 150.000 presentes/área/ano  |  NÃO é o parâmetro A oficial do 3PL (indisponível p/ 2024)") +
  theme_xtri()
ggsave(file.path(OUT, "g4_bisserial_2024_2025.png"), p, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: g4_bisserial_2024_2025\n")
print(delta)

#!/usr/bin/env Rscript
# TEMA2 — Os parâmetros oficiais reproduzem a nota? Reconstrução EAP vs nota oficial (4 áreas).
suppressMessages({library(ggplot2); library(dplyr)})
BASE <- "/Volumes/Kingston 1/microdados_enem_2025/estudo_reproduz_nota"
d <- read.csv(file.path(BASE, "tema2_scatter.csv"), sep = ";")
nomes <- c(LC = "Linguagens", CH = "Ciências Humanas", CN = "Ciências da Natureza", MT = "Matemática")
cores <- c("Linguagens" = "#2C6FBB", "Ciências Humanas" = "#C0392B",
           "Ciências da Natureza" = "#1E8449", "Matemática" = "#6C3483")
d$area_f <- factor(nomes[d$area], levels = nomes)
itens <- c("Linguagens" = "40 itens comuns", "Ciências Humanas" = "45 itens",
           "Ciências da Natureza" = "42 itens", "Matemática" = "43 itens")

# métricas por área (sobre TODOS os pontos)
lab <- d %>% group_by(area_f) %>%
  summarise(r = cor(nota, recon), rmse = sqrt(mean((recon - nota)^2)), .groups = "drop") %>%
  mutate(txt = sprintf("r = %.4f", r),
         txt2 = sprintf("RMSE = %.1f pt · %s", rmse, itens[as.character(area_f)]))

vir <- function(x) format(x, big.mark = ".", decimal.mark = ",")
theme_lp <- function() theme_minimal(base_size = 15) + theme(
  plot.background = element_rect(fill = "white", colour = NA),
  panel.background = element_rect(fill = "#FAFAFB", colour = NA),
  panel.grid.minor = element_blank(), panel.grid.major = element_line(colour = "#EAEAEC", linewidth = 0.4),
  panel.spacing = unit(1.1, "lines"),
  strip.text = element_text(face = "bold", size = 14, colour = "#1D1D20"),
  plot.title = element_text(face = "bold", size = 22, colour = "#1D1D20"),
  plot.subtitle = element_text(size = 12.5, colour = "#6B7076", margin = margin(t = 4, b = 12)),
  plot.caption = element_text(size = 9.5, colour = "#8C9298", hjust = 0, margin = margin(t = 12)),
  plot.title.position = "plot", plot.caption.position = "plot",
  axis.title = element_text(size = 12.5, colour = "#3A3A3D"), plot.margin = margin(18, 22, 14, 18))

# ---------- Gráfico 1: reconstruída vs oficial ----------
set.seed(1)
ds <- d %>% group_by(area_f) %>% slice_sample(n = 6000) %>% ungroup()
p1 <- ggplot(ds, aes(nota, recon, colour = area_f)) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", colour = "#8C9298", linewidth = 0.6) +
  geom_point(alpha = 0.10, size = 0.5, show.legend = FALSE) +
  geom_text(data = lab, aes(x = 330, y = 930, label = txt), hjust = 0, vjust = 1,
            size = 5.2, fontface = "bold", colour = "#1D1D20", inherit.aes = FALSE) +
  geom_text(data = lab, aes(x = 330, y = 878, label = txt2), hjust = 0, vjust = 1,
            size = 3.4, colour = "#6B7076", inherit.aes = FALSE) +
  facet_wrap(~area_f, ncol = 2) + scale_colour_manual(values = cores) +
  scale_x_continuous(limits = c(300, 980), breaks = seq(400, 900, 100)) +
  scale_y_continuous(limits = c(300, 980), breaks = seq(400, 900, 100)) +
  labs(title = "Os parâmetros oficiais reproduzem a nota do ENEM 2025",
       subtitle = "Nota reconstruída só com os parâmetros públicos (a, b, c) + o padrão de respostas de cada candidato (EAP),\ncontra a nota oficial do INEP. A linha tracejada é a igualdade perfeita. 40 mil candidatos por área (Azul).",
       x = "Nota oficial do INEP", y = "Nota reconstruída (só com os parâmetros)",
       caption = "Dados: Microdados ENEM 2025 / INEP · reconstrução por EAP (modelo 3PL) sobre os parâmetros de ITENS_PROVA · escala alinhada por transformação linear.") +
  theme_lp() + coord_equal()
ggsave(file.path(BASE, "reproduz_nota_scatter.png"), p1, width = 11, height = 10.4, dpi = 150, bg = "white")
cat("ok: reproduz_nota_scatter.png\n")

# ---------- Gráfico 2: acerto não é nota ----------
faixa <- d %>% group_by(area_f, ac) %>%
  summarise(p5 = quantile(nota, 0.05), p95 = quantile(nota, 0.95), nmed = median(nota), n = n(), .groups = "drop") %>%
  filter(n >= 100)
# destaque: maior amplitude robusta (p5–p95) por área
dest <- faixa %>% mutate(ampl = p95 - p5) %>% group_by(area_f) %>% slice_max(ampl, n = 1) %>% ungroup()
p2 <- ggplot(faixa, aes(ac, colour = area_f)) +
  geom_linerange(aes(ymin = p5, ymax = p95), linewidth = 1.7, alpha = 0.35, show.legend = FALSE) +
  geom_point(aes(y = nmed), size = 1.6, show.legend = FALSE) +
  geom_text(data = dest, aes(x = ac, y = p95 + 14,
            label = sprintf("%d acertos:\n%s a %s (%s pts entre 5%% e 95%%)", ac, vir(round(p5)), vir(round(p95)), vir(round(p95-p5)))),
            size = 3.0, fontface = "bold", hjust = 0.5, vjust = 0, lineheight = 0.95, inherit.aes = FALSE, colour = "#1D1D20") +
  facet_wrap(~area_f, ncol = 2) + scale_colour_manual(values = cores) +
  scale_x_continuous(breaks = seq(0, 45, 10)) +
  labs(title = "\"Acerto não é nota\": o mesmo número de acertos, notas muito diferentes",
       subtitle = "Para cada número de acertos, a barra mostra a faixa entre os 5% e 95% dos candidatos e o ponto é a mediana. Com\no mesmo total de acertos, a nota varia de ~90 a 160 pontos conforme QUAIS itens você acertou.",
       x = "Número de acertos (itens válidos)", y = "Nota oficial do INEP",
       caption = "Dados: Microdados ENEM 2025 / INEP · 40 mil candidatos por área (caderno Azul) · faixa entre percentis 5 e 95, grupos com 100+ candidatos.") +
  theme_lp()
ggsave(file.path(BASE, "acerto_nao_e_nota.png"), p2, width = 11, height = 9.2, dpi = 150, bg = "white")
cat("ok: acerto_nao_e_nota.png\n")
print(lab)

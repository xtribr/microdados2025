#!/usr/bin/env Rscript
# Estudo: poder discriminatório (parâmetro A) por área × perfil etário dos candidatos 2025.
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
      axis.text     = element_text(colour = "#1D1D20", size = 11.5),
      axis.text.x   = element_text(angle = 0),
      legend.position = "top", legend.title = element_blank(), legend.text = element_text(size = 12),
      strip.text    = element_text(face = "bold", size = 13.5, colour = "#1D1D20"),
      strip.background = element_rect(fill = "#E8E9EB", colour = NA),
      plot.margin   = margin(16, 26, 12, 16)
    )
}
CAP <- "Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2025 / INEP"
NOMES <- c(LC = "Linguagens", CH = "Ciências Humanas", CN = "Ciências da Natureza", MT = "Matemática")
AREA_COL <- c(LC = "#1FAFEF", CH = "#E84855", CN = "#2EC4B6", MT = "#3A86FF")
vir <- function(x, d = 1) gsub("\\.", ",", sprintf(paste0("%.", d, "f"), x))

dem <- fromJSON(file.path(BASE, "demografia_2025.json"))
FAIXAS <- c("<17","17","18","19","20","21","22","23","24","25","26-30","31-35","36-40",
            "41-45","46-50","51-55","56-60","61-65","66-70","70+")

# ---------- G1: distribuição etária Brasil 2025 ----------
d1 <- data.frame(faixa = factor(FAIXAS, levels = FAIXAS),
                 n = as.numeric(dem$geral_por_faixa[FAIXAS]))
d1$pct <- 100 * d1$n / sum(d1$n)
d1$destaque <- d1$faixa %in% c("66-70", "70+")
p1 <- ggplot(d1, aes(x = faixa, y = pct, fill = destaque)) +
  geom_col(width = 0.72) +
  geom_text(data = d1[d1$pct >= 1, ], aes(label = sprintf("%.1f%%", pct)), vjust = -0.5, size = 3.6, colour = "#1D1D20") +
  scale_fill_manual(values = c("FALSE" = "#1FAFEF", "TRUE" = "#FA5230"), guide = "none") +
  scale_y_continuous(limits = c(0, max(d1$pct) * 1.15), labels = function(v) paste0(v, "%"), expand = c(0, 0)) +
  annotate("label", x = 19.6, y = max(d1$pct) * 0.55,
           label = sprintf("66 a 70 anos: %s mil candidatos\nacima de 70 anos: %s mil candidatos",
                           vir(dem$n_66_70 / 1000, 1), vir(dem$n_70mais / 1000, 1)),
           hjust = 1, size = 4.2, colour = "#E8431F", fontface = "bold", fill = "#FFFFFF") +
  labs(title = "O retrato etário do ENEM 2025",
       subtitle = "Distribuição de todos os 4.810.772 inscritos por faixa de idade (questionário 100% preenchido, obrigatório desde 2025).",
       x = "Faixa etária", y = "% dos inscritos",
       caption = paste0(CAP, "  |  N = 4.810.772 inscritos  |  TP_FAIXA_ETARIA")) +
  theme_xtri() + theme(axis.text.x = element_text(size = 10.5))
ggsave(file.path(OUT, "g1_distribuicao_etaria.png"), p1, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: g1_distribuicao_etaria\n")

# ---------- G2: COP30/BAM vs Regular — mesma escala etária, populações diferentes ----------
d2a <- data.frame(faixa = factor(FAIXAS, levels = FAIXAS), grupo = "COP30/BAM (Belém-Ananindeua-Marituba)",
                  pct = as.numeric(dem$cop30_por_faixa_pct[FAIXAS]))
d2b <- data.frame(faixa = factor(FAIXAS, levels = FAIXAS), grupo = "Resto do Brasil (Regular)",
                  pct = as.numeric(dem$regular_por_faixa_pct[FAIXAS]))
d2 <- rbind(d2a, d2b)
d2$grupo <- factor(d2$grupo, levels = c("Resto do Brasil (Regular)", "COP30/BAM (Belém-Ananindeua-Marituba)"))
p2 <- ggplot(d2, aes(x = faixa, y = pct, fill = grupo)) +
  geom_col(position = position_dodge(width = 0.75), width = 0.68) +
  scale_fill_manual(values = c("Resto do Brasil (Regular)" = "#C7CBD0",
                               "COP30/BAM (Belém-Ananindeua-Marituba)" = "#FA5230")) +
  scale_y_continuous(labels = function(v) paste0(v, "%"), expand = expansion(mult = c(0, 0.08))) +
  annotate("label", x = 15, y = max(d2$pct) * 0.85,
           label = sprintf("26 anos ou mais:\nCOP30/BAM %s%%  vs  Regular %s%%",
                           vir(dem$pct_26mais_cop30), vir(dem$pct_26mais_regular)),
           hjust = 0, size = 4.3, colour = "#E8431F", fontface = "bold", fill = "#FFFFFF") +
  labs(title = "Duas populações, dois perfis etários",
       subtitle = "COP30/BAM (aplicação especial em 3 municípios do Pará) tem quase o dobro de candidatos com 26+ anos.",
       x = "Faixa etária", y = "% dentro do grupo",
       caption = sprintf("%s  |  COP30/BAM n=%s  |  Regular n=%s  |  CO_MUNICIPIO_PROVA", CAP,
                         format(dem$n_cop30, big.mark = "."), format(dem$n_regular, big.mark = "."))) +
  theme_xtri() + theme(axis.text.x = element_text(size = 10.5))
ggsave(file.path(OUT, "g2_cop30_vs_regular_idade.png"), p2, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: g2_cop30_vs_regular_idade\n")

# ---------- G3: parâmetro A por área — dot plot com faixas de Baker ----------
it <- read.csv(file.path(BASE, "discriminacao_itens.csv"), stringsAsFactors = FALSE)
it$area_lab <- factor(NOMES[it$area], levels = NOMES)
it$baker <- factor(it$baker, levels = c("moderada", "alta", "muito alta"))
BAKER_COL <- c("moderada" = "#C7CBD0", "alta" = "#FB9276", "muito alta" = "#FA5230")
meds <- aggregate(A ~ area_lab, it, median)

p3 <- ggplot(it, aes(x = area_lab, y = A, colour = baker)) +
  geom_hline(yintercept = c(1.35, 1.70), linetype = "12", colour = "#8C9298", linewidth = 0.5) +
  annotate("text", x = -Inf, y = 1.35, label = "alta (1,35)", hjust = -0.05, size = 3.4, colour = "#8C9298", vjust = -0.5) +
  annotate("text", x = -Inf, y = 1.70, label = "muito alta (1,70)", hjust = -0.05, size = 3.4, colour = "#8C9298", vjust = -0.5) +
  geom_jitter(width = 0.16, size = 3, alpha = 0.85) +
  geom_crossbar(data = meds, aes(x = area_lab, y = A, ymin = A, ymax = A), colour = "#1D1D20", width = 0.4, linewidth = 0.9, inherit.aes = FALSE) +
  scale_colour_manual(values = BAKER_COL, name = "Discriminação (Baker)") +
  scale_y_continuous(breaks = seq(0, 6, 1)) +
  labs(title = "O poder discriminatório (A) das 4 áreas — ENEM 2025",
       subtitle = "Cada ponto é um item do caderno Azul. Traço preto = mediana da área. Nenhum item, em nenhuma área, cai em 'baixa' ou 'muito baixa'.",
       x = NULL, y = "Parâmetro A (discriminação)",
       caption = paste0(CAP, "  |  Regular P1, caderno Azul  |  180 itens válidos (LC 50 c/ 2ª língua, CH 45, CN 42, MT 43)")) +
  theme_xtri()
ggsave(file.path(OUT, "g3_parametro_a_por_area.png"), p3, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
cat("ok: g3_parametro_a_por_area\n")

#!/usr/bin/env Rscript
# Gráficos ggplot — O ENEM inclui o aluno com necessidades especiais? (Censo 2025 x ENEM 2025)
suppressMessages(library(ggplot2))
suppressMessages(library(jsonlite))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025/estudo_inclusao_nee"
OUT  <- file.path(BASE, "linkedin")
dir.create(OUT, showWarnings = FALSE)

CORAL <- "#FA5230"; CORALd <- "#E8431F"; CYAN <- "#1FAFEF"; CYANd <- "#1597D8"
INK <- "#1D1D20"; GRAY <- "#8C9298"; VERDE <- "#2EA84F"; VERDEd <- "#1F8F3E"; AMBAR <- "#F2A93B"; ROXO <- "#7A5AF8"

theme_xtri <- function(base = 15) {
  theme_minimal(base_size = base) +
    theme(
      plot.background  = element_rect(fill = "#F1F1F2", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major = element_line(colour = "#E3E3E6", linewidth = 0.4),
      panel.grid.minor = element_blank(),
      plot.title    = element_text(face = "bold", size = 23, colour = INK, margin = margin(b = 3)),
      plot.subtitle = element_text(size = 13.5, colour = GRAY, margin = margin(b = 12)),
      plot.caption  = element_text(size = 9.5, colour = GRAY, hjust = 0, margin = margin(t = 14)),
      axis.title    = element_text(colour = INK, size = 13),
      axis.text     = element_text(colour = INK, size = 12),
      legend.position = "top", legend.title = element_blank(), legend.text = element_text(size = 12),
      plot.title.position = "plot", plot.caption.position = "plot",
      plot.margin   = margin(18, 28, 14, 18)
    )
}
CAP <- "Fontes: Censo Escolar 2025 e ENEM 2025 — INEP/MEC  ·  dados agregados, sem identificação de aluno  ·  @xandaoxtri"
vir <- function(x, d = 1) gsub("\\.", ",", sprintf(paste0("%.", d, "f"), x))
milhar <- function(x) formatC(x, format = "d", big.mark = ".")

D <- fromJSON(file.path(BASE, "dados_inclusao.json"))
F <- D$funil_nacional
sv <- function(p) fig_save(p)  # placeholder

# ============ G1: matrícula — classe comum x exclusiva (barra empilhada) ============
d1 <- data.frame(
  cat = factor(c("Classe comum (incluídos)", "Classe exclusiva (segregados)"),
               levels = c("Classe exclusiva (segregados)", "Classe comum (incluídos)")),
  n = c(F$nee_med_cc, F$nee_med_ce),
  pct = c(F$pct_cc, F$pct_ce))
d1$lab <- paste0(vir(d1$pct), "%\n", milhar(d1$n))
p1 <- ggplot(d1, aes(x = 1, y = n, fill = cat)) +
  geom_col(width = 0.5) +
  geom_text(aes(label = ifelse(pct > 5, lab, "")), position = position_stack(vjust = 0.5),
            colour = "white", fontface = "bold", size = 6, lineheight = 0.9) +
  annotate("text", x = 1.36, y = F$nee_med, hjust = 1,
           label = paste0("Classe exclusiva/segregada: só ", milhar(F$nee_med_ce), " (", vir(F$pct_ce), "%)"),
           colour = CORALd, fontface = "bold", size = 4.2) +
  scale_fill_manual(values = c("Classe comum (incluídos)" = VERDE, "Classe exclusiva (segregados)" = CORAL)) +
  coord_flip() +
  scale_y_continuous(labels = milhar, expand = expansion(mult = c(0, 0.02))) +
  labs(title = "Na matrícula, o Brasil inclui de verdade",
       subtitle = paste0("Das ", milhar(F$nee_med), " matrículas de Educação Especial no Ensino Médio, 99,4% estão em classe comum — como determinam\na Constituição (art. 208) e a Lei Brasileira de Inclusão (Lei 13.146/2015). Quase ninguém em sala segregada."),
       x = NULL, y = "Matrículas de Educação Especial no Ensino Médio (Censo 2025)",
       caption = paste0(CAP, "  ·  QT_MAT_ESP_MED")) +
  theme_xtri() + theme(axis.text.y = element_blank(), panel.grid.major.y = element_blank())
ggsave(file.path(OUT, "g1_matricula_inclusao.png"), p1, width = 11, height = 6, dpi = 150, bg = "#F1F1F2")

# ============ G2: tipos de prova adaptada no ENEM ============
tp <- F$enem_por_tipo
d2 <- data.frame(tipo = names(tp), n = as.numeric(unlist(tp)))
d2$tipo <- factor(d2$tipo, levels = d2$tipo[order(d2$n)])
p2 <- ggplot(d2, aes(x = tipo, y = n)) +
  geom_col(width = 0.68, fill = CORAL) +
  geom_text(aes(label = milhar(n)), hjust = -0.15, size = 4.6, fontface = "bold", colour = CORALd) +
  coord_flip(clip = "off") +
  scale_y_continuous(limits = c(0, max(d2$n) * 1.16), expand = c(0, 0), labels = milhar) +
  labs(title = "Mas no ENEM, eles quase somem",
       subtitle = paste0("Só ", milhar(F$enem_adaptado), " fizeram prova adaptada em 2025 — e o dado só 'vê' quem mudou o caderno físico.\nQuem usa só tempo adicional (TDA, TDAH, dislexia) faz o caderno comum e não deixa rastro."),
       x = NULL, y = "Candidatos, por tipo de adaptação (ENEM 2025)",
       caption = paste0(CAP, "  ·  CO_PROVA")) +
  theme_xtri() + theme(panel.grid.major.y = element_blank())
ggsave(file.path(OUT, "g2_tipos_prova.png"), p2, width = 11, height = 6, dpi = 150, bg = "#F1F1F2")

# ============ G3: índice por UF, colorido por região (flagship) ============
uf <- D$por_uf
regiao <- c(
  AC="Norte",AP="Norte",AM="Norte",PA="Norte",RO="Norte",RR="Norte",TO="Norte",
  AL="Nordeste",BA="Nordeste",CE="Nordeste",MA="Nordeste",PB="Nordeste",PE="Nordeste",PI="Nordeste",RN="Nordeste",SE="Nordeste",
  DF="Centro-Oeste",GO="Centro-Oeste",MT="Centro-Oeste",MS="Centro-Oeste",
  ES="Sudeste",MG="Sudeste",RJ="Sudeste",SP="Sudeste",
  PR="Sul",RS="Sul",SC="Sul")
d3 <- data.frame(uf = uf$uf, idx = uf$taxa_chegada_pct)
d3$regiao <- factor(regiao[d3$uf], levels = c("Nordeste","Norte","Centro-Oeste","Sudeste","Sul"))
d3$uf <- factor(d3$uf, levels = d3$uf[order(d3$idx)])
media_br <- 100 * F$enem_adaptado / F$nee_med
regcol <- c("Nordeste"=CORAL, "Norte"=CYAN, "Centro-Oeste"=AMBAR, "Sudeste"=ROXO, "Sul"=GRAY)
p3 <- ggplot(d3, aes(x = uf, y = idx, fill = regiao)) +
  geom_col(width = 0.74) +
  geom_hline(yintercept = media_br, colour = INK, linetype = "22", linewidth = 0.5) +
  annotate("text", x = 2.2, y = media_br, label = paste0("média Brasil: ", vir(media_br)),
           hjust = -0.03, vjust = -0.5, size = 3.7, colour = INK, fontface = "italic") +
  geom_text(aes(label = vir(idx)), hjust = -0.18, size = 3.5, colour = INK) +
  coord_flip(clip = "off") +
  scale_fill_manual(values = regcol) +
  scale_y_continuous(limits = c(0, max(d3$idx) * 1.12), expand = c(0, 0)) +
  labs(title = "Quais estados mais levam esse aluno ao ENEM",
       subtitle = "Provas adaptadas (ENEM) por 100 matrículas de Educação Especial no EM (Censo). Nordeste e Norte lideram;\no Sul aparece no fim. É índice de participação VISÍVEL — não um ranking de qualidade da inclusão.",
       x = NULL, y = "Provas adaptadas por 100 matrículas NEE no Ensino Médio",
       caption = paste0(CAP, "  ·  índice = adaptado (ENEM) ÷ matrículas NEE-EM (Censo)")) +
  theme_xtri(base = 13) + theme(axis.text.y = element_text(size = 10.5), panel.grid.major.y = element_blank())
ggsave(file.path(OUT, "g3_indice_uf.png"), p3, width = 11, height = 8.4, dpi = 150, bg = "#F1F1F2")

# ============ G4: o contraste / ponto cego ============
d4 <- data.frame(
  cat = factor(c("Matriculados na Educação\nEspecial (EM) — Censo", "Visíveis no ENEM com\nprova adaptada"),
               levels = c("Visíveis no ENEM com\nprova adaptada", "Matriculados na Educação\nEspecial (EM) — Censo")),
  n = c(F$nee_med, F$enem_adaptado),
  cor = c(VERDE, CORAL))
p4 <- ggplot(d4, aes(x = cat, y = n, fill = cor)) +
  geom_col(width = 0.58) +
  geom_text(aes(label = milhar(n)), hjust = -0.12, size = 6.4, fontface = "bold",
            colour = c(VERDEd, CORALd)) +
  scale_fill_identity() +
  coord_flip(clip = "off") +
  scale_y_continuous(limits = c(0, F$nee_med * 1.16), expand = c(0, 0), labels = milhar) +
  labs(title = "294 mil na escola. 22 mil visíveis na prova.",
       subtitle = "Cuidado: NÃO é 'só 8% chega ao ENEM'. Os 294 mil são o estoque dos 3 anos do EM, e muito aluno\nfaz a prova SEM caderno adaptado — logo, é invisível. É o tamanho do ponto cego, não uma taxa de exclusão.",
       x = NULL, y = NULL,
       caption = CAP) +
  theme_xtri() + theme(panel.grid.major.y = element_blank(), axis.text.y = element_text(face = "bold", size = 12.5))
ggsave(file.path(OUT, "g4_contraste.png"), p4, width = 11, height = 6, dpi = 150, bg = "#F1F1F2")

cat("ok — 4 gráficos gerados em", OUT, "\n")

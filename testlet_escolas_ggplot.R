#!/usr/bin/env Rscript
# Testlet de Linguagens (Q6–Q10 Azul, crônica "De próprio punho"): taxa de erro da escola × Brasil.
suppressMessages(library(ggplot2))
BASE <- "/Volumes/Kingston 1/microdados_enem_2025"

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
      axis.text.x   = element_text(colour = "#1D1D20", size = 13, face = "bold", lineheight = 0.9),
      axis.text.y   = element_text(colour = "#6B7076", size = 12),
      legend.title  = element_blank(), legend.text = element_text(size = 12.5),
      legend.position = "top",
      plot.margin   = margin(16, 24, 12, 16)
    )
}
vir <- function(x) gsub("\\.", ",", sprintf("%.1f", x))

JOBS <- list(
  list(dir = "estudo_cei_natal", out = "cei_testlet_erro.png",
       cores = c("CEI Romualdo" = "#FA5230", "CEI Roberto Freire" = "#1FAFEF", "Brasil" = "#8C9298"),
       n_lab = "139 + 70 alunos"),
  list(dir = "estudo_marista_natal", out = "testlet_erro.png",
       cores = c("Marista Natal" = "#FA5230", "Brasil" = "#8C9298"), n_lab = "171 alunos"),
  list(dir = "estudo_dombosco_saoluis", out = "testlet_erro.png",
       cores = c("Dom Bosco" = "#FA5230", "Brasil" = "#8C9298"), n_lab = "51 alunos")
)

for (job in JOBS) {
  d <- read.csv(file.path(BASE, job$dir, "testlet.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
  br <- unique(d[, c("q_azul", "habilidade", "erro_nacional")])
  br$escola <- "Brasil"; names(br)[3] <- "erro_pct"
  d <- rbind(d[, c("escola", "q_azul", "habilidade", "erro_pct")], br[, c("escola", "q_azul", "habilidade", "erro_pct")])
  d$escola <- factor(d$escola, levels = names(job$cores))
  labs_x <- unique(d[order(d$q_azul), c("q_azul", "habilidade")])
  d$qlab <- factor(d$q_azul, levels = labs_x$q_azul,
                   labels = paste0(labs_x$q_azul, "\n", labs_x$habilidade))
  medias <- tapply(d$erro_pct, d$escola, mean)
  esc_first <- names(job$cores)[1]
  sub <- sprintf("As Q6–Q10 (Azul P1) saem da MESMA crônica. Erro médio no bloco: %s %s%% × Brasil %s%%.",
                 esc_first, vir(medias[esc_first]), vir(medias[["Brasil"]]))

  p <- ggplot(d, aes(x = qlab, y = erro_pct, fill = escola)) +
    geom_col(position = position_dodge(width = 0.78), width = 0.7) +
    geom_text(aes(label = sprintf("%.0f%%", erro_pct)),
              position = position_dodge(width = 0.78), vjust = -0.45, size = 4.1,
              fontface = "bold", colour = "#1D1D20") +
    scale_fill_manual(values = job$cores) +
    scale_y_continuous(limits = c(0, max(d$erro_pct) * 1.16), labels = function(v) paste0(v, "%")) +
    labs(title = "O testlet de Linguagens: um texto, cinco questões — quem segurou?",
         subtitle = sub,
         x = "Questão (posição no caderno Azul) · habilidade ENEM",
         y = "Taxa de erro (% dos alunos)",
         caption = sprintf("Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2025 / INEP  |  %s  |  itens localizados no caderno (cor) de cada aluno", job$n_lab)) +
    theme_xtri()
  ggsave(file.path(BASE, job$dir, "graficos", job$out), p, width = 13.33, height = 7.5, dpi = 150, bg = "#F1F1F2")
  cat("ok:", job$dir, "/", job$out, "\n")
}

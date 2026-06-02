# 🎨 PALETA POR NICHO — @glendonassis
## Configuração visual específica para Desenvolvimento Humano, Alta Performance e Mentorias

---

## NICHO PRINCIPAL: DESENVOLVIMENTO HUMANO & MENTORIAS

**Características do público:**
- Profissionais entre 28-45 anos
- Já têm conhecimento — buscam método
- Valorizam autoridade intelectual, não hype
- Desconfiam de promessas fáceis
- Tomam decisões com base em resultado comprovado

**O que o design precisa comunicar:**
- Autoridade (não é mais um)
- Seriedade sem ser entediante
- Calor humano dentro da estrutura
- Clareza acima de criatividade
- Profissionalismo que converte

---

## PALETA PRINCIPAL — @GLENDONASSIS

```css
/* PALETA GLENDON — Versão completa */
:root {
  /* Dourado — Cor da marca, símbolo de valor e direção */
  --gl-dourado:         #C9A96E;
  --gl-dourado-claro:   #E8C98A;
  --gl-dourado-escuro:  #A07840;
  --gl-dourado-suave:   #D4B484;
  
  /* Fundos escuros — Autoridade e profundidade */
  --gl-bg-dark-1:       #1A1510;   /* principal dark */
  --gl-bg-dark-2:       #221C14;   /* variação dark */
  --gl-bg-dark-3:       #2D2419;   /* alternativa dark */
  
  /* Fundos claros — Leveza e legibilidade */
  --gl-bg-light-1:      #F5EFE6;   /* principal claro */
  --gl-bg-light-2:      #EDE4D6;   /* alternativa clara */
  --gl-bg-light-3:      #E5D9C7;   /* mais saturado */
  
  /* Textos */
  --gl-texto-claro:     #F5EFE6;
  --gl-texto-escuro:    #1A1510;
  --gl-texto-apoio:     #6B5B45;
  --gl-texto-sutil:     #9A8870;
  
  /* Accent — Terracota para destaque quente */
  --gl-terracota:       #C1622A;
  --gl-terracota-vivo:  #E07A3A;
  
  /* Neutros */
  --gl-branco:          #FFFFFF;
  --gl-preto:           #0A0805;
}
```

---

## COMO USAR AS CORES POR TIPO DE SLIDE

### Capa (Slide 01)
- **Dark version:** Fundo `--gl-bg-dark-1`, título `--gl-texto-claro`, destaque `--gl-dourado`
- **Light version:** Fundo `--gl-bg-light-1`, título `--gl-texto-escuro`, destaque `--gl-terracota`

### Slides de Contexto (02-03)
- Fundo alternado: dark → light → dark (cria ritmo visual)
- Dados e números: sempre em `--gl-dourado` ou `--gl-terracota`

### Slides de Desenvolvimento (04-07)
- Estilo editorial consistente com a capa
- Blocos de destaque: fundo `--gl-dourado` com texto `--gl-preto`

### CTA Final (Slide 09)
- Sempre dark com dourado
- Máximo de texto — deixa o visual respirar

---

## COMBINAÇÕES APROVADAS

### Combinação 1 — "Autoridade Clássica" (recomendada para Análise de Tendência)
```
Fundo:    #1A1510 (dark)
Texto:    #F5EFE6 (claro)
Destaque: #C9A96E (dourado)
Handle:   #C9A96E (dourado)
```

### Combinação 2 — "Editorial Premium" (recomendada para Explicativo)
```
Fundo:    #F5EFE6 (creme)
Texto:    #1A1510 (escuro)
Destaque: #C1622A (terracota)
Handle:   #6B5B45 (apoio)
```

### Combinação 3 — "Manchete Urbana" (recomendada para Notícia)
```
Fundo:    foto com overlay #1A1510 85% opacidade
Texto:    #FFFFFF
Destaque: #C9A96E (dourado) ou #E07A3A (terracota vivo)
Handle:   #C9A96E
```

### Combinação 4 — "Dado em Destaque" (para slides de estatística)
```
Fundo:    #1A1510
Número:   #C9A96E (muito grande, 180-220px)
Texto:    #F5EFE6
Fonte:    #6B5B45 (sutil, pequeno)
```

---

## CORES A EVITAR

❌ **Azul** — não é da marca, passa sensação de tech/corporativo
❌ **Verde** — associado a saúde/sustentabilidade, não ao nicho
❌ **Rosa/roxo** — feminilidade ou espiritualidade new age
❌ **Cinza puro** — sem personalidade, parece template
❌ **Amarelo saturado** — conflita com o dourado, parece barato
❌ **Gradientes coloridos** — parece design genérico de IA

---

## SUB-NICHOS DENTRO DO POSICIONAMENTO

### Quando o tema é ALTA PERFORMANCE:
- Preferir fundos **escuros** (transmite intensidade e foco)
- Dourado mais presente (associado a excelência)
- Tipografia maior e mais impactante

### Quando o tema é CRIAÇÃO DE MENTORIAS:
- Preferir fundos **claros** (transmite clareza e acessibilidade)
- Terracota como destaque (calor humano)
- Espaço em branco generoso

### Quando o tema é POSICIONAMENTO/VENDAS:
- Contraste máximo (autoridade e convicção)
- Dados em destaque dourado
- Texto direto, sem ornamentos

### Quando o tema é MÉTODO/SISTEMA:
- Combinação editorial (creme + escuro)
- Numeração visível nos slides
- Layout organizado que demonstra ordem e clareza

---

## FONTES ALTERNATIVAS (se Sequel Sans não disponível)

**Opção 1 — Playfair Display** (Google Fonts — gratuita)
- Para headlines: Playfair Display 900
- Para subtítulos: Playfair Display 700
- Para corpo: Playfair Display 400

**Opção 2 — Cormorant Garamond** (Google Fonts — gratuita)
- Mais elegante, levemente mais delicada
- Boa para versões light dos slides

**Opção 3 — Libre Baskerville** (Google Fonts — gratuita)
- Mais sólida e séria
- Boa para slides de dados e análise

**Nunca use:** Inter, Roboto, Helvetica, Arial, Montserrat nos slides principais
(podem aparecer em tags pequenas e secundárias com moderação)

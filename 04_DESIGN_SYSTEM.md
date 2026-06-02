# 🎨 DESIGN SYSTEM — @glendonassis
## CSS profissional com 4 estilos visuais. 1080×1350px para Instagram.

---

## IDENTIDADE VISUAL

**Logo:** Rosa dos ventos com nó céltico no centro — simboliza direção, método e tradição.
**Conceito visual:** Autoridade clássica com clareza moderna. Não é minimalismo vazio nem maximalism poluído.

---

## PALETA DE CORES

```css
:root {
  /* Cores Primárias */
  --dourado:        #C9A96E;  /* cor principal da marca */
  --dourado-claro:  #E8C98A;  /* destaques e hovers */
  --dourado-escuro: #A07840;  /* bordas e sombras */
  
  /* Backgrounds */
  --bg-escuro:      #1A1510;  /* fundo dark principal */
  --bg-medio:       #2A2018;  /* fundo dark secundário */
  --bg-claro:       #F5EFE6;  /* fundo light principal */
  --bg-creme:       #EDE4D6;  /* fundo light secundário */
  
  /* Texto */
  --texto-claro:    #F5EFE6;  /* texto em fundo escuro */
  --texto-escuro:   #1A1510;  /* texto em fundo claro */
  --texto-medio:    #6B5B45;  /* texto secundário */
  
  /* Accent */
  --terracota:      #C1622A;  /* destaque quente */
  --terracota-claro:#E07A3A;  /* variação mais viva */
  
  /* Utilitários */
  --branco:         #FFFFFF;
  --preto:          #0A0805;
}
```

---

## TIPOGRAFIA

**Fonte Principal:** Sequel Sans (quando disponível)
**Fallback Stack:** 'Playfair Display', 'Cormorant Garamond', Georgia, serif

```css
/* Hierarquia tipográfica */
.headline-capa {
  font-family: 'Sequel Sans', 'Playfair Display', Georgia, serif;
  font-size: 72px;
  font-weight: 900;
  line-height: 1.0;
  letter-spacing: -2px;
  text-transform: uppercase;
}

.subtitulo {
  font-family: 'Sequel Sans', 'Playfair Display', Georgia, serif;
  font-size: 32px;
  font-weight: 600;
  line-height: 1.2;
  letter-spacing: -0.5px;
}

.tag-editoria {
  font-family: 'Sequel Sans', Georgia, serif;
  font-size: 18px;
  font-weight: 400;
  letter-spacing: 4px;
  text-transform: uppercase;
}

.body-texto {
  font-family: 'Sequel Sans', 'Cormorant Garamond', Georgia, serif;
  font-size: 36px;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0;
}

.numero-slide {
  font-family: 'Sequel Sans', Georgia, serif;
  font-size: 120px;
  font-weight: 900;
  opacity: 0.08;
}
```

---

## 4 ESTILOS VISUAIS

### ESTILO A — "MAGAZINE DARK" (Análise de Tendência)
Fundo escuro, dourado como destaque, estética editorial premium.

```css
.slide-magazine-dark {
  width: 1080px;
  height: 1350px;
  background: var(--bg-escuro);
  position: relative;
  overflow: hidden;
  font-family: 'Sequel Sans', Georgia, serif;
}

.slide-magazine-dark .linha-topo {
  position: absolute;
  top: 60px;
  left: 60px;
  right: 60px;
  height: 2px;
  background: var(--dourado);
}

.slide-magazine-dark .tag {
  color: var(--dourado);
  font-size: 16px;
  letter-spacing: 5px;
  text-transform: uppercase;
  margin-top: 80px;
  margin-left: 60px;
}

.slide-magazine-dark .headline {
  color: var(--texto-claro);
  font-size: 72px;
  font-weight: 900;
  line-height: 1.0;
  text-transform: uppercase;
  padding: 0 60px;
  margin-top: 40px;
}

.slide-magazine-dark .headline span.destaque {
  color: var(--dourado);
}

.slide-magazine-dark .subtexto {
  color: var(--texto-claro);
  opacity: 0.7;
  font-size: 32px;
  line-height: 1.5;
  padding: 0 60px;
  margin-top: 40px;
}

.slide-magazine-dark .handle {
  position: absolute;
  bottom: 50px;
  left: 60px;
  color: var(--dourado);
  font-size: 20px;
  letter-spacing: 2px;
}

.slide-magazine-dark .linha-base {
  position: absolute;
  bottom: 80px;
  left: 60px;
  right: 60px;
  height: 1px;
  background: var(--dourado);
  opacity: 0.4;
}
```

---

### ESTILO B — "EDITORIAL CLARO" (Carrossel Explicativo)
Fundo creme, texto escuro, dourado como accent. Sensação de documento oficial.

```css
.slide-editorial-claro {
  width: 1080px;
  height: 1350px;
  background: var(--bg-claro);
  position: relative;
  overflow: hidden;
  font-family: 'Sequel Sans', Georgia, serif;
}

.slide-editorial-claro .barra-lateral {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 8px;
  background: var(--dourado);
}

.slide-editorial-claro .numero-secao {
  position: absolute;
  top: 60px;
  right: 60px;
  font-size: 120px;
  font-weight: 900;
  color: var(--dourado);
  opacity: 0.12;
  line-height: 1;
}

.slide-editorial-claro .tag {
  color: var(--texto-medio);
  font-size: 14px;
  letter-spacing: 5px;
  text-transform: uppercase;
  margin-top: 80px;
  margin-left: 80px;
}

.slide-editorial-claro .titulo {
  color: var(--texto-escuro);
  font-size: 64px;
  font-weight: 900;
  line-height: 1.05;
  text-transform: uppercase;
  padding: 0 80px;
  margin-top: 30px;
}

.slide-editorial-claro .titulo span.destaque {
  color: var(--terracota);
}

.slide-editorial-claro .corpo {
  color: var(--texto-escuro);
  font-size: 34px;
  line-height: 1.55;
  padding: 0 80px;
  margin-top: 50px;
}

.slide-editorial-claro .handle {
  position: absolute;
  bottom: 50px;
  right: 60px;
  color: var(--texto-medio);
  font-size: 18px;
  letter-spacing: 2px;
}
```

---

### ESTILO C — "NOTÍCIA URBANA" (Slide Único de Notícia)
Fundo escuro com foto, texto impactante sobre imagem, estética de manchete.

```css
.slide-noticia {
  width: 1080px;
  height: 1350px;
  position: relative;
  overflow: hidden;
  font-family: 'Sequel Sans', Georgia, serif;
}

.slide-noticia .foto-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  filter: brightness(0.4);
}

.slide-noticia .overlay-gradiente {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    transparent 30%,
    rgba(10, 8, 5, 0.9) 100%
  );
}

.slide-noticia .handle {
  position: absolute;
  top: 50px;
  left: 60px;
  color: var(--dourado);
  font-size: 20px;
  letter-spacing: 2px;
  z-index: 2;
}

.slide-noticia .manchete {
  position: absolute;
  bottom: 120px;
  left: 60px;
  right: 60px;
  z-index: 2;
}

.slide-noticia .manchete .linha-topo {
  width: 60px;
  height: 4px;
  background: var(--terracota);
  margin-bottom: 20px;
}

.slide-noticia .manchete .titulo {
  color: var(--branco);
  font-size: 68px;
  font-weight: 900;
  line-height: 1.0;
  text-transform: uppercase;
}

.slide-noticia .manchete .titulo span.destaque {
  color: var(--dourado);
}
```

---

### ESTILO D — "CONTRASTE BOLD" (Slides de Dados/Estatísticas)
Alto contraste, número grande, informação visual poderosa.

```css
.slide-contraste {
  width: 1080px;
  height: 1350px;
  background: var(--bg-escuro);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: 80px;
  position: relative;
  font-family: 'Sequel Sans', Georgia, serif;
}

.slide-contraste .numero-grande {
  font-size: 200px;
  font-weight: 900;
  color: var(--dourado);
  line-height: 0.85;
  margin-bottom: 30px;
}

.slide-contraste .contexto {
  font-size: 40px;
  color: var(--texto-claro);
  line-height: 1.4;
  max-width: 900px;
}

.slide-contraste .fonte {
  position: absolute;
  bottom: 50px;
  left: 80px;
  font-size: 18px;
  color: var(--texto-claro);
  opacity: 0.4;
  letter-spacing: 1px;
}
```

---

## TEMPLATE HTML COMPLETO — SLIDE PADRÃO

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&display=swap');
  
  * { margin: 0; padding: 0; box-sizing: border-box; }
  
  :root {
    --dourado: #C9A96E;
    --dourado-claro: #E8C98A;
    --bg-escuro: #1A1510;
    --bg-claro: #F5EFE6;
    --texto-claro: #F5EFE6;
    --texto-escuro: #1A1510;
    --texto-medio: #6B5B45;
    --terracota: #C1622A;
  }
  
  .slide {
    width: 1080px;
    height: 1350px;
    /* aplicar estilo A, B, C ou D aqui */
  }
</style>
</head>
<body>
  <div class="slide slide-magazine-dark">
    <!-- conteúdo do slide aqui -->
  </div>
</body>
</html>
```

---

## REGRAS DE DESIGN

1. **Nunca use mais de 3 cores por slide** (fundo + texto + accent)
2. **O dourado é sagrado** — só vai em headlines, destaques e handle
3. **Margens mínimas:** 60px nas laterais, 50px no topo e base
4. **Handle sempre presente:** @glendonassis em todos os slides
5. **Linha decorativa:** Use linhas finas douradas para separar seções
6. **Nunca centralize o texto** — alinhamento à esquerda cria autoridade editorial
7. **Número do slide:** visível mas discreto (opacidade 8-12%)

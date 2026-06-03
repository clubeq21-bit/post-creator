#!/usr/bin/env python3
"""
POST CREATOR v2 — @glendonassis
Sistema completo de criação e exportação de carrosséis de Instagram
"""

import sys, subprocess, os, json, webbrowser, threading, time, re
from pathlib import Path

WORKSPACE = Path(__file__).parent
PORT = 5151

# ─── AUTO-INSTALL ──────────────────────────────────────────────────────────────

def instalar():
    precisa_reiniciar = False
    print("\n⚙️  Verificando dependências...")
    for pkg in ['flask', 'playwright']:
        try:
            __import__(pkg); print(f"  ✓ {pkg}")
        except ImportError:
            print(f"  → Instalando {pkg}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])
            print(f"  ✓ {pkg} instalado")
            precisa_reiniciar = True
    if precisa_reiniciar:
        print("\n🔄 Reiniciando...\n")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(); b.close()
        print("  ✓ Chromium")
    except Exception:
        print("  → Baixando Chromium (~150MB, só uma vez)...")
        subprocess.check_call([sys.executable, '-m', 'playwright', 'install', 'chromium'])
        print("  ✓ Chromium instalado")
    print("\n✅ Pronto!\n")

instalar()
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# ─── TEMPLATES DE CARROSSEL ────────────────────────────────────────────────────

TEMPLATES = {
    "explicativo": {
        "label": "Explicativo",
        "desc": "Ensina um conceito com dados, virada e aplicação prática.",
        "icon": "📖",
        "slides": [
            {"num":1,"type":"capa",    "tag":"","headline":"SUA HEADLINE AQUI\nSUBTÍTULO FORTE\nNESSA LINHA.","bloco1":"Frase de apoio que ancora o leitor.","bloco2":"O ponto principal que você vai provar."},
            {"num":2,"type":"contexto","tag":"O Problema","headline":"O CENÁRIO\nQUE TODO MUNDO\nVIVE.","bloco1":"Item 1 do contexto\nItem 2 do contexto\nItem 3 do contexto\nItem 4 do contexto","bloco2":"A frase que sintetiza o problema."},
            {"num":3,"type":"dados",   "tag":"Os Dados","headline":"XX%","bloco1":"Contexto do dado principal aqui — o que ele significa.","bloco2":"YY% — segundo dado que complementa o argumento.\nFrase de impacto sobre o segundo dado.","extra":"Fonte: Nome da Fonte · Ano"},
            {"num":4,"type":"virada",  "tag":"A Virada","headline":"O QUE TODO\nMUNDO PENSA\nQUE É VERDADE.\nNÃO É.","bloco1":"A crença comum que precisa ser questionada.","bloco2":"O mecanismo real que explica por quê funciona diferente."},
            {"num":5,"type":"dois_col","tag":"O Contraste","headline":"Dois caminhos.\nSó um\nfunciona.","bloco1":"✕ O CAMINHO COMUM\nItem errado 1\nItem errado 2\nItem errado 3\nItem errado 4","bloco2":"✓ O CAMINHO CERTO\nItem certo 1\nItem certo 2\nItem certo 3\nItem certo 4"},
            {"num":6,"type":"cenarios","tag":"Na Prática","headline":"A DIFERENÇA\nESTÁ\nNOS DETALHES.","bloco1":"CENÁRIO A — Sem o método\nDescrição do que acontece sem o método.\nResultado medíocre.","bloco2":"CENÁRIO B — Com o método\nDescrição do que acontece com o método.\nResultado concreto.","extra":"A diferença não é talento. É SISTEMA."},
            {"num":7,"type":"sintese", "tag":"O Padrão","headline":"O padrão que\ntodos os casos\nde sucesso\ntêm em comum.","bloco1":"Passo 1 → Passo 2 → Passo 3 → Resultado","bloco2":"Você estava fazendo em ordem errada.\nO sistema não perdoa."},
            {"num":8,"type":"aplicacao","tag":"Como Aplicar","headline":"Mude\numa coisa\nAGORA.","bloco1":"PARE DE FAZER: A coisa errada\nCOMECE A FAZER: A coisa certa","bloco2":"Ação 1 concreta\nAção 2 concreta\nAção 3 concreta — o resultado vai aparecer."},
            {"num":9,"type":"cta",     "tag":"Ação","headline":"Salva\nesse\nCARROSSEL.","bloco1":"Você vai precisar dele quando errar novamente.","bloco2":"Quer aplicar isso na sua mentoria? Manda \"MÉTODO\" no meu direct."},
        ]
    },
    "lista": {
        "label": "Lista Numerada",
        "desc": "Formato direto com itens numerados. Ideal para erros, dicas ou passos.",
        "icon": "🔢",
        "slides": [
            {"num":1,"type":"capa",    "tag":"","headline":"X ERROS QUE\n[PERFIL DO LEITOR]\nCOMETE\nSEM SABER.","bloco1":"E o número X vai te surpreender.","bloco2":""},
            {"num":2,"type":"contexto","tag":"Por Que Isso Importa","headline":"A MAIORIA\nNEM PERCEBE\nQUE ESTÁ\nERRANDO.","bloco1":"Contexto geral do problema.\nO que está em jogo.\nPor que vale a pena ler até o final.","bloco2":"Esses erros custam [resultado negativo concreto]."},
            {"num":3,"type":"dados",   "tag":"Erro 01","headline":"ERRO #1","bloco1":"Nome do primeiro erro — em destaque.","bloco2":"Explicação do erro: o que é, por que acontece, como se manifesta na prática.","extra":"Por que esse erro é mais comum do que parece"},
            {"num":4,"type":"virada",  "tag":"Erro 02","headline":"ERRO #2\nTALVEZ\nO MAIS\nPERIGOSO.","bloco1":"Nome do segundo erro.","bloco2":"Por que esse é o mais perigoso: ele parece certo na superfície, mas sabota por baixo."},
            {"num":5,"type":"dois_col","tag":"Erro 03 vs Solução","headline":"Erro 03.\nE como\nresolve.","bloco1":"✕ O ERRO\nComo o erro aparece\nO que parece na superfície\nO que acontece na prática","bloco2":"✓ A SOLUÇÃO\nA mudança de perspectiva\nO que fazer diferente\nO resultado esperado"},
            {"num":6,"type":"cenarios","tag":"Erro 04","headline":"ERRO #4\nQUE NINGUÉM\nFALA\nABERTAMENTE.","bloco1":"ANTES DE CORRIGIR\nComo a situação fica quando você comete esse erro.\nResultado frustrante.","bloco2":"DEPOIS DE CORRIGIR\nComo fica depois que você resolve.\nResultado concreto.","extra":"A diferença é uma decisão, não um talento."},
            {"num":7,"type":"sintese", "tag":"Erro 05","headline":"Erro #5.\nO mais\ncomum de\ntodos.","bloco1":"Nome → Causa → Consequência → Solução","bloco2":"Quando você para de cometer esse erro, tudo muda."},
            {"num":8,"type":"aplicacao","tag":"O Diagnóstico","headline":"Você\ncomete\nquantos?","bloco1":"PARE DE FAZER: Os 5 erros listados\nCOMECE A FAZER: O oposto de cada um","bloco2":"1-2 erros: você está no caminho certo\n3-4 erros: precisa de ajuste\n5 erros: você precisa reiniciar a estratégia."},
            {"num":9,"type":"cta",     "tag":"Ação","headline":"Salva\nessa\nLISTA.","bloco1":"Manda para alguém que comete esses erros sem perceber.","bloco2":"Quer resolver os seus erros com método? Manda \"ERROS\" no meu direct."},
        ]
    },
    "storytelling": {
        "label": "Storytelling / Case",
        "desc": "Conta uma história ou caso real com início, conflito e resultado.",
        "icon": "📖",
        "slides": [
            {"num":1,"type":"capa",    "tag":"","headline":"ELE COMEÇOU\nDO ZERO.\n[RESULTADO]\nEM [TEMPO].","bloco1":"E a virada veio de uma mudança que ninguém esperava.","bloco2":""},
            {"num":2,"type":"contexto","tag":"O Começo","headline":"O PONTO DE\nPARTIDA ERA\nDESANIMADOR.","bloco1":"Situação inicial do personagem\nO que ele tinha\nO que ele não tinha\nO que ele achava que precisava","bloco2":"Mas havia um problema que ninguém via ainda."},
            {"num":3,"type":"dados",   "tag":"O Problema","headline":"X MESES\nSEM RESULTADO.","bloco1":"O que estava acontecendo em números — a frustração documentada.","bloco2":"Ele tentou tudo que a maioria tenta.\nNenhuma funcionou pelo motivo que você imagina.","extra":"O problema real nunca era o que parecia ser"},
            {"num":4,"type":"virada",  "tag":"A Virada","headline":"UM DIA\nELE PAROU\nE FEZ UMA\nPERGUNTA.","bloco1":"Qual era a pergunta que mudou tudo?","bloco2":"A resposta não estava onde ele procurava.\nEstava em um lugar óbvio que ele ignorava."},
            {"num":5,"type":"dois_col","tag":"Antes e Depois","headline":"O que\nmudou na\nprática.","bloco1":"✕ O QUE ELE FAZIA ANTES\nAção errada 1\nAção errada 2\nAção errada 3\nMentalidade anterior","bloco2":"✓ O QUE ELE FEZ DEPOIS\nNova ação 1\nNova ação 2\nNova ação 3\nNova mentalidade"},
            {"num":6,"type":"cenarios","tag":"O Processo","headline":"NÃO FOI\nDO DIA\nPARA\nA NOITE.","bloco1":"MÊS 1-2 — A fase difícil\nO que aconteceu. O que ele sentiu. Por que quase desistiu.","bloco2":"MÊS 3-6 — A aceleração\nQuando o método começou a funcionar. Os primeiros resultados reais.","extra":"O momento em que tudo clicou foi silencioso."},
            {"num":7,"type":"sintese", "tag":"O Resultado","headline":"[RESULTADO\nCONCRETO]\nem [TEMPO].","bloco1":"Dado → Prova → Validação → Próximo passo","bloco2":"O número não é o mais importante.\nO que mudou por dentro foi o que gerou o número."},
            {"num":8,"type":"aplicacao","tag":"A Lição","headline":"O que\nvocê pode\naplicar\nAGORA.","bloco1":"PARE DE ESPERAR: A condição perfeita\nCOMECE COM: O que você tem hoje","bloco2":"Passo 1: Identifique seu ponto de virada\nPasso 2: Aplique o método, não a motivação\nPasso 3: Documente o processo — o resultado vem depois."},
            {"num":9,"type":"cta",     "tag":"Ação","headline":"Você tem\numa história\nassim?\nCONTA.","bloco1":"Comenta ou manda mensagem — quero saber onde você está.","bloco2":"Se você quer construir o seu case do zero, manda \"CASE\" no meu direct."},
        ]
    },
    "comparativo": {
        "label": "Comparativo A vs B",
        "desc": "Contrasta dois perfis, abordagens ou caminhos. Forte para posicionamento.",
        "icon": "⚖️",
        "slides": [
            {"num":1,"type":"capa",    "tag":"","headline":"A DIFERENÇA\nENTRE [A]\nE [B] É\nESTA.","bloco1":"E ela define quem vai ter resultado — e quem não vai.","bloco2":""},
            {"num":2,"type":"contexto","tag":"O Que Todo Mundo Vê","headline":"NA SUPERFÍCIE,\nELES PARECEM\nIGUAIS.","bloco1":"Ambos têm o mesmo produto\nAmbos têm o mesmo conteúdo\nAmbos têm o mesmo tempo de mercado\nAmbos estão trabalhando muito","bloco2":"Mas os resultados são completamente diferentes."},
            {"num":3,"type":"dados",   "tag":"Os Números","headline":"3X","bloco1":"É a diferença média de resultado entre os dois perfis. Medida em [métrica].","bloco2":"Não é sorte. Não é talento. Não é audiência.\nÉ uma escolha que um faz e o outro não.","extra":"Fonte: Observação direta de X casos reais"},
            {"num":4,"type":"virada",  "tag":"A Diferença Real","headline":"NÃO É O\nQUE VOCÊ\nPENSA\nQUE É.","bloco1":"A maioria acha que a diferença está em [resposta óbvia].","bloco2":"A diferença real está em [resposta contraintuitiva].\nE isso muda tudo sobre o que você deveria estar fazendo."},
            {"num":5,"type":"dois_col","tag":"Os Dois Perfis","headline":"Perfil A\nvs\nPerfil B.","bloco1":"✕ PERFIL A — O resultado médio\nCaracterística 1\nCaracterística 2\nCaracterística 3\nCaracterística 4","bloco2":"✓ PERFIL B — O resultado excepcional\nCaracterística 1\nCaracterística 2\nCaracterística 3\nCaracterística 4"},
            {"num":6,"type":"cenarios","tag":"Na Prática","headline":"O MESMO\nDIA. DUAS\nDECISÕES\nDIFERENTES.","bloco1":"PERFIL A — Como age diante de [situação]\nO que pensa. O que decide. O que acontece como resultado.","bloco2":"PERFIL B — Como age diante da mesma situação\nO que pensa. O que decide. O resultado completamente diferente.","extra":"A situação é a mesma. O sistema é diferente."},
            {"num":7,"type":"sintese", "tag":"O Padrão","headline":"O Perfil B\nsempre faz\numa coisa\nque o A não faz.","bloco1":"Hábito → Decisão → Comportamento → Resultado","bloco2":"Não é disciplina. Não é motivação.\nÉ um sistema que o Perfil B construiu."},
            {"num":8,"type":"aplicacao","tag":"Qual Você É?","headline":"Você é\no Perfil A\nou o\nPerfil B?","bloco1":"PARE DE SER PERFIL A: O comportamento a abandonar\nCOMECE A SER PERFIL B: O comportamento a adotar","bloco2":"Teste 1: Como você age diante de [situação 1]?\nTeste 2: Como você age diante de [situação 2]?\nA resposta honesta define o seu perfil agora."},
            {"num":9,"type":"cta",     "tag":"Ação","headline":"Salva\nesse\nCARROSSEL.","bloco1":"Você vai lembrar dele quando perceber que está agindo como Perfil A.","bloco2":"Quer virar Perfil B com método? Manda \"PERFIL\" no meu direct."},
        ]
    }
}

DEFAULT_SIZES = {
    'capa':      {'headline': 74,  'bloco1': 30, 'bloco2': 30},
    'contexto':  {'headline': 60,  'bloco1': 31, 'bloco2': 32},
    'dados':     {'headline': 180, 'bloco1': 34, 'bloco2': 120},
    'virada':    {'headline': 60,  'bloco1': 33, 'bloco2': 33},
    'dois_col':  {'headline': 54,  'bloco1': 25, 'bloco2': 25},
    'cenarios':  {'headline': 60,  'bloco1': 27, 'bloco2': 27},
    'sintese':   {'headline': 58,  'bloco1': 19, 'bloco2': 30},
    'aplicacao': {'headline': 70,  'bloco1': 26, 'bloco2': 25},
    'cta':       {'headline': 80,  'bloco1': 27, 'bloco2': 29},
}

def make_slide(s):
    sl = dict(s)
    if 'sizes' not in sl:
        sl['sizes'] = dict(DEFAULT_SIZES.get(s.get('type','capa'), {'headline':60,'bloco1':30,'bloco2':30}))
    if 'el_colors' not in sl:
        sl['el_colors'] = {'headline':'', 'bloco1':'', 'bloco2':''}
    return sl

GOOGLE_FONTS = {
    "playfair": {
        "label": "Playfair Display",
        "desc": "Autoridade clássica. Tom editorial premium.",
        "url": "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&display=swap",
        "family": "'Playfair Display', Georgia, serif"
    },
    "cormorant": {
        "label": "Cormorant Garamond",
        "desc": "Elegante e sofisticada. Tom literário.",
        "url": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&display=swap",
        "family": "'Cormorant Garamond', Georgia, serif"
    },
    "dm_serif": {
        "label": "DM Serif Display",
        "desc": "Moderna e impactante. Tom de revista contemporânea.",
        "url": "https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&display=swap",
        "family": "'DM Serif Display', Georgia, serif"
    },
    "libre": {
        "label": "Libre Baskerville",
        "desc": "Sólida e séria. Tom acadêmico com autoridade.",
        "url": "https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap",
        "family": "'Libre Baskerville', Georgia, serif"
    }
}

# ─── STATE ─────────────────────────────────────────────────────────────────────

STATE = {
    "template": "explicativo",
    "font": "playfair",
    "nome": "meu-carrossel",
    "colors": {
        "bg": "#1A1510", "text": "#F5EFE6",
        "accent": "#C9A96E", "accent2": "#C1622A",
        "handle": "@glendonassis"
    },
    "slides": [make_slide(s) for s in TEMPLATES["explicativo"]["slides"]]
}

# ─── SLIDE RENDERERS ───────────────────────────────────────────────────────────

def slide_css(c, font_key):
    f = GOOGLE_FONTS.get(font_key, GOOGLE_FONTS["playfair"])
    return f"""
    @import url('{f["url"]}');
    *{{margin:0;padding:0;box-sizing:border-box}}
    :root{{--bg:{c['bg']};--text:{c['text']};--accent:{c['accent']};--accent2:{c['accent2']};
          --muted:rgba(245,239,230,0.45);--border:rgba(201,169,110,0.2);--font:{f["family"]}}}
    body{{width:1080px;height:1350px;overflow:hidden;background:var(--bg);font-family:var(--font)}}
    .slide{{width:1080px;height:1350px;background:var(--bg);position:relative;overflow:hidden}}
    .lt{{position:absolute;top:55px;left:60px;right:60px;height:1.5px;
         background:linear-gradient(to right,var(--accent),rgba(201,169,110,0.15))}}
    .lb{{position:absolute;bottom:100px;left:60px;right:60px;height:1px;background:var(--border)}}
    .tag{{position:absolute;top:75px;left:60px;color:var(--accent);font-size:15px;
          font-weight:400;letter-spacing:6px;text-transform:uppercase}}
    .handle{{position:absolute;bottom:62px;left:60px;color:var(--accent);font-size:19px;
             font-weight:400;letter-spacing:3px}}
    .snum{{position:absolute;bottom:65px;right:60px;color:rgba(154,136,112,0.55);
           font-size:14px;letter-spacing:3px;text-transform:uppercase}}
    .acento{{width:48px;height:3px;background:var(--accent2);margin-bottom:30px}}
    """

def wrap(content, c, s, font_key):
    n, total = s['num'], len(STATE['slides'])
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
    <style>{slide_css(c, font_key)}</style></head><body>
    <div class="slide">
      <div class="lt"></div><div class="tag">{s.get('tag','')}</div>
      {content}
      <div class="lb"></div>
      <div class="handle">{c['handle']}</div>
      <div class="snum">{str(n).zfill(2)} / {str(total).zfill(2)}</div>
    </div></body></html>"""

def hl(text, accent_last=True):
    """Converte texto com \n em <br>, última linha em destaque"""
    lines = text.split('\n')
    if accent_last and lines:
        html = '<br>'.join(lines[:-1])
        last = lines[-1]
        if html: html += f'<br><span style="color:var(--accent)">{last}</span>'
        else: html = f'<span style="color:var(--accent)">{last}</span>'
    else:
        html = '<br>'.join(lines)
    return html

def br(text): return '<br>'.join(text.split('\n'))

def sz(s, el, default):
    """Retorna tamanho configurado para o elemento, ou o default."""
    return s.get('sizes', {}).get(el, 0) or default

def ec(s, el, fallback):
    """Retorna cor configurada para o elemento, ou fallback CSS."""
    v = s.get('el_colors', {}).get(el, '')
    return v if v else fallback

def dados_hl_default(s):
    """Calcula tamanho padrão do headline do slide Dados baseado no conteúdo."""
    stored = s.get('sizes', {}).get('headline', 0)
    if stored: return stored
    hl = s.get('headline', '')
    lines = [l for l in hl.split('\n') if l.strip()]
    maxlen = max((len(l) for l in lines), default=1)
    n = len(lines)
    if n == 1 and maxlen <= 4:  return 200
    if n == 1 and maxlen <= 8:  return 130
    if n <= 2 and maxlen <= 12: return 90
    return 66

def render_capa(s, c, fk):
    hs = sz(s,'headline',74); b1s = sz(s,'bloco1',30); b2s = sz(s,'bloco2',30)
    hc = ec(s,'headline','var(--text)'); b1c = ec(s,'bloco1','var(--text)'); b2c = ec(s,'bloco2','var(--accent)')
    return wrap(f"""
    <div style="position:absolute;top:160px;left:60px;right:60px">
      <div class="acento"></div>
      <h1 style="font-size:{hs}px;font-weight:900;line-height:0.95;letter-spacing:-2px;
                 text-transform:uppercase;color:{hc}">{hl(s.get('headline',''))}</h1>
      <div style="width:100%;height:1px;background:var(--border);margin:48px 0"></div>
      <p style="font-size:{b1s}px;font-style:italic;line-height:1.5;color:{b1c};opacity:0.78">{br(s.get('bloco1',''))}</p>
      {"<p style='font-size:"+str(b2s)+"px;font-weight:700;line-height:1.5;color:"+b2c+";margin-top:14px'>" + br(s.get('bloco2','')) + "</p>" if s.get('bloco2') else ""}
    </div>""", c, s, fk)

def render_contexto(s, c, fk):
    hs = sz(s,'headline',60); b1s = sz(s,'bloco1',31); b2s = sz(s,'bloco2',32)
    hc = ec(s,'headline','var(--text)'); b1c = ec(s,'bloco1','var(--text)'); b2c = ec(s,'bloco2','var(--accent)')
    itens = [i for i in s.get('bloco1','').split('\n') if i.strip()]
    ihtml = ''.join([f"""<div style="display:flex;align-items:flex-start;gap:16px;margin-bottom:22px">
      <div style="width:5px;height:5px;border-radius:50%;background:var(--accent);margin-top:15px;flex-shrink:0"></div>
      <span style="font-size:{b1s}px;font-weight:400;color:{b1c};opacity:0.8;line-height:1.35">{i}</span>
      </div>""" for i in itens])
    return wrap(f"""
    <div style="position:absolute;top:155px;left:60px;right:60px">
      <div class="acento"></div>
      <h2 style="font-size:{hs}px;font-weight:900;line-height:1.0;letter-spacing:-1.5px;
                 text-transform:uppercase;color:{hc}">{hl(s.get('headline',''))}</h2>
    </div>
    <div style="position:absolute;top:490px;left:60px;right:60px">{ihtml}</div>
    <div style="position:absolute;bottom:128px;left:60px;right:60px;
                border-top:1px solid var(--border);padding-top:32px">
      <p style="font-size:{b2s}px;font-weight:700;font-style:italic;line-height:1.4;color:{b2c}">{br(s.get('bloco2',''))}</p>
    </div>""", c, s, fk)

def render_dados(s, c, fk):
    hs = dados_hl_default(s); b1s = sz(s,'bloco1',34); b2s = sz(s,'bloco2',120)
    hc = ec(s,'headline','var(--accent)'); b1c = ec(s,'bloco1','var(--text)'); b2c = ec(s,'bloco2','var(--accent2)')
    b2 = s.get('bloco2','').split('\n')
    num2, ctx2 = (b2[0], '\n'.join(b2[1:])) if b2 else ('','')
    # Ajuste de letter-spacing e line-height baseado no tamanho
    hl_ls = max(-6, int(-6 * hs / 200))
    ctx2_fs = max(22, b1s - 3)
    return wrap(f"""
    <div style="position:absolute;top:148px;left:60px;right:60px">
      <div style="font-size:{hs}px;font-weight:900;color:{hc};line-height:0.9;letter-spacing:{hl_ls}px">{br(s.get('headline',''))}</div>
      <p style="margin-top:18px;font-size:{b1s}px;font-weight:400;line-height:1.4;color:{b1c}">{s.get('bloco1','')}</p>
    </div>
    <div style="position:absolute;top:636px;left:60px;right:60px;height:1px;background:var(--border)"></div>
    <div style="position:absolute;top:672px;left:60px;right:60px">
      <div style="font-size:{b2s}px;font-weight:900;color:{b2c};line-height:0.9;letter-spacing:{max(-3,int(-3*b2s/120))}px">{num2}</div>
      <p style="margin-top:14px;font-size:{ctx2_fs}px;font-weight:400;line-height:1.45;color:var(--text)">{br(ctx2)}</p>
    </div>
    <div style="position:absolute;bottom:118px;left:60px;font-size:14px;
                color:rgba(154,136,112,0.65);letter-spacing:2px;text-transform:uppercase">{s.get('extra','')}</div>
    """, c, s, fk)

def render_virada(s, c, fk):
    hs = sz(s,'headline',60); b1s = sz(s,'bloco1',33); b2s = sz(s,'bloco2',33)
    hc_default = ec(s,'headline','var(--text)'); b1c = ec(s,'bloco1','var(--text)'); b2c = ec(s,'bloco2','var(--text)')
    hlines = s.get('headline','').split('\n')
    hhtml = ''
    for l in hlines:
        if hc_default != 'var(--text)':
            col = hc_default
        else:
            col = 'var(--accent)' if l.isupper() and any(x in l for x in ['VERDADE','NÃO','NUNCA','SEMPRE','CONSEQUÊNCIA','ALAVANCA','PERIGOSO']) else 'var(--accent2)' if any(x in l for x in ['NÃO','NUNCA','FALSO','ERRADO']) else 'var(--text)'
        hhtml += f'<span style="color:{col}">{l}</span><br>'
    b2_fmt = re.sub(r'\b(VOLUME|MÉTODO|SISTEMA|PROCESSO)\b', r'<strong style="color:var(--accent)">\1</strong>', s.get('bloco2',''))
    return wrap(f"""
    <div style="position:absolute;left:0;top:0;bottom:0;width:5px;
                background:linear-gradient(to bottom,var(--accent),transparent)"></div>
    <div style="position:absolute;top:148px;left:60px;right:60px">
      <div style="font-size:16px;font-style:italic;color:var(--accent);letter-spacing:1px;margin-bottom:22px">O que a maioria não percebe:</div>
      <h2 style="font-size:{hs}px;font-weight:900;line-height:1.0;letter-spacing:-1.5px;
                 text-transform:uppercase">{hhtml}</h2>
    </div>
    <div style="position:absolute;top:600px;left:60px;right:60px;border-top:1px solid var(--border);padding-top:38px">
      <p style="font-size:{b1s}px;font-weight:400;line-height:1.5;color:{b1c};opacity:0.85;margin-bottom:24px">{br(s.get('bloco1',''))}</p>
      <p style="font-size:{b2s}px;font-weight:400;line-height:1.5;color:{b2c};opacity:0.85">{b2_fmt}</p>
    </div>""", c, s, fk)

def render_dois_col(s, c, fk):
    hs = sz(s,'headline',54); b1s = sz(s,'bloco1',25); b2s = sz(s,'bloco2',25)
    hc = ec(s,'headline','var(--text)'); b1c = ec(s,'bloco1','var(--text)'); b2c = ec(s,'bloco2','var(--text)')
    c1 = s.get('bloco1','').split('\n'); c2 = s.get('bloco2','').split('\n')
    t1, i1 = (c1[0], c1[1:]) if c1 else ('', [])
    t2, i2 = (c2[0], c2[1:]) if c2 else ('', [])
    def items(lst, clr, fsize, fcolor):
        return ''.join([f'<div style="font-size:{fsize}px;color:{fcolor};padding:12px 14px;border-left:2px solid {clr};margin-bottom:12px;line-height:1.3">{x}</div>' for x in lst if x.strip()])
    return wrap(f"""
    <div style="position:absolute;top:148px;left:60px;right:60px">
      <h2 style="font-size:{hs}px;font-weight:900;line-height:1.0;letter-spacing:-1px;
                 text-transform:uppercase;color:{hc}">{hl(s.get('headline',''))}</h2>
      <div style="width:100%;height:1px;background:var(--border);margin:26px 0"></div>
    </div>
    <div style="position:absolute;top:368px;left:60px;right:60px;display:flex;gap:22px;bottom:115px">
      <div style="flex:1;padding:26px 24px;background:rgba(193,98,42,0.07);border:1px solid rgba(193,98,42,0.25);border-top:3px solid var(--accent2)">
        <div style="font-size:12px;letter-spacing:4px;text-transform:uppercase;color:var(--accent2);margin-bottom:22px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.05)">{t1}</div>
        {items(i1,'rgba(193,98,42,0.3)',b1s,b1c)}
      </div>
      <div style="flex:1;padding:26px 24px;background:rgba(201,169,110,0.07);border:1px solid rgba(201,169,110,0.22);border-top:3px solid var(--accent)">
        <div style="font-size:12px;letter-spacing:4px;text-transform:uppercase;color:var(--accent);margin-bottom:22px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.05)">{t2}</div>
        {items(i2,'rgba(201,169,110,0.3)',b2s,b2c)}
      </div>
    </div>""", c, s, fk)

def render_cenarios(s, c, fk):
    hs = sz(s,'headline',60); b1s = sz(s,'bloco1',27); b2s = sz(s,'bloco2',27)
    hc = ec(s,'headline','var(--text)'); b1c = ec(s,'bloco1','var(--text)'); b2c = ec(s,'bloco2','var(--text)')
    hh = hl(s.get('headline',''))
    c1 = s.get('bloco1','').split('\n'); c2 = s.get('bloco2','').split('\n')
    l1, t1 = (c1[0], '\n'.join(c1[1:])) if c1 else ('','')
    l2, t2 = (c2[0], '\n'.join(c2[1:])) if c2 else ('','')
    conc = s.get('extra','')
    def hi(text):
        return re.sub(r'\b(VOLUME|MÉTODO|SISTEMA|RESULTADO|DECISÃO)\b',
                      r'<strong style="color:var(--accent)">\1</strong>', text)
    return wrap(f"""
    <div style="position:absolute;top:148px;left:60px;right:60px">
      <h2 style="font-size:{hs}px;font-weight:900;line-height:1.0;letter-spacing:-1.5px;
                 text-transform:uppercase;color:{hc}">{hh}</h2>
    </div>
    <div style="position:absolute;top:510px;left:60px;right:60px">
      <div style="padding:24px 26px;background:rgba(193,98,42,0.06);border-left:4px solid rgba(193,98,42,0.5);margin-bottom:16px">
        <div style="font-size:12px;letter-spacing:4px;text-transform:uppercase;color:var(--accent2);margin-bottom:9px">{l1}</div>
        <div style="font-size:{b1s}px;color:{b1c};opacity:0.65;line-height:1.45">{hi(br(t1))}</div>
      </div>
      <div style="padding:24px 26px;background:rgba(201,169,110,0.07);border-left:4px solid var(--accent)">
        <div style="font-size:12px;letter-spacing:4px;text-transform:uppercase;color:var(--accent);margin-bottom:9px">{l2}</div>
        <div style="font-size:{b2s}px;color:{b2c};line-height:1.45">{hi(br(t2))}</div>
      </div>
    </div>
    {"<div style='position:absolute;bottom:128px;left:60px;right:60px;border-top:1px solid var(--border);padding-top:28px'><p style='font-size:29px;font-style:italic;line-height:1.5;color:var(--text);opacity:0.85'>"+hi(conc)+"</p></div>" if conc else ""}
    """, c, s, fk)

def render_sintese(s, c, fk):
    hs = sz(s,'headline',58); b1s = sz(s,'bloco1',19); b2s = sz(s,'bloco2',30)
    hc = ec(s,'headline','var(--text)'); b2c = ec(s,'bloco2','var(--accent)')
    cadeia = [x.strip() for x in s.get('bloco1','').split('→')]
    cells = ''
    for i, item in enumerate(cadeia):
        last = i == len(cadeia)-1
        cells += f'<td style="padding:15px 10px;background:rgba(201,169,110,{0.13 if last else 0.07});border:1px solid rgba(201,169,110,{0.35 if last else 0.18});text-align:center;vertical-align:middle;white-space:nowrap"><div style="font-size:{b1s}px;font-weight:900;color:{"#E8C98A" if last else "var(--accent)"};text-transform:uppercase;letter-spacing:-0.5px">{item}</div></td>'
        if not last:
            cells += '<td style="text-align:center;color:var(--accent);font-size:20px;opacity:0.5;padding:0 3px">→</td>'
    return wrap(f"""
    <div style="position:absolute;top:148px;left:60px;right:60px">
      <h2 style="font-size:{hs}px;font-weight:900;line-height:1.0;letter-spacing:-1.5px;
                 text-transform:uppercase;color:{hc}">{hl(s.get('headline',''))}</h2>
    </div>
    <div style="position:absolute;top:548px;left:60px;right:60px">
      <div style="font-size:12px;letter-spacing:5px;text-transform:uppercase;color:rgba(154,136,112,0.65);margin-bottom:32px">O padrão que explica tudo</div>
      <table style="width:100%;border-collapse:collapse"><tr>{cells}</tr></table>
    </div>
    <div style="position:absolute;bottom:140px;left:60px;right:60px;border-top:1px solid var(--border);padding-top:30px">
      <p style="font-size:{b2s}px;font-weight:700;font-style:italic;line-height:1.45;color:{b2c}">{br(s.get('bloco2',''))}</p>
    </div>""", c, s, fk)

def render_aplicacao(s, c, fk):
    hs = sz(s,'headline',70); b1s = sz(s,'bloco1',26); b2s = sz(s,'bloco2',25)
    hc = ec(s,'headline','var(--text)'); b1c = ec(s,'bloco1','var(--text)'); b2c = ec(s,'bloco2','var(--accent)')
    b1 = s.get('bloco1','').split('\n')
    pare = b1[0].replace('PARE DE FAZER:','').replace('PARE DE FAZER: ','').replace('PARE DE SER PERFIL A:','').replace('PARE DE ESPERAR:','').strip().strip('"')
    comece = b1[1].replace('COMECE A FAZER:','').replace('COMECE A FAZER: ','').replace('COMECE A SER PERFIL B:','').replace('COMECE COM:','').strip().strip('"') if len(b1)>1 else ''
    math = s.get('bloco2','').split('\n')
    math_html = ''.join([f'<div style="font-size:{b2s}px;font-weight:{"700" if i==len(math)-1 else "400"};line-height:1.5;color:{b2c if i==len(math)-1 else "var(--text)"};opacity:{1 if i==len(math)-1 else 0.85};margin-bottom:7px">{l}</div>' for i,l in enumerate(math) if l.strip()])
    return wrap(f"""
    <div style="position:absolute;top:148px;left:60px;right:60px">
      <h2 style="font-size:{hs}px;font-weight:900;line-height:0.95;letter-spacing:-2px;
                 text-transform:uppercase;color:{hc}">{hl(s.get('headline',''))}</h2>
    </div>
    <div style="position:absolute;top:420px;left:60px;right:60px">
      <div style="display:flex;align-items:center;gap:16px;margin-bottom:12px">
        <span style="font-size:11px;letter-spacing:3px;text-transform:uppercase;color:var(--accent2);min-width:80px">Pare</span>
        <span style="font-size:{b1s}px;color:{b1c};opacity:0.38;text-decoration:line-through;text-decoration-color:rgba(193,98,42,0.4)">{pare}</span>
      </div>
      <div style="width:100%;height:1px;background:var(--border);margin:10px 0 12px"></div>
      <div style="display:flex;align-items:center;gap:16px">
        <span style="font-size:11px;letter-spacing:3px;text-transform:uppercase;color:var(--accent);min-width:80px">Comece</span>
        <span style="font-size:{b1s}px;font-weight:700;color:var(--accent)">{comece}</span>
      </div>
    </div>
    <div style="position:absolute;bottom:140px;left:60px;right:60px;
                background:rgba(201,169,110,0.07);border:1px solid rgba(201,169,110,0.25);padding:26px 30px">
      <div style="font-size:11px;letter-spacing:5px;text-transform:uppercase;color:var(--accent);margin-bottom:16px">Na prática</div>
      {math_html}
    </div>""", c, s, fk)

def render_cta(s, c, fk):
    hs = sz(s,'headline',80); b1s = sz(s,'bloco1',27); b2s = sz(s,'bloco2',29)
    hc = ec(s,'headline','var(--text)'); b1c = ec(s,'bloco1','var(--text)'); b2c = ec(s,'bloco2','var(--text)')
    b2 = re.sub(r'"([^"]+)"', f'<strong style="color:var(--accent);font-size:{b2s+4}px">\"\\1\"</strong>', s.get('bloco2',''))
    return wrap(f"""
    <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(201,169,110,0.09) 0%,transparent 60%)"></div>
    <div style="position:absolute;top:175px;left:60px;right:60px">
      <h2 style="font-size:{hs}px;font-weight:900;line-height:0.92;letter-spacing:-2px;
                 text-transform:uppercase;color:{hc}">{hl(s.get('headline',''))}</h2>
      <p style="margin-top:30px;font-size:{b1s}px;font-style:italic;line-height:1.55;color:{b1c};opacity:0.7;max-width:820px">{br(s.get('bloco1',''))}</p>
      <div style="width:100%;height:1px;background:var(--border);margin:40px 0"></div>
      <div style="background:rgba(201,169,110,0.08);border:1px solid rgba(201,169,110,0.3);padding:32px 38px">
        <div style="font-size:12px;letter-spacing:5px;text-transform:uppercase;color:var(--accent);margin-bottom:13px">Próximo passo</div>
        <p style="font-size:{b2s}px;font-weight:400;line-height:1.55;color:{b2c}">{b2}</p>
      </div>
    </div>""", c, s, fk)

RENDERERS = {
    'capa': render_capa, 'contexto': render_contexto, 'dados': render_dados,
    'virada': render_virada, 'dois_col': render_dois_col, 'cenarios': render_cenarios,
    'sintese': render_sintese, 'aplicacao': render_aplicacao, 'cta': render_cta
}

def render_slide(slide, colors, font_key):
    r = RENDERERS.get(slide['type'], render_capa)
    return r(slide, colors, font_key)

# ─── FLASK ─────────────────────────────────────────────────────────────────────

@app.route('/preview/<int:n>')
def preview(n):
    idx = n - 1
    if idx < 0 or idx >= len(STATE['slides']): return 'Slide não encontrado', 404
    return render_slide(STATE['slides'][idx], STATE['colors'], STATE['font'])

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify(STATE)

@app.route('/state', methods=['POST'])
def set_state():
    d = request.json
    if 'colors' in d: STATE['colors'].update(d['colors'])
    if 'font' in d: STATE['font'] = d['font']
    if 'nome' in d: STATE['nome'] = d['nome']
    if 'slide' in d:
        idx = d['slide']['num'] - 1
        if 0 <= idx < len(STATE['slides']):
            sl = STATE['slides'][idx]
            for k, v in d['slide'].items():
                if k in ('sizes', 'el_colors') and isinstance(v, dict):
                    sl.setdefault(k, {}).update(v)
                else:
                    sl[k] = v
    if 'template' in d:
        t = d['template']
        if t in TEMPLATES:
            STATE['template'] = t
            STATE['slides'] = [make_slide(s) for s in TEMPLATES[t]['slides']]
    return jsonify({'ok': True})

@app.route('/export', methods=['POST'])
def export_pngs():
    try:
        d = request.json or {}
        nome = d.get('nome', STATE.get('nome','carrossel')).strip().lower()
        nome = ''.join(c if c.isalnum() or c in '-_' else '-' for c in nome).strip('-') or 'carrossel'
        output_dir = WORKSPACE / 'exports' / nome
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n📸 Exportando {len(STATE['slides'])} slides → exports/{nome}/")
        from playwright.sync_api import sync_playwright
        exported = []
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 1080, 'height': 1350})
            for i, slide in enumerate(STATE['slides']):
                snum = slide['num']
                print(f"  [{i+1}/{len(STATE['slides'])}] slide {snum}")
                page.goto(f'http://localhost:{PORT}/preview/{snum}', wait_until='networkidle', timeout=20000)
                page.wait_for_timeout(900)
                out = output_dir / f'slide_{i+1:02d}.png'
                page.screenshot(path=str(out), clip={'x':0,'y':0,'width':1080,'height':1350})
                exported.append(str(out))
            browser.close()
        print(f"\n✅ {len(exported)} PNGs em: {output_dir}")
        import platform
        if platform.system() == 'Darwin': subprocess.Popen(['open', str(output_dir)])
        return jsonify({'ok': True, 'count': len(exported), 'folder': str(output_dir)})
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# ─── UI ────────────────────────────────────────────────────────────────────────

UI = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Post Creator · @glendonassis</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0D1117;--panel:#161B22;--panel2:#1C2230;--panel3:#21283A;
  --gold:#C9A96E;--gold2:#E8C98A;--red:#C1622A;--green:#3FB950;
  --text:#E6EDF3;--muted:#7D8590;--border:rgba(201,169,110,0.12);
  --border2:rgba(230,237,243,0.08);
  --radius:6px;
}
html,body{height:100%;overflow:hidden;background:var(--bg);
  color:var(--text);font-family:'Inter',sans-serif;font-size:14px}

/* ── LAYOUT ── */
.layout{display:grid;grid-template-rows:56px 1fr;grid-template-columns:360px 1fr;height:100vh}

/* ── TOPBAR ── */
.topbar{grid-column:1/-1;background:var(--panel);border-bottom:1px solid var(--border2);
  display:flex;align-items:center;gap:0;padding:0;z-index:100}
.top-brand{display:flex;align-items:center;gap:12px;padding:0 20px;
  border-right:1px solid var(--border2);height:100%;min-width:200px}
.top-logo{width:32px;height:32px;background:linear-gradient(135deg,var(--gold),var(--red));
  display:flex;align-items:center;justify-content:center;color:#0D1117;
  font-size:13px;font-weight:800;border-radius:var(--radius)}
.top-title{font-size:15px;font-weight:700;color:var(--text)}
.top-sub{font-size:11px;color:var(--muted);letter-spacing:1px}
.top-tabs{display:flex;height:100%;padding:0 8px}
.top-tab{padding:0 16px;height:100%;display:flex;align-items:center;gap:7px;
  font-size:12px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
  color:var(--muted);cursor:pointer;border-bottom:2px solid transparent;transition:all .15s}
.top-tab:hover{color:var(--text)}
.top-tab.active{color:var(--gold);border-bottom-color:var(--gold)}
.top-sep{width:1px;height:28px;background:var(--border2);margin:0 4px}
.top-right{margin-left:auto;padding:0 16px;display:flex;align-items:center;gap:10px}
.nome-input{background:var(--panel3);border:1px solid var(--border2);border-radius:var(--radius);
  color:var(--text);font-family:'Inter',sans-serif;font-size:13px;
  padding:7px 12px;width:190px;outline:none;transition:border-color .15s}
.nome-input:focus{border-color:var(--gold)}
.nome-input::placeholder{color:var(--muted);font-style:italic}
.btn-template{background:var(--panel3);border:1px solid var(--border2);border-radius:var(--radius);
  color:var(--text);font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;
  padding:7px 14px;cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:6px}
.btn-template:hover{border-color:var(--gold);color:var(--gold)}
.btn-export{background:linear-gradient(135deg,var(--gold),#A07840);color:#0D1117;border:none;
  border-radius:var(--radius);font-family:'Inter',sans-serif;font-size:12px;font-weight:700;
  letter-spacing:1.5px;padding:8px 20px;cursor:pointer;transition:all .15s;text-transform:uppercase;
  display:flex;align-items:center;gap:6px}
.btn-export:hover{filter:brightness(1.1);transform:translateY(-1px)}
.btn-export:disabled{background:rgba(201,169,110,0.25);color:rgba(0,0,0,0.4);cursor:not-allowed;transform:none}

/* ── LEFT PANEL ── */
.panel{background:var(--panel);border-right:1px solid var(--border2);
  display:flex;flex-direction:column;overflow:hidden}
.tab-content{display:none;flex-direction:column;overflow-y:auto;flex:1;
  scrollbar-width:thin;scrollbar-color:var(--border2) transparent}
.tab-content.active{display:flex}
.tab-content::-webkit-scrollbar{width:4px}
.tab-content::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px}

/* TEXTO TAB */
.slide-sec{border-bottom:1px solid var(--border2)}
.slide-sec-hd{padding:11px 16px;display:flex;align-items:center;gap:10px;
  cursor:pointer;user-select:none;transition:background .15s}
.slide-sec-hd:hover{background:rgba(201,169,110,0.04)}
.slide-badge{width:28px;height:28px;border:1px solid rgba(201,169,110,0.2);border-radius:4px;
  display:flex;align-items:center;justify-content:center;font-size:11px;
  font-weight:700;color:var(--muted);flex-shrink:0;transition:all .15s}
.slide-sec-hd.open .slide-badge{border-color:var(--gold);color:var(--gold)}
.slide-sec-label{font-size:12px;font-weight:600;letter-spacing:0.5px;color:var(--muted);flex:1}
.slide-sec-hd.open .slide-sec-label{color:var(--text)}
.chev{font-size:10px;color:var(--muted);transition:transform .2s}
.slide-sec-hd.open .chev{transform:rotate(90deg);color:var(--gold)}
.slide-sec-body{display:none;padding:10px 16px 14px;gap:10px;flex-direction:column}
.slide-sec-body.open{display:flex}
.fl{font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
  color:var(--muted);margin-bottom:5px}
.fi,.ft{width:100%;background:var(--panel3);border:1px solid var(--border2);
  border-radius:4px;color:var(--text);font-family:'Inter',sans-serif;font-size:12.5px;
  padding:8px 10px;outline:none;resize:vertical;transition:border-color .15s;line-height:1.55}
.fi:focus,.ft:focus{border-color:var(--gold)}
.ft{min-height:80px}
.btn-apply{background:rgba(59,130,246,0.15);border:1px solid rgba(59,130,246,0.3);
  border-radius:4px;color:#60A5FA;font-family:'Inter',sans-serif;font-size:11px;
  font-weight:600;letter-spacing:1px;text-transform:uppercase;padding:6px 14px;
  cursor:pointer;transition:all .15s;align-self:flex-start}
.btn-apply:hover{background:rgba(59,130,246,0.25)}

/* CORES TAB */
.sec-block{padding:16px}
.sec-title{font-size:10px;font-weight:700;letter-spacing:3px;text-transform:uppercase;
  color:var(--muted);margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid var(--border2)}
.cor-row{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.cor-sw{width:36px;height:36px;border:1px solid rgba(255,255,255,0.08);border-radius:4px;
  cursor:pointer;position:relative;overflow:hidden;flex-shrink:0}
.cor-sw input[type=color]{position:absolute;inset:-4px;opacity:0;cursor:pointer;width:120%;height:120%}
.cor-nm{font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:var(--muted)}
.cor-hx{font-size:13px;color:var(--text);font-family:monospace;margin-top:2px}
.btn-ac{background:transparent;border:1px solid var(--border2);border-radius:4px;
  color:var(--gold);font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;
  padding:5px 9px;cursor:pointer;white-space:nowrap;transition:all .15s}
.btn-ac:hover{border-color:var(--gold);background:rgba(201,169,110,0.06)}
.btn-todas{width:100%;background:rgba(201,169,110,0.08);border:1px solid rgba(201,169,110,0.25);
  border-radius:4px;color:var(--gold);font-family:'Inter',sans-serif;font-size:11px;
  font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:9px;cursor:pointer;
  transition:all .15s;margin-top:6px}
.btn-todas:hover{background:rgba(201,169,110,0.15)}
.pal-row{display:flex;align-items:center;gap:8px;padding:8px;cursor:pointer;
  border-radius:4px;transition:background .15s;margin-bottom:4px}
.pal-row:hover{background:rgba(201,169,110,0.05)}
.psw{width:26px;height:26px;border-radius:3px;border:1px solid rgba(255,255,255,0.07);flex-shrink:0}
.plbl{font-size:12px;color:var(--muted);flex:1}
.parr{font-size:11px;color:var(--muted)}

/* FONTES TAB */
.font-card{padding:14px 16px;margin:0 12px 8px;border:1.5px solid var(--border2);
  border-radius:6px;cursor:pointer;transition:all .15s}
.font-card:hover{border-color:rgba(201,169,110,0.35)}
.font-card.sel{border-color:var(--gold);background:rgba(201,169,110,0.05)}
.font-name{font-size:13px;font-weight:600;color:var(--text);margin-bottom:4px}
.font-desc{font-size:11px;color:var(--muted);margin-bottom:10px}
.font-sample{font-size:22px;color:var(--text);opacity:0.7;line-height:1.2}
.font-check{width:16px;height:16px;border:1.5px solid var(--border2);border-radius:50%;
  float:right;margin-top:-30px;position:relative;top:0;transition:all .15s}
.font-card.sel .font-check{background:var(--gold);border-color:var(--gold)}

/* AJUSTES TAB */
.fmt-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}
.fmt-card{padding:12px;border:1.5px solid var(--border2);border-radius:var(--radius);
  cursor:pointer;text-align:center;transition:all .15s}
.fmt-card:hover,.fmt-card.sel{border-color:var(--gold);background:rgba(201,169,110,0.06)}
.fmt-lbl{font-size:13px;font-weight:700;color:var(--text)}
.fmt-dim{font-size:10px;color:var(--muted);margin-top:3px;letter-spacing:1px}
.info-badge{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;
  background:rgba(63,185,80,0.1);border:1px solid rgba(63,185,80,0.25);
  border-radius:12px;font-size:11px;color:var(--green);font-weight:600}

/* ── CANVAS ── */
.canvas{background:var(--bg);overflow-y:auto;padding:24px;
  scrollbar-width:thin;scrollbar-color:var(--border2) transparent}
.canvas::-webkit-scrollbar{width:6px}
.canvas::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px}
.canvas-header{display:flex;align-items:center;justify-content:space-between;
  margin-bottom:20px;padding-bottom:14px;border-bottom:1px solid var(--border2)}
.canvas-title{font-size:12px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--muted)}
.canvas-info{font-size:12px;color:var(--muted);display:flex;align-items:center;gap:6px}
.dot{width:6px;height:6px;border-radius:50%;background:var(--green)}
.slides-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.slide-card{background:var(--panel);border:1px solid var(--border2);border-radius:8px;
  overflow:hidden;cursor:pointer;transition:all .2s}
.slide-card:hover{border-color:rgba(201,169,110,0.35);transform:translateY(-2px);
  box-shadow:0 8px 24px rgba(0,0,0,0.3)}
.thumb-wrap{width:100%;padding-top:125%;position:relative;overflow:hidden;background:#090706}
.thumb-wrap iframe{position:absolute;top:0;left:0;width:1080px;height:1350px;
  border:none;pointer-events:none;transform-origin:top left}
.card-foot{padding:9px 12px;display:flex;align-items:center;justify-content:space-between;
  border-top:1px solid var(--border2)}
.card-name{font-size:11px;font-weight:600;color:var(--muted);letter-spacing:0.5px;text-transform:uppercase}
.card-num{font-size:11px;color:rgba(125,133,144,0.5);letter-spacing:2px;font-family:monospace}

/* ── TEMPLATE MODAL ── */
.modal-bg{display:none;position:fixed;inset:0;background:rgba(13,17,23,0.92);
  z-index:500;align-items:center;justify-content:center}
.modal-bg.show{display:flex}
.modal{background:var(--panel);border:1px solid var(--border2);border-radius:12px;
  width:760px;max-height:88vh;overflow-y:auto;padding:32px}
.modal-title{font-size:20px;font-weight:800;color:var(--text);margin-bottom:6px}
.modal-sub{font-size:13px;color:var(--muted);margin-bottom:28px}
.tmpl-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.tmpl-card{padding:20px;border:1.5px solid var(--border2);border-radius:8px;
  cursor:pointer;transition:all .2s}
.tmpl-card:hover{border-color:rgba(201,169,110,0.4);background:rgba(201,169,110,0.04)}
.tmpl-card.sel{border-color:var(--gold);background:rgba(201,169,110,0.07)}
.tmpl-icon{font-size:28px;margin-bottom:12px}
.tmpl-label{font-size:15px;font-weight:700;color:var(--text);margin-bottom:6px}
.tmpl-desc{font-size:12px;color:var(--muted);line-height:1.6}
.modal-footer{display:flex;justify-content:flex-end;gap:10px;margin-top:28px;
  padding-top:20px;border-top:1px solid var(--border2)}
.btn-cancel{background:transparent;border:1px solid var(--border2);border-radius:var(--radius);
  color:var(--muted);font-size:12px;font-weight:600;padding:9px 20px;cursor:pointer;transition:all .15s}
.btn-cancel:hover{border-color:var(--text);color:var(--text)}
.btn-confirm{background:linear-gradient(135deg,var(--gold),#A07840);color:#0D1117;
  border:none;border-radius:var(--radius);font-size:12px;font-weight:700;
  padding:9px 24px;cursor:pointer;transition:all .15s;letter-spacing:1px;text-transform:uppercase}
.btn-confirm:hover{filter:brightness(1.1)}

/* ── LOADING ── */
.loading-bg{display:none;position:fixed;inset:0;background:rgba(13,17,23,0.95);
  z-index:999;align-items:center;justify-content:center;flex-direction:column;gap:16px}
.loading-bg.show{display:flex}
.loading-title{font-size:20px;font-weight:800;color:var(--gold)}
.loading-sub{font-size:11px;letter-spacing:3px;text-transform:uppercase;color:var(--muted)}
.prog-wrap{width:320px;height:2px;background:rgba(201,169,110,0.1);border-radius:1px;margin-top:6px}
.prog-bar{height:100%;background:linear-gradient(to right,var(--gold),var(--gold2));
  border-radius:1px;width:15%;animation:prg 1.8s ease-in-out infinite alternate}
@keyframes prg{to{width:90%}}

/* ── CONTROLES POR ELEMENTO ── */
.el-section{margin-top:10px;padding-top:10px;border-top:1px solid var(--border2)}
.el-section-title{font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;
  color:var(--muted);margin-bottom:10px}
.sz-row{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.sz-lbl{font-size:10px;font-weight:600;letter-spacing:0.5px;color:var(--muted);width:54px;flex-shrink:0}
.sz-slider{flex:1;-webkit-appearance:none;height:3px;border-radius:2px;
  background:var(--border2);outline:none;cursor:pointer}
.sz-slider::-webkit-slider-thumb{-webkit-appearance:none;width:13px;height:13px;
  border-radius:50%;background:var(--gold);cursor:pointer;border:2px solid var(--bg)}
.sz-val{font-size:11px;color:var(--gold);font-family:monospace;width:34px;text-align:right;flex-shrink:0}
.ec-row{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.ec-sw{width:22px;height:22px;border:1px solid rgba(255,255,255,0.1);border-radius:3px;
  cursor:pointer;position:relative;overflow:hidden;flex-shrink:0}
.ec-sw input[type=color]{position:absolute;inset:-4px;opacity:0;cursor:pointer;width:130%;height:130%}
.ec-lbl{font-size:10px;font-weight:600;letter-spacing:0.5px;color:var(--muted);flex:1}
.btn-ec-reset{background:transparent;border:1px solid var(--border2);border-radius:3px;
  color:var(--muted);font-size:9px;font-weight:700;letter-spacing:0.5px;padding:3px 7px;
  cursor:pointer;transition:all .15s;white-space:nowrap}
.btn-ec-reset:hover{border-color:var(--red);color:var(--red)}

/* ── TOAST ── */
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(70px);
  background:var(--panel2);border:1px solid var(--border2);border-radius:8px;
  padding:11px 22px;font-size:13px;color:var(--text);transition:transform .25s;
  z-index:998;max-width:500px;text-align:center;box-shadow:0 8px 24px rgba(0,0,0,0.4)}
.toast.show{transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(63,185,80,0.4);color:var(--green)}
.toast.err{border-color:rgba(193,98,42,0.4);color:var(--red)}
</style>
</head>
<body>
<div class="layout">

<!-- TOPBAR -->
<div class="topbar">
  <div class="top-brand">
    <div class="top-logo">PC</div>
    <div>
      <div class="top-title">Post Creator</div>
      <div class="top-sub">@glendonassis</div>
    </div>
  </div>
  <div class="top-tabs">
    <div class="top-tab active" data-tab="texto" onclick="switchTab(this)">≡ TEXTO</div>
    <div class="top-sep"></div>
    <div class="top-tab" data-tab="fontes" onclick="switchTab(this)">T FONTES</div>
    <div class="top-sep"></div>
    <div class="top-tab" data-tab="cores" onclick="switchTab(this)">◑ CORES</div>
    <div class="top-sep"></div>
    <div class="top-tab" data-tab="ajustes" onclick="switchTab(this)">⚙ AJUSTES</div>
  </div>
  <div class="top-right">
    <button class="btn-template" onclick="openModal()">⊞ Template</button>
    <input class="nome-input" id="nomeInput" placeholder="nome-da-pasta" value="meu-carrossel">
    <button class="btn-export" onclick="exportar()">↓ Exportar!</button>
  </div>
</div>

<!-- PANEL -->
<div class="panel">

  <!-- TEXTO -->
  <div class="tab-content active" id="tab-texto"></div>

  <!-- FONTES -->
  <div class="tab-content" id="tab-fontes">
    <div style="padding:16px 12px 8px">
      <div class="sec-title">Família Tipográfica</div>
      <div style="font-size:11px;color:var(--muted);margin-bottom:16px;line-height:1.6">
        Escolha a fonte dos slides. Afeta todos os 9 slides ao mesmo tempo.
      </div>
      <div id="fontCards"></div>
    </div>
  </div>

  <!-- CORES -->
  <div class="tab-content" id="tab-cores">
    <div class="sec-block">
      <div class="sec-title">Editar Cores</div>
      <div class="cor-row">
        <div class="cor-sw" id="sw-bg" style="background:#1A1510"><input type="color" value="#1A1510" id="pk-bg" oninput="previewCor('bg',this.value)"></div>
        <div style="flex:1"><div class="cor-nm">Background</div><div class="cor-hx" id="hx-bg">#1A1510</div></div>
        <button class="btn-ac" onclick="aplicarCor('bg')">+ Aplicar</button>
      </div>
      <div class="cor-row">
        <div class="cor-sw" id="sw-text" style="background:#F5EFE6"><input type="color" value="#F5EFE6" id="pk-text" oninput="previewCor('text',this.value)"></div>
        <div style="flex:1"><div class="cor-nm">Texto</div><div class="cor-hx" id="hx-text">#F5EFE6</div></div>
        <button class="btn-ac" onclick="aplicarCor('text')">+ Aplicar</button>
      </div>
      <div class="cor-row">
        <div class="cor-sw" id="sw-accent" style="background:#C9A96E"><input type="color" value="#C9A96E" id="pk-accent" oninput="previewCor('accent',this.value)"></div>
        <div style="flex:1"><div class="cor-nm">Elementos</div><div class="cor-hx" id="hx-accent">#C9A96E</div></div>
        <button class="btn-ac" onclick="aplicarCor('accent')">+ Aplicar</button>
      </div>
      <div class="cor-row">
        <div class="cor-sw" id="sw-accent2" style="background:#C1622A"><input type="color" value="#C1622A" id="pk-accent2" oninput="previewCor('accent2',this.value)"></div>
        <div style="flex:1"><div class="cor-nm">Destaque 2</div><div class="cor-hx" id="hx-accent2">#C1622A</div></div>
        <button class="btn-ac" onclick="aplicarCor('accent2')">+ Aplicar</button>
      </div>
      <button class="btn-todas" onclick="aplicarTodas()">Aplicar Todas as Cores</button>
      <div class="sec-title" style="margin-top:20px">Paletas Sugeridas</div>
      <div class="pal-row" onclick="aplicarPaleta('#1A1510','#F5EFE6','#C9A96E','#C1622A')">
        <div class="psw" style="background:#1A1510"></div><div class="parr">→</div>
        <div class="psw" style="background:#C9A96E"></div><div class="plbl">Magazine Dark (padrão)</div>
      </div>
      <div class="pal-row" onclick="aplicarPaleta('#F5EFE6','#1A1510','#C1622A','#A07840')">
        <div class="psw" style="background:#F5EFE6"></div><div class="parr">→</div>
        <div class="psw" style="background:#C1622A"></div><div class="plbl">Editorial Claro</div>
      </div>
      <div class="pal-row" onclick="aplicarPaleta('#0A0A0A','#FFFFFF','#4A90D9','#E74C3C')">
        <div class="psw" style="background:#0A0A0A"></div><div class="parr">→</div>
        <div class="psw" style="background:#4A90D9"></div><div class="plbl">Contraste Urbano</div>
      </div>
      <div class="pal-row" onclick="aplicarPaleta('#1B1A2E','#E8E6F0','#7C6FCD','#E85D75')">
        <div class="psw" style="background:#1B1A2E"></div><div class="parr">→</div>
        <div class="psw" style="background:#7C6FCD"></div><div class="plbl">Roxo Premium</div>
      </div>
      <div class="pal-row" onclick="aplicarPaleta('#0D1F0D','#E8F5E8','#4CAF50','#FF9800')">
        <div class="psw" style="background:#0D1F0D"></div><div class="parr">→</div>
        <div class="psw" style="background:#4CAF50"></div><div class="plbl">Forest Premium</div>
      </div>
    </div>
  </div>

  <!-- AJUSTES -->
  <div class="tab-content" id="tab-ajustes">
    <div class="sec-block">
      <div class="sec-title">Formato de Exportação</div>
      <div class="fmt-grid">
        <div class="fmt-card sel"><div class="fmt-lbl">Feed</div><div class="fmt-dim">1080 × 1350</div></div>
        <div class="fmt-card" style="opacity:.5;cursor:default"><div class="fmt-lbl">Story</div><div class="fmt-dim">Em breve</div></div>
      </div>
      <div class="sec-title" style="margin-top:20px">Handle</div>
      <input class="fi" id="handleInput" value="@glendonassis" oninput="debounce(()=>updateHandle(this.value),400)">
      <div class="sec-title" style="margin-top:20px">Status</div>
      <div style="display:flex;flex-direction:column;gap:8px">
        <div class="info-badge"><span>●</span> Post Creator v2.0</div>
        <div style="font-size:11px;color:var(--muted);line-height:1.7;margin-top:6px">
          Engine: Playwright / Chromium<br>
          Fontes: Google Fonts<br>
          Export: PNG 1080 × 1350px<br>
          @glendonassis · Post Machine System
        </div>
      </div>
    </div>
  </div>

</div><!-- /panel -->

<!-- CANVAS -->
<div class="canvas">
  <div class="canvas-header">
    <div class="canvas-title" id="canvasTitle">9 slides · pronto</div>
    <div class="canvas-info"><div class="dot"></div> <span id="canvasInfo">Magazine Dark · Playfair Display</span></div>
  </div>
  <div class="slides-grid" id="slidesGrid"></div>
</div>

</div><!-- /layout -->

<!-- TEMPLATE MODAL -->
<div class="modal-bg" id="modalBg">
  <div class="modal">
    <div class="modal-title">Escolher Template</div>
    <div class="modal-sub">Selecione a estrutura narrativa do carrossel. O conteúdo de exemplo será carregado automaticamente.</div>
    <div class="tmpl-grid" id="tmplGrid"></div>
    <div class="modal-footer">
      <button class="btn-cancel" onclick="closeModal()">Cancelar</button>
      <button class="btn-confirm" onclick="confirmarTemplate()">Aplicar Template →</button>
    </div>
  </div>
</div>

<!-- LOADING -->
<div class="loading-bg" id="loadingBg">
  <div class="loading-title">Gerando PNGs...</div>
  <div class="loading-sub" id="loadingSub">Iniciando Chromium</div>
  <div class="prog-wrap"><div class="prog-bar"></div></div>
</div>

<!-- TOAST -->
<div class="toast" id="toast"></div>

<script>
// ── FONTS CONFIG (must match Python) ──────────────────────────────────────────
const FONTS = {
  playfair: {label:"Playfair Display", desc:"Autoridade clássica. Tom editorial premium.", family:"'Playfair Display', Georgia, serif"},
  cormorant: {label:"Cormorant Garamond", desc:"Elegante e sofisticada. Tom literário.", family:"'Cormorant Garamond', Georgia, serif"},
  dm_serif: {label:"DM Serif Display", desc:"Moderna e impactante. Tom de revista contemporânea.", family:"'DM Serif Display', Georgia, serif"},
  libre: {label:"Libre Baskerville", desc:"Sólida e séria. Tom acadêmico com autoridade.", family:"'Libre Baskerville', Georgia, serif"},
};

const TEMPLATES_META = {
  explicativo: {label:"Explicativo", desc:"Ensina um conceito com dados, virada e aplicação.", icon:"📖"},
  lista: {label:"Lista Numerada", desc:"Erros, dicas ou passos numerados. Formato direto.", icon:"🔢"},
  storytelling: {label:"Storytelling / Case", desc:"Conta uma história ou caso real com resultado.", icon:"🎬"},
  comparativo: {label:"Comparativo A vs B", desc:"Contrasta dois perfis ou caminhos. Forte para posicionamento.", icon:"⚖️"},
};

const SLIDE_LABELS = {
  capa:"Capa", contexto:"Contexto", dados:"Dados", virada:"Virada",
  dois_col:"Desenvolvimento 1", cenarios:"Desenvolvimento 2",
  sintese:"Síntese", aplicacao:"Aplicação", cta:"CTA"
};

const FIELDS = {
  tag: {label:"TAG", type:"input"},
  headline: {label:"HEADLINE", type:"textarea", rows:4},
  bloco1: {label:"BLOCO 1", type:"textarea", rows:5},
  bloco2: {label:"BLOCO 2", type:"textarea", rows:4},
  extra: {label:"EXTRA", type:"textarea", rows:2}
};

// ── STATE ──────────────────────────────────────────────────────────────────────
let state = null;
let timers = {};
let selectedTemplate = null;

function debounce(fn, ms, k='d') { clearTimeout(timers[k]); timers[k] = setTimeout(fn, ms); }

// ── INIT ───────────────────────────────────────────────────────────────────────
async function init() {
  const r = await fetch('/state');
  state = await r.json();
  buildTexto();
  buildFontes();
  buildGrid();
  buildTmplGrid();
  document.getElementById('nomeInput').value = state.nome || 'meu-carrossel';
  updateCanvasInfo();
}

// ── TABS ───────────────────────────────────────────────────────────────────────
function switchTab(el) {
  document.querySelectorAll('.top-tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('tab-'+el.dataset.tab).classList.add('active');
}

// ── TEXTO ──────────────────────────────────────────────────────────────────────
function buildTexto() {
  const tab = document.getElementById('tab-texto');
  tab.innerHTML = '';
  state.slides.forEach(slide => {
    const sec = document.createElement('div');
    sec.className = 'slide-sec'; sec.id = `sec-${slide.num}`;
    const hd = document.createElement('div');
    hd.className = 'slide-sec-hd'; hd.id = `hd-${slide.num}`;
    hd.innerHTML = `<div class="slide-badge">${String(slide.num).padStart(2,'0')}</div>
      <div class="slide-sec-label">${SLIDE_LABELS[slide.type]||slide.type}</div>
      <span class="chev">›</span>`;
    hd.onclick = () => toggleSec(slide.num);
    sec.appendChild(hd);
    const body = document.createElement('div');
    body.className = 'slide-sec-body'; body.id = `body-${slide.num}`;
    const keys = ['tag','headline','bloco1','bloco2'];
    if (['dados','cenarios'].includes(slide.type)) keys.push('extra');
    keys.forEach(key => {
      const f = FIELDS[key];
      const wrap = document.createElement('div');
      wrap.innerHTML = `<div class="fl">${f.label}</div>`;
      const el = f.type==='input' ? document.createElement('input') : document.createElement('textarea');
      el.className = f.type==='input' ? 'fi' : 'ft';
      if (f.rows) el.rows = f.rows;
      el.value = slide[key] || '';
      el.dataset.num = slide.num; el.dataset.key = key;
      el.addEventListener('input', function() {
        debounce(() => saveField(parseInt(this.dataset.num), this.dataset.key, this.value), 600, `${this.dataset.num}-${this.dataset.key}`);
      });
      wrap.appendChild(el); body.appendChild(wrap);
    });
    const btn = document.createElement('button');
    btn.className = 'btn-apply'; btn.textContent = 'Aplicar Texto';
    btn.onclick = () => applySlide(slide.num);
    body.appendChild(btn);
    // ── CONTROLES DE TAMANHO ──
    const szSec = document.createElement('div');
    szSec.className = 'el-section';
    szSec.innerHTML = '<div class="el-section-title">Tamanho dos elementos</div>';
    const sizes = slide.sizes || {};
    [['headline','Headline',24,160],['bloco1','Bloco 1',14,72],['bloco2','Bloco 2',14,180]].forEach(([elName,lbl,min,max]) => {
      const defVal = sizes[elName] || 0;
      const row = document.createElement('div'); row.className = 'sz-row';
      row.innerHTML = `<span class="sz-lbl">${lbl}</span>
        <input type="range" class="sz-slider" min="${min}" max="${max}" value="${defVal||40}"
          data-num="${slide.num}" data-el="${elName}" id="sz-${slide.num}-${elName}"
          oninput="onSizeChange(this)">
        <span class="sz-val" id="sv-${slide.num}-${elName}">${defVal?defVal+'px':'auto'}</span>`;
      szSec.appendChild(row);
    });
    body.appendChild(szSec);
    // ── CONTROLES DE COR POR ELEMENTO ──
    const ecSec = document.createElement('div');
    ecSec.className = 'el-section';
    ecSec.innerHTML = '<div class="el-section-title">Cor dos elementos</div>';
    const elColors = slide.el_colors || {};
    [['headline','Headline'],['bloco1','Bloco 1'],['bloco2','Bloco 2']].forEach(([elName,lbl]) => {
      const curVal = elColors[elName] || '#C9A96E';
      const hasCustom = !!(elColors[elName]);
      const row = document.createElement('div'); row.className = 'ec-row';
      row.innerHTML = `<div class="ec-sw" id="ecsw-${slide.num}-${elName}" style="background:${curVal}">
        <input type="color" value="${curVal}" data-num="${slide.num}" data-el="${elName}"
          oninput="onElColorChange(this)"></div>
        <span class="ec-lbl">${lbl}${hasCustom?' <span style="color:var(--gold)">●</span>':''}</span>
        <button class="btn-ec-reset" onclick="resetElColor(${slide.num},'${elName}')">Reset</button>`;
      ecSec.appendChild(row);
    });
    body.appendChild(ecSec);
    sec.appendChild(body);
    tab.appendChild(sec);
  });
}

function toggleSec(num) {
  document.getElementById(`hd-${num}`).classList.toggle('open');
  document.getElementById(`body-${num}`).classList.toggle('open');
}

async function saveField(num, key, val) {
  const sl = state.slides.find(s=>s.num===num);
  if (!sl) return;
  sl[key] = val;
  await post('/state', {slide:{num,...sl}});
  reloadPreview(num);
}

async function applySlide(num) {
  const body = document.getElementById(`body-${num}`);
  const sl = state.slides.find(s=>s.num===num);
  body.querySelectorAll('[data-key]').forEach(el => sl[el.dataset.key] = el.value);
  await post('/state', {slide:{num,...sl}});
  reloadPreview(num);
  toast(`✓ Texto aplicado ao slide ${num}`, 'ok');
}

// ── FONTES ─────────────────────────────────────────────────────────────────────
function buildFontes() {
  const container = document.getElementById('fontCards');
  container.innerHTML = '';
  Object.entries(FONTS).forEach(([key, f]) => {
    const card = document.createElement('div');
    card.className = 'font-card' + (state.font===key?' sel':'');
    card.id = `fc-${key}`;
    card.innerHTML = `
      <div class="font-check"></div>
      <div class="font-name">${f.label}</div>
      <div class="font-desc">${f.desc}</div>
      <div class="font-sample" style="font-family:${f.family}">Aa Bb Cc 123</div>`;
    card.onclick = () => selectFont(key);
    container.appendChild(card);
  });
}

async function selectFont(key) {
  state.font = key;
  document.querySelectorAll('.font-card').forEach(c=>c.classList.remove('sel'));
  document.getElementById(`fc-${key}`).classList.add('sel');
  await post('/state', {font:key});
  reloadAll();
  updateCanvasInfo();
  toast(`✓ Fonte: ${FONTS[key].label}`, 'ok');
}

// ── GRID ───────────────────────────────────────────────────────────────────────
function buildGrid() {
  const grid = document.getElementById('slidesGrid');
  grid.innerHTML = '';
  state.slides.forEach(slide => {
    const card = document.createElement('div');
    card.className = 'slide-card'; card.id = `card-${slide.num}`;
    card.innerHTML = `
      <div class="thumb-wrap">
        <iframe src="/preview/${slide.num}" id="ifr-${slide.num}" scrolling="no" onload="scaleIfr(${slide.num})"></iframe>
      </div>
      <div class="card-foot">
        <span class="card-name">${SLIDE_LABELS[slide.type]||slide.type}</span>
        <span class="card-num">${String(slide.num).padStart(2,'0')}</span>
      </div>`;
    card.onclick = () => {
      switchTab(document.querySelector('[data-tab="texto"]'));
      const sec = document.getElementById(`sec-${slide.num}`);
      const hd = document.getElementById(`hd-${slide.num}`);
      if (!hd.classList.contains('open')) toggleSec(slide.num);
      setTimeout(() => sec.scrollIntoView({behavior:'smooth',block:'start'}), 100);
    };
    grid.appendChild(card);
  });
}

function scaleIfr(num) {
  const wrap = document.querySelector(`#card-${num} .thumb-wrap`);
  const ifr = document.getElementById(`ifr-${num}`);
  if (!wrap||!ifr) return;
  ifr.style.transform = `scale(${wrap.offsetWidth/1080})`;
}
window.addEventListener('resize', () => state?.slides.forEach(s=>scaleIfr(s.num)));

function reloadPreview(num) {
  const ifr = document.getElementById(`ifr-${num}`);
  if (ifr) ifr.src = `/preview/${num}?t=${Date.now()}`;
}
function reloadAll() { state.slides.forEach(s=>reloadPreview(s.num)); }

// ── CORES ──────────────────────────────────────────────────────────────────────
function previewCor(k,v) {
  document.getElementById(`sw-${k}`).style.background=v;
  document.getElementById(`hx-${k}`).textContent=v;
  document.getElementById(`pk-${k}`).value=v;
}
async function aplicarCor(k) {
  const v = document.getElementById(`pk-${k}`).value;
  state.colors[k]=v;
  await post('/state',{colors:{[k]:v}});
  reloadAll(); toast(`✓ Cor aplicada`,'ok');
}
async function aplicarTodas() {
  const colors = {bg:document.getElementById('pk-bg').value,text:document.getElementById('pk-text').value,accent:document.getElementById('pk-accent').value,accent2:document.getElementById('pk-accent2').value};
  Object.assign(state.colors,colors);
  await post('/state',{colors}); reloadAll(); toast('✓ Todas as cores aplicadas','ok');
}
async function aplicarPaleta(bg,text,accent,accent2) {
  const colors={bg,text,accent,accent2};
  Object.assign(state.colors,colors);
  ['bg','text','accent','accent2'].forEach(k=>{document.getElementById(`pk-${k}`).value=colors[k];previewCor(k,colors[k]);});
  await post('/state',{colors}); reloadAll(); toast('✓ Paleta aplicada','ok');
}

// ── TAMANHO POR ELEMENTO ───────────────────────────────────────────────────────
function onSizeChange(el) {
  const num = parseInt(el.dataset.num), elName = el.dataset.el;
  const val = parseInt(el.value);
  const valEl = document.getElementById(`sv-${num}-${elName}`);
  if (valEl) valEl.textContent = val + 'px';
  const sl = state.slides.find(s=>s.num===num);
  if (!sl) return;
  if (!sl.sizes) sl.sizes = {};
  sl.sizes[elName] = val;
  debounce(() => {
    post('/state', {slide:{num, sizes:{[elName]:val}}});
    reloadPreview(num);
  }, 250, `sz-${num}-${elName}`);
}

// ── COR POR ELEMENTO ───────────────────────────────────────────────────────────
function onElColorChange(el) {
  const num = parseInt(el.dataset.num), elName = el.dataset.el;
  const val = el.value;
  const sw = document.getElementById(`ecsw-${num}-${elName}`);
  if (sw) sw.style.background = val;
  const sl = state.slides.find(s=>s.num===num);
  if (!sl) return;
  if (!sl.el_colors) sl.el_colors = {};
  sl.el_colors[elName] = val;
  debounce(() => {
    post('/state', {slide:{num, el_colors:{[elName]:val}}});
    reloadPreview(num);
  }, 250, `ec-${num}-${elName}`);
}

async function resetElColor(num, elName) {
  const sl = state.slides.find(s=>s.num===num);
  if (!sl) return;
  if (!sl.el_colors) sl.el_colors = {};
  sl.el_colors[elName] = '';
  await post('/state', {slide:{num, el_colors:{[elName]:''}}});
  reloadPreview(num);
  const sw = document.getElementById(`ecsw-${num}-${elName}`);
  if (sw) sw.style.background = '#888';
  toast(`✓ Cor resetada para padrão`,'ok');
}

// ── AJUSTES ────────────────────────────────────────────────────────────────────
async function updateHandle(v) {
  state.colors.handle=v;
  await post('/state',{colors:{handle:v}}); reloadAll();
}

// ── TEMPLATE MODAL ─────────────────────────────────────────────────────────────
function buildTmplGrid() {
  const grid = document.getElementById('tmplGrid');
  grid.innerHTML = '';
  Object.entries(TEMPLATES_META).forEach(([key,t]) => {
    const card = document.createElement('div');
    card.className = 'tmpl-card' + (state.template===key?' sel':'');
    card.id = `tmpl-${key}`;
    card.innerHTML = `<div class="tmpl-icon">${t.icon}</div><div class="tmpl-label">${t.label}</div><div class="tmpl-desc">${t.desc}</div>`;
    card.onclick = () => {
      document.querySelectorAll('.tmpl-card').forEach(c=>c.classList.remove('sel'));
      card.classList.add('sel'); selectedTemplate = key;
    };
    grid.appendChild(card);
  });
  selectedTemplate = state.template;
}
function openModal() { buildTmplGrid(); document.getElementById('modalBg').classList.add('show'); }
function closeModal() { document.getElementById('modalBg').classList.remove('show'); }
async function confirmarTemplate() {
  if (!selectedTemplate) return;
  await post('/state',{template:selectedTemplate});
  const r = await fetch('/state'); state = await r.json();
  buildTexto(); buildGrid();
  closeModal(); updateCanvasInfo();
  toast(`✓ Template "${TEMPLATES_META[selectedTemplate].label}" carregado`,'ok');
}

// ── CANVAS INFO ────────────────────────────────────────────────────────────────
function updateCanvasInfo() {
  const tl = TEMPLATES_META[state.template]?.label || state.template;
  const fl = FONTS[state.font]?.label || state.font;
  document.getElementById('canvasTitle').textContent = `${state.slides.length} slides · ${tl}`;
  document.getElementById('canvasInfo').textContent = `${fl}`;
}

// ── EXPORT ─────────────────────────────────────────────────────────────────────
async function exportar() {
  const nome = document.getElementById('nomeInput').value.trim();
  if (!nome) { toast('⚠ Digite o nome da pasta','err'); return; }
  document.getElementById('loadingBg').classList.add('show');
  document.getElementById('loadingSub').textContent = `Renderizando ${state.slides.length} slides...`;
  try {
    const r = await post('/export',{nome});
    document.getElementById('loadingBg').classList.remove('show');
    if (r.ok) toast(`✅ ${r.count} PNGs salvos em exports/${nome}/`,'ok');
    else toast('❌ '+(r.error||'Erro'),'err');
  } catch(e) {
    document.getElementById('loadingBg').classList.remove('show');
    toast('❌ Erro. Veja o terminal.','err');
  }
}

// ── UTILS ──────────────────────────────────────────────────────────────────────
async function post(url, body) {
  const r = await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  return r.json();
}
function toast(msg, type) {
  const t = document.getElementById('toast');
  t.textContent=msg; t.className='toast '+type; t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),5000);
}

init();
</script>
</body>
</html>"""

@app.route('/')
def index(): return UI

# ─── LAUNCH ────────────────────────────────────────────────────────────────────
def abrir():
    time.sleep(1.8)
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    print("\n╔══════════════════════════════════════╗")
    print("║   POST CREATOR v2  · @glendonassis  ║")
    print("╚══════════════════════════════════════╝")
    print(f"\n🌐 http://localhost:{PORT}")
    print("   Ctrl+C para encerrar\n")
    threading.Thread(target=abrir, daemon=True).start()
    app.run(port=PORT, debug=False, use_reloader=False)

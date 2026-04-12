
# 1. Fix FAQ body text no index.html (L780-781)
with open('C:/heillon_site_lc/index.html', encoding='utf-8') as f:
    c = f.read()

# Substituir o corpo do FAQ que ainda diz PWA/Companion
old_pt = 'É uma Progressive Web App (PWA) que monitoriza o sistema HEILLON em tempo real. Mostra decisões soberanas ao vivo, com veredicto, normas aplicadas e prova criptográfica. Inclui 3 análises gratuitas - você declara uma intenção e recebe um HDR real. Instale sem App Store em'
old_en = "It's a Progressive Web App (PWA) that monitors the HEILLON system in real time. Shows live sovereign decisions with verdict, applied norms, and cryptographic proof. Includes 3 free analyses - you declare an intent and receive a real HDR. Install without App Store at"

new_pt = 'É um agente soberano que corre no teu PC e monitoriza a actividade das IAs em tempo real. Detecta Cursor, Ollama, Manus, Cluely, Claude Desktop e mais. Cada acção é registada como um HDR imutável. Acesso gratuito 30 dias em'
new_en = "A sovereign agent running on your PC that monitors AI activity in real time. Detects Cursor, Ollama, Manus, Cluely, Claude Desktop and more. Every action is recorded as an immutable HDR. Free 30-day access at"

c2 = c.replace(old_pt, new_pt, 1)
c3 = c2.replace(old_en, new_en, 1)

changed1 = old_pt not in c3
changed2 = old_en not in c3
print(f'FAQ PT fixed: {changed1}')
print(f'FAQ EN fixed: {changed2}')
print(f'Companion still in index: {"Companion" in c3}')

with open('C:/heillon_site_lc/index.html', 'w', encoding='utf-8') as f:
    f.write(c3)
print('index.html saved')


# Substituir modal e script do portal com Passkey como entrada principal
import re

with open(r'C:\heillon_site_lc\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar CSS para o botao Passkey e divisor
NEW_CSS = '''
.portal-passkey-btn{width:100%;padding:1rem 1.2rem;background:rgba(201,168,76,0.1);color:#C9A84C;font-family:'DM Mono',monospace;font-size:.78rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;border:1px solid rgba(201,168,76,0.35);cursor:pointer;transition:all .25s;margin-bottom:.75rem;display:flex;align-items:center;justify-content:center;gap:.6rem}
.portal-passkey-btn:hover{background:rgba(201,168,76,0.18);border-color:rgba(201,168,76,0.6)}
.portal-passkey-btn:disabled{opacity:.35;cursor:not-allowed}
.portal-passkey-icon{font-size:1rem}
.portal-divider{display:flex;align-items:center;gap:.75rem;margin:.75rem 0;color:rgba(160,168,179,0.3);font-family:'DM Mono',monospace;font-size:.62rem;letter-spacing:.12em}
.portal-divider::before,.portal-divider::after{content:'';flex:1;height:1px;background:rgba(160,168,179,0.12)}
.portal-passkey-hint{font-family:'DM Mono',monospace;font-size:.62rem;color:rgba(160,168,179,0.4);text-align:center;margin-bottom:.5rem;letter-spacing:.06em}
'''

# Inserir CSS antes de .portal-btn
old_css = '.portal-btn{'
if old_css in content:
    content = content.replace(old_css, NEW_CSS + old_css, 1)
    print("CSS inserido OK")
else:
    print("CSS marker nao encontrado")

# 2. Substituir o corpo do modal (portal-body) para ter Passkey primeiro
OLD_BODY = '''      <div class="portal-body">
      <div class="portal-error" id="portal-error"></div>
      <div class="portal-input-wrap">
        <input type="text" class="portal-input" id="portal-code" placeholder="HEILLON-XXXX-XXXX" maxlength="18" autocomplete="off" oninput="formatCode(this)" onkeydown="if(event.key==='Enter')submitCode()">
      </div>
      <button class="portal-btn" id="portal-btn" onclick="submitCode()">
        <span class="lang-pt">Entrar →</span><span class="lang-en" style="display:none">Sign In →</span>
      </button>
      <p class="portal-note"><span class="lang-pt">Código fornecido pela HEILLON. Sem senha. Sem formulário.</span><span class="lang-en" style="display:none">Code provided by HEILLON. No password. No form.</span></p>
    </div>'''

NEW_BODY = '''      <div class="portal-body">
      <div class="portal-error" id="portal-error"></div>
      <!-- Passkey — entrada principal -->
      <p class="portal-passkey-hint" id="passkey-hint-pt">Toque para autenticar com Windows Hello, Touch ID ou Face ID.</p>
      <p class="portal-passkey-hint" id="passkey-hint-en" style="display:none">Tap to authenticate with Windows Hello, Touch ID or Face ID.</p>
      <button class="portal-passkey-btn" id="passkey-btn" onclick="runPasskeyLogin()">
        <span class="portal-passkey-icon">🔑</span>
        <span class="lang-pt">Entrar com Passkey</span><span class="lang-en" style="display:none">Sign in with Passkey</span>
      </button>
      <button class="portal-passkey-btn" id="passkey-register-btn" onclick="runPasskeyRegister()" style="font-size:.68rem;opacity:.7;margin-bottom:0">
        <span class="portal-passkey-icon">＋</span>
        <span class="lang-pt">Registar nova Passkey</span><span class="lang-en" style="display:none">Register new Passkey</span>
      </button>
      <!-- Divisor -->
      <div class="portal-divider"><span class="lang-pt">OU CÓDIGO SOBERANO</span><span class="lang-en" style="display:none">OR SOVEREIGN CODE</span></div>
      <!-- Fallback: código HEILLON -->
      <div class="portal-input-wrap">
        <input type="text" class="portal-input" id="portal-code" placeholder="HEILLON-XXXX-XXXX" maxlength="18" autocomplete="off" oninput="formatCode(this)" onkeydown="if(event.key==='Enter')submitCode()">
      </div>
      <button class="portal-btn" id="portal-btn" onclick="submitCode()">
        <span class="lang-pt">Entrar com código →</span><span class="lang-en" style="display:none">Sign in with code →</span>
      </button>
      <p class="portal-note"><span class="lang-pt">Sem senha. Sem formulário. Soberano.</span><span class="lang-en" style="display:none">No password. No form. Sovereign.</span></p>
    </div>'''

if OLD_BODY in content:
    content = content.replace(OLD_BODY, NEW_BODY, 1)
    print("Modal body substituido OK")
else:
    print("Modal body nao encontrado - verificar")

with open(r'C:\heillon_site_lc\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Ficheiro guardado")

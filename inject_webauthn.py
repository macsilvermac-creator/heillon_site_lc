
WEBAUTHN_SCRIPT = """

// ── WebAuthn / Passkey ─────────────────────────────────────────────────────
// SimpleWebAuthn browser library via CDN (ESM)
let _simpleWebAuthn = null;

async function _loadWebAuthn() {
  if (_simpleWebAuthn) return _simpleWebAuthn;
  try {
    _simpleWebAuthn = await import('https://cdn.jsdelivr.net/npm/@simplewebauthn/browser@13/+esm');
    return _simpleWebAuthn;
  } catch(e) {
    console.error('WebAuthn CDN load failed:', e);
    return null;
  }
}

function _setPasskeyBtns(loading) {
  const b1 = document.getElementById('passkey-btn');
  const b2 = document.getElementById('passkey-register-btn');
  if (b1) b1.disabled = loading;
  if (b2) b2.disabled = loading;
}

async function runPasskeyLogin() {
  const errEl = document.getElementById('portal-error');
  errEl.classList.remove('show');
  _setPasskeyBtns(true);
  const btn = document.getElementById('passkey-btn');
  const origHTML = btn ? btn.innerHTML : '';
  if (btn) btn.innerHTML = '<span>...</span>';

  try {
    const lib = await _loadWebAuthn();
    if (!lib) throw new Error('Biblioteca WebAuthn não disponível.');

    // Gerar opções de login
    const genRes = await fetch(BACKEND + '/auth/login/generate-options', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username: '' })
    });
    const genJson = await genRes.json();
    if (!genRes.ok) {
      const msg = genJson.detail || genJson.message || 'Erro ao iniciar Passkey.';
      throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    }
    const challengeId = genJson.challenge_id;
    if (!challengeId) throw new Error('challenge_id ausente na resposta.');

    // Activar autenticação no browser
    const credential = await lib.startAuthentication({ optionsJSON: genJson.options });

    // Verificar
    const verRes = await fetch(BACKEND + '/auth/login/verify', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ challenge_id: challengeId, credential })
    });
    const verJson = await verRes.json();
    if (!verRes.ok || !verJson.access_token) {
      const msg = verJson.detail || verJson.message || 'Passkey inválida.';
      throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    }

    // Sessão estabelecida
    _session = verJson;
    localStorage.setItem('heillon-session', JSON.stringify(verJson));
    closePortal();
    const role = verJson.persona_code || '';
    if (CC_ROLES.some(r => role.includes(r))) {
      window.open(CC_URL + '?token=' + verJson.access_token, '_blank');
      return;
    }
    renderDash();

  } catch(e) {
    const msg = e.message || String(e);
    if (msg.toLowerCase().includes('cancel') || msg.toLowerCase().includes('abort') || msg.toLowerCase().includes('user')) {
      errEl.textContent = 'Autenticação cancelada.';
    } else {
      errEl.textContent = msg.slice(0, 200);
    }
    errEl.classList.add('show');
  } finally {
    _setPasskeyBtns(false);
    if (btn) btn.innerHTML = origHTML;
  }
}

async function runPasskeyRegister() {
  const errEl = document.getElementById('portal-error');
  errEl.classList.remove('show');
  _setPasskeyBtns(true);
  const btn = document.getElementById('passkey-register-btn');
  const origHTML = btn ? btn.innerHTML : '';
  if (btn) btn.innerHTML = '<span>...</span>';

  // Pedir username para registo
  const username = window.prompt('Username para a Passkey (ex: marcelo@heillon.com):');
  if (!username || !username.trim()) {
    _setPasskeyBtns(false);
    if (btn) btn.innerHTML = origHTML;
    return;
  }

  try {
    const lib = await _loadWebAuthn();
    if (!lib) throw new Error('Biblioteca WebAuthn não disponível.');

    const genRes = await fetch(BACKEND + '/auth/register/generate-options', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username: username.trim(), display_name: username.trim() })
    });
    const genJson = await genRes.json();
    if (!genRes.ok) {
      const msg = genJson.detail || 'Erro ao iniciar registo.';
      throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    }
    const challengeId = genJson.challenge_id;
    if (!challengeId) throw new Error('challenge_id ausente.');

    const credential = await lib.startRegistration({ optionsJSON: genJson.options });

    const verRes = await fetch(BACKEND + '/auth/register/verify', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ challenge_id: challengeId, credential })
    });
    const verJson = await verRes.json();
    if (!verRes.ok || !verJson.access_token) {
      const msg = verJson.detail || 'Registo falhou.';
      throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    }

    // Registo + login automático
    _session = verJson;
    localStorage.setItem('heillon-session', JSON.stringify(verJson));
    closePortal();
    const role = verJson.persona_code || '';
    if (CC_ROLES.some(r => role.includes(r))) {
      window.open(CC_URL + '?token=' + verJson.access_token, '_blank');
      return;
    }
    renderDash();

  } catch(e) {
    const msg = e.message || String(e);
    if (msg.toLowerCase().includes('cancel') || msg.toLowerCase().includes('abort')) {
      errEl.textContent = 'Registo cancelado.';
    } else {
      errEl.textContent = msg.slice(0, 200);
    }
    errEl.classList.add('show');
  } finally {
    _setPasskeyBtns(false);
    if (btn) btn.innerHTML = origHTML;
  }
}
// ── fim WebAuthn ────────────────────────────────────────────────────────────
"""

with open(r'C:\heillon_site_lc\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Inserir antes do </script> final
marker = '\n</script>\n\n</body>'
if marker in content:
    content = content.replace(marker, WEBAUTHN_SCRIPT + marker, 1)
    print("Script WebAuthn inserido OK")
else:
    # Tentar variante sem newline duplo
    marker2 = '\n</script>\n</body>'
    if marker2 in content:
        content = content.replace(marker2, WEBAUTHN_SCRIPT + marker2, 1)
        print("Script WebAuthn inserido OK via marker2")
    else:
        print("Marker nao encontrado")
        # Ver os ultimos 50 chars antes de </body>
        idx = content.rfind('</body>')
        print(repr(content[idx-100:idx]))

with open(r'C:\heillon_site_lc\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Ficheiro guardado")

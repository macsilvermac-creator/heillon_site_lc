
with open('C:/heillon_site_lc/index.html', encoding='utf-8') as f:
    c = f.read()

# Adicionar link Terms ao footer
old = '<a href="/privacy.html" style="color:inherit;opacity:.6;text-decoration:none">Privacidade</a></p>'
new = '<a href="/privacy.html" style="color:inherit;opacity:.6;text-decoration:none">Privacidade</a> &middot; <a href="/terms.html" style="color:inherit;opacity:.6;text-decoration:none">Termos</a></p>'
c2 = c.replace(old, new, 1)

print('Terms link added:', 'terms.html' in c2)
print('Form present:',     'hln-contact' in c2)
print('Privacy present:',  'privacy.html' in c2)

with open('C:/heillon_site_lc/index.html', 'w', encoding='utf-8') as f:
    f.write(c2)
print('Saved OK')


with open(r'C:\heillon_site_lc\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix subtitle
old = 'Use seu c\u00f3digo soberano HEILLON-XXXX-XXXX para entrar.'
new = 'Autentique com Passkey ou use o seu c\u00f3digo soberano HEILLON-XXXX-XXXX.'
if old in content:
    content = content.replace(old, new, 1)
    print("Subtitle PT OK")

with open(r'C:\heillon_site_lc\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("OK")

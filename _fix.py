
with open('C:/heillon_site_lc/index.html', encoding='utf-8') as f:
    c = f.read()

old = '<a href="https://hpc.heillon.com" style="color:inherit;opacity:.6;text-decoration:none">HPC</a></p>'
new = '<a href="https://hpc.heillon.com" style="color:inherit;opacity:.6;text-decoration:none">HPC</a> &middot; <a href="/privacy.html" style="color:inherit;opacity:.6;text-decoration:none">Privacidade</a></p>'

c2 = c.replace(old, new, 1)
print('Privacy added:', 'privacy.html' in c2)
print('Form OK:', 'hln-contact' in c2)

with open('C:/heillon_site_lc/index.html', 'w', encoding='utf-8') as f:
    f.write(c2)
print('Saved')

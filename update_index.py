#!/usr/bin/env python3
"""重新產生 index.html（列出本目錄所有檔案）。

用法：
    python3 update_index.py          # 只更新 index.html
    python3 update_index.py --push   # 更新後 git add / commit / push
"""
import html
import os
import subprocess
import sys
import urllib.parse

BASE_URL = 'https://skhuang.github.io/ss/'
IMAGE_EXTS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
EXCLUDE = {'index.html', 'update_index.py'}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

files = sorted(
    f for f in os.listdir('.')
    if os.path.isfile(f) and not f.startswith('.') and f not in EXCLUDE
)

rows = []
for f in files:
    q = urllib.parse.quote(f)
    name = html.escape(f)
    ext = f.rsplit('.', 1)[-1].lower() if '.' in f else ''
    if ext in IMAGE_EXTS:
        rows.append(f'<li><a href="{q}">{name}</a><br>'
                    f'<a href="{q}"><img src="{q}" alt="{name}"></a></li>')
    elif ext in {'pptx', 'docx', 'xlsx', 'ppt', 'doc', 'xls'}:
        viewer = ('https://view.officeapps.live.com/op/view.aspx?src='
                  + urllib.parse.quote(BASE_URL + q, safe=''))
        rows.append(f'<li>{name}<br><a href="{viewer}" target="_blank">線上預覽</a>'
                    f' · <a href="{q}" download>下載</a></li>')
    else:
        rows.append(f'<li><a href="{q}">{name}</a></li>')

page = f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>檔案列表</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:860px;margin:2rem auto;padding:0 16px;line-height:1.6}}
li{{margin:1rem 0}} img{{max-width:100%;max-height:320px;margin-top:.4rem;border-radius:6px}}
</style></head><body>
<h1>檔案列表</h1>
<ul>
{chr(10).join(rows)}
</ul>
</body></html>
'''

with open('index.html', 'w', encoding='utf-8') as fh:
    fh.write(page)
print(f'index.html 已更新（{len(files)} 個檔案）')

if '--push' in sys.argv:
    subprocess.run(['git', 'add', '-A'], check=True)
    if subprocess.run(['git', 'diff', '--cached', '--quiet']).returncode == 0:
        print('沒有變更，不需 commit')
    else:
        subprocess.run(['git', 'commit', '-m', 'Update files and index'], check=True)
        subprocess.run(['git', 'push'], check=True)

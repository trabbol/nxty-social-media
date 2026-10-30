# Ripristino dell'area di lavoro nel container

Il 30/10/2026 il container di lavoro e' stato azzerato: `/home/claude/nxty` e lo scratchpad erano spariti,
mentre `/mnt/user-data/outputs` (le copie dei caricamenti) era rimasto. Se una regia o uno slot non trova
`/home/claude/nxty`, si ricostruisce cosi', prima di ogni altra cosa:

1. `mkdir -p /home/claude/nxty/demo` e `git clone https://github.com/trabbol/nxty-social-media.git /home/claude/nxty/repo`.
2. Copie di lavoro dal repository: `cp repo/posts.json repo/layout_usati.md repo/direttive.md /home/claude/nxty/`.
3. Logo e caratteri per i rendering: `cp repo/tools/logo_oro.png demo/`; in `demo` `npm init -y` e
   `npm install @fontsource/plus-jakarta-sans` (gli script cercano i file in `demo/node_modules/@fontsource/plus-jakarta-sans/files`).
4. `insights_history.json` NON e' nel repository (quello nella radice e' vecchio, fermo alla settimana 5, e non si usa):
   la copia buona e' sul PC, `C:\Users\fabia\Documents\NXTY INSTA\nxty_backup\insights_history.json`. Si porta nel container
   con device_stage_files e si copia in `/home/claude/nxty/insights_history.json`, controllando l'md5 con l'ultima chiusura.
5. La prova con la finta API ora sta nel repository: `python3 tools/prova_finta_api.py ID AAAA-MM-GG RID pubblicati.json cartella`
   (pubblicati.json preso da GitHub per SHA).
6. Gli script dei contenuti (reel_, audio_, caro_, batch_ e render_frames.py) sono tutti in `tools/` e si lanciano da li'.

Niente token nel container, mai: resta solo nel secret META_TOKEN e nel file di Alessandro.

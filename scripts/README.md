# scripts / スクリプト
Scripts that generate the figures, simulations, PDFs and READMEs are saved per version: `scripts/VER6/` (latest state, Python + Pillow only). Save a new folder `scripts/VERn/` with every release; never overwrite an older one.
図・シミュレーション・PDF・READMEを作るスクリプトを版ごとに保存します。新しい版を出すたびに `scripts/VERn/` を追加し、古い版は上書きしません。
Run: `python run_fig.py <fig_*_body.py> [height]`, then `compose_v5.py`, `build_manual.py`, `mk_readmes.py`. Paths inside point to the author's scratch folder; edit `SD` first.
Note: scripts of VER1-VER4 were not kept (overwritten while developing); `scripts/VER6` is the oldest kept state.

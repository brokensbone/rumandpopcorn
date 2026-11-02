# Source Sans 3

Locally served Latin subsets of the variable WOFF2 fonts from [Adobe’s Source Sans repository](https://github.com/adobe-fonts/source-sans), release commit `87b37a2daaed80fcb8e8ccb0085c4d72ddade12e`.

- `upright.woff2`: `WOFF2/VF/SourceSans3VF-Upright.ttf.woff2`
- `italic.woff2`: `WOFF2/VF/SourceSans3VF-Italic.ttf.woff2`

The subsets retain basic Latin, Latin-1, Latin Extended-A, combining accents, common punctuation, arrows, the euro and trademark symbols. Other characters use the CSS system-font fallbacks. The derived family is renamed **RNP Sans** because Adobe reserves the name “Source”. See `LICENSE.md` for the original copyright and SIL Open Font License.

Rebuild from the repository root:

```sh
uv run --with 'fonttools[woff]==4.68.0' python scripts/build-reading-fonts.py
```

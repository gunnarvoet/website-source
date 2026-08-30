#!/bin/sh
# Refresh the self-hosted webfonts in static/fonts/.
#
# The editorial theme self-hosts Archivo and IBM Plex Mono so the site has no
# runtime dependency on fonts.googleapis.com. This script asks the Google Fonts
# CSS API for the same faces the theme declares, keeps the latin and latin-ext
# subsets, and writes them next to this script. The @font-face rules live in
# assets/css/editorial.css and are hand-maintained; if a rebuilt font changes
# its axes or weights, update them there too.
#
# Run from inside themes/editorial/:   sh fetch-fonts.sh
set -eu

# A modern user agent is what makes the API return woff2 rather than ttf.
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
API='https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=IBM+Plex+Mono:wght@400;500&display=swap'

cd "$(dirname "$0")"
mkdir -p static/fonts

# Flatten the response into (subset, family, weight, url) records. \047 is an
# apostrophe, which cannot be written literally inside this awk program.
curl -sSf -A "$UA" "$API" | awk '
  /^\/\* /       { subset = $2 }
  /font-family:/ { if (match($0, /\047[^\047]+\047/)) fam = substr($0, RSTART + 1, RLENGTH - 2) }
  /font-weight:/ { wt = $2; sub(/;/, "", wt); sub(/ .*/, "", wt) }
  /src: *url\(/  { url = $0; sub(/.*url\(/, "", url); sub(/\).*/, "", url)
                   print subset "\t" fam "\t" wt "\t" url }
' | while IFS='	' read -r subset fam wt url; do
  # Only the subsets the site actually sets type in.
  case "$subset" in latin|latin-ext) ;; *) continue ;; esac
  case "$fam" in
    Archivo)         out="archivo-$subset.woff2" ;;          # one variable file, every weight and width
    "IBM Plex Mono") out="ibm-plex-mono-$wt-$subset.woff2" ;;
    *) continue ;;
  esac
  curl -sSf -o "static/fonts/$out" "$url"
  printf '  %-32s %s\n' "$out" "$url"
done

echo
ls -lh static/fonts/*.woff2
echo
echo 'Archivo and IBM Plex Mono are both under the SIL Open Font License 1.1;'
echo 'static/fonts/OFL.txt carries the license text. Keep it beside the fonts.'

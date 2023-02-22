#!/bin/sh
# shellcheck disable=SC3003

help="\
hw2.sh -i INPUT -o OUTPUT [-c csv|tsv] [-j]

Available Options:

-i: Input file to be decoded
-o: Output directory
-c csv|tsv: Output files.[ct]sv
-j: Output info.json"

while getopts i:o:c:j op 2>/dev/null; do
  case $op in
    i)
      input=$OPTARG
      ;;
    o)
      output=$OPTARG
      ;;
    c)
      XSV=$OPTARG
      if [ "$XSV" = "tsv" ]; then XSVSPL=$'\t'; fi
      if [ "$XSV" = "csv" ]; then XSVSPL=','; fi
      ;;
    j)
      infojson=1
      ;;
    *)
      >&2 echo "$help"
      exit 255
  esac
done

if [ ! "${input}" ] || [ "${input}" != "${input%\.hw2}.hw2" ] && false; then
  >&2 echo "Input file must end with .hw2 ($input)"
  >&2 echo "$help"
  exit 255
fi

mkdir -p "${output}"
if [ ! "${output}" ] || [ ! -d "${output}" ]; then
  >&2 echo "Output not directory ($output)"
  >&2 echo "$help"
  exit 255
fi

if [ "$infojson" ]; then
  name=$(jq -r '.name' "${input}")
  author=$(jq -r '.author' "${input}")
  date=$(jq -r '.date' "${input}")
  date=$(date -r "$date" -Iseconds)
  jq -r -n "{\"name\":\"$name\",\"author\":\"$author\",\"date\":\"$date\"}"  > "$output/info.json"
fi

if [ "$XSVSPL" ]; then
  echo "filename${XSVSPL}size${XSVSPL}md5${XSVSPL}sha1" > "$output/files.$XSV"
fi

error_files=$(
  jq -r '.files[] | [.name, .type, .data, .hash.md5, .hash["sha-1"]] | @tsv' "${input}" |
    while IFS=$'\t' read -r fn _ data md5 sha1; do
      f="$output/$fn"
      mkdir -p "$(dirname "$f")"
      size=$(echo "$data" | base64 -d | tee "$f" | wc -c | tr -d ' ')

      if [ "$XSVSPL" ]; then
        echo "$fn${XSVSPL}$size${XSVSPL}$md5${XSVSPL}$sha1" >> "$output/files.$XSV"
      fi

      if [ "$md5" != "$(md5sum -q "$f")" ] || [ "$sha1" != "$(sha1sum -q "$f")" ]; then
        # rm "$f"
        error_files=$((error_files+1))
        echo "$f"
      fi
    done |
  wc -l
)

# shellcheck disable=SC2086
exit $error_files

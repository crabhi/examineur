#!/bin/bash
set -e

TEST_SCRIPT=ica1_training.py
DOCKER_NET=internal
SRC_FOLDER=/home/krab/Downloads/ica1_training/

test_one () {
    sudo docker run \
        --rm -it \
        --net="$DOCKER_NET" \
        -v "$(pwd "$(dirname "$TEST_SCRIPT")")":/scriptdir:ro \
        -v "$(pwd "$(dirname "$1")")":/nbdir:ro \
        crabhi/examineur \
        /scriptdir/"$(basename "$TEST_SCRIPT")" \
        /nbdir/"$(basename "$1")" \
        -- \
        -v
}

rm -f "$SRC_FOLDER"/*.ipynb.log

if ! sudo docker network inspect "$DOCKER_NET" 2>/dev/null >/dev/null; then
    sudo docker network create --internal "$DOCKER_NET"
fi


for file in "$SRC_FOLDER"/*.ipynb; do
    outfile="$(mktemp)"
    if test_one "$file" > "$outfile"; then
        NAME=PASS
    else
        NAME=FAIL
    fi

    mv "$outfile" "$SRC_FOLDER"/"$NAME"_"$(basename "$file")".log
done

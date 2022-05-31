#!/bin/bash
uai_file="$3/vmodel-$1.uai"
mkdir temp
bash convert_uai.sh -i "${uai_file}" -o "./temp" -n 30

#!/bin/bash
while getopts "hu:m:o:" opt; do
  case ${opt} in
    h )
      echo "Usage: ./ -n bn.net -d df.odd -m constraints.txt"
      echo "	-n <filename>: Input Bayesian network file (HUGIN .net format)"
      echo "	-o <dirname>: Output directory"
      exit 0
      ;;
    m )
      constraint=$OPTARG;;
    u )
      uai_file=$OPTARG;;
    o )
      out_dir=$OPTARG;;
  esac
done
python uai_to_net.py -u $uai_file -o $out_dir
cd ..
new_out_dir="${OLDPWD}/${out_dir}"
bash obtain_joint_cnf.sh -n "${new_out_dir}/model.net" -d "${new_out_dir}/fake.odd" -m $constraint -o $new_out_dir -t
./c2d_linux -in "${new_out_dir}/combined.cnf" -dt_method 3

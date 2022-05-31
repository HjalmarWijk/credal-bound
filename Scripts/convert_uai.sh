#!/bin/bash
while getopts "hu:m:o:n:" opt; do
  case ${opt} in
    h )
      echo "Usage: ./ -n bn.net -d df.odd -m constraints.txt"
      echo "	-n <filename>: Input Bayesian network file (HUGIN .net format)"
      echo "	-o <dirname>: Output directory"
      exit 0
      ;;
    u )
      uai_file=$OPTARG;;
    o )
      out_dir=$OPTARG;;
    n )
      num_ordering=$OPTARG;;
  esac
done
python uai_to_net.py -u $uai_file -o $out_dir
order_dir="${out_dir}/orders"
python create_orderings.py -i $uai_file -o $order_dir -l $num_ordering
orders="${order_dir}/*"
i=0
for order in $orders
do
  new_out_dir="${out_dir}/order$i"
  mkdir $new_out_dir
  bash obtain_joint_cnf.sh -n "${out_dir}/model.net" -d "${out_dir}/fake.odd" -m "${order_dir}/order$i.txt" -o $new_out_dir -t
  ./c2d_linux -in "${new_out_dir}/combined.cnf" -dt_method 3
  i=i+1
od


import argparse
from credalbound.IO import read_uai_verts, write_net

parser = argparse.ArgumentParser(description='UAI to HUGIN (.net) converter')

parser.add_argument("-u", "--uai", help="UAI file name", default="model.uai")

parser.add_argument("-o", "--outdir", default = "uai_gen")

args = parser.parse_args()

filename = args.uai
out_dir = args.outdir
outfile = out_dir+"/model.net"
oddfile = out_dir+"/fake.odd"

domsizes, parents, _ = read_uai_verts(filename)
write_net(outfile, oddfile, domsizes, parents)





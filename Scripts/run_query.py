import argparse

parser = argparse.ArgumentParser(description='Convert to SPN and compute bounds')
parser.add_argument("-in", "--in_dir")
parser.add_argument("-u", "--uai")
parser.add_argument("-w", "--write_file", default=None)
parser.add_argument("-l", "--log", default=False, action='store_true')
parser.add_argument("-t", "--target", default=0)
parser.add_argument("-y", "--observed", default="")
args = parser.parse_args()

from credalbound.compilation import compile_SPN
from credalbound import lower_bound


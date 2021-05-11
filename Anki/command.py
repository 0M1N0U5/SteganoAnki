import argparse
import argparse, os

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

parser = argparse.ArgumentParser(description='Anki Stegotools.')
parser.add_argument('-r',metavar='route',dest='route', type=dir_path, nargs=1, action='store',
                    help='path of the group of cards',required=True)
parser.add_argument('-s',metavar='secret', dest='secret', type=str, nargs=1, action='store',
                    help='secret to hide',required=True)
parser.add_argument('-p',metavar='password', dest='password', type=str, nargs=1, action='store',
                    help='password to encode/decode',required=True)
parser.add_argument('-m', dest='mode', metavar='mode <0|1|2> ',choices=['0', '1', '2'],
                    help='Mode chosen: stego in image=0 or stego in text=1 or stego in flags=2',required=True)
parser.add_argument('-e',dest='estimate', action='store_true',help='Add it to activate it: estimation of capacity')

args = parser.parse_args()
if args.estimate:
    print("Estimation turned on")

if args.mode=='0':
    print("Mode Stego in image turned on")
elif args.mode=='1':
    print("Mode Stego in text turned on")
elif args.mode=='2':
    print("Mode Stego in Flags turned on")



import argparse, os

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def logo():
    print("")
    print("""\
    .d88888b    dP                                                 .d888888           dP       oo 
    88.    "'   88                                                d8'    88           88          
    `Y88888b. d8888P .d8888b. .d8888b. .d8888b. 88d888b. .d8888b. 88aaaaa88a 88d888b. 88  .dP  dP 
        `8b   88   88ooood8 88'  `88 88'  `88 88'  `88 88'  `88 88     88  88'  `88 88888"   88 
    d8'   .8P   88   88.  ... 88.  .88 88.  .88 88    88 88.  .88 88     88  88    88 88  `8b. 88 
    Y88888P    dP   `88888P' `8888P88 `88888P8 dP    dP `88888P' 88     88  dP    dP dP   `YP dP 
                                .88                                                            
                            d8888P                                                             

    """)

logo()

parser = argparse.ArgumentParser(description='Anki Stegotools.')
parser.add_argument('-r',metavar='route',dest='route', type=dir_path, nargs=1, action='store',
                    help='path of the group of cards',required=True)
parser.add_argument('-s',metavar='secret', dest='secret', type=str, nargs=1, action='store',
                    help='secret to hide',required=True)
parser.add_argument('-p',metavar='password', dest='password', type=str, nargs=1, action='store',
                    help='password to encode/decode',required=True)
parser.add_argument('-m', dest='mode', metavar='mode <0|1> ',choices=['0', '1'],
                    help='Mode chosen: stego in image=0 or stego in flags=1',required=True)
parser.add_argument('-e',dest='estimate', action='store_true',help='Add it to activate it: estimation of capacity')

args = parser.parse_args()



def main():
    if args.estimate:
        print("Estimation turned on")
    if args.mode=='0':
        print("Mode Stego in image turned on")
    elif args.mode=='1':
        print("Mode Stego in text turned on")
    elif args.mode=='2':
        print("Mode Stego in Flags turned on")
    logo()

logo()
#main()
import argparse, os

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

parser = argparse.ArgumentParser(description='Anki Stegotools.')
#parser.add_argument('-m', dest='mode', metavar='mode <enc|dec|est> ',choices=['enc', 'dec','est'],
#                    help='Mode chosen: encode=enc or decode=dec or estimate=est',required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--enc', action='store_true',dest='enc',help='encode mode of operation',action='store_true')
group.add_argument('--dec',action='store_true',dest='dec',help='decode mode of operation')
group.add_argument('--est',action='store_true',dest='est',help='estimation mode of operation')
parser.add_argument('-c', dest='cover', metavar='cover <0|1|2> ',choices=['0', '1','2'],
                    help='Cover chosen: stego in image=0 or stego in flags=1 or both=2',required=True)

subparser = parser.add_subparsers(dest='command')

encode = subparser.add_parser('enc')
encode.add_argument('-d',metavar='deck',dest='encDeck', type=str, action='store',
                    help='deck of the group of cards',required=True)
encode.add_argument('-s',metavar='secret', dest='encSecret', type=str, action='store',
                    help='secret to hide',required=True)
encode.add_argument('-p',metavar='password', dest='encPassword', type=str, action='store',
                    help='password to encode/decode',required=True)
encode.add_argument('-e',dest='encEstimate', action='store_true',help='Add it to activate it: estimation of capacity')

decode = subparser.add_parser('dec')
decode.add_argument('-d',metavar='deck',dest='decDeck', type=str, action='store',
                    help='deck of the group of cards',required=True)
decode.add_argument('-p',metavar='password', dest='decPassword', type=str, action='store',
                    help='password to encode/decode',required=True)

estimation = subparser.add_parser('est')
estimation.add_argument('-d',metavar='deck',dest='estDeck', type=str, action='store',
                    help='deck of the group of cards',required=True)
estimation.add_argument('-o',metavar='output', dest='estOutput', type=str, action='store',
                    help='output file to keep estimation calculation')

args = parser.parse_args()

def main():
    logo()
print(args.command)
if args.command == '--enc':
  print('Encode mode on. Enter commands: -d deck -s secret -p password [-e estimation]')
elif args.command == '--dec':
    print('Decode mode on. Enter commands: -d deck -p password')
elif args.command == '--est':
    print('Estimation mode on. Enter commands: -d deck [-o output]')

    #Transform to object for the orquestador
    print(vars(args))
main()
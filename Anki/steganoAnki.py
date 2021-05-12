import argparse, sys
import orquestador

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

parser = argparse.ArgumentParser(description='Anki Stegano Tools.')
subparser = parser.add_subparsers(required=True, dest="mode")
encodeGroup = subparser.add_parser('enc')
decodeGroup = subparser.add_parser('dec')
estimateGroup = subparser.add_parser('est')

encodeGroup.add_argument('-d',metavar='deck',dest='nameDeck', type=str, action='store', help='deck of the group of cards',required=True)
encodeGroup.add_argument('-s',metavar='source', dest='data', type=str, action='store', help='secret to hide, it can be a file route',required=True)
encodeGroup.add_argument('-p',metavar='password', dest='password', type=str, action='store', help='password to encode',required=True)
encodeGroup.add_argument('-m',metavar='media', dest='media', default=False, action='store', help='preestimated media file path')
#encodeGroup.add_argument('-c', dest='cover', metavar='cover <0|1|2> ',choices=['0','1','2'], help='Cover chosen: stego in image=0 or stego in flags=1 or both=2',required=True)

decodeGroup.add_argument('-d',metavar='deck',dest='nameDeck', type=str, action='store', help='deck of the group of cards',required=True)
decodeGroup.add_argument('-p',metavar='password', dest='password', type=str, action='store', help='password to decode',required=True)
#decodeGroup.add_argument('-c', dest='cover', metavar='cover <0|1|2> ',choices=['0','1','2'], help='Cover chosen: stego in image=0 or stego in flags=1 or both=2',required=True)

estimateGroup.add_argument('-d',metavar='deck',dest='nameDeck', type=str, action='store', help='deck of the group of cards',required=True)
estimateGroup.add_argument('-o',metavar='output', dest='outputMedia', default=False, type=str, action='store', help='Write estimated media into file')
#estimateGroup.add_argument('-c', dest='cover', metavar='cover <0|1|2> ',choices=['0','1','2'], help='Cover chosen: stego in image=0 or stego in flags=1 or both=2',required=True)

logo()
if len(sys.argv) <= 1:
    parser.print_help()
else:
    args = parser.parse_args()
    print(args)
    orquestador.call(vars(args))
exit(0)
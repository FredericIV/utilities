#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('field', action='store', type=str, help='Field to be evaluated for generating the barcode.')
parser.add_argument('-t', '--type', action='store', type=str, choices=['code128c'], default='code128c', help='Barcode symbology to generate. Only code128c is supported at the moment. Defaults to code128c.')
parser.add_argument('-n', '--numchars', action='store', type=int, default=8, help='Number of characters in barcode. Code128c supports only even numbers. Defaults to 8.')
parser.add_argument('-p', '--padding', action='store', type=str, default='0', help='Padding character. Ensure the character is supported by the symbology. Defaults to 0.')
parser.add_argument('-d', '--paddingDirection', action='store', type=str, choices=['left', 'right'], default='left', help='Direction to pad barcode. Defaults to left.')
args = parser.parse_args()

symbologyLookup = dict()
symbologyLookup['code128c']='''"00","Â","01","!","02",CHAR(34),"03","#","04","$","05","%","06","&","07","'","08","(","09",")","10","*","11","+","12",CHAR(44),"13","-","14",".","15","/","16","0","17","1","18","2","19","3","20","4","21","5","22","6","23","7","24","8","25","9","26",":","27",";","28","<","29","=","30",">","31","?","32","@","33","A","34","B","35","C","36","D","37","E","38","F","39","G","40","H","41","I","42","J","43","K","44","L","45","M","46","N","47","O","48","P","49","Q","50","R","51","S","52","T","53","U","54","V","55","W","56","X","57","Y","58","Z","59","[","60",CHAR(92),"61","]","62","^","63","_","64","`","65","a","66","b","67","c","68","d","69","e","70","f","71","g","72","h","73","i","74","j","75","k","76","l","77","m","78","n","79","o","80","p","81","q","82","r","83","s","84","t","85","u","86","v","87","w","88","x","89","y","90","z","91","{","92","|","93","}","94","~","95","Ã","96","Ä","97","Å","98","Æ","99","Ç"'''.split(',')


def choose(stringar:list, ifer:str) -> str:
  retval = " CHOOSE("+ifer+"+1,"
  for i in range(1, len(stringar), 2):
    retval = retval + stringar[i]
    retval = retval + (',' if i!=(len(stringar)-1) else ')')
  return retval

def broken(stringar:list, ifer:str) -> str:
  return 'IF(VALUE(' + ifer + ')<50, IF(VALUE(' + ifer + ')<25,' + choose(stringar[:50], ifer='VALUE('+ifer+')') + ',' + choose(stringar[50:100], ifer='VALUE('+ifer+')-25') + '),IF(VALUE(' + ifer + ')<75,' + choose(stringar[100:150], ifer='VALUE('+ifer+')-50') + ',' + choose(stringar[150:200], ifer='VALUE('+ifer+')-75') + '))'

def modgen(numchars:int, field:str) -> str:
  retval = " MOD(105+"
  for i in range(1, int(numchars/2)+1):
    retval = retval + "MID("+field+","+str(i+i-1)+",2)"+"*"+str(i)
    retval = retval + ('+' if i!=int(numchars/2) else ', 103)')
  return retval

if args.paddingDirection == 'left':
  field='REPT('+args.padding+','+str(args.numchars)+'-LEN('+args.field+'))&'+args.field
else:
  field=args.field+'&REPT('+args.padding+','+str(args.numchars)+'-LEN('+args.field+'))'

match args.type:
  case 'code128a':
    retval = '="Ë"&'
  case 'code128b':
    retval = '="Ì"&'
  case 'code128c':
    if(args.numchars %2 != 0):
      raise ValueError('Odd number of characters given for code128c: '+str(args.numchars))
    retval = '="Í"&'


for i in range(1, args.numchars, 2):
  retval = retval + broken(symbologyLookup[args.type], ifer="MID("+field+", "+str(i)+",2)") + '&'

retval = retval + broken(symbologyLookup[args.type], ifer=modgen(numchars=args.numchars, field=field)) + '&'
retval = retval + '"Î"'
print (retval)

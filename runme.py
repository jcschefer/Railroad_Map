# Jack Schefer, began 7/30/16
#
from subprocess import call
from sys        import argv
#
def main():
   #
   # 1. call the printer to write the js resource file
   args = ['python3', 'printer.py'] + argv
   call(args)
   #
   # 2. call the map. TODO change this for your browser of choice
   args = ['firefox', 'map.html']
   call(args)
   #
#
################################################################
#
if __name__ == '__main__':
   #
   main()
   #
#
# End of file

# Jack Schefer, began 7/30/16
#
from subprocess import call
from sys        import argv
#
def main():
   #
   # 1. call the printer to write the js resource file
   args = ['python3', 'printer.py'] + argv[1:]
   call(args)
   #
   # 2. call the map. TODO change this for your browser of choice
   args = ['firefox', 'map.html']
   call(args)
   #
   # 3. remove the temporary resource file after everything is done
   args = ['rm js_resources.js']
   call(args, shell = True)
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

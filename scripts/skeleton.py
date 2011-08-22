import os
import sys
import shutil


class SkeletonTools(object):

	args = []
	operations = set('install')

	def install(self, root, name=None):

		''' Copy the project skeleton. '''
		
		
	
	
	
def main(args):
	
	s = SkeletonTools()
	if args[0] in s.operations:
		fn_result = getattr(s, args[0])(*args[1:])
	else:
		print "NO FN '"+str(args[0])+"'"
	exit()

if __name__ == '__main__':
	main(sys.argv)
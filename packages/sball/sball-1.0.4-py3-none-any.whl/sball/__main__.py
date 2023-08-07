# __main__.py

import sys

from .sball import sbatch_all

def main():
	'''
	Run sbatch_all to submit scripts matching
	a glob expression as job arrays using Yale's dSQ.
	'''
	args = [arg for arg in sys.argv[1:] if not 'sball' in arg]
	sbatch_all(args)

if __name__ == '__main__':
	main()
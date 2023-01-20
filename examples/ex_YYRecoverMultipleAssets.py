#!/usr/bin/python3.9

# Example for recovering multiple assets from a GMS2 project
# For this example, provide paths to the assets separated by a space

from personal_gamedev_asset_tools import yy_recover_single
from sys import argv

def main():
	path_col=argv[1:]
	for p in path_col:
		res=yy_recover_single(".",p)
		print("\nRecovery results:",res)

main()

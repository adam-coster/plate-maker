# PLATEMAKER
# by Adam D. Coster <software@adamcoster.com>
# Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# http://creativecommons.org/licenses/by-sa/4.0/deed.en_US
#
# PURPOSE
# To rapidly create a CSV file annotating
# a microwell plate.
#
# ALGORITHM
# 1. Choose plate type
# 2. Set well boundaries
# 3. Annotate wells

import re

def getPlateType():
    types = ['96','384']
    print('Choose plate type:')
    for ti, ty in enumerate(types):
        print('(', ti ,') ', ty )
    choice = int(input(''))
    if choice-1 >= len(types):
        print('Choice out of bounds.')
        return getPlateType()
    return types[ choice ]

def main():
    
    # Choose plate type
    plateType = getPlateType()
    print(plateType)
    
if __name__ == '__main__':
    main()
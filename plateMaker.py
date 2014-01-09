# PLATEMAKER
# by Adam D. Coster <software@adamcoster.com>
# 2014 GPLv3
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
    print('Choose plate type: ')
    for ti, ty in enumerate(types):
        print('(', ti ,') ', ty )
    choice = int(input(''))
    if choice-1 >= len(types):
        print('Choice out of bounds.')
        return getPlateType()
    return types[ choice ]

def getPlateRows( plateType ):
    endRow = {'96':'H','384':'P'}[plateType]
    rows   = [chr(let) for let in range(65,ord(endRow)+1)]
    return rows

def getPlateCols( plateType ):
    endCol = {'96':12,'384':24}[plateType]
    cols   = [str(i) for i in range(1,endCol+1)]
    return cols

def displayPlate( rows, cols, selection=[] ):
    print( ' ' + ''.join([c.rjust(2) for c in cols]) ) 
    for row in rows:
        line = row
        selectionsInRow = [s for s in selection if s[0] == row]
        selectionCols   = [s[1:] for s in selectionsInRow]
        for s in cols:
            if s in selectionCols:
                line += ' X'
            else:
                line += '  '
        print(line)
    return True

def yesNoBoolean( question, emptyResponse=False ):
    answer = input( question )
    if len(answer) == 0:
        return emptyResponse
    shorthand = answer[0].upper()
    return {'Y':True}.get(shorthand,False)
    
def getLimits( superset, question ):
    limits = []
    limitsInput = input(question).upper().strip()
    subsets = limitsInput.strip().split(' ')
    for subset in subsets:
        if subset in superset:
            limits += subset
        elif subset.find('-')>-1:
            # Will need to create a range
            ends  = subset.split('-')
            start = superset.index(ends[0])
            end   = superset.index(ends[1])
            limits += superset[start:end+1]
    # Sort them to deal with middle-zeros (if present)
    limits = [ l.zfill(2) for l in limits ]
    limits = sorted(limits)
    limits = [re.sub(r'0([\d\w])$',r'\1',l) for l in limits]
    return limits

def expandWellInput( rows, cols, message ):
    allWells = [r+c for r in rows for c in cols]
    rawInput = input( message ).strip().upper()
    if rawInput == 'ALL': return allWells
    if rawInput == '':    return []
    
    wellSets = rawInput.split(' ')
    
    # Allowed input formats are row, row-row, col, col-col,
    # rowcol, rowcol-rowcol
    # special keywords: all
    rowColRegex = r'^([A-Z]{0,1})(\d{0,2})-{0,1}([A-Z]{0,1})(\d{0,2})$'
    wellSubset = []
    for wellSet in wellSets:
        if wellSet == 'ALL': return allWells
        
        # Break into row and column parts
        try:
            rowStart, colStart, rowEnd, colEnd = re.match(rowColRegex,wellSet).groups()
        except:
            input('Something was wrong with your input.')
            exit()
        

        # Fill out the missing values
        if rowEnd   == '':
            if rowStart=='':
                rowStart = rows[0]
                rowEnd   = rows[-1] 
            else:
                rowEnd = rowStart

        if colEnd   == '':
            if colStart=='':
                colStart = cols[0]
                colEnd   = cols[-1] 
            else:
                colEnd = colStart
        
        subRows = [chr(r) for r in range(ord(rowStart),ord(rowEnd)+1)]
        subCols = [str(c) for c in range(int(colStart),int(colEnd)+1)]
        
        subWells = [r+c for r in subRows for c in subCols if r in rows and c in cols ]
        wellSubset += subWells
        
    return wellSubset
            
def main():
    
    # Choose plate type
    plateType = getPlateType()
    
    # For this plate type, get the set of
    # possible wells
    plateRows = getPlateRows( plateType )
    plateCols = getPlateCols( plateType )
    
    displayPlate( plateRows, plateCols )
    
    # Store annotations is dict of dicts
    # {well:{field:value,...},...}
    annotations = {}
    annotationFields = []
    
    # Allow for annotating limited subsets
    while True:
        experimentName = input( 'Experiment name: ' )
        
        if experimentName.upper() in ['','QUIT','Q','EXIT']: break
        
        setLimits = yesNoBoolean( 'Limit to a subset of wells? ', False )
        if not setLimits:
            rows, cols = (plateRows,plateCols)
        else:
            rows = getLimits(plateRows,'Rows (e.g. "a-d", "b d f-h"): ')
            cols = getLimits(plateCols,'Cols (e.g. "1-3", "2 4 6-9"): ')

        allWells = [r+c for r in rows for c in cols]
        annotations.update({w:{'experiment':experimentName} for w in allWells})
        
        print( experimentName + ' occurs only in the following wells:')
        
        # Now that we have boundaries,
        # allow for more complex selections
        # within. For each selection, add
        # annotations.
        while True:
            displayPlate(plateRows,plateCols,allWells)
            wells = expandWellInput( rows, cols, 'Wells to annotate: ' )
            if len(wells) == 0: break
            
            print('You have selected the following wells:')

            while True:
                displayPlate( plateRows, plateCols, wells )
                field = input('Field: ').strip()
                if field.upper() in ['QUIT','EXIT','Q','']: break
                annotationFields += field
                
                value = input('Value: ').strip()
                for well in wells:
                    annotations[well][field] = value
                    
        # Should now have complete set of annotations
    savename = input('File savename: ').strip() + '.csv'
    save = open(savename,'w')
    save.write('well,' + ','.join(annotationFields) + '\n' )
    for well in annotations.keys():
        save.write( well + ',' )
        values = [annotations[well].get(field,'') for field in annotationFields]
        save.write( ','.join(values) + '\n' )
    save.close()
    
if __name__ == '__main__':
    main()
from optparse import OptionParser    # parse command-line parameters
from apriori import Apriori

if __name__ == '__main__':
    
    # Parsing command-line parameters
    optParser = OptionParser()
    optParser.add_option('-f', '--file', 
                         dest='filePath',
                         help='Input a text file',
                         type='string',
                         default='./categories.txt')  # input a text file
                         
    optParser.add_option('-s', '--minSup', 
                         dest='minSup',
                         help='Mininum support',
                         type='float',
                         default=0.01)  # mininum support value 
                         
    optParser.add_option('-n', '--fname', dest='fname',
                         help='file name',
                         type='string',
                         default='patterns.txt')  # name file to save all-term freq

    (options, args) = optParser.parse_args()       
        
    # Get parameters
    filePath = options.filePath
    minSup  = options.minSup
    fname = options.fname
    print("""Parameters: \n - filePath: {} \n - mininum support: {} \n - save file name: {} \n""".\
          format(filePath,minSup,fname))

    # Run and save
    objApriori = Apriori(minSup)
    itemCountDict, freqSet = objApriori.fit(filePath)
    with open(fname,"w+") as f:
        for key, values in freqSet.items():
            for var in values:
                line = ';'.join([x for x in var])
                line = '{}:'.format(itemCountDict[var])+line +'\n'
                f.write(line) 
    print("Save done!")        
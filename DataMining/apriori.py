from collections import defaultdict


class Apriori(object):
    def __init__(self, minSup):
        """ Parameters setting
        """
        self.minSup = minSup  # min support

    def fit(self, filePath):
        """ Run the apriori algorithm, return the frequent all-term sets. 
        """
        # Initialize some variables to hold the tmp result
        transListSet  = self.getTransListSet(filePath)   # get transactions
        itemSet       = self.getOneItemSet(transListSet) # get 1-item set
        itemCountDict = defaultdict(int)         # key=candiate k-item, value=count
        freqSet       = dict()                   # a dict store all frequent all-items set
        
        self.transLength = len(transListSet)     # number of transactions
        self.itemSet     = itemSet
        
        # Get the frequent 1-term set
        freqOneTermSet = self.getItemsWithMinSup(transListSet, itemSet, 
                                             itemCountDict, self.minSup)

        # Loop
        k = 1
        currFreqTermSet = freqOneTermSet
        while currFreqTermSet != set():
            freqSet[k] = currFreqTermSet  # save the result
            k += 1
            currCandiItemSet = self.getJoinedItemSet(currFreqTermSet, k) # get new candiate k-terms set
            currFreqTermSet  = self.getItemsWithMinSup(transListSet, currCandiItemSet, 
                                                   itemCountDict, self.minSup) # frequent k-terms set
            
        self.itemCountDict = itemCountDict # All candidates and the number of occurrences (not just frequent items) are used to calculate confidence
        self.freqSet       = freqSet       # Only frequent items(a dict: freqSet[1] indicate frequent 1-term set )
        return itemCountDict, freqSet
    
        
    def getJoinedItemSet(self, termSet, k):
        """ Generate new k-terms candiate itemset"""
        return set([term1.union(term2) for term1 in termSet for term2 in termSet 
                    if len(term1.union(term2))==k])
    
        
    def getOneItemSet(self, transListSet):
        """ Get unique 1-item set in 'set' format 
        """
        itemSet = set()
        for line in transListSet:
            for item in line:
                itemSet.add(frozenset([item]))
        return itemSet
        
    
    def getTransListSet(self, filePath):
        """ Get transactions in list format 
        """
        transListSet = []
        with open(filePath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                transListSet.append(set(sorted(line[:-1].split(';')))) 

        return transListSet
                    
    def getItemsWithMinSup(self, transListSet, itemSet, freqSet, minSup):
        """ Get frequent item set using min support
        """
        itemSet_  = set()
        localSet_ = defaultdict(int)
        for item in itemSet:
            freqSet[item]   += sum([1 for trans in transListSet if item.issubset(trans)])
            localSet_[item] += sum([1 for trans in transListSet if item.issubset(trans)])
        
        # Only conserve frequent item-set 
        n = len(transListSet)
        for item, cnt in localSet_.items():
            itemSet_.add(item) if float(cnt)/n >= minSup else None

        return itemSet_
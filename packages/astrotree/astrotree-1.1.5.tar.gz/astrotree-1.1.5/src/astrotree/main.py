from .adstree import *
import treelib as tl
import argparse as ap


def treePlot(rootID, rootTitle, citeList, titleList, treeObj=''):

    if isEmpty(treeObj): tree = tl.Tree()
    else: tree = treeObj

    
    rootNodeName =  '[{id}] '.format(id=rootID)+rootTitle
    try: tree.create_node(tag=rootNodeName, identifier=rootID, parent=None)
    except: pass

    for i, (id, title) in enumerate(zip(citeList, titleList)):

        if title is not None and id is not None:
            nodeName =  '[{id}] '.format(id=id)+title
            
            node_added = False
            j = 0
            while not node_added:
                try: 
                    tree.create_node(tag=nodeName, identifier=id+'x'*j, parent=rootID)
                    node_added = True
                except:
                    j+=1
                    continue

        else: tree.create_node(tag='NONE', parent=rootID)

    return tree
    


def build_reference_tree(rootID):

    exit_build = False
    figTree = ''
    i=0
    while not exit_build:

        rootTitle = getTitle(rootID)
        if i==0: rootIDTrue = rootID
        refList = getAllReferences(rootID)
        titleList = [getTitle(item) if item is not None else None for item in refList]


        # Build
        figTree = treePlot(rootID, rootTitle, refList, titleList, treeObj=figTree)
        figTree.show()


        # Build again?
        response_valid = False
        while not response_valid:
            response = str(input('Enter ID to continue building, or n to save and exit: '))
            if response == 'n': 
                response_valid = True
                figTree.save2file('ref-'+rootIDTrue+'-tree.txt')
                exit_build = True
            
            elif figTree.contains(response):
                response_valid = True
                rootID = response
                i+=1
                


def build_citation_tree(rootID):

    exit_build = False
    figTree = ''
    i=0
    while not exit_build:

        if i==0: rootIDTrue = rootID
        rootTitle = getTitle(rootID)
        citeList = getAllCitations(rootID)
        titleList = [getTitle(item) for item in citeList]


        # Build 
        figTree = treePlot(rootID, rootTitle, citeList, titleList, treeObj=figTree)
        figTree.show()


        # Build again?
        response_valid = False
        while not response_valid:
            response = str(input('Enter ID to continue building, or n to save and exit: '))
            if response == 'n': 
                response_valid = True
                figTree.save2file('cite-'+rootIDTrue+'-tree.txt')
                exit_build = True
            
            elif figTree.contains(response):
                response_valid = True
                rootID = response
                i+=1
                
         
#if __name__ == '__main__':
def main():
    
    parser = ap.ArgumentParser(description='Kill cluster zombies.')
    parser.add_argument('--identifier', '-id', metavar='articleID', dest='rootID', type=str, nargs=1, help='ADS identifier of article', required=True)
    parser.add_argument('--ref', default=False, action="store_true", help="Build reference tree")
    parser.add_argument('--cite', default=False, action="store_true", help="Build citation tree")
    args = parser.parse_args()
    rootID = args.rootID[0]
    
    if args.ref: build_reference_tree(rootID)
    if args.cite: build_citation_tree(rootID)
    


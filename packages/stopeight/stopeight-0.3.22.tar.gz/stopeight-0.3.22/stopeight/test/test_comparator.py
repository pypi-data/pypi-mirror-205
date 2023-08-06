def test_comparator():
    from stopeight.util.parser import process_directory
    from stopeight import legacy
    from stopeight.multiprocessing import pooling
    from numpy import array
    import os
    listoflines = process_directory(os.path.join('stopeight-clibs','legacy','test-data'),'.sp',legacy.parse_file,legacy.stroke_sequential)
    listofarrays = []
    for line in listoflines:
        listofarrays.append(array(line))
    comparator = pooling.MPLine(listofarrays)
    for i,line in enumerate(listofarrays):
        matches = comparator.matchLine(line)
        print('Line ' + str(i) + ' matched ' + str(len(matches)) + ' occurences ' + str(matches))
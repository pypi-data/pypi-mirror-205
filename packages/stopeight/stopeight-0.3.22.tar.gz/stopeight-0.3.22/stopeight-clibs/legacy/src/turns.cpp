// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "turns.h"

//#define debug() QDebug(QtDebugMsg)//::QDebug(QtDebugMsg)
//#define debug() QNoDebug()

//ShapeMatcher::findTurns
/*template<> QList<dpoint> Turns<dpoint>::findTurns(ListCopyable<dpoint> toBeProcessed){
    //debug()<<"Turns::findTurns started with "<<toBeProcessed.size()<<" input points";
    QList<dpoint> result = QList<dpoint>();
    TurnAnalyzer<dpoint> crest = TurnAnalyzer<dpoint>(toBeProcessed);
    // TODO bool foundOne = false;
    while (crest.size()>4){
        ListCopyable<dpoint> triplet = crest.getFirstTurnByTriplets();
        result<<triplet.last();
    }
    // The last one is the end of the crest
    //if (result.size()>1){
    result.removeLast();
    //}
    return result;
}*/

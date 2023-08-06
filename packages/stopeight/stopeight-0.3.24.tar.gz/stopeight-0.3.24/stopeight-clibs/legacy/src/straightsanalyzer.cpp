// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "straightsanalyzer.h"

#define debug() QNoDebug()

template<> bool StraightsAnalyzer<dpoint>::checkIfSectionIsStraightLine(qreal sumLengthFactor){
    ListCopyable<dpoint> section= ListCopyable<dpoint>();
    for (int i=0;i<this->size();i++){
        section << this->at(i);
    }
    // maybe we should remove values that could jeoparize integration
    // This is a hack!
    removeIllegalPoints();

    // Check if segment is a line
    StraightsCalculator<dpoint> line = StraightsCalculator<dpoint>(*this);
    //if ( sumLength/(1+1/3)>sumRotY ) {
    if ( sumLength()*sumLengthFactor>sumOfLinesRotY() ) {
        // It is a straight line!
        return true;
    } else {
        return false;
    }
}

// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "straightscalculator.h"

// being used by triplets
template <> qreal StraightsCalculator<dpoint>::sumRotYFrom(int start){
    qreal sumRotY = 0;
    for (int i=start;i<this->size();i++) {
        sumRotY += this->at(i).rot.y();
    }
    return sumRotY;
}

// being used by checkIfSectionIsStraight
template <> qreal StraightsCalculator<dpoint>::sumOfLinesRotY(){
    qreal sumRotY = 0;
    for (int i=0;i<this->size();i++) {
        sumRotY += fabs(this->at(i).rot.y());
    }
    return sumRotY;
}

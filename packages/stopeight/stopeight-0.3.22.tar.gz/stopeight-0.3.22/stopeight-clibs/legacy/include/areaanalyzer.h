// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef AREAANALYZER_H
#define AREAANALYZER_H

#include "listswitchable.h"
#include "areacalculator.h"
#include "cliffsanalyzer.h"
#include "areanormalizer.h"

namespace AreaAnalyzer {
    template<typename T>  ListSwitchable<T> getFirstArea(ListSwitchable<T>& This,qreal limit);
    // new Area function
    template<typename T>  ListSwitchable<T> getArea(ListSwitchable<T>& This,qreal limit,T START,qreal preceding=0);
    // protected
    // Segment-Radius-Area; should be non-static with diameter=lengthStartToEnd from instance
     qreal area(qreal diameter, qreal base);
}

/*template<typename T> class AreaAnalyzer : public AreaNormalizer<T>
{
public:
    using AreaNormalizer<T>::AreaNormalizer;

    ListSwitchable<dpoint> getFirstArea(qreal limit);

    // new Area function
    ListSwitchable<dpoint> getArea(qreal limit,QPointF START,qreal preceding=0);
protected:

    // Segment-Radius-Area; should be non-static with diameter=lengthStartToEnd from instance
    static qreal area(qreal diameter, qreal base);


};*/

#endif // AREAANALYZER_H

// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "corners.h"

#define debug() QNoDebug()

//ShapeMatcher::findCorners
template<typename T> QList<T> Corners::findCorners(ListSwitchable<T> toBeProcessed){
    auto result = QList<T>();

    auto crest = ListSwitchable<dpoint>(toBeProcessed);
    // do this once and don't do it anymore for the rest of the journey: rotation inside
    CornerNormalizer::cornerFilters(crest);

    while (crest.size()>size_t(0)){
        auto corner = CornerAnalyzer::getFirstCorner(crest);
        result<<corner.last();
    }
    // The last one is the end of the crest
    result.removeLast();
    //debug()<<"ShapeMatcher::findCorners: detected "<<result.size()<<" corners in algorithm.";
    return result;
}
template QList<dpoint> Corners::findCorners(ListSwitchable<dpoint> toBeProcessed);
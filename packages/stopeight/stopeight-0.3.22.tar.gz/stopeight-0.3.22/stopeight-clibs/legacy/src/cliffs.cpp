// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "cliffs.h"

//#define debug() QDebug(QtDebugMsg)//::QDebug(QtDebugMsg)
#define debug() QNoDebug()

//ShapeMatcher::findCliffs
template<typename T> ListSwitchable<T> Cliffs::findCliffs(const ListSwitchable<T> toBeProcessed){
    //test for illegalPointRemoval
    auto result=ListSwitchable<T>();
    auto calculator = ListSwitchable<T>(toBeProcessed);
    while (calculator.size()>size_t(2)) {
        CliffsNormalizer::cliffFilters(calculator);
        //older
        auto firstLegal = CliffsAnalyzer::getFirstLegalSegment(calculator);
        //if (!(firstLegal.size() > size_t(1)))
        //    throw std::logic_error("getFirstLegalSegment has returned illegal length");
        auto cliff = ListSwitchable<dpoint>(std::move(firstLegal));
        //or newer impl?
        //ListCopyable<dpoint> cliff = calculator.getFirstCliff();
        //if (!(cliff.size() > size_t(1)))
        //    throw std::logic_error("ListSwitchable upcast not working");
        result << cliff.last();
    }
    // The last one is the end of the stroke
    result.removeLast();
    return result;
}
template ListSwitchable<dpoint> Cliffs::findCliffs(const ListSwitchable<dpoint> toBeProcessed);
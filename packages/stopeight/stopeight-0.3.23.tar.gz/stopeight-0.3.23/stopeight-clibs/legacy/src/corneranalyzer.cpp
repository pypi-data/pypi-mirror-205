// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "corneranalyzer.h"

#define debug() QNoDebug()

template <typename T> ListSwitchable<T> CornerAnalyzer::getFirstCorner(ListSwitchable<T>& This){
    auto result = ListSwitchable<T>();

    // used to be >1
    if (This.size()>size_t(3)){
        //careful!
        result << This.at(size_t(0)) << This.at(size_t(1)) << This.at(size_t(2));

        // changed from this to calc
        auto calc = ListSwitchable<T>(This);
        for (auto i=size_t(3);i<calc.size();i++){
            //if (i==4)
            //    break;
            if (CliffsCalculator::deriv1Crossed(calc,i)){
                break;
            }
            result << calc.at(i);
        }

    } else {
        //throw "ListAnalyzer::getFirstCorner: Segment is below 4. too short for detecting corners.";
        for (auto i=size_t(0);i<This.size();i++){
            result<<This.at(i);
        }
    }

    // removing
    for (auto i=size_t(0);i<result.size();i++){
        This.removeFirst();
    }

    // don't ever rotate in here!

    return std::move(result);
}
template ListSwitchable<dpoint> CornerAnalyzer::getFirstCorner(ListSwitchable<dpoint>& This);
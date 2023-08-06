// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "analyzer.h"

#define debug() QNoDebug()

// Sould only be allowed in ListCopyable
// only call ONCE
template<typename T> void Analyzer::reverseOrder(ListSwitchable<T>& This){
    auto reversed= ListSwitchable<dpoint>();
    int pointer = 0;
    for (int i=This.size()-size_t(1);i>=size_t(0);i--){
        dpoint point = This.at(i);
        point.position=pointer;
        reversed << point;
        pointer++;
    }
    This.clear();
    This.append(reversed);
}
template void Analyzer::reverseOrder(ListSwitchable<dpoint>& This);

ListSwitchable<dpoint> Analyzer::populateTurns(const ListBase<dpoint> originalData, const QList<ListSwitchable<dpoint> > slices){
    auto result = ListSwitchable<dpoint>();
    for (int k=size_t(0);k<slices.size();k++){
        for (int l=size_t(0);l<slices[k].size()-size_t(1);l++){
            result << slices[k][l];
            // this is for debugging turn detection
            //ListBase<dpoint> lst = iter.chopCopy(slices[k][l].position,slices[k][l+1].position);
            ListBase<dpoint>& temp = const_cast<ListBase<dpoint>&>(originalData);
            auto it = temp.position_to_iterator(slices[k][l].position,slices[k][l+1].position);
            auto mid = ListSwitchable<dpoint>();
            std::copy(it[0],it[1],std::back_inserter(mid));
            auto middle = CornerNormalizer::getPointInTheMiddle(mid);
            middle.position = -1;
            result << middle;
            //result << mid.getPointInTheMiddle();
        }
        if ((k==slices.size()-size_t(1)) && (slices[k].size()>size_t(0))){
            result << slices[k].last();
        }
    }
    return result;
}
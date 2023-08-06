// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "cliffscalculator.h"

#define ZERO_INCLIN1 0
#define ZERO_INCLIN2 0

// inline specialisation
template<typename T> T CliffsCalculator::delta1At(ListSwitchable<T>& This,size_t position){

    if (position<This.size()){

        // this has to change to steepest possible
        //this->rotateSegmentToXAxis();
        T point1,point2;
        T delta1;

        auto i = QListIterator<T>(This);
        if (i.findNext(This.at(position))) {
            if (i.hasPrevious()){
                point1 = i.previous();
                if (i.hasNext()){
                    i.next();
                    if (i.hasNext()){
                        point2 = i.next();
                        delta1 = point2.rot-point1.rot;
                        return delta1;
                    } else {
                        return T(0,0);
                    }
                }
            } else {
                return T(0,0);
            }
        } else {
            return T(0,0);
        }
    } else {
        throw "ListCalculator<dpoint>::delta1At: index out of range";
        // never happens
        return T(0,0);
    }
    throw "ListCalculator<dpoint>::delta1At";
    // never happens
    return T(0,0);
}
template dpoint CliffsCalculator::delta1At(ListSwitchable<dpoint>& This,size_t position);

template <typename T> qreal CliffsCalculator::inclin1At(ListSwitchable<T>& This,size_t i){
    T d1 = CliffsCalculator::delta1At(This,i);
    //if (d1.x()==0) {
    //    return 0;
    //} else {
    return d1.y()/d1.x();
    //}
}
template qreal CliffsCalculator::inclin1At(ListSwitchable<dpoint>& This,size_t i);

// Warning: this is looking back
template <typename T> bool CliffsCalculator::deriv1Crossed(ListSwitchable<T>& This,size_t pos){
    if(pos < size_t(1))
        return false;

    qreal d1 = CliffsCalculator::inclin1At(This,pos-size_t(1));
    qreal d2 = CliffsCalculator::inclin1At(This,pos);

    // This will get the first corner but might be catching too early: d1=0,d2=0
    if ( (d2>=ZERO_INCLIN1&&d1<=-ZERO_INCLIN1) || (d2<=-ZERO_INCLIN1&&d1>=ZERO_INCLIN1)){
        return true;
    }
    return false;
}
template bool CliffsCalculator::deriv1Crossed(ListSwitchable<dpoint>& This,size_t pos);

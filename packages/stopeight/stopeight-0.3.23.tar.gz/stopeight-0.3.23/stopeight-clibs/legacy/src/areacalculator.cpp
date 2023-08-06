// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "areacalculator.h"
//#define debug() QNoDebug()
// this is buggy has to be reworked. inlays are not properly removed by just subtracting them!
template <typename T> qreal AreaCalculator::sumOfDxAreasRotY(ListSwitchable<T>& This){
    qreal sum = 0;
    if (This.size()>size_t(1)){
        for (int i = size_t(0);i<This.size()-size_t(1);i++){
            if (This.at(i+1).rot.x()>This.at(i).rot.x()){
            qreal piece =
                    //fabs(this->at(i+1).rot.x()-this->at(i).rot.x())
                    (This.at(i+1).rot.x()-This.at(i).rot.x())
                    *
                    //jitter big - needed unless turns detected - results more accurate with seg-rad-area
                    // actually this may not be jitter, but just negative rotation (from start)
                    //fabs(this->at(i).rot.y())
                    This.at(i).rot.y()
                    +
                    (
                            //jitter small
                            //fabs(this->at(i+1).rot.y()-this->at(i).rot.y())
                            (This.at(i+size_t(1)).rot.y()-This.at(i).rot.y())
                            *
                            //fabs(this->at(i+1).rot.x()-this->at(i).rot.x())
                            (This.at(i+size_t(1)).rot.x()-This.at(i).rot.x())
                            )/2
                    ;
            if ((sum>0 && piece<0) ||
                (sum<0 && piece>0) )
            {
                //this is jitter! perform turn detection before spiral subsectioning
                //debug()<<"sum: "<<sum<<" piece: "<<piece<<" at position "<<this->at(i).position;
                throw legacy::alg_logic_error("AreaCalculator::sumOfDxAreasRotY: jitter detected. detect turns first and then make ascending/descending",__FILE__,"");
            } else {
            sum += piece;
            }
        } else {
            throw legacy::alg_logic_error("AreaCalculator::sumOfDXArea: bug in getFirstLegalSegment",__FILE__,"");
        }
        }
    }
    return fabs(sum);
}
template qreal AreaCalculator::sumOfDxAreasRotY(ListSwitchable<dpoint>& This);

template <typename T> qreal AreaCalculator::lengthFromStartToEnd(ListSwitchable<T>& This){
    dpoint start = This.first();
    dpoint end = This.last();
    return ListBase<dpoint>::lengthOf(end-start);
}
template qreal AreaCalculator::lengthFromStartToEnd(ListSwitchable<dpoint>& This);

template <typename T> qreal AreaCalculator::triangleArea(T A, T B, T C)
{
    auto a = ListSwitchable<T>();
    a << C << B;
    auto b = ListSwitchable<T>();
    b << A << C;
    auto c = ListSwitchable<T>();
    c << A << B;
    qreal s = ((AreaCalculator::lengthFromStartToEnd(a))+(AreaCalculator::lengthFromStartToEnd(b))+(AreaCalculator::lengthFromStartToEnd(c)))/qreal(2);
    qreal Area = sqrt( s * (s-AreaCalculator::lengthFromStartToEnd(a)) * (s-AreaCalculator::lengthFromStartToEnd(b)) * (s-AreaCalculator::lengthFromStartToEnd(c)) );
    if (Area<qreal(0)){throw "AreaCalculator::triangleArea: is below zero";}

    return Area;
}
template qreal AreaCalculator::triangleArea(dpoint A, dpoint B, dpoint C);
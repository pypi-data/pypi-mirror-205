// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "spirals.h"
//#define debug() QNoDebug()

#define MAX_POINTS 5
//#define LIMIT_TEST M_El
//#define LIMIT_TEST M_PIl
#define LIMIT_ITERATION_STEP 0.1

template<typename T> ListSwitchable<T> Spirals::findAreas(const ListSwitchable<T> stroke, qreal limit){
    auto spiral = ListSwitchable<T>(stroke);

    auto result=ListSwitchable<T>();

    while (spiral.size()>size_t(2)){
        //if (stroke.size()>2){
        auto area = AreaAnalyzer::getFirstArea(spiral,limit);
        if (area.size()>size_t(0)){
            //result << areas;
            result << area.last();
        }
    }
    //result<<stroke.last();

    // The very last one is the end of the stroke
    if (result.size()>size_t(0)){
        result.removeLast();
    }
    return result;
}
template ListSwitchable<dpoint> Spirals::findAreas(const ListSwitchable<dpoint> stroke, qreal limit);

// TODO use listcopyables
template<typename T> qreal Spirals::findLimit(const ListSwitchable<T> toBeProcessed){
    qreal MyLimit;
    //Old working:
    //MyLimit = M_El;
    MyLimit = M_PIl;
    //MyLimit = (M_El+M_PIl)/2;
    //MyLimit = 3.135;
    //MyLimit=2*M_PIl/M_El;
    //MyLimit=M_PIl/2;

    // other block:
    //MyLimit=M_PIl/2;
    //MyLimit=0.66666666666666666666666666666666666666666666666666666666666666666666666666 * M_PIl;
    //MyLimit=2*M_PIl/M_El;
    //MyLimit = M_El;

    //throw "ShapeMatcher::process: invalid MyLimit";
    auto cliffs = findAreas(toBeProcessed,MyLimit);
    if (cliffs.size()>size_t(0)){
            //debug()<<"Found "<<cliffs.size()<<"cliffs, adjusting limit to current minimum";
            size_t selector=cliffs.size();
            auto backup = ListSwitchable<dpoint>();
            qreal backupLimit;
            while (cliffs.size()==(selector)){
                backupLimit = MyLimit;
                backup=cliffs;
                MyLimit -= LIMIT_ITERATION_STEP;
                cliffs=findAreas(toBeProcessed,MyLimit);
            }
            MyLimit=backupLimit;
            cliffs=backup;

    }
    //if ( (cliffs.size()!=0) && (fmod(cliffs.size(),2) == 0)){
    //    throw "ShapeMatcher::verify: Inconsistency: even number of cliffs not allowed";
    //}
    return MyLimit;
}
template qreal Spirals::findLimit(const ListSwitchable<dpoint> toBeProcessed);

template<typename T> ListSwitchable<T> Spirals::findSpiralCliffs(const ListSwitchable<T> toBeProcessed){

    //qreal frontSpiral= toBeProcessed.measureSpiral();
    //debug()<<"Forward Spiral Size is: "<<frontSpiral;
    qreal limit = findLimit(toBeProcessed);
    //debug()<<"Limit from forward analysis is: "<<limit;

    auto reversed = ListSwitchable<T>(toBeProcessed);
    //reversed.tripletFilters();
    Analyzer::reverseOrder(reversed);
    //qreal backSpiral= reversed.measureSpiral();
    //debug()<<"Backward Spiral Size is: "<<backSpiral;
    const ListSwitchable<dpoint> backward = ListSwitchable<dpoint>(std::move(reversed));
    qreal backLimit = findLimit(backward);
    //debug()<<"Limit from backward analysis is: "<<backLimit;
    //if (static_cast<int>(frontSpiral)!=static_cast<int>(backSpiral)){
        //throw "ShapeMatcher::process: spiral-size front/back not equal";
    //}

    // change: use reference?
    auto cliffs = ListSwitchable<dpoint>();
    if (limit!=backLimit){
        //debug()<< "ShapeMatcher::process: different limits found, using larger";
        if (backLimit>limit){
            cliffs = findAreas(backward,backLimit);
            //if (cliffs->size()>0){
            auto calc = ListSwitchable<dpoint>(cliffs);
            calc.reverse();
            cliffs = calc;
            //}
        } else {
            cliffs = findAreas(toBeProcessed,limit);
        }
    } else {
        //debug()<<"******************* findAreas::Main **********************";
        cliffs = findAreas(toBeProcessed,limit);
    }
    return cliffs;
}
template ListSwitchable<dpoint> Spirals::findSpiralCliffs(const ListSwitchable<dpoint> toBeProcessed);

// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "areaanalyzer.h"

#define debug() QNoDebug()
// Segment-Radius-Area
qreal AreaAnalyzer::area(qreal diameter, qreal base){
    qreal squareOfRadius = pow(diameter/2,2);
    //qreal criteria = (squareOfRadius*(base))/2;
    // accounting for integration error; dangerous when iterating limit
    qreal criteria = (squareOfRadius*(base-M_LOG10El))/2;

    if (criteria<0){throw "AreaCalculator.h::area criteria below zero";}
    return criteria;
}

template<typename T> ListSwitchable<T> AreaAnalyzer::getArea(ListSwitchable<T>& This,qreal limit,T start,qreal preceding){
    auto result = ListSwitchable<T>();

    bool foundOne=false;

    if (This.size()>size_t(1)){
        result<<This.first();
        for (int i=size_t(1);i<This.size();i++){
            result<<This.at(i);

            result.rotateSegmentToXAxis();

            qreal currentArea = 0;
            if (preceding>0){
                // calculate current triangle based on iteration
                // we need area starting point for this!
                // currentArea += triangle
                currentArea += AreaCalculator::triangleArea(start,result.first(),result.last());
            }
            // instead of this we could be using an implementation that sums up doubleTriangles
            currentArea += AreaCalculator::sumOfDxAreasRotY(result);

            if (preceding<0){throw "ListAnalyzer::getArea: preceding is below zero";}
            if (currentArea<0){throw "ListAnalyzer::getArea: currentArea is below zero";}

            // IF preceding + currentArea >= norm: norm is area(fullDIAMETER from start, pi or e, 0)

            auto StartEnd = ListSwitchable<T>();
            StartEnd << start << result.last();
            qreal diameter = AreaCalculator::lengthFromStartToEnd(StartEnd);
            // using sumOfDx would require having all preceding legalSegments from start and adding up sums

            qreal norm = area(diameter,limit);//,0);
            if (norm<0){throw "ListAnalyzer::getArea: norm is below zero";}

            //if (currentArea>=criteria){
            if ((preceding+currentArea)>=norm){
                //debug()<<"#"<<result.last().position<<" Area "<<preceding+currentArea<<" is bigger than norm "<<norm;
                foundOne=true;
                break;
            }
        }
        if (foundOne){
            result.removeLast();
        }
    }
    else {
		throw legacy::alg_logic_error("Before area search segment size is below 2",__FILE__,"");
		//C++11
        //throw legacy::alg_logic_error("Before area search segment size is below 2",__FILE__,__func__);
        for (auto i=size_t(0);i<This.size();i++){
            result<<This.at(i);
        }
    }
    // removing
    for (int i=size_t(0);i<result.size();i++){
        This.removeFirst();
    }

    return result;
}
template ListSwitchable<dpoint> AreaAnalyzer::getArea(ListSwitchable<dpoint>& This,qreal limit,dpoint start,qreal preceding);

template<typename T> ListSwitchable<T> AreaAnalyzer::getFirstArea(ListSwitchable<T>& This,qreal limit){
    auto result = T();
    // needs to be and is a COPY
    auto calculator = ListSwitchable<T>(This);

    bool foundOne = false;
    int illegalSegmentCounter=0;

    if (calculator.size()>size_t(1)){
        //ListSwitchable<dpoint> tmp = ListSwitchable<dpoint>(calculator.getFirstLegalSegment());
        auto legalSegment = ListSwitchable<T>{ std::move(CliffsAnalyzer::getFirstLegalSegment(calculator)) };
        illegalSegmentCounter++;
        AreaNormalizer::areaFilters(legalSegment);
        //tmp = legalSegment.getArea(limit,legalSegment.first());
        auto preceding = ListSwitchable<T>{std::move(AreaAnalyzer::getArea(legalSegment,limit, legalSegment.first()))};
        if (legalSegment.size()>size_t(0)){
            foundOne = true;
            result = preceding.last();
        } else {
            qreal sumOfAllPreceding = 0;
            if (calculator.size()>size_t(1)){
                calculator.prepend(preceding.last());
                //tmp = calculator.getFirstLegalSegment();
                legalSegment = ListSwitchable<T>{ std::move(CliffsAnalyzer::getFirstLegalSegment(calculator)) };
                illegalSegmentCounter++;
                AreaNormalizer::areaFilters(legalSegment);
                AreaNormalizer::areaFilters(preceding);
                //tmp = legalSegment.getArea(limit,this->first(),preceding.sumOfDxAreasRotY());
                preceding = ListSwitchable<T>{ std::move(AreaAnalyzer::getArea(legalSegment,limit, This.first(), AreaCalculator::sumOfDxAreasRotY(preceding))) };
                if (legalSegment.size()>size_t(0)){
                    foundOne = true;
                    result = preceding.last();
                } else {
                    while (calculator.size()>size_t(1)){
                        calculator.prepend(preceding.last());
                        //tmp = calculator.getFirstLegalSegment();
                        legalSegment = ListSwitchable<T>{ std::move(CliffsAnalyzer::getFirstLegalSegment(calculator)) };
                        illegalSegmentCounter++;
                        AreaNormalizer::areaFilters(legalSegment);
                        AreaNormalizer::areaFilters(preceding);
                        // sumOfDx over illegal segments is too agressive -> jitter/illegal separation
                        sumOfAllPreceding += AreaCalculator::sumOfDxAreasRotY(preceding) + AreaAnalyzer::area(AreaCalculator::lengthFromStartToEnd(preceding),limit);
                        //tmp = legalSegment.getArea(limit,this->first(),sumOfAllPreceding);
                        preceding = ListSwitchable<T>{ std::move(AreaAnalyzer::getArea(legalSegment,limit, This.first(), sumOfAllPreceding)) };
                        if (legalSegment.size()>size_t(0)){
                            foundOne = true;
                            result = preceding.last();
                            break;
                        }
                    }
                }
            }
        }
    }
    auto area = ListSwitchable<T>();
    if (foundOne){
        //area = util.chopCopy(util.first().position,result.position);
        area.clear();
        auto it = This.position_to_iterator(This.first().position,result.position);
        std::copy(it[0],it[1],std::back_inserter(area));
        //debug()<<"Area has "<<illegalSegmentCounter<<" legal segments.";
    } else {
        area = This;
    }
    // removing
    for (int i=size_t(0);i<area.size();i++){
        This.removeFirst();
    }
    return area;
}
template ListSwitchable<dpoint> AreaAnalyzer::getFirstArea(ListSwitchable<dpoint>& This,qreal limit);


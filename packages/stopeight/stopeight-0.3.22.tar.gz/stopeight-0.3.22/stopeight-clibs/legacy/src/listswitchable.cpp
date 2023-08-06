// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "listswitchable.h"

//#define debug() QDebug::QDebug(QtDebugMsg)
//#define debug() QNoDebug()

/*//Upcast Copy Constructor
template<>template<typename F,typename> ListSwitchable<dpoint>::ListSwitchable(const ListSwitchable<dpoint>& list) {
    auto copy = TurnCalculator<dpoint>(list);//BUG
    *this = static_cast<F&>(copy);
}
//Upcast Move Constructor
template<>template<typename F,typename> ListSwitchable<dpoint>::ListSwitchable(ListSwitchable<dpoint>&& list) {
    auto copy = std::move(list);
    *this = static_cast<F>(copy);
}*/

/*#include "cliffsanalyzer.h"
template ListSwitchable<dpoint>::ListSwitchable(CliffsAnalyzer<dpoint>&&);
template ListSwitchable<dpoint>::ListSwitchable(AreaCalculator<dpoint>&&);
#include "areaanalyzer.h"
template ListSwitchable<dpoint>::ListSwitchable(const AreaAnalyzer<dpoint>&);
template ListSwitchable<dpoint>::ListSwitchable(AreaAnalyzer<dpoint>&&);
template ListSwitchable<dpoint>::ListSwitchable(const AreaNormalizer<dpoint>&);
template ListSwitchable<dpoint>::ListSwitchable(AreaNormalizer<dpoint>&&);
template ListSwitchable<dpoint>::ListSwitchable(const CliffsNormalizer<dpoint>&);
template ListSwitchable<dpoint>::ListSwitchable(const CornerNormalizer<dpoint>&);
template ListSwitchable<dpoint>::ListSwitchable(CornerNormalizer<dpoint>&&);
#include "corneranalyzer.h"
template ListSwitchable<dpoint>::ListSwitchable(const CornerAnalyzer<dpoint>&);
#include "analyzer.h"
template ListSwitchable<dpoint>::ListSwitchable(Analyzer<dpoint>&&);
#include "cliffs.h"
template ListSwitchable<dpoint>::ListSwitchable(const Cliffs<dpoint>&);
#include "spirals.h"
template ListSwitchable<dpoint>::ListSwitchable(const Spirals<dpoint>&);

#include "areacalculator.h"
template AreaCalculator<dpoint>::AreaCalculator(const ListSwitchable<dpoint>&);
#include "cliffsnormalizer.h"
template CliffsNormalizer<dpoint>::CliffsNormalizer(const ListSwitchable<dpoint>&);
#include "cliffsanalyzer.h"
template CliffsAnalyzer<dpoint>::CliffsAnalyzer(const ListSwitchable<dpoint>&);*/

/*//Upcast Copy Assignment
template<>template<typename F,typename> F& ListSwitchable<dpoint>::operator=(const ListSwitchable<dpoint>& list) {
    auto copy = TurnCalculator<dpoint>(list);//BUG
    return std::move(static_cast<F&>(copy));
    //this->swap(copy);
}
//Upcast Move Assignment
template<>template<typename F,typename> F& ListSwitchable<dpoint>::operator=(ListSwitchable<dpoint>&& list) {
   ////REQUIRES PHYSICAL COPY: ERROR MSVC
   ////MEMORY LEAK
   //ListBase<dpoint> copy = ListBase<dpoint>(list);
   //*this = static_cast<ListSwitchable<dpoint>&>(copy);
   ////throw std::runtime_error("ListSwitchable assigned with const");
    return std::move(static_cast<F&&>(list));
}*/

template <> void ListSwitchable<dpoint>::removeAt(int i) {
    if (i<0) {
        //debug()<<"Illegal position for point removal: "<<i;
        return;
    }
    if (i>this->size()-size_t(1)) {
        //debug()<<"Illegal position for point removal: "<<i;
        return;
    }
    if ( (i==size_t(0) )|| (i==this->size()-size_t(1)) ){
        //debug() << "WARNING: deleting first or last point in subsegment, pos: "<< this->at(i).position;
    }
    QList<dpoint>::removeAt(i);
    // watch out, this happens AFTER remove
    if ( (i==size_t(0) )|| (i==this->size()) ){
        //this has to change to steepest possible
        rotateSegmentToXAxis();
        //this->rotateLastVectorToYAxis();
    }
}

template <> void ListSwitchable<dpoint>::reverse(){
    ListSwitchable<dpoint> reversed= ListSwitchable<dpoint>();
    for (int i=this->size()-size_t(1);i>=size_t(0);i--){
        reversed << this->at(i);
    }
    this->clear();
    this->append(reversed);
}

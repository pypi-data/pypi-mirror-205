// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "spiralsanalyzer.h"

//#define debug() QNoDebug()

template<typename T> bool SpiralsAnalyzer::consistencyCheck(const QList<T>& cliffs){
    //debug()<<"We have "<< cliffs.size() << " cliffs in input.";
	//if (cliffs.size()!=0 && fmod(cliffs.size(),2) == 0){
    if (cliffs.size()!=size_t(0) && (cliffs.size()%size_t(2)) == size_t(0)){
        //debug()<< "ShapeMatcher::verify: ";
        throw legacy::alg_logic_error("Inconsistency: even number of cliffs not allowed",__FILE__,"");
               //C++11
        //throw legacy::alg_logic_error("Inconsistency: even number of cliffs not allowed",__FILE__,__func__);
    } else {
        return true;
    }
    return false;
}
template bool SpiralsAnalyzer::consistencyCheck(const QList<dpoint>& cliffs);
// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "turncalculator.h"

// this has performance penalty!
template <> qreal TurnCalculator<dpoint>::getRegressionValueFor2Points(int pos, bool value){
    if (pos>=0 && pos<this->size()-3){
        ListRotator<dpoint> regSeg = ListRotator<dpoint>();
        regSeg << this->at(pos) << this->at(pos+1) << this->at(pos+2) << this->at(pos+3);
        // this has to stay on XAxis
        regSeg.rotateSegmentToXAxis();
        qreal regH1 = regSeg.at(1).rot.y();
        qreal regH2 = regSeg.at(2).rot.y();
        if (value == REGH1) {
            return regH1;
        } else if (value == REGH2) {
            return regH2;
        }
    }
    throw "ListCalculator<dpoint>::getRegressionValue";
}

template <> qreal TurnCalculator<dpoint>::regH1At(int i){
    qreal cregH1 = getRegressionValueFor2Points(i,REGH1);
    return cregH1;
}

template <> qreal TurnCalculator<dpoint>::regH2At(int i){
    qreal cregH2 = getRegressionValueFor2Points(i,REGH2);
    return cregH2;
}

template <> bool TurnCalculator<dpoint>::isRegLineThroughAt(int i){
    qreal regH1 = this->regH1At(i);
    qreal regH2 = this->regH2At(i);
    if (/*(regH1 >=0 && regH2 <0) ||
        (regH1 <0 && regH2 >=0) ||
        (regH1 ==0 && regH2 ==0) */
            (regH1 >=0 && regH2 <0) ||
            (regH1 <=0 && regH2 >0)) {
        return true;
    } else {
        return false;
    }
}

template <> void TurnCalculator<dpoint>::smoothingJitter(int pos) {
    bool foundOne = false;
    for (int i = pos; i < this->size() - 3; i++) {
        //if ( (this->sumOfRegressionAt(i) <= 0.5) &&
        if (
            (!this->isRegLineThroughAt(i))) {
            //if (this->isJitterAt(i) == true) {
            this->removeAt(i + 1);
            // danger index change
            this->removeAt(i + 1);
            foundOne = true;
            break;
        }
    }
    if (foundOne) {
        smoothingJitter(pos + 1);
    }
}

template <> void TurnCalculator<dpoint>::risingJitter(int pos) {
    bool foundOne = false;
    for (int i = pos; i < this->size() - 3; i++) {
        //if ( (this->sumOfRegressionAt(i) <= 0.5) &&
        if (
            (this->isRegLineThroughAt(i))) {
            //if (this->isJitterAt(i) == true) {
            this->removeAt(i + 1);
            // danger index change
            this->removeAt(i + 1);
            //this->removeAt(i);
            foundOne = true;
            break;
        }
    }
    if (foundOne) {
        risingJitter(pos + 1);
    }
}

template <> int TurnCalculator<dpoint>::hasIllegalSegment() {
    ListRotator<dpoint> rotator = ListRotator<dpoint>(*this);
    // has to change to steepest possible?
    rotator.rotateSegmentToXAxis();
    //rotateLastVectorToYAxis();

    for (int i = 0; i < rotator.size() - 1; i++) {
        if ((rotator.at(i + 1).rot.x() <= rotator.at(i).rot.x())
            //&&(rotator.at(i+1).rot.y()<HIGHPASS_LOW_LIMIT)
            )
        {
            //debug() << "Illegal Segment found at " << rotator.at(i+1);
            return rotator.at(i + 1).position;
        }
    }
    return -1;
}
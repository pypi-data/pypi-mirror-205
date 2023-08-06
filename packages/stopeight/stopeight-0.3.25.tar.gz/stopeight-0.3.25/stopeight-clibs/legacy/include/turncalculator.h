// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef TURNCALCULATOR_H
#define TURNCALCULATOR_H

#include "listrotator.h"

#define REGH1 true
#define REGH2 false

template<typename T> class TurnCalculator : public ListRotator<T>
{
public:
    using ListRotator<T>::ListRotator;

    bool isRegLineThroughAt(int i);
    //from TurnNormalizer
    //ACL: foreign
    // this will just produce a whole lot of straight lines
    void smoothingJitter(int pos);
    // supposed to produce curves -> will be replaced by dot product intrapolation
    void risingJitter(int pos);
    //from CliffsAnalyzer
    // used by filters and analyzer
    int hasIllegalSegment();
private:
    qreal regH1At(int i);
    qreal regH2At(int i);
    // has performance issues and is being used by regH1At and regH2At above
    qreal getRegressionValueFor2Points(int pos, bool value);

};

#endif // TURNCALCULATOR_H

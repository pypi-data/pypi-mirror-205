// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef STRAIGHTSCALCULATOR_H
#define STRAIGHTSCALCULATOR_H

#include "listcopyable.h"

template<typename T> class StraightsCalculator : public ListCopyable<T>
{
public:
    using ListCopyable<T>::ListCopyable;

    qreal sumRotYFrom(int start);
    // erroneos integration
    qreal sumOfLinesRotY();
};

#endif // STRAIGHTSCALCULATOR_H

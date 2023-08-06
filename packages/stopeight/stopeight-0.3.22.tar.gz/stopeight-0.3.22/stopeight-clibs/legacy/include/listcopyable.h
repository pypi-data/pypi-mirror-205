// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef LISTCOPYABLE_H
#define LISTCOPYABLE_H

#include "turncalculator.h"

template<typename T> class ListCopyable : public TurnCalculator<T>
{
public:
    //ListCopyable<T>() = default;
    //~ListCopyable<T>() = default;
    //ListCopyable<T>(const ListCopyable<T>& list) = default;
    //ListCopyable<T>(ListCopyable<T>&& list) = default;

    //ListCopyable<dpoint> chopCopy(int startPosition, int endPosition);

    //void reverse();

    void removeIllegalPoints();

};

#endif // LISTCOPYABLE_H

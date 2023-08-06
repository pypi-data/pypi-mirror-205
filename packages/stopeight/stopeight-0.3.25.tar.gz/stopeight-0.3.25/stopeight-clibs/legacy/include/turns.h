// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef TURNS_H
#define TURNS_H

#include "listcopyable.h"

template<typename T> class Turns : public ListCopyable<T>
{
public:
    using ListCopyable<T>::ListCopyable;

    // Note: These only work as expected, if crests have been sliced. Otherwise: Only 1st result reliable
    //static QList<dpoint> findTurns(ListCopyable<dpoint> toBeProcessed);

};

#endif // TURNS_H

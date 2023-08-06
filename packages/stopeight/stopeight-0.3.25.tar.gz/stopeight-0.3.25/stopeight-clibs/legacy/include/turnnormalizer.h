// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef TURNNORMALIZER_H
#define TURNNORMALIZER_H

#include "listcopyable.h"

template<typename T> class TurnNormalizer : public ListCopyable<T>
{
public:
    using ListCopyable<T>::ListCopyable;

    void tripletFilters();
};

#endif // TURNNORMALIZER_H

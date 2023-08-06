// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef STRAIGHTSNORMALIZER_H
#define STRAIGHTSNORMALIZER_H

#include "straightscalculator.h"

template<typename T> class StraightsNormalizer : public StraightsCalculator<T>
{
public:
    using StraightsCalculator<T>::StraightsCalculator;

};

#endif // STRAIGHTSNORMALIZER_H

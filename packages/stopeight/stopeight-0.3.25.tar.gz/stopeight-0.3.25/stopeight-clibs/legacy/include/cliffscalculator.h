// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef CLIFFSCALCULATOR_H
#define CLIFFSCALCULATOR_H

#include "listswitchable.h"

namespace CliffsCalculator {
    template<typename T>  T delta1At(ListSwitchable<T>& This,size_t position);
    template<typename T>  bool deriv1Crossed(ListSwitchable<T>& This,size_t pos);
    template<typename T>  qreal inclin1At(ListSwitchable<T>& This,size_t i);

}

#endif // CLIFFSCALCULATOR_H

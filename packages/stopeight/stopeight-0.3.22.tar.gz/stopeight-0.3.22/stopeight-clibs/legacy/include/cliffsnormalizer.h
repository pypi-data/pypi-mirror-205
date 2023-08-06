// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef CLIFFSNORMALIZER_H
#define CLIFFSNORMALIZER_H

#include "listswitchable.h"
#include "cornernormalizer.h"
namespace CliffsNormalizer {
    // these methods are being used for cleaning up the segments before the corner detection
    template<typename T> void cliffFilters(ListSwitchable<T>& This);
}

/*template<typename T> class CliffsNormalizer : public AreaCalculator<T>
{
public:
    using AreaCalculator<T>::AreaCalculator;

    // these methods are being used for cleaning up the segments before the corner detection
    void cliffFilters();
};*/

#endif // CLIFFSNORMALIZER_H

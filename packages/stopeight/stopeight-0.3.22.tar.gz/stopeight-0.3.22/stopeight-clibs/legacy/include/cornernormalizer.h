// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef CORNERNORMALIZER_H
#define CORNERNORMALIZER_H

#include "listswitchable.h"

namespace CornerNormalizer {
    //All Non-Const
    template<typename T> void requireMinimumLength(ListSwitchable<T>& This,qreal length);
    template<typename T> void intRaster(ListSwitchable<T>& This,qreal threshold);

    // utilities for line-detection
    dpoint getPointInTheMiddle(ListSwitchable<dpoint>& This);

    template<typename T> void cornerFilters(ListSwitchable<T>& This);
}

/*template<typename T> class CornerNormalizer : public CornerCalculator<T>
{
public:
    using CornerCalculator<T>::CornerCalculator;

    void requireMinimumLength(qreal length);
	void intRaster(qreal threshold);

    // utilities for line-detection
    T getPointInTheMiddle();

    void cornerFilters();
};*/

#endif // CORNERNORMALIZER_H

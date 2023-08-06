// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef AREANORMALIZER_H
#define AREANORMALIZER_H

#include "listswitchable.h"
#include "cornernormalizer.h"
//Should be listcopyble!
namespace AreaNormalizer {
    //Non-Const!
    // these methods are being used for cleaning up the segments before the corner detection
    template<typename T>  void areaFilters(ListSwitchable<T>& This);
    // crafting out spirals: 3point segment direction change
    template<typename T>  void removeInlays(ListSwitchable<T>& This);
}

/*template<typename T> class AreaNormalizer : public AreaCalculator<T>
{
public:
    using AreaCalculator<T>::AreaCalculator;


    //Non-Const!
    // these methods are being used for cleaning up the segments before the corner detection
    void areaFilters();

    // crafting out spirals: 3point segment direction change
    void removeInlays();
};*/

#endif // AREANORMALIZER_H

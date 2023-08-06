// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef SPIRALS_H
#define SPIRALS_H

#include "listswitchable.h"
#include "areaanalyzer.h"
#include "analyzer.h"

namespace Spirals {
    template<typename T>  ListSwitchable<T> findSpiralCliffs(const ListSwitchable<T> output);

    //private
    template<typename T>  ListSwitchable<T> findAreas(const ListSwitchable<T> stroke, qreal limit);
    //auxiliary function for findAreas
    template<typename T>  qreal findLimit(const ListSwitchable<T> toBeProcessed);

}

/*template<typename T> class Spirals : public ListSwitchable<T>
{
public:
    using ListSwitchable<T>::ListSwitchable;

    static ListSwitchable<T> findSpiralCliffs(const ListSwitchable<T> output);

private:
    static ListSwitchable<T> findAreas(const ListSwitchable<T> stroke, qreal limit);
    //auxiliary function for findAreas
    static qreal findLimit(const ListSwitchable<T> toBeProcessed);

};*/

#endif // SPIRALS_H

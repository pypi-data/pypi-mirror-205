// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef AREACALCULATOR_H
#define AREACALCULATOR_H

#include "listswitchable.h"

namespace AreaCalculator {
    // a.k.a integration up to triangle / curvature not included
    template<typename T>  qreal sumOfDxAreasRotY(ListSwitchable<T>& This);
    // should be static OR member of List
    template<typename T>  qreal triangleArea(T A, T B, T C);
    template<typename T>  qreal lengthFromStartToEnd(ListSwitchable<T>& This);

}

/*template<typename T> class AreaCalculator : public ListSwitchable<T>
{
public:
    using ListSwitchable<T>::ListSwitchable;

    // a.k.a integration up to triangle / curvature not included
    qreal sumOfDxAreasRotY();

    // should be static OR member of List
    qreal triangleArea(QPointF A, QPointF B, QPointF C);
    // "pure" diameter
    qreal lengthFromStartToEnd();


};*/

#endif // AREACALCULATOR_H

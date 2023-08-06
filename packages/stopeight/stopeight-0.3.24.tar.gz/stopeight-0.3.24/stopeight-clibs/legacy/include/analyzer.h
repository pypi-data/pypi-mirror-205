// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef ANALYZER_H
#define ANALYZER_H

#include "listswitchable.h"
#include "calculator.h"
#include "cornernormalizer.h"

namespace Analyzer {
// careful: this is changing order
    // does not change index-numbering variable
    template<typename T>  void reverseOrder(ListSwitchable<T>& This);
    // make const?
    ListSwitchable<dpoint> populateTurns(const ListBase<dpoint> originalData, const QList<ListSwitchable<dpoint> > slices);

}

/*template<typename T> class Analyzer : public Calculator<T>
{
public:
    using Calculator<T>::Calculator;

    // careful: this is changing order
    // does not change index-numbering variable
    void reverseOrder();

    // make const?
    static Calculator<dpoint> populateTurns(const ListBase<dpoint>& originalData, const QList<ListSwitchable<dpoint> > slices);

};*/

#endif // ANALYZER_H

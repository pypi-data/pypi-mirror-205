// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef CLIFFSANALYZER_H
#define CLIFFSANALYZER_H

#include "listswitchable.h"

namespace CliffsAnalyzer {
    // This is the replacement for getFirstCliff
    template<typename T> ListSwitchable<T> getFirstLegalSegment(ListSwitchable<T>& This);

    template<typename T> ListSwitchable<T> getFirstCliff(ListSwitchable<T>& This,qreal limit=M_PIl);
    //ListCopyable<dpoint> getFirstCliffTCT(ListSwitchable<T>& This,qreal limit=M_PIl);
}

/*template<typename T> class CliffsAnalyzer : public CliffsNormalizer<T>
{
public:
    using CliffsNormalizer<T>::CliffsNormalizer;

    // This is the replacement for getFirstCliff
    ListSwitchable<T> getFirstLegalSegment();

    ListSwitchable<T> getFirstCliff(qreal limit=M_PIl);
    //ListCopyable<dpoint> getFirstCliffTCT(qreal limit=M_PIl);

};*/

#endif // CLIFFSANALYZER_H

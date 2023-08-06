// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef SPIRALSANALYZER_H
#define SPIRALSANALYZER_H

#include "spiralscalculator.h"

namespace SpiralsAnalyzer {
    template<typename T>  bool consistencyCheck(const QList<T>& cliffs);
}

/*template<typename T> class SpiralsAnalyzer : public SpiralsCalculator<T>
{
public:
    using SpiralsCalculator<T>::SpiralsCalculator;

    static bool consistencyCheck(QList<dpoint> cliffs);


};*/

#endif // SPIRALSANALYZER_H

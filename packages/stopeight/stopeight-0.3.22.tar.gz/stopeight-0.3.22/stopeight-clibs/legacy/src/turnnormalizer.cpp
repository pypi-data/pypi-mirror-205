// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "turnnormalizer.h"

template <> void TurnNormalizer<dpoint>::tripletFilters(){
	// CHECKPRECISION?!
    //this->risingJitter(0);
    this->smoothingJitter(0);
    //only corners and turns need rotation: derivative
    // rotation is absolutely needed if using crossing 0. getFirstTurn contains rotation in point removal
    //remainingSlice.rotateSegmentToXAxis();
}

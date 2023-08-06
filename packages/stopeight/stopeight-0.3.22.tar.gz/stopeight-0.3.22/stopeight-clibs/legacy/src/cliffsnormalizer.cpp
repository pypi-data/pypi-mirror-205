// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "cliffsnormalizer.h"

//BROKEN
template <typename T> void CliffsNormalizer::cliffFilters(ListSwitchable<T>& This) {
	if (This.checkPrecision()) {
		auto b = ListSwitchable<dpoint>(This);
		CornerNormalizer::requireMinimumLength(b,1);
		// enabling this is good for circles, bad for certain spirals, sinus and strokes without enough input data
		b.risingJitter(0);
		//
		b.smoothingJitter(0);
		b.risingJitter(0);
	}
	else {
		auto b = ListSwitchable<dpoint>(This);
		CornerNormalizer::requireMinimumLength(b,2);
		//// enabling this is good for circles, bad for certain spirals, sinus and strokes without enough input data
		////toBeProcessed.risingJitter(0);
		b.smoothingJitter(0);
		//c.risingJitter(0);
	}
}
template void CliffsNormalizer::cliffFilters(ListSwitchable<dpoint>& This);
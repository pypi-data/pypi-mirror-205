// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "areanormalizer.h"
//hdojo version
template <typename T> void AreaNormalizer::removeInlays(ListSwitchable<T>& This){
    if (This.size()>4){
        for (int i=size_t(0);i<This.size()-size_t(4);i++) {
            ListSwitchable<T> first, second, third = ListSwitchable<T>();
            first << This.at(size_t(0))<< This.at(size_t(1))<< This.at(size_t(2));first.rotateSegmentToXAxis(); qreal firstValue = first.at(size_t(1)).rot.y();
            second << This.at(size_t(1))<<This.at(size_t(2))<<This.at(size_t(3));second.rotateSegmentToXAxis(); qreal secondValue = second.at(size_t(1)).rot.y();
            third << This.at(size_t(2))<<This.at(size_t(3))<<This.at(size_t(4));third.rotateSegmentToXAxis(); qreal thirdValue = third.at(size_t(1)).rot.y();
            if ((firstValue>0 && secondValue<0&&thirdValue<0) ||
                (firstValue<0 && secondValue>0&&thirdValue>0)) {This.removeAt(size_t(1));AreaNormalizer::removeInlays(This);break;}
            else if ((secondValue>0 && firstValue<0&&thirdValue<0) ||
                     (secondValue<0 && firstValue>0&&thirdValue>0)) {This.removeAt(size_t(2));AreaNormalizer::removeInlays(This);break;}
            else if ((thirdValue>0 && firstValue<0&&secondValue<0) ||
                     (thirdValue<0 && firstValue>0&&secondValue>0)) {This.removeAt(size_t(3));AreaNormalizer::removeInlays(This);break;}
        }
    }
}
template void AreaNormalizer::removeInlays(ListSwitchable<dpoint>& This);

template <typename T>void AreaNormalizer::areaFilters(ListSwitchable<T>& This){
	if (This.checkPrecision()) {
		//START OLD
		//This.smoothingJitter(0);
		//This.risingJitter(0);
		//END OLD


		auto zero = ListSwitchable<T>(This);//BEFORE REFACTORING std::move(This)
		CornerNormalizer::requireMinimumLength(zero,5);

		//from linux wacom only:
		//smoothing0
		//rising0
		//removeinlays
		//

		zero.risingJitter(0);
		//a.smoothingJitter(0);
		zero.risingJitter(0);

		//

		auto b = ListSwitchable<T>(std::move(zero));
		//from below
		CornerNormalizer::requireMinimumLength(b,7);
		//
		b.rotateSegmentToXAxis();
		This = ListSwitchable<T>(std::move(b));
		AreaNormalizer::removeInlays(This);
	}
	//if (This.checkPrecision()) {
	//	CornerNormalizer<dpoint> a = CornerNormalizer<dpoint>(*this);
	//	a.intRaster(0.2);
	//	*this = AreaNormalizer<dpoint>(a);
	//}
	else {
		//BEFORE REFACTORING here :This.smoothingJitter(0);
		auto b = ListSwitchable<T>(This);
		b.smoothingJitter(0);//INSTEAD OF
		CornerNormalizer::requireMinimumLength(b,9);
		b.rotateSegmentToXAxis();

		//Port: UNUSED
		//This.risingJitter(0);

		This = ListSwitchable<T>(std::move(b));
		AreaNormalizer::removeInlays(This);
	}

}
template void AreaNormalizer::areaFilters(ListSwitchable<dpoint>& This);
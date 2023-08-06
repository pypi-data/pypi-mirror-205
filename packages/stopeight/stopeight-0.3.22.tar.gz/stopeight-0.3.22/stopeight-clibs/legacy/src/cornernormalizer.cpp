// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "cornernormalizer.h"

template <typename T> void CornerNormalizer::requireMinimumLength(ListSwitchable<T>& This,qreal lnt){
    bool foundOne = false;
    //throw size
    for (int i=This.size()-size_t(2);i>size_t(0);i--){

        if (This.lengthAt(i)<lnt){
            This.removeAt(i);
            foundOne = true;
            break;
        }
    }
    if (foundOne){
        CornerNormalizer::requireMinimumLength(This,lnt);
    }
}
template void CornerNormalizer::requireMinimumLength(ListSwitchable<dpoint>& This,qreal lnt);

template<typename T>void CornerNormalizer::intRaster(ListSwitchable<T>& This,qreal threshold)
{
    auto newlist = ListSwitchable<T>();
	for (int i = size_t(0); i < This.size(); i++) {
		if ( (fmod(This.at(i).x(),1) <=threshold) &&
			 (fmod(This.at(i).y(),1) <= threshold) ) {
			newlist << This.at(i);
		}
	}
    This = std::move(newlist);
}
template void CornerNormalizer::intRaster(ListSwitchable<dpoint>& This,qreal threshold);

//CORNERFILTERS ARE BROKEN
template <typename T> void CornerNormalizer::cornerFilters(ListSwitchable<T>& This){
	// CHECKPRECISION?!
	//debug() << "Before filter corner: ";
    //BEFORE REFACTORING WAS HERE : This.smoothingJitter(0);
    auto b = ListSwitchable<T>(This);
    b.smoothingJitter(0);// AFTER HERE
    CornerNormalizer::requireMinimumLength(b,1.00001);
    auto c = ListSwitchable<T>(std::move(b));
    c.rotateSegmentToXAxis();
    //This.normalizeCorners();
    //debug() << "After filter corner: ";
}
template void CornerNormalizer::cornerFilters(ListSwitchable<dpoint>& This);

//HACK
dpoint CornerNormalizer::getPointInTheMiddle(ListSwitchable<dpoint>& This){
    auto myself = ListSwitchable<dpoint>(This);
    if (myself.size()>size_t(2)){
        dpoint middle;

        // It is a straight line!
        //draw corner or turn in middle
        // use middle of start and end
        //middle = (myself.last()+myself.first())/2;

        dpoint p = dpoint();
        // this point does not have a position!!
        // -> create one
        // get the length of section
        // find position of adjacent to half length
        auto newsection = ListSwitchable<dpoint>();
        newsection << myself.first();
        for (int i=size_t(1);i<myself.size();i++){
            newsection<<myself.at(i);
            if (newsection.sumLength()>(myself.sumLength()/qreal(2))){
                // get the point1 < position
                dpoint point1 = myself.at(i-size_t(1));
                // get the point2 > position
                dpoint point2 = myself.at(i);
                // use middle of two adjacent points
                middle = (point1+point2)/2;
                if (point1.position==-1){
                    if (point2.position==-1){
                        throw std::logic_error("There should not be any inserted points at this stage of the algorithm");
                    } else {
                        p.position = point2.position;
                    }
                    break;
                }
                if (point2.position==-1){
                    if (point1.position==-1){
                        throw std::logic_error("There should not be any inserted points at this stage of the algorithm");
                    } else {
                        p.position = point1.position;
                    }
                    break;
                }
                // set the new position to p1+p2/2
                p.position=point1.position+((point2.position-point1.position)/2);
                break;
            }
        }
        p.setX(middle.x());
        p.setY(middle.y());
        return p;
    } else if (myself.size()==size_t(2)){
        //special case that might happen with integrating triplets from start/reverse
        if (myself.at(size_t(0)).position==myself.at(size_t(1)).position){
            return myself.at(size_t(0));
        } else {
            dpoint middle = dpoint();
            middle.setX((myself.at(size_t(0)).x()+myself.at(size_t(1)).x())/2);
            middle.setY((myself.at(size_t(0)).y()+myself.at(size_t(1)).y())/2);
            // setting the new index to half, got better solution?
            middle.position=myself.at(size_t(0)).position+((myself.at(size_t(1)).position-myself.at(size_t(0)).position)/2);
            return middle;
        }
    }else if (myself.size()==size_t(1)) {
        throw legacy::alg_logic_error("Tried to get middle from 1 point",__FILE__,"");
        return myself.at(size_t(0));
    } else {
		throw legacy::alg_logic_error("Tried to get middle from 0 points", __FILE__, "");
    }
}
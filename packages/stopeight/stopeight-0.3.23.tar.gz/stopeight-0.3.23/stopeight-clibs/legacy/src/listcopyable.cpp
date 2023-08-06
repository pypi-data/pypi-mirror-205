// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "listcopyable.h"
//#define debug() QNoDebug()

/*template<> ListCopyable<dpoint> ListCopyable<dpoint>::chopCopy(int startPosition, int endPosition){
    ListCopyable<dpoint> filet = ListCopyable<dpoint>();
    for (int i=0;i<this->size();i++){
        if ((this->at(i).position >= startPosition &&
             this->at(i).position <= endPosition) ||
            // this is for reversed pieces, should work...?
            (this->at(i).position <= startPosition &&
             this->at(i).position >= endPosition)
            ){
            filet << this->at(i);
        }
    }
    return filet;
}*/




/*template <> void ListCopyable<dpoint>::reverse(){
    ListCopyable<dpoint> reversed= ListCopyable<dpoint>();
    for (int i=this->size()-1;i>=0;i--){
        reversed << this->at(i);
    }
    this->clear();
    this->append(reversed);
}*/

template <> void ListCopyable<dpoint>::removeIllegalPoints(){
//    debug() << "Before removeIllegalPoints: " <<this->size();
    while (this->hasIllegalSegment()!=-1){
        for (int i=0;i<this->size();i++){
            if (this->at(i).position == this->hasIllegalSegment()){
                //debug() << "removeIllegalPoints: "<<"Removed point "<<this->at(i)<<".";
                this->removeAt(i);
                break;
            }
        }
    }
//    debug() << "After removeIllegalPoints: " <<this->size();
}

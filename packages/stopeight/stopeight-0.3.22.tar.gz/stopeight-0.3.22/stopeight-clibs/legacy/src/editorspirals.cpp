// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "editorspirals.h"
//#define debug() QDebug(QtDebugMsg)//::QDebug(QtDebugMsg)
//#define debug() QNoDebug()

EditorSpirals::EditorSpirals() : EditorCliffs()
{
}

//EditorSpirals::~EditorSpirals(){
//    EditorBase::~EditorBase();
//}

//toBeProcessed is modifying data.output
void EditorSpirals::process(ListSwitchable<dpoint> &toBeProcessed){
    // use of output is a hack
    if (this->getOutput().size()>size_t(0)) {
        /* SHARED CLIFFS&SPIRALS */        
        const ListSwitchable<dpoint> cliffs= Spirals::findSpiralCliffs(toBeProcessed);

        /* SHARED CLIFFS&SPIRALS, But replace cornerMeasuring?? */
        QList<ListSwitchable<dpoint> > slices= QList<ListSwitchable<dpoint> >();

        mainIterator(cliffs,slices);

        auto result = ListSwitchable<dpoint>();

        /* SPIRALS&CLIFFS check */
        SpiralsAnalyzer::consistencyCheck(cliffs);

        /* SHARED */
        result = Analyzer::populateTurns(this->getOutput(),slices);

        //hack
        this->setOutput(result);
    } else {
        throw "EditorSpirals::process called without any data";
    }
}

ListSwitchable<dpoint> EditorSpirals::processSegment(ListSwitchable<dpoint>::iterator start, ListSwitchable<dpoint>::iterator end){
    return EditorCliffs::processSegment(start,end);
}

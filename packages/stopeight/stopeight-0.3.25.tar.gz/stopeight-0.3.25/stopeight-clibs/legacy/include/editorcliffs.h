// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef EDITORCLIFFS_H
#define EDITORCLIFFS_H

#include "editorbase.h"
#include "cliffs.h"
#include "spiralsanalyzer.h"
#include "analyzer.h"
class EditorCliffs : public EditorBase<ListSwitchable<dpoint> >
{
    friend class EditorSpirals;
public:
    EditorCliffs();
    //~EditorCliffs();


protected:
    void process(ListSwitchable<dpoint>& toBeProcessed);

private:
    ListSwitchable<dpoint> processSegment(ListSwitchable<dpoint>::iterator start,ListSwitchable<dpoint>::iterator end);

};

#endif // EDITORCLIFFS_H

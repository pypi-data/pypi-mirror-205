// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef EDITORSPIRALS_H
#define EDITORSPIRALS_H

#include "editorcliffs.h"
#include "spirals.h"
#include "spiralsanalyzer.h"
class EditorSpirals : public EditorCliffs
{
public:
    EditorSpirals();
    //~EditorSpirals();


protected:
    // automatic detection of "spirals" that don't include any illegal segments, which would make derivations invalid. See throw jitter detected
    void process(ListSwitchable<dpoint>& toBeProcessed);

private:
    ListSwitchable<dpoint> processSegment(ListSwitchable<dpoint>::iterator start,ListSwitchable<dpoint>::iterator end);

};

#endif // EDITORSPIRALS_H

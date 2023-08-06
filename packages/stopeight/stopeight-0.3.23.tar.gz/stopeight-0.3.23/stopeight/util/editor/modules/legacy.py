# Copyright (C) 2018 Fassio Blatter
version="TooOld"
import stopeight.legacy
from stopeight.util.editor.data import ScribbleData

import stopeight.logging as log

def stroke_parallel(data:ScribbleData)->ScribbleData:
    return _convert(stopeight.legacy.stroke_parallel(list(map(tuple,data['coords'].tolist()))))

def stroke_sequential(data:ScribbleData)->ScribbleData:
    # type: (ScribbleData) -> ScribbleData
    return _convert(stopeight.legacy.stroke_sequential(list(map(tuple,data['coords'].tolist()))))

def _parse_file(filename):
    legacy_data= stopeight.legacy.parse_file(filename)
    return _convert(legacy_data)

def _convert(legacy_data):
    scribbledata = ScribbleData(size=len(legacy_data))
    for i,v in enumerate(legacy_data):
        scribbledata[i]['coords'] = [v[0],v[1]]
    return scribbledata

def open_SP()->ScribbleData:
    from stopeight.util.editor.runnable import EditorApp
    from PySide2.QtWidgets import QFileDialog
    filename = QFileDialog.getOpenFileName(EditorApp().window)
    assert type(filename[0]) == str
    assert len(filename[0]) != 0
    data = _parse_file(filename[0])
    return data

def TCT_to_bezier(data:ScribbleData)->ScribbleData:
    return stopeight.legacy.TCT_to_bezier(data)

import stopeight.finders
from stopeight.getters import ListSwitchable

def _intList_to_ScribbleData(original: ScribbleData, mylist: list)->ScribbleData:
    assert len(original)>1
    newsize=len(mylist)+2
    data = ScribbleData(size=newsize)
    data[0]['coords']=[original[0]['coords'][0],original[0]['coords'][1]]
    data[newsize-1]['coords']=[original[-1]['coords'][0],original[-1]['coords'][1]]
    for i,index in enumerate(mylist):
        data[i+1]['coords'] = [original[index]['coords'][0],original[index]['coords'][1]]
    return data

def sequential(data:ScribbleData)->ScribbleData:
    log.info("Invoking findCliffs...")
    ql = stopeight.getters.ListSwitchable(data)
    turns = stopeight.finders.findCliffs(ql)
    print(turns)
    assert type(turns) == list
    return _intList_to_ScribbleData(data,turns)

def parallel(data:ScribbleData)->ScribbleData:
    log.info("Invoking findSpiralCliffs...")
    ql = stopeight.getters.ListSwitchable(data)
    turns = stopeight.finders.findSpiralCliffs(ql)
    print(turns)
    assert type(turns) == list
    return _intList_to_ScribbleData(data,turns)

import stopeight.getters
import numpy as np

def getFirstTurnByTriplets(data:ScribbleData)->ScribbleData:
    log.setLevel(log.DEBUG)
    log.info("Invoking getFirstTurnByTriplets with "+str(len(data))+" data points...")
    ta = stopeight.getters.TurnAnalyzer(data)
    log.debug("Invoking turn chopping algorithm length "+str(len(ta)))
    out = ta.getFirstTurnByTriplets(ta)
    log.debug("Read length of a object of type "+str(type(out))+" and length "+str(len(out)))
    return out.view(ScribbleData)

def getFirstCorner(data:ScribbleData)->ScribbleData:
    log.setLevel(log.DEBUG)
    log.info("Invoking getFirstCorner with "+str(len(data))+" data points...")
    ql = stopeight.getters.ListSwitchable(data)
    log.debug("Invoking corner chopping algorithm length "+str(len(ql)))
    out = stopeight.getters.getFirstCorner(ql)
    log.debug("Read length of a object of type "+str(type(out))+" and length "+str(len(out)))
    return out.view(ScribbleData)

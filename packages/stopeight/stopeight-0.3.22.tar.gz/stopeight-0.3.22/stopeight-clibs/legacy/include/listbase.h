// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef LISTBASE_H
#define LISTBASE_H

#include "legacy_global.h"

#include <QtCore/QString>
#include <QtCore/QFile>
#include <QtCore/QFileInfo>
#include <QtCore/QDataStream>

#include "dpoint.h"
#include "myreal.h"

#include "error.h"

#include <array>
#include <QtCore/QList>
struct ArrayOfTwoQListDpointIterators : std::array<QList<dpoint>::iterator, 2>{};

/* This is being used by both the qt-based editor AND python legacy-wrappers! */
template<typename T> class ListBase : public QList<T>
{
public:
    using QList<T>::QList;

    // method for access from python
    static QList<QPointF> open(const char* fileName);
    // method for access from legacy editor
    static QList<QPointF> loadSPFile(const QString &fileName);
	// for old files
//	static ListBase<dpoint> loadSPFile(const QString &fileName);
	// method for access from both
	static QList<QPointF> convert(ListBase<dpoint> list);

    //from ListCopyAble
    ArrayOfTwoQListDpointIterators position_to_iterator(int startPosition, int endPosition);
    qreal lengthAt(int i);
    static qreal lengthOf(QPointF difference);
    //from Straights
    // length of curve between "all"! points / curvature not included
    qreal sumLength();


//protected:
	bool checkPrecision();

};

//GCC bug?
//extern template class ListBase<dpoint>;

//Windows
//template class LEGACYSHARED_EXPORT ListBase<dpoint>;
//template class LEGACYSHARED_EXPORT ListBase<QPointF>;


#endif // LISTBASE_H

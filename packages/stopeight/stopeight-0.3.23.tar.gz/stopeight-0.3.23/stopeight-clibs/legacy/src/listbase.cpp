// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "listbase.h"


//#define debug() QNoDebug()

//using namespace legacy;

//WAS: template<> QList<QPointF> ListBase<QPointF>::loadSPFile(const QString& fileName)
template<> QList<QPointF> ListBase<dpoint>::loadSPFile(const QString& fileName)
{
    QFile file(fileName);
    QFileInfo info(file);
    if (info.size() == 0) {
        //throw legacy::runtime_error("File " + fileName.toStdString()+" is empty");
        return QList<QPointF>();
    }
    if (!file.open(QIODevice::ReadOnly)) {
        throw legacy::runtime_error(file.errorString().toStdString()+" "+fileName.toStdString(),__FILE__,__func__);
    }
    QDataStream in(&file);
    in.setVersion(QDataStream::Qt_4_5);
    unsigned int MagicNumber = 0x8E42B972;
    unsigned int magic;
    in >> magic;
    if (magic != MagicNumber) {
        throw legacy::runtime_error("Wrong magic number: "+std::to_string(magic)+" in file "+fileName.toStdString(),__FILE__,__func__);
    }

    dpoint p;
    QList<QPointF> input;
    input.clear();
    while (!in.atEnd()) {
        in >> p;
        input.push_back(QPointF(p.x(),p.y()));
    }
    return input;
}

template<> QList<QPointF> ListBase<dpoint>::convert(ListBase<dpoint> list) {
	QList<QPointF> newlist = QList<QPointF>();
	while (!list.isEmpty()) {
		dpoint point = list.takeFirst();
		newlist.append(QPointF(point.x(),point.y()));
	}
	return newlist;
}

template<> QList<QPointF> ListBase<dpoint>::open(const char *fileName){
    const QString& myString = QString::fromLatin1(fileName);
    //return ListBase<dpoint>::convert(ListBase<dpoint>::loadSPFile(myString));
    QList<QPointF> fromFile = ListBase<dpoint>::loadSPFile(myString);
    //ListBase<dpoint> result = ListBase<dpoint>();
    //std::copy(std::begin(fromFile),std::end(fromFile),std::back_inserter(result));
	return fromFile;

}

//needed for wrapper!
//template QList<QPointF> ListBase<dpoint>::open(const char *fileName);
//template QList<QPointF> ListBase<dpoint>::convert(ListBase<dpoint> list);

template<> bool ListBase<dpoint>::checkPrecision() {
	/*
	Check if the list contains float values and set precision to high
	*/
	for (int i = 0; i<this->size(); i++) {
		if (!MyReal(this->at(i).x()).isInt() ||
			!MyReal(this->at(i).y()).isInt())
		{
			return true;
		}
	}
	return false;
}

template <> ArrayOfTwoQListDpointIterators ListBase<dpoint>::position_to_iterator(int startPosition, int endPosition) {
    auto start = size_t(startPosition);
    auto end = size_t(endPosition);
    if (start > end)
        throw std::out_of_range("Trying to chop from reverse.");
    QList<dpoint>::iterator first = std::begin(*this) + (start - size_t(std::begin(*this)->position));
    QList<dpoint>::iterator last = std::begin(*this) + (end - size_t(std::begin(*this)->position));
    auto chop_length = std::distance(first, last);
    if ((end - start) != chop_length) {
        throw std::length_error("List is missing elements. This is not allowed for derived classes of ListSwitchable.");
    }
    else {
        return ArrayOfTwoQListDpointIterators{ first,last };
    }
}

template <> qreal ListBase<dpoint>::lengthOf(QPointF difference) {
    return sqrt(pow(difference.x(), 2) + pow(difference.y(), 2));
}

template <> qreal ListBase<dpoint>::lengthAt(int position) {
    QListIterator<dpoint> i(*this);
    if (i.findNext(this->at(position))) {
        dpoint point1;
        if (i.hasPrevious()) {
            point1 = i.previous();
            if (i.hasNext()) {
                i.next();
                if (i.hasNext()) {
                    dpoint point2 = i.next();
                    dpoint point = point2 - point1;
                    return lengthOf(point);
                }
                else {
                    return 0;
                }
            }
            else {
                return 0;
            }

        }
        else {
            return 0;
        }

    }
    else {
        return 0;
    }
}

template <> qreal ListBase<dpoint>::sumLength() {
    qreal sumLength = 0;
    for (int i = 0; i < this->size() - 1; i++) {
        sumLength += lengthAt(i);
    }
    return sumLength;
}
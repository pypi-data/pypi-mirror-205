// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef LISTSWITCHABLE_H
#define LISTSWITCHABLE_H

#define HIGHPASS_LOW_LIMIT 0.0001

#include "turncalculator.h"
//#include <limits>

template<typename T> class ListSwitchable : public TurnCalculator<T>
{
public:
    //using TurnCalculator<T>::TurnCalculator;
    ListSwitchable<T>() = default;
    virtual ~ListSwitchable<T>()=default;
    //for technical reasons, copy constructors are never generated from templates p.679
    ListSwitchable<T>(const ListSwitchable<T>&) = default;
    ListSwitchable<T>(ListSwitchable<T>&&) = default;
    ListSwitchable<T>& operator=(const ListSwitchable<T>&) = default;
    ListSwitchable<T>& operator=(ListSwitchable<T>&&) = default;
    /*
    //Virtual Contructors are not allowed
    //clang specialization error
    //GCC no inheritance
    //MSVC works
    //Upcast Constructors and Assignments
    template<typename F= ListSwitchable<T>
        , typename = typename std::enable_if_t<std::is_base_of<ListSwitchable<T>, F>() || std::is_same<ListSwitchable<T>, F>()>
    > ListSwitchable<T>(const ListSwitchable<T>&);
    template<typename F= ListSwitchable<T>
        , typename = typename std::enable_if_t<std::is_base_of<ListSwitchable<T>, F>() || std::is_same<ListSwitchable<T>, F>()>
    > ListSwitchable<T>(ListSwitchable<T>&&);
//THIS THING AND ALL INHERITING CAN NOT BE COPIED
    template<typename F
        , typename = typename std::enable_if_t<std::is_base_of<ListSwitchable<T>, F>() || std::is_same<ListSwitchable<T>, F>()>
    > F& operator=(const ListSwitchable<T>& list);
    template<typename F
        , typename = typename std::enable_if_t<std::is_base_of<ListSwitchable<T>, F>() || std::is_same<ListSwitchable<T>, F>()>
    > F& operator=(ListSwitchable<T>&& list);
    */

    void removeAt(int i);
    // Note: this is simple reversal. it is not checking order. Should be static.
    void reverse();
};

#endif // LISTSWITCHABLE_H

#undef NDEBUG
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

#include "turnanalyzer.h"
#include "corneranalyzer.h"
#include <stopeight-clibs/shared_types.h>
#include <stopeight-clibs/Matrix.h>

template<typename F> class ListCopyableWrapper : public F
{
  public:
    using F::F;
    ListCopyableWrapper(py::array_t<sp::timecode<double>, py::array::c_style> other);
    ListCopyableWrapper(const F& other);

    py::array_t<sp::timecode<double>, py::array::c_style> toPyArray();
};

class ListSwitchableWrapper : public ListSwitchable<dpoint>{
  public:
    ListSwitchableWrapper(py::array_t<sp::timecode<double>, py::array::c_style> other);
    ListSwitchableWrapper(ListSwitchable<dpoint>&& other);

    py::array_t<sp::timecode<double>, py::array::c_style> toPyArray();
};
#include "git.h"
#include <IFPyShared.h>
#undef NDEBUG
#include <pybind11/pybind11.h>

PYBIND11_MODULE(getters, g){
	if(GitMetadata::Populated()) {
		py::object sha;
	        if(GitMetadata::AnyUncommittedChanges()) {
			sha = py::cast(GitMetadata::CommitSHA1()+"+dirty");
	        } else {
			sha = py::cast(GitMetadata::CommitSHA1());
		}
		g.attr("version") = sha;
	}
    py::class_<ListCopyableWrapper<ListCopyable<dpoint>>>(g,"ListCopyable", py::buffer_protocol())
	.def(py::init<py::array_t<sp::timecode<double>,py::array::c_style>>())
	.def("__len__",[](ListCopyableWrapper<ListCopyable<dpoint>>& in)->int{return in.size();})
	;
    py::class_<ListCopyableWrapper<TurnAnalyzer<dpoint>>>(g,"TurnAnalyzer", py::buffer_protocol())
	.def(py::init<py::array_t<sp::timecode<double>,py::array::c_style>>())
	.def("__len__",[](ListCopyableWrapper<TurnAnalyzer<dpoint>>& in)->int{return in.size();})
	.def("getFirstTurnByTriplets",[](ListCopyableWrapper<TurnAnalyzer<dpoint>>& in){
		in.rotateSegmentToXAxis();
		ListCopyableWrapper<ListCopyable<dpoint>> result = in.getFirstTurnByTriplets();
		return result.toPyArray();
	})
	;
	/*g.def("getFirstTurnByTriplets",[](ListCopyableWrapper<TurnAnalyzer<dpoint>>& in){
		in.rotateSegmentToXAxis();
		ListCopyableWrapper<ListCopyable<dpoint>> result = in.getFirstTurnByTriplets();
		return result.toPyArray();
	});*/
	py::class_<ListSwitchableWrapper>(g,"ListSwitchable", py::buffer_protocol())
	.def(py::init<py::array_t<sp::timecode<double>,py::array::c_style>>())
	.def("__len__",[](ListSwitchableWrapper& in)->int{return in.size();})
	;
	g.def("getFirstCorner",[](ListSwitchableWrapper& in){
		in.rotateSegmentToXAxis();
		ListSwitchableWrapper result = CornerAnalyzer::getFirstCorner(in);//Uses LSW move constructor
		return result.toPyArray();
	});
}

// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1
#include "git.h"
#include <stopeight-clibs/grapher.h>
#include <stopeight-clibs/Matrix.h>

#undef NDEBUG
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include <pybind11/numpy.h>

PYBIND11_MAKE_OPAQUE(std::vector<double>);

using namespace pybind11;

PYBIND11_MODULE(grapher, m){
	if(GitMetadata::Populated()) {
		object sha;
	        if(GitMetadata::AnyUncommittedChanges()) {
			sha = cast(GitMetadata::CommitSHA1()+"+dirty");
	        } else {
			sha = cast(GitMetadata::CommitSHA1());
		}
		m.attr("version") = sha;
	}
	object matrix_module = module::import("stopeight.matrix");
	bind_vector<std::vector<double>>(m,"VectorDouble");
    /*class_<std::vector<double>>(m,"VectorDouble",buffer_protocol())
	.def(init<>())
	.def(init([](array_t<double,array::c_style> buffer){
		auto info = buffer.request();
		if (info.format != format_descriptor<double>::format())
			throw std::runtime_error("Incompatible format: Expected a double array format descriptor");
		if (info.itemsize != sizeof(double))
			throw std::runtime_error("Incompatible format: Expected double size items");
		if (info.ndim!= 1)
			throw std::runtime_error("Incompatible buffer dimensions");
		auto data = static_cast<double*>(info.ptr);
		auto vector =  new std::vector<double>(data,data+info.shape[0]);
		return vector;
	}))
	.def_buffer([](std::vector<double>& vector) -> buffer_info{
		return buffer_info(
			vector.data(),
			sizeof(double),
			format_descriptor<double>::format(),
			1,
			{size_t(vector.size())},
			{sizeof(double)}
		);
		})
	//.def("create_vector_graph", [](std::vector<double>& vec, int samplesPerVector, double unitaryLength, bool relative , double average, double averageScale)->Vectors<std::vector<sp::timecode<double>>>{
	//	auto op = speczilla::Buffer<double>(&vec,vec.size(),samplesPerVector,unitaryLength,relative,average,averageScale);
	//	return op();//is sp::result, not std::vector<timecode>
    //},arg("samplesPerVector")=1,arg("unitaryLength")=1.0,arg("relative")=false,arg("average")=0.0,arg("averageScale")=1.0)
	;*/
	m.def("create_vector_graph", [](std::vector<double>& vec, int samplesPerVector, double unitaryLength, bool relative , double average, double averageScale)->array_t<sp::timecode<double>,array::c_style>{
		auto op = speczilla::Buffer<double>(&vec,vec.size(),samplesPerVector,unitaryLength,relative,average,averageScale);
		Vectors<std::vector<sp::timecode<double>>> result = Vectors<std::vector<sp::timecode<double>>>{std::move(op())};
		return cast(result);//is sp::result, not std::vector<timecode>
	},arg("vector"),arg("samplesPerVector")=1,arg("unitaryLength")=1.0,arg("relative")=false,arg("average")=0.0,arg("averageScale")=1.0);

//    class_<samples_To_VG<double>>(m,"Samples_To_VG")
//            .def(init<size_t,double,std::vector<size_t>>())//needs std::vector<size_t> type
////            .def("exec",overload_cast<fexec&, vector_single<double>,vector_single<double>,vector_pair<double>,angle::angle&>(&samples_To_VG::operator()<fexec,vector_single<double>,vector_pair<double>,angle::angle>))
////            .def("exec",overload_cast<fexec&, vector_single<double>,vector_single<double>,vector_pair<double>,angle::angle&>(&samples_To_VG::operator()))
////            .def("exec",(void (samples_To_VG::*)(fexec&, vector_single<double>,vector_single<double>,vector_pair<double>,angle::angle&)) &samples_To_VG::operator()<fexec,vector_single<double>,vector_pair<double>,angle::angle> )
////            .def("exec",(void (samples_To_VG::*)(fexec&, vector_single<double>,vector_single<double>,vector_pair<double>,angle::angle&)) &samples_To_VG::operator() )
//            .def("exec", &samples_To_VG<double>::operator()<angle::sharing_angle&>)//return type needs definition of sp::result!!!
//            ;

}

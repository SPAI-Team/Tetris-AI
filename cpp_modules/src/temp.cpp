#include <boost/python.hpp>

int adder(int a, int b) {
	return a + b;
}

BOOST_PYTHON_MODULE(hello_ext) {
	using namespace boost::python;
	def ('adder', adder)
}
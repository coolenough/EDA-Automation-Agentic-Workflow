#include <pybind11/pybind11.h>

namespace py = pybind11;

#include<thread>
#include<vector>

#define CORES = std::thread::hardware_concurrency();

template<typename Func ,typename DataType>
void parrallel_processing(Func tool , DataType data , size_t size)
{
    // ensure that you create new threads only when you have proper data 
    // or else you might end up doing the same work repetedly on all of your CORES;
    if(size == 0) return;
    
    //unlocking gil to make sure that we can use multi threading;
    //uses RAII -- > resource aquisitaion as initiliaztion
    py::gil_scoped_release release;

    // typically the data is the start pointer and 
    // here size = end - data 
    // assuming end to be exclusive
    // using size_t to ensure they are unsigned
    std::vector<std::thread> workers;

    size_t chunkSize = size/CORES;
    

    for(int i = 0; i < CORES ; i++)
    {
        std::cout<<"Starting Thread : "<< i + 1<<std::endl;

        DataType start = data + (i*chunkSize);
        DataType end =  (i == CORES - 1) ? (size + data) : (start + chunkSize);

        workers.push_back(std::thread(tool , start , end));
    }

    for(std::thread &t : workers){
        if(t.joinable()) t.join();
    }
    return;
}
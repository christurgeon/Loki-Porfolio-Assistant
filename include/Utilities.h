#pragma once

#include <math.h>

class Utilities 
{
    public:
        static double delta(double open, double current)
        {
            return (current - open) / open * 100;
        }
};
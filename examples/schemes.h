#pragma once

#include <stdint.h>

class User
{
public:
    int32_t GetId() const;
    const char* GetName() const;
     
private:
    int32_t m_i32Id;
    char m_szName;
     
};

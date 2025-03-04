
int64_t CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_01_bad()

{
    void* fsbase;
    int64_t rax = *(fsbase + 0x28);
    void* const var_28 = "0123456789abcdef0123456789abcde";
    printLine("0123456789abcdef0123456789abcde");
    void var_38;
    memcpy(&var_38, "0123456789abcdef0123456789abcde", 0x20);
    char var_29 = 0;
    printLine(&var_38);
    printLine(var_28);
    int64_t result = (rax ^ *(fsbase + 0x28));

    if (result == 0)
        return result;

    __stack_chk_fail();
    
}
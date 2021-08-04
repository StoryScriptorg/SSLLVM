from llvmlite import ir

# Integers
int_sbyte = ir.IntType(8)  # Signed byte
int_short = ir.IntType(16)  # Short
int_integer = ir.IntType(32)  # Standard Integer
int_long = ir.IntType(64)  # Long

# Type Size reference: C# Type byte size

# Other numeric types
float_float = ir.FloatType()
double_double = ir.DoubleType()

# Special types
void_void = ir.VoidType()  # Return type for methods

# Arrays
def InitializeArray(valtype, size):
    """
    Initialize an Array.
    """
    return ir.ArrayType(valtype, size)


def InitializeList(valtype, start_size):
    """
    Initialize a Vector. (Dynamic Array)
    """
    return ir.VectorType(valtype, start_size)

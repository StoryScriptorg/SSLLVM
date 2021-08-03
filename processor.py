from builder import buildIRFromCache
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int
from argparse import ArgumentParser

def create_execution_engine():
	"""
	Create an ExecutionEngine suitable for JIT code generation on
	the host CPU. The engine is reusable for an arbitrary number of
	modules.
	"""

	# Create a target machine representing the host
	target = llvm.Target.from_default_triple()
	target_machine = target.create_target_machine()
	# And an execution engine with an empty backing module
	backing_mod = llvm.parse_assembly("")
	engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
	llvm.check_jit_execution()
	return engine

def init():
	llvm.initialize()
	llvm.initialize_native_target()
	llvm.initialize_native_asmprinter()
	version = llvm.llvm_version_info
	print(f"[DEBUG] Running on LLVM v{version[0]}.{version[1]}.{version[2]}")
	global engine
	engine = create_execution_engine()

def compile_ir(llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()
    return mod

if __name__ == "__main__":
	parser = ArgumentParser(description="JITed version of StoryScript.")
	parser.add_argument("-i", "--input", help="The input file.")
	parser.add_argument("--emit-ir", help="Emit LLVM IR to a file or not.", action="store_true")
	args = parser.parse_args()
	init()
	# Enter the REPL If the input is not specified.
	if not args.input:
		print("// SSLLVM / IR Generation from Cache testing / v0.0.1a //")
		print("Type .help to see all REPL commands.")
		commands = []
		while True:
			command = input("> ")
			if command == ".buildAndGetIR":
				print(buildIRFromCache(commands))
			elif command.startswith(".buildToFile"):
				file = command.split()[1]
				with open(file, "w") as f:
					f.write(buildIRFromCache(commands))
			elif command == ".buildAndRun":
				compile_ir(buildIRFromCache(commands))

				cfunc = CFUNCTYPE(restype=c_int)(engine.get_function_address("main"))
				cfunc()
			elif command == ".help":
				print(""".help - Print this help message
.buildandGetIR - Build the IR
.buildToFile file - Build the IR to the specified file
.buildAndRun - Build the IR and run""")
			else:
				commands.append(command)

	llvm.shutdown()

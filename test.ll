; ModuleID = "main"
; LLVM IR generated by SSLLVM

@.gtempstr_0 = private unnamed_addr constant [15 x i8] c"Hello, there!\0A\00"
@.gtempstr_108 = private unnamed_addr constant [17 x i8] c"Another message\0A\00"


define i32 @main() {
entry:
	%temp_str_0 = getelementptr inbounds [15 x i8]*, @.gtempstr_0, i32 0, i32 0
	call i32 @puts(i8* %temp_str_0)
%temp_str_108 = getelementptr inbounds [17 x i8]*, @.gtempstr_108, i32 0, i32 0
	call i32 @puts(i8* %temp_str_108)

	ret i32 0
}

declare i32 @puts(i8*)

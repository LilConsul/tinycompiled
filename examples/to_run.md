
nasm -f elf64 -o test.o hello_world.asm && ld test.o -o test && ./test && rm test.o test

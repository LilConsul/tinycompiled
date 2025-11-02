To assemble and run an x86-64 assembly file named `FILENAME.asm`, use the following command in your terminal:

```bash
nasm -f elf64 -o test.o FILENAME.asm && ld test.o -o test && ./test && rm test.o test
```

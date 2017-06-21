all: multiple

libTest.a: lib.o
	ar rcs $@ $^

%.o: %.c
	gcc -c $^ -o $@

multiple: main.o libTest.a
	gcc $^ -o $@

clean:
	@ rm -f multiple *.a *.o

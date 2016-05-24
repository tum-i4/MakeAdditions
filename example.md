# Some usage examples

... time to see this tool in action ...


## bzip2

```
wget -c "http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz"
tar -zxf bzip2-1.0.6.tar.gz
cd bzip2-1.0.6
make+llvm
```

```
/home/huto/build/llvm/Release/bin/lli bzip2.x.bc --version
```

---------------
# Everything above is working


## flex

```
git clone --depth 1 --branch v2.6.1 https://github.com/westes/flex.git
cd flex
./autogen.sh
./configure CC=/home/huto/build/llvm/Release/bin/clang
make+llvm
```

## grep

** TODO

git://git.sv.gnu.org/gnulib.git

```
git clone --branch v2.25 http://git.savannah.gnu.org/r/grep.git
cd grep
./bootstrap
./configure CC=/home/huto/build/llvm/Release/bin/clang
```

### Error

```
grep.c:595:12: error: cast from 'const char *' to 'const uword *' (aka 'const unsigned long long *') increases required alignment from 1 to
      4 [-Werror,-Wcast-align]
  for (s = CAST_ALIGNED (uword const *, p); ! (*s & unibyte_mask); s++)
           ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
grep.c:540:35: note: expanded from macro 'CAST_ALIGNED'
# define CAST_ALIGNED(type, val) ((type) (val))
                                  ^~~~~~~~~~~~
1 error generated.
```

## wget

```
git clone --branch v1.17.1 http://git.savannah.gnu.org/r/wget.git
cd wget
./bootstrap
./configure CC=/home/huto/build/llvm/Release/bin/clang
```

## ngircd

```
git clone --depth 1 --branch rel-23 https://github.com/ngircd/ngircd.git
cd ngircd
./autogen.sh
./configure CC=/home/huto/build/llvm/Release/bin/clang
```

## coreutils
```
git clone --branch v8.25 http://git.savannah.gnu.org/r/coreutils.git
cd coreutils
./bootstrap
./configure CC=/home/huto/build/llvm/Release/bin/clang
```

## OpenSSL

```
git clone --depth 1 --branch OpenSSL_1_0_1t https://github.com/openssl/openssl
cd openssl
./Configure CC=/home/huto/build/llvm/Release/bin/clang

```
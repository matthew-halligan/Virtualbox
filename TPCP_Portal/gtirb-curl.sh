curl -F transform=to-static -F binary=@$(which ls) $(ldd $(which ls) | \
grep -v vdso | sed 's|^[^/]*/lib|/lib|;s/^[[:space:]]*//;s/.*$//' | sed 's/^/-F library=@/') --output ls.ts.gtirb gtirb/simple
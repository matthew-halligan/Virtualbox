#curl -F transform=ddisasm -F binary=@$(which ls) $(ldd $(which ls) | \
#grep -v vdso | sed 's|^[^/]*/lib|/lib|;s/^[[:space:]]*//;s/ .*$//'| \
#sed 's/^/-F library=@/')  --output ls.ts.gtirb http://172.20.0.6/simple --trace-ascii -


#curl -F transform=ddisasm,binary-print -F binary=@$(which ls) --output ls.ts.gtirb http://172.17.0.1/simple


#$(ldd $(which ls) | \
#grep -v vdso | sed 's|^[^/]*/lib|/lib|;s/^[[:space:]]*//;s/ .*$//'| \
#sed 's/^/-F library=@/')

curl -F transform=to-static,stack-stamp -F binary=@$(which ls) $(ldd $(which ls) | \
grep -v vdso | sed 's|^[^/]*/lib|/lib|;s/^[[:space:]]*//;s/ .*$//'| \
sed 's/^/-F library=@/')  --output ls.tss.gtirb http://$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' gtirb)/simple

sudo chmod 777 ls.tss.gtirb
sudo curl -F transform=static-binary-print -F gtirb=@./ls.tss.gtirb $(ldd $(which ls) | grep -v vdso | sed 's|^[^/]*/lib|/lib|;s/^[[:space:]]*//;s/ .*$//'| sed 's/^/-F library=@/') --output ls.tss.sbp http://$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' gtirb)/simple
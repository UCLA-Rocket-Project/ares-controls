MKDIR_BIN = @mkdir -p bin
EXEC_PERMS = chmod +x

cdhserv: cdh-server/*.py
	@echo "Making CDH Server"
	${MKDIR_BIN}
	@cd cdh-server && zip -r -q ../bin/cdh-temp.zip *
	@echo '#!/usr/bin/env python3' | cat - bin/cdh-temp.zip > bin/cdhserv
	@rm bin/cdh-temp.zip
	@${EXEC_PERMS} bin/cdhserv
	@echo "Created executable bin/cdhserv" 

cdhserv-deploy: cdhserv
	@cp bin/cdhserv /deploy/

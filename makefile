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

cdh-service-setup:
	cp pi-service/cdhserv.service /lib/systemd/system/
	chmod 644 /lib/systemd/system/cdhserv.service
	systemctl daemon-reload

moist-client: moist/*.py
	@echo "Making MOIST client"
	${MKDIR_BIN}
	@cd moist && zip -r -q ../bin/moist-temp.zip *
	@echo '#!/usr/bin/env python3' | cat - bin/moist-temp.zip > bin/moist
	@rm bin/moist-temp.zip
	@${EXEC_PERMS} bin/moist
	@echo "Created executable bin/moist"
       	
moist-deploy: moist-client
	@cp bin/moist /deploy/

moist-service-setup:
	cp pi-service/moist.service /lib/systemd/system/
	chmod 644 /lib/systemd/system/moist.service
	systemctl daemon-reload

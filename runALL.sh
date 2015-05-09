#! /bin/sh

/etc/init.d/noControlButton.sh start
/etc/init.d/noControlPhoto.sh start
/etc/init.d/noControlRequests.sh start
/etc/init.d/noControlGPS.sh start


while true
do
	/etc/init.d/noControlPhoto.sh status
	statusPhoto="$?"
	echo "StatusPhoto" "$statusPhoto"
	if [ $statusPhoto -ne 0 ]; then
		/etc/init.d/noControlPhoto.sh restart
	fi


	/etc/init.d/noControlRequests.sh status
	statusRequests="$?"
	echo "StatusRequests" "$statusRequests"
	if [ $statusRequests -ne 0 ]; then
		/etc/init.d/noControlRequests.sh restart
	fi


	/etc/init.d/noControlGPS.sh status
	statusGPS="$?"
	echo "StatusGPS" "$statusGPS"
	if [ $statusGPS -ne 0 ]; then
		/etc/init.d/noControlGPS.sh restart
	fi


	/etc/init.d/noControlButton.sh status
	statusButton="$?"
	echo "StatusButton" "$statusButton"
	if [ $statusButton -ne 0 ]; then
		/etc/init.d/noControlButton.sh restart
	fi


done

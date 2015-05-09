#! /bin/sh

### BEGIN INIT INFO
# Provide:		noControlGPS
# Required-Start:	$remote_fs $syslog
# Required-Stop:	$remote_fs $syslog
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description:	service to start python script noControlGPS
# Description:		service to start stop and restart if the script break
### END INIT INFO

DIR=/home/pi/scripts
DAEMON=$DIR/noControlGPS.py
DAEMON_NAME=noControlGPS

DAEMON_OPTS=""

DAEMON_USER=root

PIDFILE=/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start(){
	log_daemon_msg "Starting system $DAEMON_NAME daemon"
	start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --startas $DAEMON -- $DAEMON_OPTS
	log_end_msg $?
}
do_stop(){
	log_daemon_msg "Stopping system $DAEMON_NAME daemon"
	start-stop-daemon --stop --pidfile $PIDFILE --retry 10
	log_end_msg $?
}

case "$1" in

	start|stop)
		do_${1}
		;;

	restart|reload|force-reload)
		do_stop
		do_start
		;;

	status)
		status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
		;;

	*)
		echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
		exit 1
		;;
esac

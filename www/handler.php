<?php
$HOST = "18.111.23.79"; #this really should be the IP of the server on which dodona runs.
//$HOST = gethostbyname("localhost");
$PORT = 9999;
//$data = $_POST['msg'];
$data = $_GET['msg']; //I should make sure that this is in fact _GETing a set
if (!$data) $data = 0;

$verbose = $_GET['verbose'];
function debug($msg, $level){
	 global $verbose;
	 if ($level <= $verbose) echo $msg;
}

/* Create a TCP/IP socket. */
debug('Creating socket...',1);
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if ($socket === false) {
    debug("socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n",1);
} else {
    debug("OK.\n",1);
}

debug("Attempting to connect to '$HOST' on port '$PORT'...",1);
$result = socket_connect($socket, $HOST, $PORT);
if ($result === false) {
    debug("socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)) . "\n",1);
} else {
    debug("OK.\n",1);
}

debug("Sending...",1);
socket_write($socket, $data, strlen($data));
debug("OK.\n",1);

debug("Reading response...",1);
$response = '';
while ($out = socket_read($socket, 2048)) {
    $response.=$out;
}
debug("OK.\n\n",1);
debug('Sent: '.$data."\n",1);
debug('Response: '.$response."\n\n",1);

debug("Closing socket...",1);
socket_close($socket);
debug("OK.\n\n",1);

echo $response; //I should escape this echo so that if dodona responds with html, it is not rendered as such

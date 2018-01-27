<?php

// the only configuration: set your IoT device registration password here:

$passwd="passwort";


function write_php_ini($array, $file)
{
    $res = array();
    foreach($array as $key => $val)
    {
        if(is_array($val))
        {
            $res[] = "[$key]";
            foreach($val as $skey => $sval) $res[] = "$skey = ".(is_numeric($sval) ? $sval : '"'.$sval.'"');
        }
        else $res[] = "$key = ".(is_numeric($val) ? $val : '"'.$val.'"');
    }
    safefilerewrite($file, implode("\r\n", $res));
}

function safefilerewrite($fileName, $dataToSave)
{    if ($fp = fopen($fileName, 'w'))
    {
        $startTime = microtime(TRUE);
        do
        {            $canWrite = flock($fp, LOCK_EX);
           // If lock not obtained sleep for 0 - 100 milliseconds, to avoid collision and CPU load
           if(!$canWrite) usleep(round(rand(0, 100)*1000));
        } while ((!$canWrite)and((microtime(TRUE)-$startTime) < 5));

        //file was locked so now we can store information
        if ($canWrite)
        {            fwrite($fp, $dataToSave);
            flock($fp, LOCK_UN);
        }
        fclose($fp);
    }
}

if (isset($_GET['name']))
{
	// the GET variables shall be
	// url
	// name
	// password
	$iniFileName="settings.ini";
	$ini_array = parse_ini_file($iniFileName);
	// request to store IP
	if($_GET['password']==$passwd and isset($_GET['url']))
	{
		$ini_array[$_GET['name']]=$_GET['url'];
		write_php_ini($ini_array, $iniFileName);
		echo "Device registered as ".$_GET['name']. " with the URL " .$_GET['url'];
	}else{
		if(isset($ini_array[$_GET['name']]))
		{
			header("Location: ".$ini_array[$_GET['name']]);
			die();
		}else{
			echo "Unknown Device: ".$_GET['name'];
		}
	}
}else{
?>
<html>
<body>
<h2>Simple URL Redirector</h2>
Let you register IoT devices with changing IP addresses on a server with fixed URL:
<p>
<h3>Usage</h3>
To register a device, call this page with a GET call containing the parameters: name: The name the device should be reached by /url: the urlencoded URL to which it should be redirected to / password= the password as configured
<p>
To get forwarded to a registered device, call this page with a GET call containing the parameter name: The name the device should be reached by
</body>
</html>
<?php
}
?>
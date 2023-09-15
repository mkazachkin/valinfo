<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
$zip = new ZipArchive;
if ($zip->open('../upload.zip') === TRUE) {
    $zip->extractTo('../db/');
    $zip->close();
    $result = 'success';
} else {
    $result = 'failed';
}
unlink('../upload.zip');
header("Content-Type:text/plain");
echo $result;
?>
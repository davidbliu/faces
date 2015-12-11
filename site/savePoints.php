<?php
if(!empty($_POST['data'])){
$data = $_POST['data'];
$imRoot = $_POST['imRoot'];
$fname = $imRoot;

$file = fopen("./points/" .$fname, 'w');//creates new file
fwrite($file, $data);
fclose($file);
}
?>

<?php
 //$json_string = $_POST["sfg"];
 //echo $json_string;
 $result  = file_get_contents('php://input');
 echo json_encode($result);
?>
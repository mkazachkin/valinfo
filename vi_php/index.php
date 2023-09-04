<?php
$cadnum = "11:10:5701001:10";
$data_file = fopen('data.csv', 'r') or die($php_errormsg);
$data = array();
$data_w_cost = array();
$cost_tours = array();
$flag = false;
$done = false;
$head = fgetcsv($data_file, 4096, '&');
while ($row = fgetcsv($data_file, 4096, '&') and !$done) {
    if ($row[0] == $cadnum) {
        $data[] = ($row);
        if ($row[2] == 'Кадастровая стоимость') {
            $cost_tours[] = $row[1];
        }
        $flag = true;
    } elseif ($flag) {
        $done = true;
    }
}
fclose($data_file);
foreach ($data as $row) {
    if (in_array($row[1], $cost_tours)) {
        $data_w_cost[] = $row;
    }
}
$flag = true;
$table_opened = false;
$tour = 0;
foreach ($data_w_cost as $row) {
    if ($row[1] != $cost_tours[$tour]) {
        $tour++;
        $flag = true;
    }
    if ($flag) {
        if ($table_opened) {
            echo ("</table>\n");
        }
        echo ("<p>Тур оценки: " . $cost_tours[$tour] . "</p>\n");
        $flag = false;
        echo ("<table>\n");
        echo ("<tr><th>" . $head[2] . "</th><th>" . $head[3] . "</th><th>" . $head[4] . "</th></tr>\n");
        $table_opened = true;
    }
    echo ("<tr><td>" . $row[2] . "</td><td>" . $row[3] . "</td><td>" . $row[4] . "</td></tr>\n");
}
if ($table_opened) {
    echo ("</table>\n");
}
?>
<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
if (isset($_POST['cadnum'])) {
    $cadnum = $_POST['cadnum'];
    $level1 = substr(str_replace(':', '', $cadnum), -3, 1);
    $level2 = substr($cadnum, -2, 1);
    $level3 = substr($cadnum, -1);
    $file_name = "../db/{$level1}/{$level2}/{$level3}/data.csv";
    $result = "";
    if (file_exists($file_name) && ($data_file = fopen($file_name, 'r')) !== false) {
        $data = array();
        $data_w_cost = array();
        $cost_tours = array();
        $flag = false;
        $done = false;
        $head = fgetcsv($data_file, 4096, '&');
        while ($row = fgetcsv($data_file, 4096, '&') and !$done) {
            if ($row[0] == $cadnum) {
                $data[] = $row;
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
        if (!empty($data_w_cost)) {
            $result = $result . "<h2>Кадастровый номер: " . $cadnum . "</h2>\n";
            foreach ($data_w_cost as $row) {
                if ($row[1] != $cost_tours[$tour]) {
                    $tour++;
                    $flag = true;
                }
                if ($flag) {
                    if ($table_opened) {
                        $result = $result . "</table>\n";
                    }
                    $result = $result . "<h3>Тур оценки: " . $cost_tours[$tour] . "</h3>\n";
                    $flag = false;
                    $result = $result . "<table class='table_blur' border='0' cellpadding = '0' width='100%'>\n";
                    $result = $result . "<thead><tr><th width = '25%'>" . $head[2] . "</th><th width = '60%'>" . $head[3] . "</th><th width = '15%'>" . $head[4] . "</th></tr></thead>\n";
                    $result = $result . "<tbody>";
                    $table_opened = true;
                }
                $result = $result . "<tr><td>" . $row[2] . "</td><td>" . $row[3] . "</td><td>" . $row[4] . "</td></tr>\n";
            }
            if ($table_opened) {
                $result = $result . "</tbody>\n</table>\n";
            }
        } else {
            $result = $result . '<h2>Кадастровый номер ' . $cadnum . ' отсутствует в базе данных учреждения</h2>';
        }
    }
} else {
    $result = $result . '<h2>Кадастровый номер ' . $cadnum . ' отсутствует в базе данных учреждения</h2>';
}
header("Content-Type:text/plain");
echo $result;
?>
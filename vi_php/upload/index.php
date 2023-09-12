<?php
require_once($_SERVER["DOCUMENT_ROOT"] . "/bitrix/header.php");
$APPLICATION->SetTitle("Поиск объекта недвижимости");
?>
<link href="/assessment/style.css" rel="stylesheet" />
<link href="/fa/css/all.css" rel="stylesheet" />
<div id="search_kn_wrap">
    <form id="search_kn_form">
        <input type="text" id="search_kn_input" placeholder="11:__:_______:_____" data-slots="_" data-accept="\d" />
        <div class="search_kn_button" onclick="search_cadnum();">
            <i class="fas fa-search"></i>
            <span>Поиск</span>
            <div class="search_loader_wrap">
                <div class="find_spin_wrapper">
                    <svg width="100%" height="100%" viewBox="0 0 42 42" class="find_spin">
                        <circle class="find_spin_segment" cx="21" cy="21" r="15.91549430918954" fill="transparent"
                            stroke="#68497f" stroke-width="3" stroke-dasharray="0 100" stroke-dashoffset="25"></circle>
                    </svg>
                </div>
            </div>
        </div>
    </form>
    <div id="res_table">

    </div>
</div>
<div id="tax_info">
    <p>
        Расчет налога на имущество физических лиц, доступен на сайте&nbsp;<a
            href="https://www.nalog.ru/rn11/service/nalog_calc/" target="_blank">ФНС России.</a>
    </p>
    <p>
        Налоговые ставки и льготы для физических и юридических лиц см. в разделе&nbsp;<a
            href="https://www.nalog.ru/rn11/service/tax/" target="_blank">справочной информации</a>
        &nbsp;сайта ФНС России.
    </p>
</div>
<script src="/assessment/jquery/jquery.js"></script>
<script src="/assessment/jquery/maskedinput.js"></script>
<script src="/assessment/nfind/scripts/valinfo.js"></script>

<?php
require_once($_SERVER["DOCUMENT_ROOT"] . "/bitrix/footer.php");
?>
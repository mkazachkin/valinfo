SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE valuation_info_2023_1;
CREATE DATABASE valuation_info_2023_1 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Russian_Russia.1251';
ALTER DATABASE valuation_info_2023_1 OWNER TO postgres;
\connect valuation_info_2023_1
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
CREATE SCHEMA public;
ALTER SCHEMA public OWNER TO postgres;
COMMENT ON SCHEMA public IS 'standard public schema';

CREATE TYPE public.datatype AS ENUM (
    '_integer',
    '_float',
    '_date',
    '_datetime',
    '_string'
);
ALTER TYPE public.datatype OWNER TO postgres;
SET default_tablespace = '';
SET default_table_access_method = heap;

CREATE TABLE public.d_paragraph (
    paragraph_id integer NOT NULL,
    paragraph_code character varying(10) NOT NULL,
    paragraph_annotation character varying NOT NULL
);
ALTER TABLE public.d_paragraph OWNER TO postgres;
COMMENT ON TABLE public.d_paragraph IS 'Перечень статей ФЗ О государственной кадастровой оценке, по которым производится оценка кадастровой стоимости недвижимости';
COMMENT ON COLUMN public.d_paragraph.paragraph_id IS 'Идентификатор';
COMMENT ON COLUMN public.d_paragraph.paragraph_code IS 'Номер статьи ФЗ О государственной кадастровой оценке';
COMMENT ON COLUMN public.d_paragraph.paragraph_annotation IS 'Название статьи ФЗ О государственной кадастровой оценке';

CREATE TABLE public.d_parameter_type (
    param_typ_id integer NOT NULL,
    unit_id integer,
    param_type_datatype public.datatype NOT NULL,
    param_annotation character varying
);
ALTER TABLE public.d_parameter_type OWNER TO postgres;
COMMENT ON TABLE public.d_parameter_type IS 'Словарь характеристик объектов';
COMMENT ON COLUMN public.d_parameter_type.param_typ_id IS 'Идентификатор';
COMMENT ON COLUMN public.d_parameter_type.unit_id IS 'Идентификатор единицы измерения';
COMMENT ON COLUMN public.d_parameter_type.param_type_datatype IS 'Тип данных';
COMMENT ON COLUMN public.d_parameter_type.param_annotation IS 'Название характеристики';

CREATE TABLE public.d_realty (
    realty_id integer NOT NULL,
    realty_code character varying(12) NOT NULL,
    realty_annotation character varying NOT NULL
);
ALTER TABLE public.d_realty OWNER TO postgres;
COMMENT ON TABLE public.d_realty IS 'Виды объектов недвижимости';
COMMENT ON COLUMN public.d_realty.realty_id IS 'Идентификатор';
COMMENT ON COLUMN public.d_realty.realty_code IS 'Код по справочнику dRealty';
COMMENT ON COLUMN public.d_realty.realty_annotation IS 'Вид объекта недвижимости';

CREATE TABLE public.d_unit (
    unit_id integer NOT NULL,
    unit_code character varying(4) NOT NULL,
    unit_annotation character varying NOT NULL
);
ALTER TABLE public.d_unit OWNER TO postgres;
COMMENT ON TABLE public.d_unit IS 'Единицы измерений по ОКЕИ';
COMMENT ON COLUMN public.d_unit.unit_id IS 'Идентификатор';
COMMENT ON COLUMN public.d_unit.unit_code IS 'Код по справочнику dUnit';
COMMENT ON COLUMN public.d_unit.unit_annotation IS 'Единица измерения';

CREATE TABLE public.l_xml_to_cadnum (
    link_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    xml_id uuid NOT NULL,
    cadnum_id uuid NOT NULL
);
ALTER TABLE public.l_xml_to_cadnum OWNER TO postgres;
COMMENT ON TABLE public.l_xml_to_cadnum IS 'Привязка объекта недвижимости к XML файлу';
COMMENT ON COLUMN public.l_xml_to_cadnum.link_id IS 'Идентификатор';
COMMENT ON COLUMN public.l_xml_to_cadnum.xml_id IS 'Идентификатор XML файла';
COMMENT ON COLUMN public.l_xml_to_cadnum.cadnum_id IS 'Идентификатор кадастрового номера объекта недвижимости';

CREATE TABLE public.t_cadnum (
    cadnum_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    realty_id integer NOT NULL,
    cadnum_code character varying(40) NOT NULL,
    first_list_id uuid NOT NULL
);
ALTER TABLE public.t_cadnum OWNER TO postgres;
COMMENT ON TABLE public.t_cadnum IS 'Перечень кадастровых номеров объектов';
COMMENT ON COLUMN public.t_cadnum.cadnum_id IS 'Идентификатор';
COMMENT ON COLUMN public.t_cadnum.realty_id IS 'Идентификатор вида объекта недвижимости';
COMMENT ON COLUMN public.t_cadnum.cadnum_code IS 'Написание кадастрового номера';
COMMENT ON COLUMN public.t_cadnum.first_list_id IS 'Идентификатор перечня, в котором впервые на оценку пришел объект недвижимости';

CREATE TABLE public.t_list (
    list_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    paragraph_id integer NOT NULL,
    rr_code character varying NOT NULL,
    rr_date date NOT NULL,
    in_code character varying NOT NULL,
    in_date date NOT NULL,
    in_new_objects_num integer NOT NULL,
    in_old_objects_num integer NOT NULL,
    found_date_f date NOT NULL,
    found_date_l date NOT NULL,
    act_code character varying,
    act_date date,
    out_new_objects_rated integer,
    out_old_objects_rated integer,
    out_objects_not_rated integer
);
ALTER TABLE public.t_list OWNER TO postgres;
COMMENT ON TABLE public.t_list IS 'Список перечней объектов недвижимости, поступивших на оценку кадастровой стоимости';
COMMENT ON COLUMN public.t_list.list_id IS 'Идентификатор';
COMMENT ON COLUMN public.t_list.paragraph_id IS 'Идентификатор статьи ФЗ о кадастровой оценке';
COMMENT ON COLUMN public.t_list.rr_code IS 'Исходящий номер сопроводительного письма с входящим перечнем';
COMMENT ON COLUMN public.t_list.rr_date IS 'Исходящая дата сопроводительного письма с входящим перечнем';
COMMENT ON COLUMN public.t_list.in_code IS 'Входящий номер сопроводительного письма с входящим перечнем';
COMMENT ON COLUMN public.t_list.in_date IS 'Входящая дата сопроводительного письма с входящим перечнем';
COMMENT ON COLUMN public.t_list.in_new_objects_num IS 'Количество вновь учтенных объектов во входящем перечне';
COMMENT ON COLUMN public.t_list.in_old_objects_num IS 'Количество ранее учтенных объектов во входящем перечне';
COMMENT ON COLUMN public.t_list.found_date_f IS 'Начальная дата периода возникновения основания для определения кадастровой стоимости объектов входящего перечня';
COMMENT ON COLUMN public.t_list.found_date_l IS 'Конечная дата периода возникновения основания для определения кадастровой стоимости объектов входящего перечня';
COMMENT ON COLUMN public.t_list.act_code IS 'Номер акта определения кадастровой стоимости';
COMMENT ON COLUMN public.t_list.act_date IS 'Дата составления акта определения кадастровой стоимости';
COMMENT ON COLUMN public.t_list.out_new_objects_rated IS 'Количество вновь учтенных объектов, для которых была проведена оценка кадастровой стоимости';
COMMENT ON COLUMN public.t_list.out_old_objects_rated IS 'Количество ранее учтенных объектов, для которых была проведена оценка кадастровой стоимости';
COMMENT ON COLUMN public.t_list.out_objects_not_rated IS 'Количество объектов, для которых определение кадастровой стоимости не проводилось';

CREATE TABLE public.t_list_xml (
    xml_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    list_id uuid NOT NULL,
    xml_name character varying(260) NOT NULL,
    is_result bool NOT NULL
);
ALTER TABLE public.t_list_xml OWNER TO postgres;
COMMENT ON TABLE public.t_list_xml IS 'Список XML файлов';
COMMENT ON COLUMN public.t_list_xml.xml_id IS 'Идентификатор';
COMMENT ON COLUMN public.t_list_xml.list_id IS 'Идентификатор перечня объектов недвижимости';
COMMENT ON COLUMN public.t_list_xml.xml_name IS 'Имя файла';
COMMENT ON COLUMN public.t_list_xml.is_result IS 'Признак файла с результатами оценки';

CREATE TABLE public.t_parameter (
    param_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    link_id uuid NOT NULL,
    param_typ_id integer NOT NULL,
    value character varying
);
ALTER TABLE public.t_parameter OWNER TO postgres;
COMMENT ON TABLE public.t_parameter IS 'Список характеристик объекта';
COMMENT ON COLUMN public.t_parameter.param_id IS 'Идентификатор';
COMMENT ON COLUMN public.t_parameter.link_id IS 'Идентификатор связи объекта с XML файлом (и перечнем)';
COMMENT ON COLUMN public.t_parameter.param_typ_id IS 'Идентификатор названия параметра';

CREATE TABLE public.t_parameter_annulment (
    annulment_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    list_id uuid NOT NULL,
    param_id uuid NOT NULL
);
ALTER TABLE public.t_parameter_annulment OWNER TO postgres;
COMMENT ON TABLE public.t_parameter_annulment IS 'Таблица аннулированных результатов оценки кадастровой стоимости';
COMMENT ON COLUMN public.t_parameter_annulment.annulment_id IS 'Идентификатор';
COMMENT ON COLUMN public.t_parameter_annulment.list_id IS 'Идентификатор перечня корректировки';
COMMENT ON COLUMN public.t_parameter_annulment.param_id IS 'Идентификатор корректируемого параметра';

INSERT INTO public.d_paragraph VALUES (130, 'Ст. 13', 'Перечень объектов недвижимости, подлежащий государственной кадастровой оценке');
INSERT INTO public.d_paragraph VALUES (150, 'Ст. 15', 'Перечень вновь учтенных и ранее учтенных объектов, в сведения о которых внесены изменения до даты начала применения кадастровой стоимости');
INSERT INTO public.d_paragraph VALUES (160, 'Ст. 16', 'Перечень вновь учтенных объектов и ранее учтенных объектов, в сведения о которых внесены изменения');
INSERT INTO public.d_paragraph VALUES (161, 'Ст. 16.15', 'Перечень вновь учтенных и ранее учтенных объектов, оцениваемых по ст. 15 после завершения соответствующего тура оценки');
INSERT INTO public.d_paragraph VALUES (210, 'Ст. 21', 'Перечень объектов недвижимости, в сведениях о которых содержались ошибки при определении кадастровой стоимости');
INSERT INTO public.d_paragraph VALUES (211, 'Ст. 21.00', 'Перечень объектов недвижимости, в сведениях о которых содержались ошибки при определении кадастровой стоимости');
INSERT INTO public.d_paragraph VALUES (212, 'Ст. 21.16', 'Перечень вновь учтенных объектов и ранее учтенных объектов, оцениваемых после завершения соответствующего тура оценки');

INSERT INTO public.d_parameter_type VALUES (1000, 1001, '_string', 'Вид земельного участка');
INSERT INTO public.d_parameter_type VALUES (2000, 55, '_float', 'Площадь');
INSERT INTO public.d_parameter_type VALUES (3000, 1001, '_string', 'Местоположение');
INSERT INTO public.d_parameter_type VALUES (4000, 1001, '_string', 'Категория земель');
INSERT INTO public.d_parameter_type VALUES (5000, 1001, '_string', 'Вид разрешенного использования');
INSERT INTO public.d_parameter_type VALUES (6000, 1002, '_float', 'Удельный показатель кадастровой стоимости');
INSERT INTO public.d_parameter_type VALUES (7000, 383, '_float', 'Кадастровая стоимость');
INSERT INTO public.d_parameter_type VALUES (8000, 1001, '_string', 'Группа расчета');
INSERT INTO public.d_parameter_type VALUES (9000, 1001, '_date', 'Дата применения кадастровой стоимости');

INSERT INTO public.d_realty VALUES (2001001000, '002001001000', 'Земельный участок');
INSERT INTO public.d_realty VALUES (2001002000, '002001002000', 'Здание');
INSERT INTO public.d_realty VALUES (2001003000, '002001003000', 'Помещение');
INSERT INTO public.d_realty VALUES (2001004000, '002001004000', 'Сооружение');
INSERT INTO public.d_realty VALUES (2001005000, '002001005000', 'Объект незавершённого строительства');
INSERT INTO public.d_realty VALUES (2001006000, '002001006000', 'Предприятие как имущественный комплекс');
INSERT INTO public.d_realty VALUES (2001008000, '002001008000', 'Единый недвижимый комплекс');
INSERT INTO public.d_realty VALUES (2001009000, '002001009000', 'Машино-место');
INSERT INTO public.d_realty VALUES (2001010000, '002001010000', 'Иной объект недвижимости');

INSERT INTO public.d_unit VALUES (3, '003', 'Миллиметр');
INSERT INTO public.d_unit VALUES (4, '004', 'Сантиметр');
INSERT INTO public.d_unit VALUES (5, '005', 'Дециметр');
INSERT INTO public.d_unit VALUES (6, '006', 'Метр');
INSERT INTO public.d_unit VALUES (8, '008', 'Километр');
INSERT INTO public.d_unit VALUES (9, '009', 'Мегаметр');
INSERT INTO public.d_unit VALUES (47, '047', 'Морская миля');
INSERT INTO public.d_unit VALUES (50, '050', 'Квадратный миллиметр');
INSERT INTO public.d_unit VALUES (51, '051', 'Квадратный сантиметр');
INSERT INTO public.d_unit VALUES (53, '053', 'Квадратный дециметр');
INSERT INTO public.d_unit VALUES (55, '055', 'Квадратный метр');
INSERT INTO public.d_unit VALUES (58, '058', 'Тысяча квадратных метров');
INSERT INTO public.d_unit VALUES (59, '059', 'Гектар');
INSERT INTO public.d_unit VALUES (61, '061', 'Квадратный километр');
INSERT INTO public.d_unit VALUES (109, '109', 'Ар (100 м2)');
INSERT INTO public.d_unit VALUES (359, '359', 'Сутки');
INSERT INTO public.d_unit VALUES (360, '360', 'Неделя');
INSERT INTO public.d_unit VALUES (361, '361', 'Декада');
INSERT INTO public.d_unit VALUES (362, '362', 'Месяц');
INSERT INTO public.d_unit VALUES (364, '364', 'Квартал');
INSERT INTO public.d_unit VALUES (365, '365', 'Полугодие');
INSERT INTO public.d_unit VALUES (366, '366', 'Год');
INSERT INTO public.d_unit VALUES (383, '383', 'Рубль');
INSERT INTO public.d_unit VALUES (384, '384', 'Тысяча рублей');
INSERT INTO public.d_unit VALUES (385, '385', 'Миллион рублей');
INSERT INTO public.d_unit VALUES (386, '386', 'Миллиард рублей');
INSERT INTO public.d_unit VALUES (1000, '1000', 'Неопределено');
INSERT INTO public.d_unit VALUES (1001, '1001', '');
INSERT INTO public.d_unit VALUES (1002, '1002', 'Рублей за кв. метр');
INSERT INTO public.d_unit VALUES (1003, '1003', 'Рублей за ар');
INSERT INTO public.d_unit VALUES (1004, '1004', 'Рублей за гектар');
INSERT INTO public.d_unit VALUES (1005, '1005', 'Иные');

ALTER TABLE ONLY public.d_paragraph
    ADD CONSTRAINT d_paragraph_pkey PRIMARY KEY (paragraph_id);
ALTER TABLE ONLY public.d_parameter_type
    ADD CONSTRAINT d_parameter_type_pkey PRIMARY KEY (param_typ_id);
ALTER TABLE ONLY public.d_realty
    ADD CONSTRAINT d_realty_pkey PRIMARY KEY (realty_id);
ALTER TABLE ONLY public.d_unit
    ADD CONSTRAINT d_unit_pkey PRIMARY KEY (unit_id);
ALTER TABLE ONLY public.l_xml_to_cadnum
    ADD CONSTRAINT l_xml_to_cadnum_pkey PRIMARY KEY (link_id);
ALTER TABLE ONLY public.t_cadnum
    ADD CONSTRAINT t_cadnum_pkey PRIMARY KEY (cadnum_id);
ALTER TABLE ONLY public.t_list
    ADD CONSTRAINT t_list_pkey PRIMARY KEY (list_id);
ALTER TABLE ONLY public.t_list_xml
    ADD CONSTRAINT t_list_xml_pkey PRIMARY KEY (xml_id);
ALTER TABLE ONLY public.t_parameter
    ADD CONSTRAINT t_parameter_pkey PRIMARY KEY (param_id);
ALTER TABLE ONLY public.t_parameter_annulment
    ADD CONSTRAINT t_parameter_annulment_pkey PRIMARY KEY (annulment_id);

CREATE UNIQUE INDEX d_paragraph_paragraph_code_idx ON public.d_paragraph USING btree (paragraph_code);
CREATE INDEX d_parameter_type_unit_id_idx ON public.d_parameter_type USING btree (unit_id);
CREATE UNIQUE INDEX d_realty_realty_code_idx ON public.d_realty USING btree (realty_code);
CREATE UNIQUE INDEX d_unit_unit_code_idx ON public.d_unit USING btree (unit_code);
CREATE INDEX l_xml_to_cadnum_cadnum_id_idx ON public.l_xml_to_cadnum USING btree (cadnum_id);
CREATE INDEX l_xml_to_cadnum_xml_id_idx ON public.l_xml_to_cadnum USING btree (xml_id);
CREATE INDEX t_cadnum_realty_id_idx ON public.t_cadnum USING btree (realty_id);
CREATE INDEX t_cadnum_first_list_id_idx ON public.t_cadnum USING btree (first_list_id);
CREATE UNIQUE INDEX t_list_list_code_idx ON public.t_list USING btree (in_code);
CREATE INDEX t_list_paragraph_id_idx ON public.t_list USING btree (paragraph_id);
CREATE INDEX t_list_xml_list_id_idx ON public.t_list_xml USING btree (list_id);
CREATE INDEX t_parameter_link_id_idx ON public.t_parameter USING btree (link_id);
CREATE INDEX t_parameter_param_typ_id_idx ON public.t_parameter USING btree (param_typ_id);
CREATE INDEX t_parameter_annulment_list_id_idx ON public.t_parameter_annulment USING btree (list_id);
CREATE UNIQUE INDEX t_parameter_annulment_param_id_idx ON public.t_parameter_annulment USING btree (param_id);

ALTER TABLE ONLY public.d_parameter_type
    ADD CONSTRAINT d_parameter_type_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.d_unit(unit_id);
ALTER TABLE ONLY public.l_xml_to_cadnum
    ADD CONSTRAINT l_xml_to_cadnum_cadnum_id_fkey FOREIGN KEY (cadnum_id) REFERENCES public.t_cadnum(cadnum_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.l_xml_to_cadnum
    ADD CONSTRAINT l_xml_to_cadnum_xml_id_fkey FOREIGN KEY (xml_id) REFERENCES public.t_list_xml(xml_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_cadnum
    ADD CONSTRAINT t_cadnum_realty_id_fkey FOREIGN KEY (realty_id) REFERENCES public.d_realty(realty_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_cadnum
    ADD CONSTRAINT t_cadnum_first_list_id_fkey FOREIGN KEY (first_list_id) REFERENCES public.t_list(list_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_list
    ADD CONSTRAINT t_list_paragraph_id_fkey FOREIGN KEY (paragraph_id) REFERENCES public.d_paragraph(paragraph_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_list_xml
    ADD CONSTRAINT t_list_xml_list_id_fkey FOREIGN KEY (list_id) REFERENCES public.t_list(list_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_parameter
    ADD CONSTRAINT t_parameter_link_id_fkey FOREIGN KEY (link_id) REFERENCES public.l_xml_to_cadnum(link_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_parameter
    ADD CONSTRAINT t_parameter_param_typ_id_fkey FOREIGN KEY (param_typ_id) REFERENCES public.d_parameter_type(param_typ_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_parameter_annulment
    ADD CONSTRAINT t_parameter_annulment_list_id_fkey FOREIGN KEY (list_id) REFERENCES public.t_list(list_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_parameter_annulment
    ADD CONSTRAINT t_parameter_annulment_param_id_fkey FOREIGN KEY (param_id) REFERENCES public.t_parameter(param_id) ON DELETE CASCADE;
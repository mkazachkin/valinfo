CREATE SCHEMA public;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
ALTER SCHEMA public OWNER TO postgres;
COMMENT ON SCHEMA public IS 'standard public schema';
SET default_tablespace = '';
SET default_table_access_method = heap;

CREATE TYPE public.datatype AS ENUM (
    '_integer',
    '_float',
    '_date',
    '_datetime',
    '_string'
);
ALTER TYPE public.datatype OWNER TO postgres;

CREATE TABLE public.d_paragraph (
    paragraph_id int4 NOT NULL,
    paragraph_code character varying(6) NOT NULL,
    paragraph_annotation character varying NOT NULL
);
ALTER TABLE public.d_paragraph OWNER TO postgres;
COMMENT ON TABLE public.d_paragraph IS 'Перечень статей ФЗ О государственной кадастровой оценке, по которым производится оценка кадастровой стоимости недвижимости';
COMMENT ON COLUMN public.d_paragraph.paragraph_id IS 'Идентификатор';
COMMENT ON COLUMN public.d_paragraph.paragraph_code IS 'Номер статьи ФЗ О государственной кадастровой оценке';
COMMENT ON COLUMN public.d_paragraph.paragraph_annotation IS 'Название статьи ФЗ О государственной кадастровой оценке';

CREATE TABLE public.d_parameter_type (
    param_typ_id int4 NOT NULL,
    unit_id int4,
    param_type_datatype public.datatype NOT NULL,
    param_annotation character varying,
);
ALTER TABLE public.d_parameter_type OWNER TO postgres;
COMMENT ON TABLE public.d_parameter_type IS 'Словарь характеристик объектов';
COMMENT ON COLUMN public.d_parameter_type.param_typ_id IS 'Идентификатор';
COMMENT ON COLUMN public.d_parameter_type.unit_id IS 'Идентификатор единицы измерения';
COMMENT ON COLUMN public.d_parameter_type.param_type_datatype IS 'Тип данных';
COMMENT ON COLUMN public.d_parameter_type.param_annotation IS 'Название характеристики';
COMMENT ON COLUMN public.d_parameter_type.param_code IS 'Порядок вывода характеристики';

CREATE TABLE public.d_realty (
    realty_id int4 NOT NULL,
    realty_code character varying(12) NOT NULL,
    realty_annotation character varying NOT NULL
);
ALTER TABLE public.d_realty OWNER TO postgres;
COMMENT ON TABLE public.d_realty IS 'Виды объектов недвижимости';
COMMENT ON COLUMN public.d_realty.realty_id IS 'Идентификатор';
COMMENT ON COLUMN public.d_realty.realty_code IS 'Код по справочнику dRealty';
COMMENT ON COLUMN public.d_realty.realty_annotation IS 'Вид объекта недвижимости';

CREATE TABLE public.d_unit (
    unit_id int4 NOT NULL,
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
    realty_id int4 NOT NULL,
    cadnum_code character varying(40) NOT NULL
);
ALTER TABLE public.t_cadnum OWNER TO postgres;
COMMENT ON TABLE public.t_cadnum IS 'Перечень кадастровых номеров объектов';
COMMENT ON COLUMN public.t_cadnum.cadnum_id IS 'Идентификатор';
COMMENT ON COLUMN public.t_cadnum.realty_id IS 'Идентификатор вида объекта недвижимости';
COMMENT ON COLUMN public.t_cadnum.cadnum_code IS 'Написание кадастрового номера';

CREATE TABLE public.t_list (
    list_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    paragraph_id int4 NOT NULL,
    list_code character varying NOT NULL,
    list_annotation character varying,
    list_date date NOT NULL,
    start_date date NOT NULL,
    end_date date
);
ALTER TABLE public.t_list OWNER TO postgres;
COMMENT ON TABLE public.t_list IS 'Список перечней объектов недвижимости, поступивших на оценку кадастровой стоимости';
COMMENT ON COLUMN public.t_list.list_id IS 'Идентификатор';
COMMENT ON COLUMN public.t_list.paragraph_id IS 'Идентификатор статьи ФЗ О государственной кадастровой оценке';
COMMENT ON COLUMN public.t_list.list_code IS 'Номер перечня';
COMMENT ON COLUMN public.t_list.list_annotation IS 'Сопроводительная информация';
COMMENT ON COLUMN public.t_list.list_date IS 'Дата формирования перечня';
COMMENT ON COLUMN public.t_list.start_date IS 'Дата принятия перечня в работу';
COMMENT ON COLUMN public.t_list.end_date IS 'Дата определения кадастровой стоимости';

CREATE TABLE public.t_list_xml (
    xml_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    list_id uuid NOT NULL,
    xml_name character varying(260) NOT NULL,
    is_result boolean NOT NULL
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
    param_typ_id int4 NOT NULL,
    value character varying
);
ALTER TABLE public.t_parameter OWNER TO postgres;
COMMENT ON TABLE public.t_parameter IS 'Список характеристик объекта';
COMMENT ON COLUMN public.t_parameter.param_id IS 'Идентификатор';
COMMENT ON COLUMN public.t_parameter.link_id IS 'Идентификатор связи объекта с XML файлом (и перечнем)';
COMMENT ON COLUMN public.t_parameter.param_typ_id IS 'Идентификатор названия параметра';

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

CREATE UNIQUE INDEX d_paragraph_paragraph_code_idx ON public.d_paragraph USING btree (paragraph_code);
CREATE INDEX d_parameter_type_unit_id_idx ON public.d_parameter_type USING btree (unit_id);
CREATE UNIQUE INDEX d_realty_realty_code_idx ON public.d_realty USING btree (realty_code);
CREATE UNIQUE INDEX d_unit_unit_code_idx ON public.d_unit USING btree (unit_code);
CREATE INDEX l_xml_to_cadnum_cadnum_id_idx ON public.l_xml_to_cadnum USING btree (cadnum_id);
CREATE INDEX l_xml_to_cadnum_xml_id_idx ON public.l_xml_to_cadnum USING btree (xml_id);
CREATE INDEX t_cadnum_realty_id_idx ON public.t_cadnum USING btree (realty_id);
CREATE UNIQUE INDEX t_list_list_code_idx ON public.t_list USING btree (list_code);
CREATE INDEX t_list_paragraph_id_idx ON public.t_list USING btree (paragraph_id);
CREATE INDEX t_list_xml_list_id_idx ON public.t_list_xml USING btree (list_id);
CREATE INDEX t_parameter_link_id_idx ON public.t_parameter USING btree (link_id);
CREATE INDEX t_parameter_param_typ_id_idx ON public.t_parameter USING btree (param_typ_id);

ALTER TABLE ONLY public.d_parameter_type
    ADD CONSTRAINT d_parameter_type_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.d_unit(unit_id);
ALTER TABLE ONLY public.l_xml_to_cadnum
    ADD CONSTRAINT l_xml_to_cadnum_cadnum_id_fkey FOREIGN KEY (cadnum_id) REFERENCES public.t_cadnum(cadnum_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.l_xml_to_cadnum
    ADD CONSTRAINT l_xml_to_cadnum_xml_id_fkey FOREIGN KEY (xml_id) REFERENCES public.t_list_xml(xml_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_cadnum
    ADD CONSTRAINT t_cadnum_realty_id_fkey FOREIGN KEY (realty_id) REFERENCES public.d_realty(realty_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_list
    ADD CONSTRAINT t_list_paragraph_id_fkey FOREIGN KEY (paragraph_id) REFERENCES public.d_paragraph(paragraph_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_list_xml
    ADD CONSTRAINT t_list_xml_list_id_fkey FOREIGN KEY (list_id) REFERENCES public.t_list(list_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_parameter
    ADD CONSTRAINT t_parameter_link_id_fkey FOREIGN KEY (link_id) REFERENCES public.l_xml_to_cadnum(link_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.t_parameter
    ADD CONSTRAINT t_parameter_param_typ_id_fkey FOREIGN KEY (param_typ_id) REFERENCES public.d_parameter_type(param_typ_id) ON DELETE CASCADE;

COPY public.d_paragraph (paragraph_id, paragraph_code, paragraph_annotation) FROM stdin;
13	Ст. 13	Перечень объектов недвижимости, подлежащий государственной кадастровой оценке
15	Ст. 15	Перечень вновь учтенных и ранее учтенных объектов, в сведения о которых внесены изменения до даты начала применения кадастровой стоимости
16	Ст. 16	Перечень вновь учтенных объектов и ранее учтенных объектов, в сведения о которых внесены изменения
21	Ст. 21	Перечень объектов недвижимости, в сведениях о которых содержались ошибки при определении кадастровой стоимости
\.

COPY public.d_parameter_type (param_typ_id, unit_id, param_type_datatype, param_annotation) FROM stdin;
1000	1001	_string	Вид земельного участка
2000	55	_float	Площадь
3000	1001	_string	Местоположение
4000	1001	_string	Категория земель
5000	1001	_string	Вид разрешенного использования
6000	1002	_float	Удельный показатель кадастровой стоимости
7000	383	_float	Кадастровая стоимость
8000	1001	_string	Группа расчета
9000	1001	_date	Дата применения кадастровой стоимости
\.

COPY public.d_realty (realty_id, realty_code, realty_annotation) FROM stdin;
2001001000	002001001000	Земельный участок
2001002000	002001002000	Здание
2001003000	002001003000	Помещение
2001004000	002001004000	Сооружение
2001005000	002001005000	Объект незавершённого строительства
2001006000	002001006000	Предприятие как имущественный комплекс
2001008000	002001008000	Единый недвижимый комплекс
2001009000	002001009000	Машино-место
2001010000	002001010000	Иной объект недвижимости
\.

COPY public.d_unit (unit_id, unit_code, unit_annotation) FROM stdin;
3	003	Миллиметр
4	004	Сантиметр
5	005	Дециметр
6	006	Метр
8	008	Километр
9	009	Мегаметр
47	047	Морская миля
50	050	Квадратный миллиметр
51	051	Квадратный сантиметр
53	053	Квадратный дециметр
55	055	Квадратный метр
58	058	Тысяча квадратных метров
59	059	Гектар
61	061	Квадратный километр
109	109	Ар (100 м2)
359	359	Сутки
360	360	Неделя
361	361	Декада
362	362	Месяц
364	364	Квартал
365	365	Полугодие
366	366	Год
383	383	Рубль
384	384	Тысяча рублей
385	385	Миллион рублей
386	386	Миллиард рублей
1000	1000	Неопределено
1001	1001	
1002	1002	Рублей за кв. метр
1003	1003	Рублей за ар
1004	1004	Рублей за гектар
1005	1005	Иные
\.
# Виды характеристик объектов
d_param_t = {
    # Вид земельного участка
    1000: '05553d82-ee6a-4403-8d36-5bbca0d0b71a',
    # Площадь
    2000: 'e5d72f5b-aff1-4e68-9fd0-f18ec505fd3e',
    # Местоположение
    3000: '7b885d26-3083-499d-bde8-959c08999e00',
    # Категория земель
    4000: '33e95a82-e9f5-483d-870b-4d2574e1d36e',
    # Вид разрешенного использования
    5000: '55f94c3f-8685-46f2-999d-4e206ec9a517',
    # Удельный показатель кадастровой стоимости
    6000: '4fd24453-7cd8-4378-a212-57870da84d06',
    # Кадастровая стоимость
    7000: '776b49df-7499-4b89-992e-5adf6d6c7d31',
    # Дата начала применения кадастровой стоимости
    8000: 'fbb085be-42b2-4e9d-9e3e-d32a611efdde',
    # Группа расчета
    9000: '05250279-376a-4793-82d4-4ab1ff3b0626'}

# Виды объектов недвижимости dReality и перечень кодов характеристик
d_realty = {
    'Parcel': '0dd33307-ed06-4a20-9725-95800164339a',
    'Building': '45aa3535-f5c7-469c-bd6b-5218b214a5af',
    'Flat': '8d77691c-2cfb-472f-ab5c-fdf356c5bbbb',
    'Construction': '39f35d09-bd89-4638-b5f9-5faf47952e64',
    'Uncompleted': 'd86fc823-c2cb-43c9-a218-f0f9ec4a05e6',
    'CarParkingSpace': 'd49cb8a0-b730-4f94-ba48-3fb9bc64e18d'}

# Виды земельных участков dParcels
d_parcels = {
    '01': 'Землепользование',
    '02': 'Единое землепользование',
    '03': 'Обособленный участок',
    '04': 'Условный участок',
    '05': 'Многоконтурный участок'}

# Категория земель dCategory
d_categories = {
    '003001000000': 'Земли сельскохозяйственного назначения',
    '003002000000': 'Земли населенных пунктов',
    '003003000000': 'Земли промышленности, энергетики, транспорта, связи, радиовещания, телевидения, информатики, '
                    'земли для обеспечения космической деятельности, земли обороны, безопасности и земли иного '
                    'специального назначения',
    '003004000000': 'Земли особо охраняемых территорий и объектов',
    '003005000000': 'Земли лесного фонда',
    '003006000000': 'Земли водного фонда',
    '003007000000': 'Земли запаса',
    '003008000000': 'Категория не установлена'}

# Виды разрешенного использования dUtilizations
d_util = {
    '141000000000': 'Для размещения объектов сельскохозяйственного назначения и сельскохозяйственных угодий',
    '141001000000': 'Для сельскохозяйственного производства',
    '141001010000': 'Для использования в качестве сельскохозяйственных угодий',
    '141001020000': 'Для размещения зданий, строений, сооружений, используемых для производства, хранения и первичной '
                    'переработки сельскохозяйственной продукции',
    '141001030000': 'Для размещения внутрихозяйственных дорог и коммуникаций',
    '141001040000': 'Для размещения водных объектов',
    '141002000000': 'Для ведения крестьянского (фермерского) хозяйства',
    '141003000000': 'Для ведения личного подсобного хозяйства',
    '141004000000': 'Для ведения гражданами садоводства и огородничества',
    '141005000000': 'Для ведения гражданами животноводства',
    '141006000000': 'Для дачного строительства',
    '141007000000': 'Для размещения древесно-кустарниковой растительности, предназначенной для защиты земель от '
                    'воздействия негативных (вредных) природных, антропогенных и техногенных явлений',
    '141008000000': 'Для научно-исследовательских целей',
    '141009000000': 'Для учебных целей',
    '141010000000': 'Для сенокошения и выпаса скота гражданами',
    '141011000000': 'Фонд перераспределения',
    '141012000000': 'Для размещения объектов охотничьего хозяйства',
    '141013000000': 'Для размещения объектов рыбного хозяйства',
    '141014000000': 'Для иных видов сельскохозяйственного использования',
    '142000000000': 'Для размещения объектов, характерных для населенных пунктов',
    '142001000000': 'Для объектов жилой застройки',
    '142001010000': 'Для индивидуальной жилой застройки',
    '142001020000': 'Для многоквартирной застройки',
    '142001020100': 'Для малоэтажной застройки',
    '142001020200': 'Для среднеэтажной застройки',
    '142001020300': 'Для многоэтажной застройки',
    '142001020400': 'Для иных видов жилой застройки',
    '142001030000': 'Для размещения объектов дошкольного, начального, общего и среднего (полного) общего образования',
    '142001040000': 'Для размещения иных объектов, допустимых в жилых зонах и не перечисленных в классификаторе',
    '142002000000': 'Для объектов общественно-делового значения',
    '142002010000': 'Для размещения объектов социального и коммунально-бытового назначения',
    '142002020000': 'Для размещения объектов здравоохранения',
    '142002030000': 'Для размещения объектов культуры',
    '142002040000': 'Для размещения объектов торговли',
    '142002040100': 'Для размещения объектов розничной торговли',
    '142002040200': 'Для размещения объектов оптовой торговли',
    '142002050000': 'Для размещения объектов общественного питания',
    '142002060000': 'Для размещения объектов предпринимательской деятельности',
    '142002070000': 'Для размещения объектов среднего профессионального и высшего профессионального образования',
    '142002080000': 'Для размещения административных зданий',
    '142002090000': 'Для размещения научно-исследовательских учреждений',
    '142002100000': 'Для размещения культовых зданий',
    '142002110000': 'Для стоянок автомобильного транспорта',
    '142002120000': 'Для размещения объектов делового назначения, в том числе офисных центров',
    '142002130000': 'Для размещения объектов финансового назначения',
    '142002140000': 'Для размещения гостиниц',
    '142002150000': 'Для размещения подземных или многоэтажных гаражей',
    '142002160000': 'Для размещения индивидуальных гаражей',
    '142002170000': 'Для размещения иных объектов общественно-делового значения, обеспечивающих жизнь граждан',
    '142003000000': 'Для общего пользования (уличная сеть)',
    '142004000000': 'Для размещения объектов специального назначения',
    '142004010000': 'Для размещения кладбищ',
    '142004020000': 'Для размещения крематориев',
    '142004030000': 'Для размещения скотомогильников',
    '142004040000': 'Под объектами размещения отходов потребления',
    '142004050000': 'Под иными объектами специального назначения',
    '142005000000': 'Для размещения коммунальных, складских объектов',
    '142006000000': 'Для размещения объектов жилищно-коммунального хозяйства',
    '142007000000': 'Для иных видов использования, характерных для населенных пунктов',
    '143000000000': 'Для размещения объектов промышленности, энергетики, транспорта, связи, радиовещания, '
                    'телевидения, информатики, обеспечения космической деятельности, обороны, безопасности и иного '
                    'специального назначения',
    '143001000000': 'Для размещения промышленных объектов',
    '143001010000': 'Для размещения производственных и административных зданий, строений, сооружений и обслуживающих '
                    'их объектов',
    '143001010100': 'Для размещения производственных зданий',
    '143001010200': 'Для размещения коммуникаций',
    '143001010300': 'Для размещения подъездных путей',
    '143001010400': 'Для размещения складских помещений',
    '143001010500': 'Для размещения административных зданий',
    '143001010600': 'Для размещения культурно-бытовых зданий',
    '143001010700': 'Для размещения иных сооружений промышленности',
    '143001020000': 'Для добычи и разработки полезных ископаемых',
    '143001030000': 'Для размещения иных объектов промышленности',
    '143002000000': 'Для размещения объектов энергетики',
    '143002010000': 'Для размещения электростанций и обслуживающих сооружений и объектов',
    '143002010100': 'Для размещения гидроэлектростанций',
    '143002010200': 'Для размещения атомных станций',
    '143002010300': 'Для размещения ядерных установок',
    '143002010400': 'Для размещения пунктов хранения ядерных материалов и радиоактивных веществ энергетики',
    '143002010500': 'Для размещения хранилищ радиоактивных отходов',
    '143002010600': 'Для размещения тепловых станций',
    '143002010700': 'Для размещения иных типов электростанций',
    '143002010800': 'Для размещения иных обслуживающих сооружений и объектов',
    '143002020000': 'Для размещения объектов электросетевого хозяйства',
    '143002020100': 'Для размещения воздушных линий электропередачи',
    '143002020200': 'Для размещения наземных сооружений кабельных линий электропередачи',
    '143002020300': 'Для размещения подстанций',
    '143002020400': 'Для размещения распределительных пунктов',
    '143002020500': 'Для размещения других сооружений и объектов электросетевого хозяйства',
    '143002030000': 'Для размещения иных объектов энергетики',
    '143003000000': 'Для размещения объектов транспорта',
    '143003010000': 'Для размещения и эксплуатации объектов железнодорожного транспорта',
    '143003010100': 'Для размещения железнодорожных путей и их конструктивных элементов',
    '143003010200': 'Для размещения полос отвода железнодорожных путей',
    '143003010300': 'Для размещения, эксплуатации, расширения и реконструкции строений, зданий, сооружений, '
                    'в том числе железнодорожных вокзалов, железнодорожных станций, а также устройств и других '
                    'объектов, необходимых для эксплуатации, содержания, строительства, реконструкции, ремонта, '
                    'развития наземных и подземных зданий, строений, сооружений, устройств и других объектов '
                    'железнодорожного транспорта',
    '143003010301': 'Для размещения железнодорожных вокзалов',
    '143003010302': 'Для размещения железнодорожных станций',
    '143003010303': 'Для размещения устройств и других объектов, необходимых для эксплуатации, содержания, '
                    'строительства, реконструкции, ремонта, развития наземных и подземных зданий, строений, '
                    'сооружений, устройств и других объектов железнодорожного транспорта',
    '143003020000': 'Для размещения и эксплуатации объектов автомобильного транспорта и объектов дорожного хозяйства',
    '143003020100': 'Для размещения автомобильных дорог и их конструктивных элементов',
    '143003020200': 'Для размещения полос отвода',
    '143003020300': 'Для размещения объектов дорожного сервиса в полосах отвода автомобильных дорог',
    '143003020400': 'Для размещения дорожных сооружений',
    '143003020500': 'Для размещения автовокзалов и автостанций',
    '143003020600': 'Для размещения иных объектов автомобильного транспорта и дорожного хозяйства',
    '143003030000': 'Для размещения и эксплуатации объектов морского, внутреннего водного транспорта',
    '143003030100': 'Для размещения искусственно созданных внутренних водных путей',
    '143003030200': 'Для размещения морских и речных портов, причалов, пристаней',
    '143003030300': 'Для размещения иных объектов морского, внутреннего водного транспорта',
    '143003030400': 'Для выделения береговой полосы',
    '143003040000': 'Для размещения и эксплуатации объектов воздушного транспорта',
    '143003040100': 'Для размещения аэропортов и аэродромов',
    '143003040200': 'Для размещения аэровокзалов',
    '143003040300': 'Для размещения взлетно-посадочных полос',
    '143003040400': 'Для размещения иных наземных объектов воздушного транспорта',
    '143003050000': 'Для размещения и эксплуатации объектов трубопроводного транспорта',
    '143003050100': 'Для размещения нефтепроводов',
    '143003050200': 'Для размещения газопроводов',
    '143003050300': 'Для размещения иных трубопроводов',
    '143003050400': 'Для размещения иных объектов трубопроводного транспорта',
    '143003060000': 'Для размещения и эксплуатации иных объектов транспорта',
    '143004000000': 'Для размещения объектов связи, радиовещания, телевидения, информатики',
    '143004010000': 'Для размещения эксплуатационных предприятий связи и обслуживания линий связи',
    '143004020000': 'Для размещения кабельных, радиорелейных и воздушных линий связи и линий радиофикации на трассах '
                    'кабельных и воздушных линий связи и радиофикации и их охранные зоны',
    '143004030000': 'Для размещения подземных кабельных и воздушных линий связи и радиофикации и их охранные зоны',
    '143004040000': 'Для размещения наземных и подземных необслуживаемых усилительных пунктов на кабельных линиях '
                    'связи и их охранные зоны',
    '143004050000': 'Для размещения наземных сооружений и инфраструктур спутниковой связи',
    '143004060000': 'Для размещения иных объектов связи, радиовещания, телевидения, информатики',
    '143005000000': 'Для размещения объектов, предназначенных для обеспечения космической деятельности',
    '143005010000': 'Для размещения космодромов, стартовых комплексов и пусковых установок',
    '143005020000': 'Для размещения командно-измерительных комплексов, центров и пунктов управления полетами '
                    'космических объектов, приема, хранения и переработки информации',
    '143005030000': 'Для размещения баз хранения космической техники',
    '143005040000': 'Для размещения полигонов приземления космических объектов и взлетно-посадочных полос',
    '143005050000': 'Для размещения объектов экспериментальной базы для отработки космической техники',
    '143005060000': 'Для размещения центров и оборудования для подготовки космонавтов',
    '143005070000': 'Для размещения других наземных сооружений и техники, используемых при осуществлении космической '
                    'деятельности',
    '143006000000': 'Для размещения объектов, предназначенных для обеспечения обороны и безопасности',
    '143006010000': 'Для обеспечения задач обороны',
    '143006010100': 'Для размещения военных организаций, учреждений и других объектов',
    '143006010200': 'Для дислокации войск и сил флота',
    '143006010300': 'Для проведения учений и иных мероприятий',
    '143006010400': 'Для испытательных полигонов',
    '143006010500': 'Для мест уничтожения оружия и захоронения отходов',
    '143006010600': 'Для создания запасов материальных ценностей в государственном и мобилизационном резервах ('
                    'хранилища, склады и другие)',
    '143006010700': 'Для размещения иных объектов обороны',
    '143006020000': 'Для размещения объектов (территорий), обеспечивающих защиту и охрану Государственной границы '
                    'Российской Федерации',
    '143006020100': 'Для обустройства и содержания инженерно-технических сооружений и заграждений',
    '143006020200': 'Для обустройства и содержания пограничных знаков',
    '143006020300': 'Для обустройства и содержания пограничных просек',
    '143006020400': 'Для обустройства и содержания коммуникаций',
    '143006020500': 'Для обустройства и содержания пунктов пропуска через Государственную границу Российской Федерации',
    '143006020600': 'Для размещения иных объектов для защиты и охраны Государственной границы Российской Федерации',
    '143006030000': 'Для размещения иных объектов обороны и безопасности',
    '143007000000': 'Для размещения иных объектов промышленности, энергетики, транспорта, связи, радиовещания, '
                    'телевидения, информатики, обеспечения космической деятельности, обороны, безопасности и иного '
                    'специального назначения',
    '144000000000': 'Для размещения особо охраняемых историко-культурных и природных объектов (территорий)',
    '144001000000': 'Для размещения особо охраняемых природных объектов (территорий)',
    '144001010000': 'Для размещения государственных природных заповедников (в том числе биосферных)',
    '144001020000': 'Для размещения государственных природных заказников',
    '144001030000': 'Для размещения национальных парков',
    '144001040000': 'Для размещения природных парков',
    '144001050000': 'Для размещения дендрологических парков',
    '144001060000': 'Для размещения ботанических садов',
    '144001070000': 'Для размещения объектов санаторного и курортного назначения',
    '144001080000': 'Территории месторождений минеральных вод, лечебных грязей, рапы лиманов и озер',
    '144001090000': 'Для традиционного природопользования',
    '144001100000': 'Для размещения иных особо охраняемых природных территорий (объектов)',
    '144002000000': 'Для размещения объектов (территорий) природоохранного назначения',
    '144003000000': 'Для размещения объектов (территорий) рекреационного назначения',
    '144003010000': 'Для размещения домов отдыха, пансионатов, кемпингов',
    '144003020000': 'Для размещения объектов физической культуры и спорта',
    '144003030000': 'Для размещения туристических баз, стационарных и палаточных туристско-оздоровительных лагерей, '
                    'домов рыболова и охотника, детских туристических станций',
    '144003040000': 'Для размещения туристических парков',
    '144003050000': 'Для размещения лесопарков',
    '144003060000': 'Для размещения учебно-туристических троп и трасс',
    '144003070000': 'Для размещения детских и спортивных лагерей',
    '144003080000': 'Для размещения скверов, парков, городских садов',
    '144003090000': 'Для размещения пляжей',
    '144003100000': 'Для размещения иных объектов (территорий) рекреационного назначения',
    '144004000000': 'Для размещения объектов историко-культурного назначения',
    '144004010000': 'Для размещения объектов культурного наследия народов Российской Федерации (памятников истории и '
                    'культуры), в том числе объектов археологического наследия',
    '144004020000': 'Для размещения военных и гражданских захоронений',
    '144005000000': 'Для размещения иных особо охраняемых историко-культурных и природных объектов (территорий)',
    '145000000000': 'Для размещения объектов лесного фонда',
    '145001000000': 'Для размещения лесной растительности',
    '145002000000': 'Для восстановления лесной растительности',
    '145003000000': 'Для прочих объектов лесного хозяйства',
    '146000000000': 'Для размещения объектов водного фонда',
    '146001000000': 'Под водными объектами',
    '146002000000': 'Для размещения гидротехнических сооружений',
    '146003000000': 'Для размещения иных сооружений, расположенных на водных объектах',
    '147000000000': 'Земли запаса (неиспользуемые)'}

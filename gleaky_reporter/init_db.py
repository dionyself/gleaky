#!/usr/bin/env python
import os
from traceback import print_exc
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gleaky_reporter.settings")
django.setup()

from django.conf import settings
from tenant_users.tenants.utils import create_public_tenant
from tenant_users.tenants.tasks import provision_tenant
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from customers.models import CountryGrouping, Country


UserModel = get_user_model()
main_host = settings.TENANT_USERS_DOMAIN
main_email = settings.SYSTEM_EMAIL

test_tenant_group_name = settings.TEST_TENANT_GROUP_NAME
test_tenant_name = settings.TEST_TENANT_NAME
test_tenant_host = settings.TEST_TENANT_HOST
test_tenant_email = settings.ADMIN_EMAIL
test_tenant_password = settings.ADMIN_PASSWORD

# Create public tenant and user.
create_public_tenant(main_host, main_email)

# creating permissions
for model in apps.get_models():
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.create(
        codename='can_read',
        name='Can read %s' % model._meta.verbose_name,
        content_type=content_type)

# creating permissions_group
customer_group = Group.objects.create(name="customer")
editor_group = Group.objects.create(name="editor")
crawler_group = Group.objects.create(name="crawler")
purchasingmanager_group = Group.objects.create(name="commonperson")
storeadmin_group = Group.objects.create(name="countryadmin")

user = UserModel.objects.create_user(
    email=test_tenant_email, password=test_tenant_password, is_staff=True)

print("Created a user [{}]".format(test_tenant_email))



print("Creating default COUNTRY GROUPS...")

groups = [
    {"name": "Asia-Pacific", "abreb": "APAC" , "description": "Asia-Pacific"},
    {"name": "America", "abreb": "America" , "description": "The United States of America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "Central America", "abreb": "America" , "description": "Central America"},
    {"name": "Latin America and the Caribbean", "abreb": "America" , "description": "Latin America and the Caribbean"},
    {"name": "The Caribbean", "abreb": "America" , "description": "The Caribbean"},
    {"name": "Latin America", "abreb": "America" , "description": "Latin America"},
    {"name": "South America", "abreb": "America" , "description": "South America"},
    {"name": "Americas", "abreb": "America" , "description": "Continental America"},
    {"name": "Australia and New Zealand", "abreb": "ANZ" , "description": "Australia and New Zealand"},
    {"name": "Australia-New Zealand-Italy", "abreb": "ANZIT" , "description": "Australia-New Zealand-Italy Trilateral relations"},
    {"name": "Australia, New Zealand and the United Kingdom", "abreb": "ANZUK" , "description": "Trilateral relations between Australia, New Zealand and the United Kingdom"},
    {"name": "Asia Pacific and Japan", "abreb": "APJ" , "description": "Asia Pacific and Japan"},
    {"name": "Asia Pacific and Singapore", "abreb": "APSG" , "description": "Asia Pacific and Singapore"},
    {"name": "African Union", "abreb": "AU" , "description": "Continental union consisting of all fifty-five countries on the African continent."},
    {"name": "Asia-Pacific Economic Cooperation", "abreb": "APEC" , "description": "forum for 21 Pacific Rim member economies that promotes free trade throughout the Asia-Pacific region"},
    {"name": "Four Asian Tigers", "abreb": "Four Asian Tigers" , "description": "the economies of Hong Kong, Singapore, South Korea and Taiwan, which underwent rapid industrialization and maintained exceptionally high growth rate between the early 1960s"},
    {"name": "Arab League", "abreb": "Arab League" , "description": "regional organization of Arab countries in and around North Africa, the Horn of Africa and Arabia, Algeria, Bahrain, Comoros, Djibouti, Egypt, Iraq, Jordan, Kuwait, Lebanon, Libya, Mauritania, Morocco, Oman, Palestine, Qatar, Saudi Arabia, Somalia, Sudan, Syria, Tunisia, United Arab Emirates, Yemen, to draw closer the relations between member States and co-ordinate collaboration between them, to safeguard their independence and sovereignty, and to consider in a general way the affairs and interests of the Arab countries"},
    {"name": "The Association of Southeast Asian Nations", "abreb": "ASEAN" , "description": "regional organisation comprising ten Southeast Asian states"},
    {"name": "ASEAN+3", "abreb": "ASEAN+3" , "description": "The ASEAN countries, plus China, Japan, and the Republic of Korea"},
    {"name": "Association of Caribbean States", "abreb": "ACS" , "description": "union of nations centered on the Caribbean Basin"},
    {"name": "Baltics", "abreb": "Baltics" , "description": "three sovereign states in Northern Europe on the eastern coast of the Baltic Sea: Estonia, Latvia, and Lithuania"},
    {"name": "BASIC countries", "abreb": "BASIC" , "description": "four large newly industrialized countries, Brazil, South Africa, India, China, to act jointly on climate change and emissions reduction"},
    {"name": "Benelux", "abreb": "Benelux" , "description": "politico-economic union of three neighbouring states in western Europe: Belgium, the Netherlands, and Luxembourg."},
    {"name": "Big Four (Western Europe)", "abreb": "Big Four" , "description": "France, Germany, Italy and the United Kingdom  when these countries added to Spain, are turned the BIG 5."},
    {"name": "BIMSTEC", "abreb": "BIMSTEC" , "description": "A group of countries in South Asia and South East Asia around the Bay of Bengal to promote technological and economic co-operation, which includes Bangladesh, Bhutan, India, Myanmar, Nepal, Sri Lanka, and Thailand."},
    {"name": "BRIC", "abreb": "BRIC" , "description": "Brazil, Russia, India, and China, which are all deemed to be at a similar stage of newly advanced economic development"},
    {"name": "BRICS", "abreb": "BRICS" , "description": "Brazil, Russia, India, China and South Africa"},
    {"name": "The Organization of the Black Sea Economic Cooperation", "abreb": "BSEC" , "description": "The Organization of the Black Sea Economic Cooperation is a regional organization focusing on multilateral political and economic initiatives aimed at fostering cooperation in the Black Sea region."},
    {"name": "Central America and Latin America", "abreb": "CALA" , "description": "Central America and Latin America, or the Caribbean and Latin America"},
    {"name": "CAME", "abreb": "CAME" , "description": "Central Asia and the Middle East"},
    {"name": "CANZUK", "abreb": "CANZUK" , "description": "international organisation composed of Canada, Australia, New Zealand, and the United Kingdom"},
    {"name": "Caribbean Community", "abreb": "CARICOM" , "description": "Organization of fifteen Caribbean nations and dependencies"},
    {"name": "Central European Free Trade Agreement", "abreb": "CEFTA" , "description": "Free Trade Agreement, current members: Montenegro, Serbia, Albania, Bosnia-Herzegovina, Moldova, North Macedonia and UNMIK for the territory of Kosovo"},
    {"name": "Caribbean Free Trade Association", "abreb": "CARIFTA" , "description": "Caribbean Free Trade Association"},
    {"name": "CIVETS", "abreb": "CIVETS" , "description": "six emerging markets countries, Colombia, Indonesia, Vietnam, Egypt, Turkey, and South Africa, a diverse and dynamic economy and a young, growing population"},
    {"name": "Cambodia, Laos, Myanmar and Vietnam", "abreb": "CLMV" , "description": "south east Asia, members of ASEAN"},
    {"name": "Council of Mutual Economic Assistance", "abreb": "Comecon" , "description": "socialist economies within the Communist world: the Soviet Union, Bulgaria, Cuba, Czechoslovakia, East Germany, Hungary, Mongolia, Poland, Romania, and Vietnam. The organization existed from 1949 to 1991 during the Cold War."},
    {"name": "Community for Democracy and Rights of Nations", "abreb": "Community for Democracy and Rights of Nations" , "description": "Members include Abkhazia, South Ossetia, Transnistria and the Republic of Artsakh."},
    {"name": "Commonwealth of Independent States", "abreb": "CIS" , "description": "political alliance between the former Soviet Republics of Russia, Armenia, Azerbaijan, Belarus, Moldova, Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan, Uzbekistan."},
    {"name": "Commonwealth of Nations", "abreb": "Commonwealth of Nations" , "description": "fifty-three member states that are mostly former territories of the British Empire."},
    {"name": "Community of Portuguese Language Countries", "abreb": "Community of Portuguese Language Countries" , "description": "Community of Portuguese Language Countries"},
    {"name": "Collective Security Treaty Organization", "abreb": "Collective Security Treaty Organization" , "description": "military alliance between Russia, Armenia, Belarus, Kazakhstan, Kyrgyzstan, Tajikistan and observer members Serbia and Afghanistan."},
    {"name": "Council of Europe", "abreb": "Council of Europe" , "description": "political alliance of 47 European countries"},
    {"name": "Central and Eastern Europe", "abreb": "CEE" , "description": "Central and Eastern Europe"},
    {"name": "Canada and the United States", "abreb": "CUSA" , "description": "Canada and the United States"},
    {"name": "Development Assistance Committee", "abreb": "DAC" , "description": "discuss issues surrounding aid, development and poverty reduction in developing countries"},
    {"name": "Majority German-speaking states of Central Europe", "abreb": "DACH" , "description": "Germany (Deutschland), Austria (Austria) and Switzerland (Confoederatio Helvetica)"},
    {"name": "Deutschland, Österreich, and Schweiz", "abreb": "DOS" , "description": "uncommon, DACH is more widely used"},
    {"name": "East African Community", "abreb": "EAC" , "description": "intergovernmental organisation composed of six countries in the African Great Lakes region"},
    {"name": "Eastern Partnership", "abreb": "Eastern Partnership" , "description": "group of former soviet republics forging closer economic and political ties with the European Union."},
    {"name": "Economic Cooperation Organization", "abreb": "ECO" , "description": " Afghanistan, Azerbaijan, Iran, Kazakhstan, Kyrgyz, Pakistan, Tajikistan, Turkey, Turkmenistan, Uzbekistan, a political and economic organization, a platform to discuss ways to improve development and promote trade and investment opportunities"},
    {"name": "The European Economic Area", "abreb": "EEA" , "description": "contains the European Union counties, plus Norway, Iceland and Liechtenstein"},
    {"name": "Eurasian Economic Union", "abreb": "EAEU" , "description": "economic union of Belarus, Kazakhstan, Russia, Armenia, Kyrgyzstan and observer member Moldova."},
    {"name": "The European Union", "abreb": "EU" , "description": "The European Union, a political and economic union of 27 member states that are located primarily in Europe."},
    {"name": "The European Union + the European Economic Area + Switzerland", "abreb": "EU+EEA+CH" , "description": "The European Union + the European Economic Area + Switzerland"},
    {"name": "European Free Trade Association", "abreb": "EFTA" , "description": "European Free Trade Association"},
    {"name": "Europe, the Middle East and Africa", "abreb": "EMEA" , "description": "Europe, the Middle East and Africa"},
    {"name": "Europe, the Middle East, Africa and India", "abreb": "EMEA" , "description": "Europe, the Middle East, Africa and India"},
    {"name": "Europe and Northwest Asia", "abreb": "ENWA" , "description": "Europe and Northwest Asia"},
    {"name": "Five Gleakys", "abreb": "FVEY" , "description": "anglophone intelligence alliance comprising Australia, Canada, New Zealand, the United Kingdom and the United States"},
    {"name": "Four Asian Tigers", "abreb": "Four Asian Tigers" , "description": "economies of Hong Kong, Singapore, South Korea, Taiwan, underwent rapid industrialization and maintained exceptionally high growth rates, now developed into advanced and high-income economies."},
    {"name": "France-Latin America", "abreb": "FLAME" , "description": "France-Latin America relationship"},
    {"name": "Francamérique", "abreb": "Francamérique" , "description": "French Overseas region and collectivities in the Americas"},
    {"name": "France and Spain", "abreb": "FRES" , "description": "France and Spain"},
    {"name": "France and Italy", "abreb": "FRIT" , "description": "France and Italy"},
    {"name": "France, Italy and Spain", "abreb": "FRITES" , "description": "France, Italy and Spain"},
    {"name": "nations, Brazil, Germany, India, and Japan", "abreb": "G4" , "description": "four countries which support each other’s bids for permanent seats on the United Nations Security Council."},
    {"name": "Global Governance Group", "abreb": "G3" , "description": "a group of 30 small to medium member countries which collectively provides representation and input to the G20."},
    {"name": "Group of Two", "abreb": "G2" , "description": "United States and China (informal) focusing on Sino-American relations. Per being considered two of the most influential and powerful countries in the world"},
    {"name": "EU's G6", "abreb": "EUG6" , "description": "France, Germany, Italy, Poland, Spain, and the United Kingdom—with the largest populations and thus with the majority of votes in the Council of the European Union"},
    {"name": "Group of Seven", "abreb": "G7" , "description": "Canada, France, Germany, Italy, Japan, the United Kingdom, the United States, the seven major advanced economies as reported by the International Monetary Fund."},
    {"name": "G8+5", "abreb": "G8+5" , "description": "the G8 nations, plus the five leading emerging economies (Brazil, China, India, Mexico, and South Africa)"},
    {"name": "G20", "abreb": "G20" , "description": "Group of Twenty, twenty major economies, Argentina, Australia, Brazil, Canada, China, European Union, France, Germany, India, Indonesia, Italy, Japan, South Korea, Mexico, Russia, Saudi Arabia, South Africa, Turkey, United Kingdom, United States, for studying, reviewing, and promoting high-level discussion of policy issues pertaining to the promotion of international financial stability."},
    {"name": "Group of 77", "abreb": "G77" , "description": "a loose coalition of developing nations, designed to promote its members' collective economic interests and create an enhanced joint negotiating capacity in the United Nations."},
    {"name": "Georgia, Ukraine, Azerbaijan, and Moldova", "abreb": "GUAM" , "description": "Organization for Democracy and Economic Development"},
    {"name": "Gulf Cooperation Council", "abreb": "Gulf Cooperation Council" , "description": "Bahrain, Kuwait, Oman, Qatar, Saudi Arabia, and the UAE. A regional intergovernmental political and economic union consisting of all Arab states of the Persian Gulf, except for Iraq."},
    {"name": "Greater China", "abreb": "Greater China" , "description": "Mainland China, Hong Kong, Macau, and Taiwan"},
    {"name": "DACH", "abreb": "GAS" , "description": "Germany, Austria, and Switzerland"},
    {"name": "IBSA", "abreb": "IBSA" , "description": "Dialogue Forum, India, Brazil, South Africa, an international tripartite grouping for promoting international cooperation among these countries."},
    {"name": "IMEA", "abreb": "IMEA" , "description": "India, Middle East and Africa"},
    {"name": "Inner Six", "abreb": "Inner Six" , "description": "founding member states of the European Communities."},
    {"name": "International Solar Alliance", "abreb": "ISA" , "description": "alliance of more than 122 countries initiated by India, most of them being sunshine countries, which lie either completely or partly between the Tropic of Cancer and the Tropic of Capricorn."},
    {"name": "Interparliamentary Assembly on Orthodoxy", "abreb": "Interparliamentary Assembly on Orthodoxy" , "description": "Assembly on Orthodoxy, Inter-parliamentary institution of 21 national parliaments representing Orthodox Christians"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    {"name": "North America", "abreb": "America" , "description": "North America"},
    
]
"""
La Francophonie: an international organization representing countries and regions where French is a lingua franca or customary language
LATAM: Latin America
LATCAR: Latin America and Caribbean[5]
Levant: Cyprus, Israel, Jordan, Lebanon, Palestine, Syria (broadly includes: Egypt, Iraq, Turkey, Greece)
M
Mercosur (Southern Common Market), Argentina, Brazil, Paraguay, Uruguay, to promote free trade and the fluid movement of goods, people, and currency.
MIKTA, an informal partnership between Mexico, Indonesia, Republic of Korea, Turkey, Australia, to support effective global governance.
MINT, the economies of Mexico, Indonesia, Nigeria, and Turkey.
MART: Middle East, Africa, Russia and Turkey
MEA: Middle East and Africa
MEATI: Middle East, Africa, Turkey & India[6]
MEESA: Middle East, Eastern and Southern Africa
MENA: Middle East and North Africa
MEP: Middle East and Pakistan[7]
META: Middle East, Turkey and Africa
N
NAC: North America and the Caribbean
NATO: North Atlantic treaty organisation; NATO is formal group country to defend itself from the Soviet Union.
NAFTA: North American Free Trade Agreement, is an agreement signed by Canada, Mexico, and the United States, creating a trilateral trade bloc in North America.
Next Eleven (N11), Bangladesh, Egypt, Indonesia, Iran, Mexico, Nigeria, Pakistan, the Philippines, Turkey, South Korea, and Vietnam – identified as having a high potential of becoming, along with the BRICS countries, among the world's largest economies in the 21st century.
NACE: North Atlantic and Central Europe
NALA: North America and Latin America
NORAM or NA or NAMER: North American Region (Canada, United States, and Mexico)
Nordics: in addition to the Scandinavian countries Denmark, Norway and Sweden, also Finland and Iceland are included.
NWA: Northwest Asia
O
OIC, The Organisation of Islamic Cooperation is an international organization founded in 1969, consisting of 57 member states, with a collective population of over 1.8 billion as of 2015 with 54 countries being Muslim-majority countries.
OAS, Organization of American States, is a continental organization of the 35 independent nations within North and South America
OECD, Organisation for Economic Co-operation and Development, to stimulate economic progress and world trade, countries committed to democracy and the market economy, most OECD members are high-income economies with a very high Human Development Index (HDI) and are regarded as developed countries.
OECS, a group of island nations located in the Eastern Caribbean.
OIAS, Organization of Ibero-American States, an organization of Portuguese and Spanish Speaking Nations of the Americas, Africa, and Europe.
OPEC, Organization of the Petroleum Exporting Countries, thirteen countries accounting for an estimated 42 percent of global oil production and 73 percent of the world's proven oil reserves.
P
P5, permanent members of the United Nations Security Council, China, France, Russia, the United Kingdom, and the United States.
Pacific Alliance, a trade bloc of states that border the Pacific Ocean. Permanent members include Chile, Colombia, Mexico, and Peru.
The Pacific Pumas , a political and economic grouping of countries along Latin America’s Pacific coast that includes Chile, Colombia, Mexico and Peru. The term references the four larger Pacific Latin American emerging markets that share common trends of positive growth, stable macroeconomic foundations, improved governance and an openness to global integration.
Paris Club, a group of major creditor countries whose officials meet ten times a year in the city of Paris, with the intent to find coordinated and sustainable solutions to the payment difficulties experienced by debtor countries.
PIGS, also PIIGS, the economies of the countries of Portugal, Greece, Spain, Italy and/or Ireland.
R
Rio Group, was an international organization of Latin American and some Caribbean states that was succeeded in 2010 by the Community of Latin American and Caribbean States.
ROME: Rest of Middle East
S
SAARC, a geopolitical union of nations in South Asia
SCA: South and Central America
Scandinavia: Denmark, Norway and Sweden (in some definitions, Finland is included due to strong historical ties to Sweden)
Shanghai Cooperation Organisation (SCO), A Eurasian political, economic, and security organisation comprising China, Kazakhstan, Kyrgyzstan, Russia, Tajikistan, Uzbekistan, India and Pakistan.
SaarLorLux: Saarland, Lorraine, Luxembourg
SEA: South-East Asia
Southern Cone (Cono Sur): Argentina, Chile, Paraguay, Uruguay and Southern Brazil.
South Asia: Afghanistan, Bangladesh, Bhutan, Maldives, Nepal, India, Pakistan and Sri Lanka
T
Turkic Council: an international organization comprising some of the Turkic countries (Turkey, Azerbaijan, Kazakhstan, Uzbekistan, Kyrgyzstan and Hungary).
U
United Kingdom (UK), a country in Western Europe consisting of England, Scotland, Wales, and Northern Ireland.
United Nations (UN), an intergovernmental organization to promote international co-operation, 193 member states.
Union State of Eurasia (USE), a Sovereign state made up of Russia and Belarus.
V
V4, Visegrád Group, an alliance of four Central European States: the Czech Republic, Hungary, Poland, and Slovakia.
VISTA (Vietnam, Indonesia, South Africa, Turkey, and Argentina) is an emerging markets grouping proposed in 2006 by BRICs Economic Research Institute of Japan.
"""



China	9,388,211
India	2,973,190
United States	9,147,420
Indonesia	1,811,570
Pakistan	770,880
Brazil	8,358,140
Nigeria	910,770
Bangladesh	130,170
Russia	16,376,870
Mexico	1,943,950
Japan	364,555
Ethiopia	1,000,000
Philippines	298,170
Egypt	995,450
Vietnam		310,070
DR Congo	2,267,050
Turkey	769,630
Iran	1,628,550
Germany	348,560
Thailand	510,890
United Kingdom	241,930
France	547,557
Italy	294,140
Tanzania	885,800
South Africa	1,213,090
Myanmar	653,290
Kenya	569,140
South Korea	97,230
Colombia	1,109,500
Spain	498,800
Uganda	199,810
Argentina	2,736,690
Algeria	2,381,740
Sudan	1,765,048
Ukraine	579,320
Iraq	434,320
Afghanistan	652,860
Poland	306,230
Canada	9,093,510
Morocco	446,300
Saudi Arabia	2,149,690
Uzbekistan	425,400
Peru	1,280,000
Angola	1,246,700
Malaysia	328,550
Mozambique	786,380
Ghana	227,540
Yemen	527,970
Nepal	143,350
Venezuela	882,050
Madagascar	581,795
Cameroon	472,710
Côte d'Ivoire	318,000
North Korea	120,410
Australia	7,682,300
Niger	1,266,700
Sri Lanka	62,710
Burkina Faso	273,600
Mali	1,220,190
Romania	230,170
Malawi	94,280
Chile	743,532
Kazakhstan	2,699,700
Zambia	743,390
Guatemala	107,160
Ecuador	248,360
Syria	183,630
Netherlands	33,720
Senegal	192,530
Cambodia	176,520
Chad	1,259,200
Somalia	627,340
Zimbabwe	386,850
Guinea	245,720
Rwanda	24,670
Benin	112,760
Burundi	25,680
Tunisia	155,360
Bolivia	1,083,300
Belgium	30,280
Haiti	27,560
Cuba	106,440
South Sudan	610,952
Dominican Republic	48,320
Czech Republic (Czechia)	77,240
Greece	128,900
Jordan	88,780
Portugal	91,590
Azerbaijan	82,658
Sweden	410,340
Honduras	111,890
United Arab Emirates	83,600
Hungary	90,530
Tajikistan	139,960
Belarus	202,910
Austria	82,409
Papua New Guinea	452,860
Serbia	87,460
Israel	21,640
Switzerland	39,516
Togo	54,390
Sierra Leone	72,180
Laos	230,800
Paraguay	397,300
Bulgaria	108,560
Libya	1,759,540
Lebanon		10,230
Nicaragua	6,624,554	0.1 %	120,340
Kyrgyzstan	6,524,195	0.1 %	191,800
El Salvador	6,486,205	0.1 %	20,720
Turkmenistan	6,031,200	0.1 %	469,930
Singapore	5,850,342	0.1 %	700
Denmark	5,792,202	0.1 %	42,430
Finland	5,540,720	0.1 %	303,890
Congo	5,518,087	0.1 %	341,500
Slovakia	5,459,642	0.1 %	48,088
Norway	5,421,241	0.1 %	365,268
Oman	5,106,626	0.1 %	309,500
State of Palestine	5,101,414	0.1 %	6,020
Costa Rica	5,094,118	0.1 %	51,060
Liberia	5,057,681	0.1 %	96,320
Ireland	4,937,786	0.1 %	68,890
Central African Republic	4,829,767	0.1 %	622,980
New Zealand	4,822,233	0.1 %	263,310
Mauritania	4,649,658	0.1 %	1,030,700
Panama	4,314,767	0.1 %	74,340
Kuwait	4,270,571	0.1 %	17,820
Croatia	4,105,267	0.1 %	55,960
Moldova	4,033,963	0.1 %	32,850
Georgia	3,989,167	0.1 %	69,490
Eritrea	3,546,421	0 %	101,000
Uruguay	3,473,730	0 %	175,020
Bosnia and Herzegovina	3,280,819	0 %	51,000
Mongolia	3,278,290	0 %	1,553,560
Armenia	2,963,243	0 %	28,470
Jamaica	2,961,167	0 %	10,830
Qatar	2,881,053	0 %	11,610
Albania	2,877,797	0 %	27,400
Lithuania	2,722,289	0 %	62,674
Namibia	2,540,905	0 %	823,290
Gambia	2,416,668	0 %	10,120
Botswana	2,351,627	0 %	566,730
Gabon	2,225,734	0 %	257,670
Lesotho	2,142,249	0 %	30,360
North Macedonia	2,083,374	0 %	25,220
Slovenia	2,078,938	0 %	20,140
Guinea-Bissau	1,968,001	0 %	28,120
Latvia	1,886,198	0 %	62,200
Bahrain	1,701,575	0 %	760
Equatorial Guinea	1,402,985	0 %	28,050
Trinidad and Tobago	1,399,488	0 %	5,130
Estonia	1,326,535	0 %	42,390
Timor-Leste	1,318,445	0 %	14,870
Mauritius	1,271,768	0 %	2,030
Cyprus	1,207,359	0 %	9,240
Eswatini	1,160,164	0 %	17,200
Djibouti	988,000	0 %	23,180
Fiji	896,445	0 %	18,270
Comoros	869,601	0 %	1,861
Guyana	786,552	0 %	196,850
Bhutan	771,608	0 %	38,117
Solomon Islands	686,884	0 %	27,990
Montenegro	628,066	0 %	13,450
Luxembourg	625,978	0 %	2,590
Suriname	586,632	0 %	156,000
Cabo Verde	555,987	0 %	4,030
Maldives	540,544	0 %	300
Malta	441,543	0 %	320
Brunei	437,479	0 %	5,270
Belize	397,628	0 %	22,810
Bahamas	393,244	0 %	10,010
Iceland	341,243	0 %	100,250
Vanuatu	307,145	0 %	12,190
Barbados	287,375	0 %	430
Sao Tome & Principe	219,159	0 %	960
Samoa	198,414	0 %	2,830
Saint Lucia	183,627	0 %	610
Kiribati	119,449	0 %	810
Micronesia	115,023	0 %	700
Grenada	112,523	0 %	340
St. Vincent & Grenadines	110,940	0 %	390
Tonga	105,695	0 %	720
Seychelles	98,347	0 %	460
Antigua and Barbuda	97,929	0 %	440
Andorra	77,265	0 %	470
Dominica	71,986	0 %	750
Marshall Islands	59,190	0 %	180
Saint Kitts & Nevis	53,199	0 %	260
Monaco	39,242	0 %	1
Liechtenstein	38,128	0 %	160
San Marino	33,931	0 %	60
Palau	18,094	0 %	460
Tuvalu	11,792	0 %	30
Nauru	10,824	0 %	20
Holy See	801	0 %	0

try:
    if settings.AUTO_CREATE_TEST_TENANT:
        print("Creating a test country Using host [{}] and name [{}]... to avoid this set AUTO_CREATE_TEST_TENANT to False".format(test_tenant_host, test_tenant_name))
        # create tenant
        fqdn = provision_tenant(test_tenant_name, test_tenant_host, test_tenant_email, is_staff=True)
        print("Added Store: {}".format(test_tenant_name))
        print("Creating a normal user {} for Store: {}".format("user@{}".format(main_host), test_tenant_name))
        user = UserModel.objects.create_user(email="user@{}".format(main_host), password="password", is_staff=False)
        tenant = Store.objects.filter(domains__domain=fqdn).first()s
        tenant.add_user(user, is_superuser=False, is_staff=False)
        print("User added")

    if settings.AUTO_CREATE_TEST_TENANT_GROUP:
        print("Creating a test corporation... to avoid this set AUTO_CREATE_TEST_TENANT_GROUP to False")
        corp = Corporation.objects.create(
            name=test_tenant_group_name,
            phone="1-555-5555"
        )
        user.corporation = corp
        user.save()
        print("Added Corporation: {}".format(test_tenant_group_name))

except Exception as e:
    print_exc()
    print(e)
    print("Unable to configure test schema.")
    
for raw_group in groups:
    Group.objects.create(**raw_group)
    
for raw_country in countries:
    Country.objects.create(**raw_country)
    
group_country_mapping = [

]

# extra data for testing
#user1 = UserModel.objects.create_user(email="user1@gleaky.com", password="password", is_staff=False)
#tenant = Store.objects.filter(domain_url=fqdn).first()
#tenant.add_user(user1, is_superuser=False, is_staff=False)
#user1 = UserModel.objects.create_user(email="user1@gleaky.com", password="password", is_staff=False)
#user2 = UserModel.objects.create_user(email="user2@gleaky.com", password="password", is_staff=False)
#fqdn = provision_tenant("Test store1", "test1", "user1@gleaky.com", is_staff=False)
#fqdn = provision_tenant("Test store2", "test2", "user2@gleaky.com", is_staff=False)
#from customers.models import Store
#tenant2 = Store.objects.filter(domain_url=fqdn).first()
#tenant2.add_user(user1, is_superuser=False, is_staff=False)

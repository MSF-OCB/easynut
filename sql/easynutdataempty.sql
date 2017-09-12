-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 12, 2017 at 09:33 AM
-- Server version: 5.6.30-1+deb.sury.org~xenial+2
-- PHP Version: 7.0.22-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `easynutdataempty`
--

-- --------------------------------------------------------

--
-- Table structure for table `easy_roles`
--

CREATE TABLE `easy_roles` (
  `_id` int(11) NOT NULL,
  `group_id` tinyint(4) NOT NULL,
  `table_id` tinyint(4) NOT NULL,
  `view_table` tinyint(4) NOT NULL,
  `add_table` tinyint(4) NOT NULL,
  `edit_table` tinyint(4) NOT NULL,
  `delete_table` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `easy_roles`
--

INSERT INTO `easy_roles` (`_id`, `group_id`, `table_id`, `view_table`, `add_table`, `edit_table`, `delete_table`) VALUES
(1, 5, 1, 1, 0, 0, 0),
(2, 1, 1, 1, 1, 1, 0),
(3, 1, 3, 1, 1, 1, 0),
(4, 1, 5, 1, 1, 1, 0),
(5, 11, 1, 1, 0, 0, 0),
(6, 11, 3, 1, 1, 1, 0),
(7, 11, 5, 1, 1, 1, 0),
(8, 7, 7, 1, 1, 1, 0),
(9, 8, 10, 1, 1, 1, 0),
(10, 9, 11, 1, 1, 1, 0),
(11, 4, 1, 1, 0, 0, 0),
(12, 4, 2, 1, 1, 1, 0),
(13, 4, 3, 1, 1, 1, 0),
(14, 4, 4, 1, 1, 1, 0),
(15, 4, 5, 1, 1, 1, 0),
(16, 4, 6, 1, 1, 1, 0),
(17, 4, 7, 1, 1, 1, 0),
(18, 4, 8, 1, 1, 1, 0),
(19, 4, 9, 1, 1, 1, 0),
(20, 4, 10, 1, 1, 1, 0),
(21, 4, 11, 1, 1, 1, 0),
(22, 4, 13, 1, 1, 1, 0),
(23, 4, 15, 1, 1, 1, 0),
(24, 6, 2, 1, 0, 0, 0),
(25, 6, 14, 1, 1, 1, 0),
(26, 10, 12, 1, 1, 1, 0),
(27, 10, 13, 1, 0, 0, 0),
(28, 10, 15, 1, 0, 0, 0),
(29, 10, 16, 1, 1, 1, 0),
(30, 9, 5, 1, 1, 1, 0),
(31, 12, 1, 1, 1, 1, 0),
(32, 13, 17, 1, 1, 1, 0),
(33, 12, 2, 1, 1, 1, 0),
(34, 12, 3, 1, 1, 1, 0),
(35, 12, 4, 1, 1, 1, 0),
(36, 12, 5, 1, 1, 1, 0),
(37, 12, 6, 1, 1, 1, 0),
(38, 12, 7, 1, 1, 1, 0),
(39, 12, 8, 1, 1, 1, 0),
(40, 12, 9, 1, 1, 1, 0),
(41, 12, 10, 1, 1, 1, 0),
(42, 12, 13, 1, 1, 1, 0),
(43, 12, 14, 1, 1, 1, 0),
(44, 12, 15, 1, 1, 1, 0),
(45, 12, 16, 1, 1, 1, 0),
(46, 12, 17, 1, 1, 1, 0),
(47, 12, 11, 1, 1, 1, 0),
(48, 12, 12, 1, 1, 1, 0),
(49, 4, 18, 1, 1, 1, 0),
(50, 1, 18, 1, 1, 1, 0),
(51, 9, 18, 1, 1, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `tablas`
--

CREATE TABLE `tablas` (
  `_id` int(11) NOT NULL,
  `tabla_id` text NOT NULL,
  `presentador` text NOT NULL,
  `registros` int(11) DEFAULT NULL,
  `hal` text,
  `last` int(11) DEFAULT NULL,
  `buscar_todo` text,
  `orden` text,
  `orden_sen` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tablas`
--

INSERT INTO `tablas` (`_id`, `tabla_id`, `presentador`, `registros`, `hal`, `last`, `buscar_todo`, `orden`, `orden_sen`) VALUES
(1, '1', 'Bio data', 1, NULL, NULL, 'true', 'campo_2', 'ASC'),
(2, '2', 'Drug Prescription', 9, NULL, NULL, 'true', 'campo_1', 'DESC'),
(3, '3', 'MUAC & Temperature', 2, NULL, NULL, 'true', 'campo_1', 'DESC'),
(4, '4', 'Discharges', 14, NULL, NULL, 'true', 'campo_1', 'DESC'),
(5, '5', 'Internal movements', 13, NULL, NULL, 'true', 'campo_1', 'DESC'),
(6, '6', 'Immunizations', 6, NULL, NULL, 'true', 'campo_1', 'DESC'),
(7, '7', 'Weight & Height', 3, NULL, NULL, 'true', 'campo_1', 'DESC'),
(8, '8', 'Consultations', 7, NULL, NULL, 'true', 'campo_1', 'DESC'),
(9, '9', 'Medical History', 8, NULL, NULL, 'true', 'campo_1', 'DESC'),
(10, '10', 'Malaria test', 4, NULL, NULL, 'true', 'campo_1', 'DESC'),
(11, '11', 'Appetite test', 5, NULL, NULL, 'true', 'campo_1', 'DESC'),
(12, '12', 'PPN distribution', 16, NULL, NULL, 'true', 'campo_1', 'DESC'),
(13, '13', 'PPN Prescription', 10, NULL, NULL, 'true', 'campo_1', 'DESC'),
(14, '14', 'Dispense', 15, NULL, NULL, 'true', 'campo_1', 'DESC'),
(15, '15', 'FPR', 11, NULL, NULL, 'true', 'campo_1', 'DESC'),
(16, '16', 'Household information', 17, NULL, NULL, 'true', 'campo_1', 'DESC'),
(17, '17', 'Absence', 18, NULL, NULL, 'true', 'campo_1', 'DESC'),
(18, '18', 'Referral to ITFC ER', 12, NULL, NULL, 'true', 'campo_1', 'DESC');

-- --------------------------------------------------------

--
-- Table structure for table `tablas_relaciones`
--

CREATE TABLE `tablas_relaciones` (
  `_id` int(11) NOT NULL,
  `tabla1_id` text NOT NULL,
  `campo1_id` text NOT NULL,
  `tabla2_id` text NOT NULL,
  `campo2_id` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tablas_relaciones`
--

INSERT INTO `tablas_relaciones` (`_id`, `tabla1_id`, `campo1_id`, `tabla2_id`, `campo2_id`) VALUES
(3, '1', 'campo_1', '4', 'campo_2'),
(4, '1', 'campo_1', '5', 'campo_2'),
(5, '1', 'campo_1', '6', 'campo_2'),
(6, '1', 'campo_1', '7', 'campo_2'),
(7, '1', 'campo_1', '8', 'campo_2'),
(8, '1', 'campo_1', '9', 'campo_1'),
(9, '1', 'campo_1', '10', 'campo_2'),
(10, '1', 'campo_1', '11', 'campo_2'),
(11, '1', 'campo_1', '12', 'campo_2'),
(12, '1', 'campo_1', '13', 'campo_2'),
(13, '1', 'campo_1', '14', 'campo_2'),
(14, '1', 'campo_1', '15', 'campo_2'),
(15, '1', 'campo_1', '16', 'campo_2');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_1`
--

CREATE TABLE `tabla_1` (
  `_id` int(11) NOT NULL,
  `campo_1` varchar(128) DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` varchar(128) DEFAULT NULL,
  `campo_5` varchar(128) DEFAULT NULL,
  `campo_6` varchar(128) DEFAULT NULL,
  `campo_7` varchar(128) DEFAULT NULL,
  `campo_8` varchar(128) DEFAULT NULL,
  `campo_9` varchar(128) DEFAULT NULL,
  `campo_10` varchar(128) DEFAULT NULL,
  `campo_12` varchar(128) DEFAULT NULL,
  `campo_13` varchar(128) DEFAULT NULL,
  `campo_14` varchar(128) DEFAULT NULL,
  `campo_15` varchar(128) DEFAULT NULL,
  `campo_16` varchar(128) DEFAULT NULL,
  `campo_17` varchar(128) DEFAULT NULL,
  `campo_18` date DEFAULT NULL,
  `campo_19` varchar(128) DEFAULT NULL,
  `campo_20` varchar(128) DEFAULT NULL,
  `campo_21` date DEFAULT NULL,
  `campo_22` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_1_des`
--

CREATE TABLE `tabla_1_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_1_des`
--

INSERT INTO `tabla_1_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'MSF ID', 'texto', '', 'true', 'true', 'true', 'true', 'true', 1, 'true', 'true'),
(2, 'campo_2', 'campo_2', 'Name (Given, Father\'s, Grandfather\'s)', 'texto', '', 'true', 'true', 'true', 'true', 'true', 2, 'true', ''),
(3, 'campo_3', 'campo_3', 'Care taker 1', 'texto', '', 'true', 'true', 'true', 'true', 'true', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Care taker 2', 'texto', '', 'false', 'true', 'true', 'true', 'true', 4, 'true', ''),
(5, 'campo_5', 'campo_5', 'Age category', 'radio', '<6m,6-59m,5-10y', 'false', 'true', 'true', 'true', 'true', 5, 'true', ''),
(6, 'campo_6', 'campo_6', 'Age number', 'select', '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24', 'true', 'true', 'true', 'true', 'true', 6, 'true', ''),
(7, 'campo_7', 'campo_7', 'Age (unit)', 'radio', 'Weeks,Months,Years', 'true', 'true', 'true', 'true', 'true', 7, 'true', ''),
(8, 'campo_8', 'campo_8', 'Sex', 'radio', 'Male, Female', 'true', 'false', 'true', 'true', 'true', 8, 'true', ''),
(9, 'campo_9', 'campo_9', 'Address (ward-subward-village)', 'select', 'Abbaram,Ajiri,Alau,Auno,Ayi_Yasku,Bale_Galtimari-Bale_Galtimari_-Ali Dawari,Bale_Galtimari-Bale_Galtimari_-Femari,Bale_Galtimari-Bale_Galtimari_-Molai Kura,Bale_Galtimari-Bale_Galtimari_-Other,Bale_Galtimari-Fori-Ajari 1,Bale_Galtimari-Fori-Ajari 2,Bale_Galtimari-Fori-Balai Kura,Bale_Galtimari-Fori-Fori 1,Bale_Galtimari-Fori-Fori 2 / Galtimari 2,Bale_Galtimari-Fori-Fori 3,Bale_Galtimari-Fori-Fori 4,Bale_Galtimari-Fori-Fori 5,Bale_Galtimari-Fori-Fori 6 (212 Gombole),Bale_Galtimari-Fori-Fori Wulari,Bale_Galtimari-Fori-Giwa Barrack 1,Bale_Galtimari-Fori-Giwa Barrack 2,Bale_Galtimari-Fori-Giwa Barracks (no houses),Bale_Galtimari-Fori-Wadiya Abbari,Bale_Galtimari-Fori-Wadiya Gana,Bale_Galtimari-Fori-Wadiya Kellumari,Bale_Galtimari-Fori-Wadiya Kura,Bale_Galtimari-Fori-Other,Bale_Galtimari-Galtimari-Assembly Quarters,Bale_Galtimari-Galtimari-Bololo,Bale_Galtimari-Galtimari-Capital,Bale_Galtimari-Galtimari-Galtimari,Bale_Galtimari-Galtimari-Galtimari G.R.A.,Bale_Galtimari-Galtimari-Galtimari Ngawo Bulaye,Bale_Galtimari-Galtimari-Mami Giwa Barrack,Bale_Galtimari-Galtimari-Ushmanti,Bale_Galtimari-Galtimari-Other,Bale_Galtimari-Jiddare_Polo-122 Jiddari,Bale_Galtimari-Jiddare_Polo-Jiddari 1,Bale_Galtimari-Jiddare_Polo-Jiddari 2,Bale_Galtimari-Jiddare_Polo-Jiddari 3,Bale_Galtimari-Jiddare_Polo-Jiddari 4,Bale_Galtimari-Jiddare_Polo-Jiddari 5,Bale_Galtimari-Jiddare_Polo-Jiddari Afganistan,Bale_Galtimari-Jiddare_Polo-Other,Bale_Galtimari-Bale_Galtimari-Bale_Galtimari,Bale_Galtimari-Other,Bolori_I,Bolori_II,Bulablin,Dala_Lawanti,Dalori_Wanori-Dalori-Abba Malumti,Dalori_Wanori-Dalori-Dalori Mainari,Dalori_Wanori-Dalori-Dalori Shuwari 1,Dalori_Wanori-Dalori-Dalori Shuwari 2,Dalori_Wanori-Dalori-Dalorima Usmanti,Dalori_Wanori-Dalori-Gomari Kare Kiri,Dalori_Wanori-Dalori-Kofa,Dalori_Wanori-Dalori-Other,Dalori_Wanori-Other,Dalwa,Dusuma,Fezzan,Gajigana,Gamburu_Liberty,Gomari,Gongulong,Goniri,Gumna,Gwange_I,Gwange_II,Gwange_III-New_GRA-Line A,Gwange_III-New_GRA-Line B,Gwange_III-New_GRA-Line C,Gwange_III-New_GRA-Line D,Gwange_III-New_GRA-Line E,Gwange_III-New_GRA-Shetimari,Gwange_III-New_GRA-Other,Gwange_III-Other-Other,Hausari,Hoyo_Chingowa,Jakana,Kararam,Kawuri,Konduga,Koshebe,Lamisula,Lege,Limanti,Loskuri,Mafa,Mafoni,Magumeri,Maimusari,Mairi-Mairi_A-202 & 303 Housing Estate,Mairi-Mairi_A-Abba Aji Mosque,Mairi-Mairi_A-Dalori Veterinary,Mairi-Mairi_A-Ferobe,Mairi-Mairi_A-Gabtchari Side,Mairi-Mairi_A-Lawanti,Mairi-Mairi_A-Layin Acada,Mairi-Mairi_A-Mai Allo Mosque,Mairi-Mairi_A-Mairi Palace,Mairi-Mairi_A-Sani Carpenter,Mairi-Mairi_A-Side Pocket,Mairi-Mairi_A-University of Maiduguri,Mairi-Mairi_A-Other,Mairi-Mairi_B-Gawu Biyu (Layin Gawu),Mairi-Mairi_B-Gidan Film,Mairi-Mairi_B-Kasuwan Dare 1 (Layin Iyaka Da Mafa),Mairi-Mairi_B-Kasuwan Dare 2 (Layin TH),Mairi-Mairi_B-Kasuwan Dare 3 (Layin Karshe),Mairi-Mairi_B-Kuwait Bus Stop,Mairi-Mairi_B-Late Bulama Dudu Street & Gate 5,Mairi-Mairi_B-Layin Bukarti,Mairi-Mairi_B-Layin F.G.C.,Mairi-Mairi_B-Layin Kandahar,Mairi-Mairi_B-Layin Ultimate,Mairi-Mairi_B-Zakariya Street,Mairi-Mairi_B-Other,Mairi-Other,Maisandari-Maisandari_1-44-G,Maisandari-Maisandari_1-Arabic Quarter,Maisandari-Maisandari_1-Bulamari,Maisandari-Maisandari_1-Circular Road 1,Maisandari-Maisandari_1-Circular Road 2,Maisandari-Maisandari_1-Damboa Road Abakarti,Maisandari-Maisandari_1-Damboa Road Anguwan Indimi,Maisandari-Maisandari_1-Depot (no house),Maisandari-Maisandari_1-Durkwari A,Maisandari-Maisandari_1-Durkwari B,Maisandari-Maisandari_1-Femari 1,Maisandari-Maisandari_1-Femari 2,Maisandari-Maisandari_1-Forestry,Maisandari-Maisandari_1-Goliri 1,Maisandari-Maisandari_1-Goliri 2,Maisandari-Maisandari_1-International Hotel (No houses),Maisandari-Maisandari_1-Jiddumri,Maisandari-Maisandari_1-Kirikasama,Maisandari-Maisandari_1-Kulluluri 1,Maisandari-Maisandari_1-Kulluluri 2,Maisandari-Maisandari_1-Layin Borehole,Maisandari-Maisandari_1-Layin Modu Mustapha,Maisandari-Maisandari_1-Mafoni Liberty 1,Maisandari-Maisandari_1-Maidokiri,Maisandari-Maisandari_1-Maisandari Ngaddabul,Maisandari-Maisandari_1-Moduganari Bad (3),Maisandari-Maisandari_1-Moduganari Bayan Makabanta,Maisandari-Maisandari_1-Moduganari Bayan Police College,Maisandari-Maisandari_1-Moduganari Bayan Sheraton,Maisandari-Maisandari_1-Moduganari Bus Stop,Maisandari-Maisandari_1-Moduganari By Pass,Maisandari-Maisandari_1-Moduganari Kuwait,Maisandari-Maisandari_1-Moduganari Layin Masallaci,Maisandari-Maisandari_1-Moduganari Primary (5),Maisandari-Maisandari_1-Moduganari Shuwari 1,Maisandari-Maisandari_1-Moduganari Shuwari 2,Maisandari-Maisandari_1-Moduganari Tudu 1,Maisandari-Maisandari_1-Moduganari Tudu 2,Maisandari-Maisandari_1-Moduganari Ward 1,Maisandari-Maisandari_1-Molai Bariki,Maisandari-Maisandari_1-Police College,Maisandari-Maisandari_1-Sabon Gari,Maisandari-Maisandari_1-Shehu Garbai Maisandari,Maisandari-Maisandari_1-Shuwari 2,Maisandari-Maisandari_1-Shuwari 3,Maisandari-Maisandari_1-Shuwari 5,Maisandari-Maisandari_1-Shuwari 6,Maisandari-Maisandari_1-Shuwari 7,Maisandari-Maisandari_1-Shuwari Tashan Kano 1,Maisandari-Maisandari_1-Zannari,Maisandari-Maisandari_1-Zulari Block A,Maisandari-Maisandari_1-Zulari Block B,Maisandari-Maisandari_1-Zulari Block C,Maisandari-Maisandari_1-Other,Maisandari-Maisandari_2-Abbajitiri,Maisandari-Maisandari_2-Abuja Kulluri,Maisandari-Maisandari_2-Abuja Shankafori,Maisandari-Maisandari_2-Abuja Sheraton 1,Maisandari-Maisandari_2-Abuja Sheraton 2,Maisandari-Maisandari_2-Abuja Sheraton 3,Maisandari-Maisandari_2-Abuja Sheraton 4 (Layiin Hadiza),Maisandari-Maisandari_2-Abuja Sheraton Mai Deribe,Maisandari-Maisandari_2-Abuja Talakawa,Maisandari-Maisandari_2-Alajeri 1,Maisandari-Maisandari_2-Alajeri 2,Maisandari-Maisandari_2-Alhajiri,Maisandari-Maisandari_2-Anguwar Hamisu,Maisandari-Maisandari_2-Ashemri,Maisandari-Maisandari_2-Bojouri,Maisandari-Maisandari_2-Dairi 1,Maisandari-Maisandari_2-Dairi 3,Maisandari-Maisandari_2-Dairi 4,Maisandari-Maisandari_2-Dairi 5,Maisandari-Maisandari_2-Dairi 6,Maisandari-Maisandari_2-Dairi 7,Maisandari-Maisandari_2-Dala Dairi 2,Maisandari-Maisandari_2-Dala Furka,Maisandari-Maisandari_2-Dala Shuwari,Maisandari-Maisandari_2-Dala Wulari,Maisandari-Maisandari_2-Dala Yajiwa 1,Maisandari-Maisandari_2-Dala Yajiwa 2,Maisandari-Maisandari_2-Dala Yazara,Maisandari-Maisandari_2-Goni Kyariri,Maisandari-Maisandari_2-Irrigated Farmlands (No houses),Maisandari-Maisandari_2-Isari,Maisandari-Maisandari_2-Kangadiri,Maisandari-Maisandari_2-Kululluri Alajeri (3),Maisandari-Maisandari_2-Modu Sulumri 1,Maisandari-Maisandari_2-Mustapha Mallambe,Maisandari-Maisandari_2-Ngomdori,Maisandari-Maisandari_2-Sabon Gari 1,Maisandari-Maisandari_2-Sabon Gari 2,Maisandari-Maisandari_2-Zannari 1,Maisandari-Maisandari_2-Zannari 2,Maisandari-Maisandari_2-Other,Maisandari-Maisandari_3-CBN Quarters,Maisandari-Maisandari_3-Kushari,Maisandari-Maisandari_3-Kushiri,Maisandari-Maisandari_3-Sulemanti 1,Maisandari-Maisandari_3-Sulemanti 2,Maisandari-Maisandari_3-Sulemanti 3,Maisandari-Maisandari_3-Sulemanti 4,Maisandari-Maisandari_3-Sultakmari 1,Maisandari-Maisandari_3-Sultakmari 2,Maisandari-Maisandari_3-Sultakmari 3 (Mulai Quarter),Maisandari-Maisandari_3-Other,Maisandari-Old_GRA-Air Force Mess (no House),Maisandari-Old_GRA-Circular Road GRA,Maisandari-Old_GRA-Gombole Road GRA,Maisandari-Old_GRA-Government House GRA,Maisandari-Old_GRA-GRA Extension (Damboa Road),Maisandari-Old_GRA-Kabba Gombole,Maisandari-Old_GRA-Lagos Street GRA,Maisandari-Old_GRA-NIPOST Quarters,Maisandari-Old_GRA-Nursing Home GRA,Maisandari-Old_GRA-Old GRA 2,Maisandari-Old_GRA-Old GRA Gombole Road,Maisandari-Old_GRA-Pampam Village (Karakara),Maisandari-Old_GRA-Polo Ground Old GRA,Maisandari-Old_GRA-Sanda Kyarimi Street GRA,Maisandari-Old_GRA-Shehu Laminu Way GRA 1,Maisandari-Old_GRA-Uni Town GRA,Maisandari-Old_GRA-Other,Maisandari-Other,Malari,Mashamari,Masu,Miye,Ngalbi_Amari,Nguda_Addamari,Old_Maiduguri,Shehuri_North,Shehuri_South,Tamsu_Ngamdua,Titiwa,Tuba,WardName,Yabal,Yale,Yewija,Zangebe,Other', 'false', 'true', 'true', 'true', 'true', 9, 'false', ''),
(10, 'campo_10', 'campo_10', 'Address (other)', 'texto', '', 'false', 'false', 'true', 'true', 'true', 10, 'true', ''),
(12, 'campo_12', 'campo_12', 'Origin LGA', 'select', 'Abadam,Askira-Uba,Bama,Bayo,Biu,Chibok,Damboa,Dikwa,Gubio,Guzamala,Gwoza,Hawul,Jere,Kaga,Kala-Balge,Konduga,Kukawa,Kwaya,Kusar,Mafa,Magumeri,Maiduguri,Marte,Mobbar,Monguno,Ngala,Nganzai,Shani,Other', 'false', 'false', 'true', 'true', 'true', 12, 'true', ''),
(13, 'campo_13', 'campo_13', 'Status', 'radio', 'Host Population, IDP', 'false', 'true', 'true', 'true', 'true', 13, 'true', ''),
(14, 'campo_14', 'campo_14', 'Phone number', 'texto', '', 'false', 'true', 'true', 'true', 'true', 14, 'true', ''),
(15, 'campo_15', 'campo_15', 'Admission type', 'radio', 'NEW,Internal Movement (ITFC),Readm after default,Readm after transfer,Relapse,Transfer from different MSF ATFC,Transfer from different MSF ITFC', 'false', 'true', 'true', 'true', 'true', 15, 'true', NULL),
(16, 'campo_16', 'campo_16', 'Admission criteria', 'radio', 'Oedema,MUAC,W/HZs,Other', 'false', 'true', 'true', 'true', 'true', 16, 'true', NULL),
(17, 'campo_17', 'campo_17', 'SAM Entry Diagnosis', 'radio', 'None,Marasmus,Kwashiorkor,Marasmic-Kwashiorkor', 'false', 'true', 'true', 'true', 'true', 17, 'true', NULL),
(18, 'campo_18', 'campo_18', 'Admission date', 'fecha', NULL, 'false', 'true', 'true', 'true', 'true', 18, 'true', NULL),
(19, 'campo_19', 'campo_19', 'Old ID number', 'texto', NULL, 'false', 'true', 'true', 'true', 'true', 19, 'true', NULL),
(20, 'campo_20', 'campo_20', 'Referral type', 'radio', 'Outreach,Spontaneous,SFC,HOSP,OPD,OCB Dala,Other', 'false', 'true', 'true', 'true', 'true', 20, 'true', NULL),
(21, 'campo_21', 'campo_21', 'Referral date', 'fecha', NULL, 'false', 'true', 'true', 'true', 'true', 21, 'true', NULL),
(22, 'campo_22', 'campo_22', 'Notes', 'notes', '', 'false', 'true', 'true', 'true', 'true', 22, 'true', '');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_2`
--

CREATE TABLE `tabla_2` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` varchar(128) DEFAULT NULL,
  `campo_5` varchar(128) DEFAULT NULL,
  `campo_6` varchar(128) DEFAULT NULL,
  `campo_7` varchar(128) DEFAULT NULL,
  `campo_8` varchar(128) DEFAULT NULL,
  `campo_9` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_2_des`
--

CREATE TABLE `tabla_2_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_2_des`
--

INSERT INTO `tabla_2_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 1, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 2, 'true', ''),
(3, 'campo_3', 'campo_3', 'Amoxicillin 250mg', 'select', '0,1/2 tab b.d. x5d,3/4 tab b.d. x5d,1 tab b.d. x5d,1 1/4 tab b.d. x5d,1 1/2 tab b.d. x5d,2 tab b.d. x5d,2 1/2 tab b.d. x5d,3 tab b.d. x5d', 'true', 'true', 'true', 'true', 'true', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Abendazole 400mg', 'select', '0,1/2 tab single dose at D7,1 tab single dose at D7', 'true', 'true', 'true', 'true', 'true', 4, 'true', ''),
(5, 'campo_5', 'campo_5', 'Retinol (Vit. A)', 'select', '0,one cap daily D1-D2-D8', 'true', 'true', 'true', 'true', 'true', 5, 'true', NULL),
(6, 'campo_6', 'campo_6', 'Arthem/Lumi', 'select', '0,2 tab b.d. x3d,1 tab b.d. x3d', 'true', 'true', 'true', 'true', 'true', 6, 'true', NULL),
(7, 'campo_7', 'campo_7', 'Tinidazole 500mg', 'select', '0,1 tab once,1/2 tab once', 'true', 'true', 'true', 'true', 'true', 7, 'true', NULL),
(8, 'campo_8', 'campo_8', 'Ferrus', 'select', '0,1 tab daily for 1 month,1/2 tab daily for 1 month', 'true', 'true', 'true', 'true', 'true', 8, 'true', NULL),
(9, 'campo_9', 'campo_9', 'Other', 'notes', NULL, 'true', 'true', 'true', 'true', 'true', 9, 'true', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tabla_3`
--

CREATE TABLE `tabla_3` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` float DEFAULT NULL,
  `campo_4` float DEFAULT NULL,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_3_des`
--

CREATE TABLE `tabla_3_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_3_des`
--

INSERT INTO `tabla_3_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 1, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 2, 'true', ''),
(3, 'campo_3', 'campo_3', 'MUAC (mm)', 'entero', '', 'true', 'true', 'true', 'true', 'true', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Temperature (C)', 'entero', '', 'true', 'true', 'true', 'true', 'true', 4, 'true', '');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_4`
--

CREATE TABLE `tabla_4` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_4_des`
--

CREATE TABLE `tabla_4_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_4_des`
--

INSERT INTO `tabla_4_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 1, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 2, 'true', ''),
(3, 'campo_3', 'campo_3', 'Type', 'radio', 'Cured,Death,Default,Transferred,Non-Respondent,Disqualified', 'true', 'true', 'true', 'true', 'true', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Notes', 'notes', '', 'false', 'true', 'true', 'true', 'true', 4, 'true', '');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_5`
--

CREATE TABLE `tabla_5` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` date DEFAULT NULL,
  `campo_5` date DEFAULT NULL,
  `campo_6` float DEFAULT NULL,
  `campo_7` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_5_des`
--

CREATE TABLE `tabla_5_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_5_des`
--

INSERT INTO `tabla_5_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 1, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 2, 'true', ''),
(3, 'campo_3', 'campo_3', 'Type', 'radio', 'IM-IN,IM-OUT', 'true', 'true', 'true', 'true', 'true', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Admission date in MSF TFC programme', 'fecha', '', 'false', 'true', 'true', 'true', 'true', 4, 'true', ''),
(5, 'campo_5', 'campo_5', 'Date of entry phase II', 'fecha', '', 'false', 'true', 'true', 'true', 'true', 5, 'true', ''),
(6, 'campo_6', 'campo_6', 'Weight at phase II entry (kg)', 'entero', NULL, 'false', 'true', 'true', 'true', 'true', 6, 'true', NULL),
(7, 'campo_7', 'campo_7', 'Notes', 'notes', '', 'false', 'true', 'true', 'true', 'true', 7, 'true', '');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_6`
--

CREATE TABLE `tabla_6` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` date DEFAULT NULL,
  `campo_5` varchar(128) DEFAULT NULL,
  `campo_6` varchar(128) DEFAULT NULL,
  `campo_7` varchar(128) DEFAULT NULL,
  `campo_8` varchar(128) DEFAULT NULL,
  `campo_9` varchar(128) DEFAULT NULL,
  `campo_10` varchar(128) DEFAULT NULL,
  `campo_11` varchar(128) DEFAULT NULL,
  `campo_12` varchar(128) DEFAULT NULL,
  `campo_13` varchar(128) DEFAULT NULL,
  `campo_14` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_6_des`
--

CREATE TABLE `tabla_6_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_6_des`
--

INSERT INTO `tabla_6_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 1, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 2, 'true', ''),
(3, 'campo_3', 'campo_3', 'Measles', 'radio', 'No,Yes', 'true', 'true', 'true', 'true', 'true', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Date of measles immunization', 'fecha', NULL, 'false', 'true', 'true', 'true', 'true', 4, 'true', NULL),
(5, 'campo_5', 'campo_5', 'Measles confirmed', 'radio', 'No,Yes', 'true', 'true', 'true', 'true', 'true', 5, 'true', ''),
(6, 'campo_6', 'campo_6', 'Routine vaccine by MoH OPD', 'radio', 'No,Yes', 'true', 'true', 'true', 'true', 'true', 6, 'true', ''),
(7, 'campo_7', 'campo_7', 'BCG', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 7, 'true', NULL),
(8, 'campo_8', 'campo_8', 'Hep. B monov.', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 8, 'true', NULL),
(9, 'campo_9', 'campo_9', 'Polio', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 9, 'true', NULL),
(10, 'campo_10', 'campo_10', 'DTP - Hep. B - Hib', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 10, 'true', NULL),
(11, 'campo_11', 'campo_11', 'Pneumo', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 11, 'true', NULL),
(12, 'campo_12', 'campo_12', 'Yellow fever', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 12, 'true', NULL),
(13, 'campo_13', 'campo_13', 'H Influenza', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 13, 'true', NULL),
(14, 'campo_14', 'campo_14', 'Notes', 'notes', '', 'false', 'true', 'true', 'true', 'true', 14, 'true', '');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_7`
--

CREATE TABLE `tabla_7` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` float DEFAULT NULL,
  `campo_4` float DEFAULT NULL,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_7_des`
--

CREATE TABLE `tabla_7_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_7_des`
--

INSERT INTO `tabla_7_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 1, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'false', 2, 'true', ''),
(3, 'campo_3', 'campo_3', 'Weight (kg)', 'entero', '', 'true', 'true', 'false', 'true', 'false', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Height (cm)', 'entero', '', 'true', 'true', 'false', 'true', 'false', 4, 'true', '');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_8`
--

CREATE TABLE `tabla_8` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` float DEFAULT NULL,
  `campo_5` varchar(128) DEFAULT NULL,
  `campo_6` float DEFAULT NULL,
  `campo_7` varchar(128) DEFAULT NULL,
  `campo_8` varchar(128) DEFAULT NULL,
  `campo_9` varchar(128) DEFAULT NULL,
  `campo_10` varchar(128) DEFAULT NULL,
  `campo_11` varchar(128) DEFAULT NULL,
  `campo_12` varchar(128) DEFAULT NULL,
  `campo_13` varchar(128) DEFAULT NULL,
  `campo_14` varchar(128) DEFAULT NULL,
  `campo_15` varchar(128) DEFAULT NULL,
  `campo_16` varchar(128) DEFAULT NULL,
  `campo_17` varchar(128) DEFAULT NULL,
  `campo_18` varchar(128) DEFAULT NULL,
  `campo_19` varchar(128) DEFAULT NULL,
  `campo_20` varchar(128) DEFAULT NULL,
  `campo_21` varchar(128) DEFAULT NULL,
  `campo_22` varchar(128) DEFAULT NULL,
  `campo_23` varchar(128) DEFAULT NULL,
  `campo_24` varchar(128) DEFAULT NULL,
  `campo_25` varchar(128) DEFAULT NULL,
  `campo_26` varchar(128) DEFAULT NULL,
  `campo_27` varchar(128) DEFAULT NULL,
  `campo_28` text,
  `campo_29` text,
  `campo_30` date DEFAULT NULL,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_8_des`
--

CREATE TABLE `tabla_8_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_8_des`
--

INSERT INTO `tabla_8_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 1, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'false', 2, 'true', ''),
(3, 'campo_3', 'campo_3', 'Z-Score', 'radio', '<-3,-3,<-2,-2,<-1,-1,>-1', 'true', 'true', 'false', 'true', 'false', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Respiratory rate br/min', 'entero', '', 'false', 'true', 'true', 'true', 'true', 4, 'true', ''),
(5, 'campo_5', 'campo_5', 'Cough', 'radio', 'Yes,No', 'false', 'true', 'true', 'true', 'true', 5, 'true', ''),
(6, 'campo_6', 'campo_6', 'Diarrhea (nb/day)', 'entero', '', 'true', 'true', 'true', 'true', 'true', 6, 'true', ''),
(7, 'campo_7', 'campo_7', 'Vomiting', 'radio', 'No,Yes', 'true', 'true', 'true', 'true', 'true', 7, 'true', ''),
(8, 'campo_8', 'campo_8', 'Dehydration', 'radio', '0,+,++,+++', 'false', 'true', 'true', 'true', 'true', 8, 'true', ''),
(9, 'campo_9', 'campo_9', 'Anaemia', 'radio', '0,+,++,+++', 'false', 'true', 'true', 'true', 'true', 9, 'true', ''),
(10, 'campo_10', 'campo_10', 'Alert', 'radio', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 10, 'true', ''),
(11, 'campo_11', 'campo_11', 'Oedema', 'radio', '0,+,++,+++', 'true', 'true', 'true', 'true', 'true', 11, 'true', ''),
(12, 'campo_12', 'campo_12', 'Malaria', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 12, 'true', ''),
(13, 'campo_13', 'campo_13', 'ARI', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 13, 'true', ''),
(14, 'campo_14', 'campo_14', 'Watery Diarrhoea', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 14, 'true', ''),
(15, 'campo_15', 'campo_15', 'Bloody Diarrhoea', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 15, 'true', ''),
(16, 'campo_16', 'campo_16', 'UOF', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 16, 'true', ''),
(17, 'campo_17', 'campo_17', 'Measles', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 17, 'true', ''),
(18, 'campo_18', 'campo_18', 'Susp. Meningitis', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 18, 'true', ''),
(19, 'campo_19', 'campo_19', 'Anaemia', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 19, 'true', ''),
(20, 'campo_20', 'campo_20', 'Hypothermia', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 20, 'true', ''),
(21, 'campo_21', 'campo_21', 'Hypoglycaemia', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 21, 'true', ''),
(22, 'campo_22', 'campo_22', 'Shock', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 22, 'true', ''),
(23, 'campo_23', 'campo_23', 'Severe dehydration', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 23, 'true', ''),
(24, 'campo_24', 'campo_24', 'TB', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 24, 'true', ''),
(25, 'campo_25', 'campo_25', 'HIV', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 25, 'true', ''),
(26, 'campo_26', 'campo_26', 'Other', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 26, 'true', ''),
(27, 'campo_27', 'campo_27', 'Unknown', 'select', 'No,Yes', 'false', 'true', 'true', 'true', 'true', 27, 'true', ''),
(28, 'campo_28', 'campo_28', 'Medical observations', 'notes', '', 'false', 'true', 'true', 'true', 'true', 28, 'true', ''),
(29, 'campo_29', 'campo_29', 'Diagnosis / Clinical impression', 'notes', NULL, 'true', 'true', 'true', 'true', 'true', 29, 'true', NULL),
(30, 'campo_30', 'campo_30', 'Next visit', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 30, 'true', '');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_9`
--

CREATE TABLE `tabla_9` (
  `_id` int(11) NOT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_1` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_9_des`
--

CREATE TABLE `tabla_9_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_9_des`
--

INSERT INTO `tabla_9_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'History', 'notes', '', 'true', 'true', 'true', 'true', 'true', 2, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 1, 'true', '');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_10`
--

CREATE TABLE `tabla_10` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_10_des`
--

CREATE TABLE `tabla_10_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_10_des`
--

INSERT INTO `tabla_10_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 2, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 1, 'true', ''),
(3, 'campo_3', 'campo_3', 'Result', 'radio', 'Negative,Positive', 'true', 'true', 'false', 'true', 'true', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Notes', 'notes', '', 'false', 'true', 'true', 'true', 'true', 4, 'true', '');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_11`
--

CREATE TABLE `tabla_11` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_11_des`
--

CREATE TABLE `tabla_11_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_11_des`
--

INSERT INTO `tabla_11_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 2, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 1, 'true', ''),
(3, 'campo_3', 'campo_3', 'Result', 'radio', 'Pass,Fail', 'true', 'true', 'false', 'true', 'true', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Notes', 'notes', '', 'false', 'true', 'true', 'true', 'true', 4, 'true', '');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_12`
--

CREATE TABLE `tabla_12` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` varchar(128) DEFAULT NULL,
  `campo_5` varchar(128) DEFAULT NULL,
  `campo_6` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_12_des`
--

CREATE TABLE `tabla_12_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_12_des`
--

INSERT INTO `tabla_12_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 2, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 1, 'true', ''),
(3, 'campo_3', 'campo_3', 'RUTF Distributed', 'radio', '0,14,21,28,42,56,Other\n', 'true', 'true', 'false', 'true', 'true', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'FPR Distributed', 'radio', 'Yes,No', 'true', 'true', 'true', 'true', 'true', 4, 'true', ''),
(5, 'campo_5', 'campo_5', 'Mosquito net distributed', 'radio', 'No,Yes', 'true', 'true', 'true', 'true', 'true', 5, 'true', ''),
(7, 'campo_6', 'campo_6', 'Notes', 'notes', NULL, 'false', 'true', 'true', 'true', 'true', 6, 'true', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tabla_13`
--

CREATE TABLE `tabla_13` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_13_des`
--

CREATE TABLE `tabla_13_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_13_des`
--

INSERT INTO `tabla_13_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 2, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 1, 'true', ''),
(3, 'campo_3', 'campo_3', 'RUTF', 'radio', '0,14,21,28,42,56,Other', 'true', 'true', 'false', 'true', 'true', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Notes', 'notes', '', 'true', 'true', 'true', 'true', 'true', 4, 'true', '');

-- --------------------------------------------------------

--
-- Table structure for table `tabla_14`
--

CREATE TABLE `tabla_14` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` varchar(128) DEFAULT NULL,
  `campo_5` varchar(128) DEFAULT NULL,
  `campo_6` varchar(128) DEFAULT NULL,
  `campo_7` varchar(128) DEFAULT NULL,
  `campo_8` varchar(128) DEFAULT NULL,
  `campo_9` varchar(128) DEFAULT NULL,
  `campo_10` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_14_des`
--

CREATE TABLE `tabla_14_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_14_des`
--

INSERT INTO `tabla_14_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 1, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 2, 'true', ''),
(3, 'campo_3', 'campo_3', 'Amoxicillin 250mg', 'select', '0,5 tabs,7.5 tabs,10 tabs,12.5 tabs,15 tabs,20 tabs,25 tabs,30 tabs', 'true', 'true', 'true', 'true', 'true', 3, 'true', ''),
(4, 'campo_4', 'campo_4', 'Abendazole 400mg', 'select', '0,1/2 tab,1 tab', 'true', 'true', 'true', 'true', 'true', 4, 'true', ''),
(5, 'campo_5', 'campo_5', 'Retinol (Vit. A)', 'select', '0,3 tabs', 'true', 'true', 'true', 'true', 'true', 5, 'true', NULL),
(6, 'campo_6', 'campo_6', 'Arthem/Lumi', 'select', '0,6 tabs,12 tabs', 'true', 'true', 'true', 'true', 'true', 6, 'true', NULL),
(7, 'campo_7', 'campo_7', 'Tinidazole 500mg', 'select', '0,1 tab,1/2 tab', 'true', 'true', 'true', 'true', 'true', 7, 'true', NULL),
(8, 'campo_8', 'campo_8', 'Ferrus', 'select', '0,15 tabs,30 tabs', 'true', 'true', 'true', 'true', 'true', 8, 'true', NULL),
(9, 'campo_9', 'campo_9', 'NAAN', 'select', '0,1,2,3,4', 'false', 'true', 'true', 'true', 'true', 9, 'true', NULL),
(10, 'campo_10', 'campo_10', 'Other', 'notes', NULL, 'true', 'true', 'true', 'true', 'true', 10, 'true', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tabla_15`
--

CREATE TABLE `tabla_15` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_15_des`
--

CREATE TABLE `tabla_15_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_15_des`
--

INSERT INTO `tabla_15_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 2, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 1, 'true', ''),
(3, 'campo_3', 'campo_3', 'FPR', 'radio', '50,33.5,None', 'true', 'true', 'true', 'true', 'true', 3, 'true', NULL),
(4, 'campo_4', 'campo_4', 'Notes', 'notes', '', 'true', 'true', 'true', 'true', 'true', 4, 'true', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tabla_16`
--

CREATE TABLE `tabla_16` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` float DEFAULT NULL,
  `campo_5` float DEFAULT NULL,
  `campo_6` text,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_16_des`
--

CREATE TABLE `tabla_16_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_16_des`
--

INSERT INTO `tabla_16_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 2, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 1, 'true', ''),
(3, 'campo_3', 'campo_3', 'Family size', 'entero', '', 'true', 'true', 'false', 'true', 'true', 3, 'true', ''),
(5, 'campo_5', 'campo_5', 'Number of children under 5', 'entero', '', 'true', 'true', 'true', 'true', 'true', 5, 'true', NULL),
(6, 'campo_6', 'campo_6', 'Notes', 'notes', '', 'true', 'true', 'true', 'true', 'true', 6, 'true', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tabla_17`
--

CREATE TABLE `tabla_17` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_17_des`
--

CREATE TABLE `tabla_17_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_17_des`
--

INSERT INTO `tabla_17_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 2, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 1, 'true', ''),
(3, 'campo_3', 'campo_3', 'Reason for absence', 'texto', '', 'true', 'true', 'true', 'true', 'true', 3, 'true', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tabla_18`
--

CREATE TABLE `tabla_18` (
  `_id` int(11) NOT NULL,
  `campo_1` date DEFAULT NULL,
  `campo_2` varchar(128) DEFAULT NULL,
  `campo_3` varchar(128) DEFAULT NULL,
  `campo_4` varchar(128) DEFAULT NULL,
  `user` varchar(128) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tabla_18_des`
--

CREATE TABLE `tabla_18_des` (
  `_id` int(11) NOT NULL,
  `campo` text NOT NULL,
  `campo_id` text NOT NULL,
  `presentador` text NOT NULL,
  `tipo` text NOT NULL,
  `varios` text,
  `listado` text,
  `detalle` text,
  `buscar` text,
  `nuevaLinea` text,
  `editable` text,
  `pos` int(11) DEFAULT NULL,
  `usar` text,
  `relacionado` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tabla_18_des`
--

INSERT INTO `tabla_18_des` (`_id`, `campo`, `campo_id`, `presentador`, `tipo`, `varios`, `listado`, `detalle`, `buscar`, `nuevaLinea`, `editable`, `pos`, `usar`, `relacionado`) VALUES
(1, 'campo_1', 'campo_1', 'Date', 'fecha', '', 'true', 'true', 'true', 'true', 'true', 2, 'true', ''),
(2, 'campo_2', 'campo_2', 'MSF ID', 'texto', '', 'false', 'true', 'true', 'true', 'true', 1, 'true', ''),
(3, 'campo_3', 'campo_3', 'Patient type', 'radio', 'New,Follow up', 'true', 'true', 'true', 'true', 'true', 3, 'true', NULL),
(4, 'campo_4', 'campo_4', 'Referral type', 'radio', 'From registration,From appetite test,From nurse clinician', 'true', 'true', 'true', 'true', 'true', 4, 'true', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `easy_roles`
--
ALTER TABLE `easy_roles`
  ADD PRIMARY KEY (`_id`);

--
-- Indexes for table `tablas`
--
ALTER TABLE `tablas`
  ADD PRIMARY KEY (`_id`);

--
-- Indexes for table `tablas_relaciones`
--
ALTER TABLE `tablas_relaciones`
  ADD PRIMARY KEY (`_id`);

--
-- Indexes for table `tabla_1`
--
ALTER TABLE `tabla_1`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`),
  ADD UNIQUE KEY `campo_1` (`campo_1`);

--
-- Indexes for table `tabla_1_des`
--
ALTER TABLE `tabla_1_des`
  ADD PRIMARY KEY (`_id`);

--
-- Indexes for table `tabla_2`
--
ALTER TABLE `tabla_2`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_2_des`
--
ALTER TABLE `tabla_2_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_3`
--
ALTER TABLE `tabla_3`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_3_des`
--
ALTER TABLE `tabla_3_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_4`
--
ALTER TABLE `tabla_4`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_4_des`
--
ALTER TABLE `tabla_4_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_5`
--
ALTER TABLE `tabla_5`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_5_des`
--
ALTER TABLE `tabla_5_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_6`
--
ALTER TABLE `tabla_6`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_6_des`
--
ALTER TABLE `tabla_6_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_7`
--
ALTER TABLE `tabla_7`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_7_des`
--
ALTER TABLE `tabla_7_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_8`
--
ALTER TABLE `tabla_8`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_8_des`
--
ALTER TABLE `tabla_8_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_9`
--
ALTER TABLE `tabla_9`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_9_des`
--
ALTER TABLE `tabla_9_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_10`
--
ALTER TABLE `tabla_10`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_10_des`
--
ALTER TABLE `tabla_10_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_11`
--
ALTER TABLE `tabla_11`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_11_des`
--
ALTER TABLE `tabla_11_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_12`
--
ALTER TABLE `tabla_12`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_12_des`
--
ALTER TABLE `tabla_12_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_13`
--
ALTER TABLE `tabla_13`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_13_des`
--
ALTER TABLE `tabla_13_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_14`
--
ALTER TABLE `tabla_14`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_14_des`
--
ALTER TABLE `tabla_14_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_15`
--
ALTER TABLE `tabla_15`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_15_des`
--
ALTER TABLE `tabla_15_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_16`
--
ALTER TABLE `tabla_16`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_16_des`
--
ALTER TABLE `tabla_16_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_17`
--
ALTER TABLE `tabla_17`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_17_des`
--
ALTER TABLE `tabla_17_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_18`
--
ALTER TABLE `tabla_18`
  ADD PRIMARY KEY (`_id`),
  ADD UNIQUE KEY `_id` (`_id`);

--
-- Indexes for table `tabla_18_des`
--
ALTER TABLE `tabla_18_des`
  ADD UNIQUE KEY `_id` (`_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `easy_roles`
--
ALTER TABLE `easy_roles`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;
--
-- AUTO_INCREMENT for table `tablas`
--
ALTER TABLE `tablas`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
--
-- AUTO_INCREMENT for table `tablas_relaciones`
--
ALTER TABLE `tablas_relaciones`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `tabla_1`
--
ALTER TABLE `tabla_1`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_1_des`
--
ALTER TABLE `tabla_1_des`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
--
-- AUTO_INCREMENT for table `tabla_2`
--
ALTER TABLE `tabla_2`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_3`
--
ALTER TABLE `tabla_3`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_4`
--
ALTER TABLE `tabla_4`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_5`
--
ALTER TABLE `tabla_5`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_6`
--
ALTER TABLE `tabla_6`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_7`
--
ALTER TABLE `tabla_7`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_8`
--
ALTER TABLE `tabla_8`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_9`
--
ALTER TABLE `tabla_9`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_10`
--
ALTER TABLE `tabla_10`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_11`
--
ALTER TABLE `tabla_11`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_12`
--
ALTER TABLE `tabla_12`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_13`
--
ALTER TABLE `tabla_13`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_14`
--
ALTER TABLE `tabla_14`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_15`
--
ALTER TABLE `tabla_15`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_16`
--
ALTER TABLE `tabla_16`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_17`
--
ALTER TABLE `tabla_17`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tabla_18`
--
ALTER TABLE `tabla_18`
  MODIFY `_id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

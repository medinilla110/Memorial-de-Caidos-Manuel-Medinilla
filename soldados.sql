-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-05-2025 a las 05:22:40
-- Versión del servidor: 10.4.32-MariaDB-log
-- Versión de PHP: 7.2.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `soldados`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `batallas`
--

CREATE TABLE `batallas` (
  `battle_id` int(11) NOT NULL,
  `name` varchar(120) NOT NULL,
  `operation_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `batallas`
--

INSERT INTO `batallas` (`battle_id`, `name`, `operation_id`, `country_id`, `start_date`, `end_date`) VALUES
(1, 'Caida de Berlin', 1, 1, '1975-05-06', '1975-05-06');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `branch`
--

CREATE TABLE `branch` (
  `branch_id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `branch`
--

INSERT INTO `branch` (`branch_id`, `name`) VALUES
(1, 'Rama Central');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `burial`
--

CREATE TABLE `burial` (
  `soldier_id` int(11) NOT NULL,
  `place_id` int(11) NOT NULL,
  `cemetery` varchar(120) NOT NULL,
  `plot` varchar(50) NOT NULL,
  `is_unknown` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `burial`
--

INSERT INTO `burial` (`soldier_id`, `place_id`, `cemetery`, `plot`, `is_unknown`) VALUES
(1, 1, 'BerlinCentral', '1', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cause_of_death`
--

CREATE TABLE `cause_of_death` (
  `cause_id` int(11) NOT NULL,
  `description` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `cause_of_death`
--

INSERT INTO `cause_of_death` (`cause_id`, `description`) VALUES
(1, 'Bombardeo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `country`
--

CREATE TABLE `country` (
  `country_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `iso_code` char(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `country`
--

INSERT INTO `country` (`country_id`, `name`, `iso_code`) VALUES
(1, 'Alemania', 'ALM');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `medal`
--

CREATE TABLE `medal` (
  `medal_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `country_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `medal`
--

INSERT INTO `medal` (`medal_id`, `name`, `description`, `country_id`) VALUES
(1, 'General', 'Por generar tropas', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `member`
--

CREATE TABLE `member` (
  `email` varchar(120) NOT NULL,
  `full_name` varchar(120) NOT NULL,
  `country_id` int(11) DEFAULT NULL,
  `joined_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `member`
--

INSERT INTO `member` (`email`, `full_name`, `country_id`, `joined_at`) VALUES
('forest@gmial.com', 'Forest Gump', 1, '2025-05-30 05:13:47');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `operaciones`
--

CREATE TABLE `operaciones` (
  `operation_id` int(11) NOT NULL,
  `name` varchar(120) NOT NULL,
  `code_name` varchar(60) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `operaciones`
--

INSERT INTO `operaciones` (`operation_id`, `name`, `code_name`, `start_date`, `end_date`) VALUES
(1, 'Defensa de Berlin', '1', '1975-05-05', '1975-05-06');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `place`
--

CREATE TABLE `place` (
  `place_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `state_province` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `place`
--

INSERT INTO `place` (`place_id`, `country_id`, `state_province`, `city`, `latitude`, `longitude`) VALUES
(1, 1, 'Berlin', 'Capital', 52.524444, 52.524444);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rangos`
--

CREATE TABLE `rangos` (
  `rank_id` int(11) NOT NULL,
  `name` varchar(60) NOT NULL,
  `branch_id` int(11) DEFAULT NULL,
  `seniority` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `rangos`
--

INSERT INTO `rangos` (`rank_id`, `name`, `branch_id`, `seniority`) VALUES
(1, 'General', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `soldier`
--

CREATE TABLE `soldier` (
  `soldier_id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `patronymic` varchar(50) DEFAULT NULL,
  `last_name` varchar(80) DEFAULT NULL,
  `country_id` int(11) DEFAULT NULL,
  `birth_place_id` int(11) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `death_place_id` int(11) DEFAULT NULL,
  `death_date` date DEFAULT NULL,
  `cause_id` int(11) DEFAULT NULL,
  `branch_id` int(11) DEFAULT NULL,
  `death_transport_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `soldier`
--

INSERT INTO `soldier` (`soldier_id`, `first_name`, `patronymic`, `last_name`, `country_id`, `birth_place_id`, `birth_date`, `death_place_id`, `death_date`, `cause_id`, `branch_id`, `death_transport_id`) VALUES
(1, 'Forest', NULL, 'Gump', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `soldier_battle`
--

CREATE TABLE `soldier_battle` (
  `soldier_id` int(11) NOT NULL,
  `battle_id` int(11) NOT NULL,
  `role` varchar(50) DEFAULT NULL,
  `wounded` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `soldier_medal`
--

CREATE TABLE `soldier_medal` (
  `soldier_id` int(11) NOT NULL,
  `medal_id` int(11) NOT NULL,
  `award_date` date DEFAULT NULL,
  `citation` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `soldier_rank`
--

CREATE TABLE `soldier_rank` (
  `soldier_id` int(11) NOT NULL,
  `rank_id` int(11) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `soldier_superior`
--

CREATE TABLE `soldier_superior` (
  `subordinate_id` int(11) NOT NULL,
  `superior_id` int(11) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `soldier_unit`
--

CREATE TABLE `soldier_unit` (
  `soldier_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `transport`
--

CREATE TABLE `transport` (
  `transport_id` int(11) NOT NULL,
  `type` varchar(100) NOT NULL,
  `nature` varchar(100) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `transport`
--

INSERT INTO `transport` (`transport_id`, `type`, `nature`, `location`) VALUES
(1, 'Sin transporte', 'Sin transporte', 'Campo de batalla');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `unit`
--

CREATE TABLE `unit` (
  `unit_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `unit_type` enum('Division','Regiment','Battalion','Company','Platoon') NOT NULL,
  `parent_unit_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `unit`
--

INSERT INTO `unit` (`unit_id`, `name`, `unit_type`, `parent_unit_id`) VALUES
(1, 'Unidad', 'Division', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `batallas`
--
ALTER TABLE `batallas`
  ADD PRIMARY KEY (`battle_id`),
  ADD KEY `operation_id` (`operation_id`),
  ADD KEY `country_id` (`country_id`);

--
-- Indices de la tabla `branch`
--
ALTER TABLE `branch`
  ADD PRIMARY KEY (`branch_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `burial`
--
ALTER TABLE `burial`
  ADD PRIMARY KEY (`soldier_id`),
  ADD KEY `place_id` (`place_id`);

--
-- Indices de la tabla `cause_of_death`
--
ALTER TABLE `cause_of_death`
  ADD PRIMARY KEY (`cause_id`),
  ADD UNIQUE KEY `description` (`description`);

--
-- Indices de la tabla `country`
--
ALTER TABLE `country`
  ADD PRIMARY KEY (`country_id`),
  ADD UNIQUE KEY `iso_code` (`iso_code`);

--
-- Indices de la tabla `medal`
--
ALTER TABLE `medal`
  ADD PRIMARY KEY (`medal_id`),
  ADD KEY `country_id` (`country_id`);

--
-- Indices de la tabla `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`email`),
  ADD KEY `country_id` (`country_id`);

--
-- Indices de la tabla `operaciones`
--
ALTER TABLE `operaciones`
  ADD PRIMARY KEY (`operation_id`);

--
-- Indices de la tabla `place`
--
ALTER TABLE `place`
  ADD PRIMARY KEY (`place_id`),
  ADD KEY `country_id` (`country_id`);

--
-- Indices de la tabla `rangos`
--
ALTER TABLE `rangos`
  ADD PRIMARY KEY (`rank_id`),
  ADD KEY `branch_id` (`branch_id`);

--
-- Indices de la tabla `soldier`
--
ALTER TABLE `soldier`
  ADD PRIMARY KEY (`soldier_id`),
  ADD KEY `country_id` (`country_id`),
  ADD KEY `birth_place_id` (`birth_place_id`),
  ADD KEY `death_place_id` (`death_place_id`),
  ADD KEY `cause_id` (`cause_id`),
  ADD KEY `branch_id` (`branch_id`);

--
-- Indices de la tabla `soldier_battle`
--
ALTER TABLE `soldier_battle`
  ADD PRIMARY KEY (`soldier_id`,`battle_id`),
  ADD KEY `battle_id` (`battle_id`);

--
-- Indices de la tabla `soldier_medal`
--
ALTER TABLE `soldier_medal`
  ADD PRIMARY KEY (`soldier_id`,`medal_id`),
  ADD KEY `medal_id` (`medal_id`);

--
-- Indices de la tabla `soldier_rank`
--
ALTER TABLE `soldier_rank`
  ADD PRIMARY KEY (`soldier_id`,`rank_id`),
  ADD KEY `rank_id` (`rank_id`);

--
-- Indices de la tabla `soldier_superior`
--
ALTER TABLE `soldier_superior`
  ADD PRIMARY KEY (`subordinate_id`,`superior_id`),
  ADD KEY `superior_id` (`superior_id`);

--
-- Indices de la tabla `soldier_unit`
--
ALTER TABLE `soldier_unit`
  ADD PRIMARY KEY (`soldier_id`,`unit_id`),
  ADD KEY `unit_id` (`unit_id`);

--
-- Indices de la tabla `transport`
--
ALTER TABLE `transport`
  ADD PRIMARY KEY (`transport_id`);

--
-- Indices de la tabla `unit`
--
ALTER TABLE `unit`
  ADD PRIMARY KEY (`unit_id`),
  ADD KEY `parent_unit_id` (`parent_unit_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `batallas`
--
ALTER TABLE `batallas`
  MODIFY `battle_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `branch`
--
ALTER TABLE `branch`
  MODIFY `branch_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `cause_of_death`
--
ALTER TABLE `cause_of_death`
  MODIFY `cause_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `country`
--
ALTER TABLE `country`
  MODIFY `country_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `medal`
--
ALTER TABLE `medal`
  MODIFY `medal_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `operaciones`
--
ALTER TABLE `operaciones`
  MODIFY `operation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `place`
--
ALTER TABLE `place`
  MODIFY `place_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `rangos`
--
ALTER TABLE `rangos`
  MODIFY `rank_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `soldier`
--
ALTER TABLE `soldier`
  MODIFY `soldier_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `transport`
--
ALTER TABLE `transport`
  MODIFY `transport_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `unit`
--
ALTER TABLE `unit`
  MODIFY `unit_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `batallas`
--
ALTER TABLE `batallas`
  ADD CONSTRAINT `fk_batallas_operacion` FOREIGN KEY (`operation_id`) REFERENCES `operaciones` (`operation_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_batallas_pais` FOREIGN KEY (`country_id`) REFERENCES `country` (`country_id`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `burial`
--
ALTER TABLE `burial`
  ADD CONSTRAINT `fk_burial_place` FOREIGN KEY (`place_id`) REFERENCES `place` (`place_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_burial_soldier` FOREIGN KEY (`soldier_id`) REFERENCES `soldier` (`soldier_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `medal`
--
ALTER TABLE `medal`
  ADD CONSTRAINT `medal_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `country` (`country_id`);

--
-- Filtros para la tabla `member`
--
ALTER TABLE `member`
  ADD CONSTRAINT `fk_member_country` FOREIGN KEY (`country_id`) REFERENCES `country` (`country_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `place`
--
ALTER TABLE `place`
  ADD CONSTRAINT `place_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `country` (`country_id`);

--
-- Filtros para la tabla `rangos`
--
ALTER TABLE `rangos`
  ADD CONSTRAINT `rangos_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`);

--
-- Filtros para la tabla `soldier`
--
ALTER TABLE `soldier`
  ADD CONSTRAINT `soldier_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `country` (`country_id`),
  ADD CONSTRAINT `soldier_ibfk_2` FOREIGN KEY (`birth_place_id`) REFERENCES `place` (`place_id`),
  ADD CONSTRAINT `soldier_ibfk_3` FOREIGN KEY (`death_place_id`) REFERENCES `place` (`place_id`),
  ADD CONSTRAINT `soldier_ibfk_4` FOREIGN KEY (`cause_id`) REFERENCES `cause_of_death` (`cause_id`),
  ADD CONSTRAINT `soldier_ibfk_5` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`);

--
-- Filtros para la tabla `soldier_battle`
--
ALTER TABLE `soldier_battle`
  ADD CONSTRAINT `fk_sb_battle` FOREIGN KEY (`battle_id`) REFERENCES `batallas` (`battle_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_sb_soldier` FOREIGN KEY (`soldier_id`) REFERENCES `soldier` (`soldier_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `soldier_medal`
--
ALTER TABLE `soldier_medal`
  ADD CONSTRAINT `fk_sm_medal` FOREIGN KEY (`medal_id`) REFERENCES `medal` (`medal_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_sm_soldier` FOREIGN KEY (`soldier_id`) REFERENCES `soldier` (`soldier_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `soldier_rank`
--
ALTER TABLE `soldier_rank`
  ADD CONSTRAINT `fk_sr_rank` FOREIGN KEY (`rank_id`) REFERENCES `rangos` (`rank_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_sr_soldier` FOREIGN KEY (`soldier_id`) REFERENCES `soldier` (`soldier_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `soldier_superior`
--
ALTER TABLE `soldier_superior`
  ADD CONSTRAINT `fk_ss_sub` FOREIGN KEY (`subordinate_id`) REFERENCES `soldier` (`soldier_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_ss_sup` FOREIGN KEY (`superior_id`) REFERENCES `soldier` (`soldier_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `soldier_unit`
--
ALTER TABLE `soldier_unit`
  ADD CONSTRAINT `fk_su_soldier` FOREIGN KEY (`soldier_id`) REFERENCES `soldier` (`soldier_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_su_unit` FOREIGN KEY (`unit_id`) REFERENCES `unit` (`unit_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `unit`
--
ALTER TABLE `unit`
  ADD CONSTRAINT `unit_ibfk_1` FOREIGN KEY (`parent_unit_id`) REFERENCES `unit` (`unit_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 20, 2025 at 12:37 PM
-- Server version: 8.0.42
-- PHP Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `olympiada`
--

-- --------------------------------------------------------

--
-- Table structure for table `app_answer`
--

CREATE TABLE `app_answer` (
  `id` bigint NOT NULL,
  `text` longtext NOT NULL,
  `correctness_weight` decimal(5,3) NOT NULL,
  `partial_score` decimal(10,2) NOT NULL,
  `penalty_weight` decimal(5,3) NOT NULL,
  `explanation` longtext NOT NULL,
  `difficulty_modifier` decimal(3,2) NOT NULL,
  `priority` int UNSIGNED NOT NULL,
  `order` int UNSIGNED NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `metadata` json NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `question_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_answer`
--

INSERT INTO `app_answer` (`id`, `text`, `correctness_weight`, `partial_score`, `penalty_weight`, `explanation`, `difficulty_modifier`, `priority`, `order`, `is_active`, `metadata`, `created_at`, `question_id`) VALUES
(140, 'O(log n)', '1.000', '0.00', '0.000', 'Массив делится пополам', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 52),
(141, 'O(n)', '-1.000', '0.00', '0.500', 'Линейный поиск', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 52),
(142, 'O(n log n)', '-1.000', '0.00', '0.500', 'Сложность сортировок', '1.00', 3, 3, 1, '{}', '2025-12-20 14:25:44.000000', 52),
(143, 'Массив', '0.500', '0.50', '0.000', 'Линейная структура', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 53),
(144, 'Связный список', '0.500', '0.50', '0.000', 'Линейная структура', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 53),
(145, 'Дерево', '-1.000', '0.00', '0.500', 'Иерархическая структура', '1.00', 3, 3, 1, '{}', '2025-12-20 14:25:44.000000', 53),
(146, 'Граф', '-1.000', '0.00', '0.500', 'Нелинейная структура', '1.00', 4, 4, 1, '{}', '2025-12-20 14:25:44.000000', 53),
(147, 'Структура LIFO', '1.000', '0.00', '0.000', 'Последним пришёл — первым вышел', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 54),
(148, 'Структура FIFO', '-1.000', '0.00', '0.500', 'Это очередь', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 54),
(149, 'Структура FIFO', '1.000', '0.00', '0.000', 'Первым пришёл — первым вышел', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 55),
(150, 'Структура LIFO', '-1.000', '0.00', '0.500', 'Это стек', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 55),
(151, 'Использует ключи', '1.000', '0.00', '0.000', 'Ключи для быстрого доступа', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 56),
(152, 'Не использует ключи', '-1.000', '0.00', '0.500', 'Неверно', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 56),
(153, '3x²', '1.000', '0.00', '0.000', 'Верно', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 57),
(154, 'x²', '-1.000', '0.00', '0.500', 'Пропущен коэффициент', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 57),
(155, '2', '0.500', '0.50', '0.000', 'Простое', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 58),
(156, '3', '0.500', '0.50', '0.000', 'Простое', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 58),
(157, '4', '-1.000', '0.00', '0.500', 'Составное', '1.00', 3, 3, 1, '{}', '2025-12-20 14:25:44.000000', 58),
(158, 'πr²', '1.000', '0.00', '0.000', 'Правильная формула', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 59),
(159, '2πr', '-1.000', '0.00', '0.500', 'Это периметр круга', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 59),
(160, 'cos(x)', '1.000', '0.00', '0.000', 'Верно', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 60),
(161, '-sin(x)', '-1.000', '0.00', '0.500', 'Неверно', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 60),
(162, 'e^x', '1.000', '0.00', '0.000', 'Верно', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 61),
(163, 'x*e^x', '-1.000', '0.00', '0.500', 'Неверно', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 61),
(164, 'F = m · a', '1.000', '0.00', '0.000', 'Верная формула', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 62),
(165, 'F = m / a', '-1.000', '0.00', '0.500', 'Неверно', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 62),
(166, 'Изменение скорости тела за единицу времени', '1.000', '0.00', '0.000', 'Правильно', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 63),
(167, 'Скорость тела', '-1.000', '0.00', '0.500', 'Неверно', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 63),
(168, 'Энергия сохраняется и может переходить из одной формы в другую', '1.000', '0.00', '0.000', 'Правильно', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 64),
(169, 'Энергия создаётся при движении тела', '-1.000', '0.00', '0.500', 'Неверно', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 64),
(170, 'Количество вещества в теле', '1.000', '0.00', '0.000', 'Верно', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 65),
(171, 'Вес тела', '-1.000', '0.00', '0.500', 'Неверно', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 65),
(172, 'Изменение положения тела за единицу времени', '1.000', '0.00', '0.000', 'Верно', '1.00', 1, 1, 1, '{}', '2025-12-20 14:25:44.000000', 66),
(173, 'Постоянное расстояние', '-1.000', '0.00', '0.500', 'Неверно', '1.00', 2, 2, 1, '{}', '2025-12-20 14:25:44.000000', 66);

-- --------------------------------------------------------

--
-- Table structure for table `app_answer_conflicts_with_answers`
--

CREATE TABLE `app_answer_conflicts_with_answers` (
  `id` bigint NOT NULL,
  `from_answer_id` bigint NOT NULL,
  `to_answer_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_answer_requires_other_answers`
--

CREATE TABLE `app_answer_requires_other_answers` (
  `id` bigint NOT NULL,
  `from_answer_id` bigint NOT NULL,
  `to_answer_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_contactform`
--

CREATE TABLE `app_contactform` (
  `id` bigint NOT NULL,
  `name` varchar(200) NOT NULL,
  `email` varchar(254) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `app_contactform`
--

INSERT INTO `app_contactform` (`id`, `name`, `email`, `subject`, `message`, `status`, `created_at`, `updated_at`) VALUES
(2, 'test', 'test@gmail.com', 'Тестовая тема', 'Тестовое сообщение желательно немного длиннее', 'reviewed', '2025-12-19 13:28:54.320900', '2025-12-19 13:42:47.899680'),
(3, 'Второй', 'sf@gmail.com', 'Вторая тема', 'флвапфловарп', 'not_processed', '2025-12-19 13:31:56.124896', '2025-12-19 13:31:56.124896');

-- --------------------------------------------------------

--
-- Table structure for table `app_customuser`
--

CREATE TABLE `app_customuser` (
  `id` bigint NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `middle_name` varchar(150) NOT NULL,
  `student_id` varchar(50) DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `app_customuser`
--

INSERT INTO `app_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `middle_name`, `student_id`, `phone`, `date_of_birth`, `created_at`, `updated_at`) VALUES
(1, 'pbkdf2_sha256$1000000$oa8kubKd4tIqOcRvYIsGR8$MtzdDKeK97OdQbar+peuqSgImT6BvNTNHoheWdmllLE=', '2025-12-20 09:46:21.409264', 0, 'user', 'Тестовый', 'Пользователь', 'user@gmail.com', 0, 1, '2025-12-19 12:53:30.521116', '', '123456', '', NULL, '2025-12-19 12:53:31.332979', '2025-12-19 13:52:11.185232'),
(2, 'pbkdf2_sha256$1000000$2oetCPULCYFPysGIEpIiGE$NfFoejSvfNyZzKud0ew/qzy6rkf2edTPd4uFz3Iwj4A=', '2025-12-20 12:34:27.569492', 1, 'admin', 'Администратор', 'Тестовый', 'admin@gmail.com', 1, 1, '2025-12-19 13:15:06.870693', '', NULL, '', NULL, '2025-12-19 13:15:07.722768', '2025-12-19 13:21:33.416763'),
(3, 'pbkdf2_sha256$1000000$YMQlp5dctVGAvKBwnN8m1J$9hWIJa0RXWtyeTb1uYBy/A4xXw9/Ivs/fMyD0yNBP8E=', '2025-12-20 11:38:37.404671', 0, 'kurator', 'Куратор', 'Тестовый', 'kurator@gmail.com', 1, 1, '2025-12-19 14:29:47.855417', '', NULL, '', NULL, '2025-12-19 14:29:48.632915', '2025-12-19 14:30:06.060182');

-- --------------------------------------------------------

--
-- Table structure for table `app_customuser_groups`
--

CREATE TABLE `app_customuser_groups` (
  `id` bigint NOT NULL,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_customuser_user_permissions`
--

CREATE TABLE `app_customuser_user_permissions` (
  `id` bigint NOT NULL,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_examsession`
--

CREATE TABLE `app_examsession` (
  `id` bigint NOT NULL,
  `session_token` char(32) NOT NULL,
  `attempt_number` int UNSIGNED NOT NULL,
  `status` varchar(20) NOT NULL,
  `started_at` datetime(6) DEFAULT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `last_activity_at` datetime(6) NOT NULL,
  `is_paused` tinyint(1) NOT NULL,
  `paused_at` datetime(6) DEFAULT NULL,
  `pause_count` int UNSIGNED NOT NULL,
  `total_pause_duration_seconds` int UNSIGNED NOT NULL,
  `current_question_index` int UNSIGNED NOT NULL,
  `questions_answered_count` int UNSIGNED NOT NULL,
  `question_order` json NOT NULL,
  `is_random_order` tinyint(1) NOT NULL,
  `question_timings` json NOT NULL,
  `time_spent_seconds` int UNSIGNED NOT NULL,
  `checkpoint_data` json NOT NULL,
  `last_checkpoint_at` datetime(6) DEFAULT NULL,
  `score` decimal(10,2) NOT NULL,
  `max_score` decimal(10,2) NOT NULL,
  `penalty_points` decimal(10,2) NOT NULL,
  `bonus_points` decimal(10,2) NOT NULL,
  `final_score` decimal(10,2) NOT NULL,
  `answer_changes_count` int UNSIGNED NOT NULL,
  `questions_skipped_count` int UNSIGNED NOT NULL,
  `questions_reviewed_count` int UNSIGNED NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `user_agent` longtext NOT NULL,
  `browser_fingerprint` varchar(255) NOT NULL,
  `allow_back_navigation` tinyint(1) NOT NULL,
  `show_correct_answers` tinyint(1) NOT NULL,
  `is_proctored` tinyint(1) NOT NULL,
  `suspicious_activities` json NOT NULL,
  `warning_count` int UNSIGNED NOT NULL,
  `metadata` json NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `student_id` bigint NOT NULL,
  `olympiad_subject_id` bigint NOT NULL,
  `registration_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_examsession`
--

INSERT INTO `app_examsession` (`id`, `session_token`, `attempt_number`, `status`, `started_at`, `completed_at`, `last_activity_at`, `is_paused`, `paused_at`, `pause_count`, `total_pause_duration_seconds`, `current_question_index`, `questions_answered_count`, `question_order`, `is_random_order`, `question_timings`, `time_spent_seconds`, `checkpoint_data`, `last_checkpoint_at`, `score`, `max_score`, `penalty_points`, `bonus_points`, `final_score`, `answer_changes_count`, `questions_skipped_count`, `questions_reviewed_count`, `ip_address`, `user_agent`, `browser_fingerprint`, `allow_back_navigation`, `show_correct_answers`, `is_proctored`, `suspicious_activities`, `warning_count`, `metadata`, `created_at`, `updated_at`, `student_id`, `olympiad_subject_id`, `registration_id`) VALUES
(1, '52a7c6e8e8d947549dca221b52859413', 1, 'in_progress', '2025-12-20 09:27:22.105518', NULL, '2025-12-20 09:27:22.110740', 0, NULL, 0, 0, 0, 0, '[]', 0, '{}', 0, '{}', NULL, '0.00', '0.00', '0.00', '0.00', '0.00', 0, 0, 0, NULL, '', '', 1, 0, 0, '[]', 0, '{}', '2025-12-20 09:27:22.110740', '2025-12-20 09:27:22.110740', 1, 35, 2),
(2, '0182755534864296a557df44e6e8549b', 1, 'in_progress', '2025-12-20 09:27:24.433441', NULL, '2025-12-20 09:27:24.435658', 0, NULL, 0, 0, 0, 0, '[]', 0, '{}', 0, '{}', NULL, '0.00', '0.00', '0.00', '0.00', '0.00', 0, 0, 0, NULL, '', '', 1, 0, 0, '[]', 0, '{}', '2025-12-20 09:27:24.435658', '2025-12-20 09:27:24.435658', 1, 36, 2),
(3, 'e09452dc03654c92a273fdf159a8adaf', 1, 'in_progress', '2025-12-20 09:27:25.469632', NULL, '2025-12-20 09:27:25.471644', 0, NULL, 0, 0, 0, 0, '[]', 0, '{}', 0, '{}', NULL, '0.00', '0.00', '0.00', '0.00', '0.00', 0, 0, 0, NULL, '', '', 1, 0, 0, '[]', 0, '{}', '2025-12-20 09:27:25.472695', '2025-12-20 09:27:25.472695', 1, 37, 2),
(4, 'e6f0421d666842c0a6e7b7b26bc6fec9', 2, 'completed', '2025-12-20 09:46:26.612958', '2025-12-20 09:49:16.884255', '2025-12-20 09:49:16.913565', 0, NULL, 0, 0, 1, 2, '[1, 2]', 0, '{}', 0, '{}', NULL, '0.50', '2.00', '0.00', '0.00', '0.50', 0, 0, 0, NULL, '', '', 1, 0, 0, '[]', 0, '{}', '2025-12-20 09:46:26.615953', '2025-12-20 09:49:16.913565', 1, 35, 2),
(5, '2513ebbcbf3949eeb91bea0ef15218f3', 2, 'completed', '2025-12-20 09:49:27.036379', '2025-12-20 09:49:32.989768', '2025-12-20 09:49:33.004911', 0, NULL, 0, 0, 0, 0, '[3]', 0, '{}', 0, '{}', NULL, '1.00', '1.00', '0.00', '0.00', '1.00', 0, 0, 0, NULL, '', '', 1, 0, 0, '[]', 0, '{}', '2025-12-20 09:49:27.038388', '2025-12-20 09:49:33.004911', 1, 36, 2),
(6, '4bfa5919aca645399a617f322d94349a', 2, 'completed', '2025-12-20 09:49:38.177965', '2025-12-20 09:49:45.340164', '2025-12-20 09:49:45.353175', 0, NULL, 0, 0, 0, 0, '[4]', 0, '{}', 0, '{}', NULL, '1.00', '1.00', '0.00', '0.00', '1.00', 0, 0, 0, NULL, '', '', 1, 0, 0, '[]', 0, '{}', '2025-12-20 09:49:38.180059', '2025-12-20 09:49:45.353175', 1, 37, 2),
(7, '4367431b65624137b4199c2a25aef468', 3, 'completed', '2025-12-20 10:20:58.033358', '2025-12-20 10:21:44.615023', '2025-12-20 10:21:44.707167', 0, NULL, 0, 0, 9, 9, '[22, 37, 23, 38, 24, 39, 25, 40, 26, 41]', 0, '{}', 0, '{}', NULL, '2.00', '10.00', '0.00', '0.00', '2.00', 0, 0, 0, NULL, '', '', 1, 0, 0, '[]', 0, '{}', '2025-12-20 10:20:58.035367', '2025-12-20 10:21:44.707167', 1, 35, 2),
(8, '6d42ff8e0bd74e098d29e825686b09cb', 3, 'completed', '2025-12-20 10:22:02.881464', '2025-12-20 10:22:34.791011', '2025-12-20 10:22:34.906448', 0, NULL, 0, 0, 9, 9, '[27, 42, 28, 43, 29, 44, 30, 45, 31, 46]', 0, '{}', 0, '{}', NULL, '6.00', '10.00', '0.00', '0.00', '6.00', 0, 0, 0, NULL, '', '', 1, 0, 0, '[]', 0, '{}', '2025-12-20 10:22:02.883972', '2025-12-20 10:22:34.906448', 1, 36, 2),
(9, '54ec9171637c4b78be3d2b5c70bdd4bd', 3, 'completed', '2025-12-20 10:22:48.419642', '2025-12-20 10:23:26.923863', '2025-12-20 10:23:27.008912', 0, NULL, 0, 0, 9, 9, '[32, 47, 33, 48, 34, 49, 35, 50, 36, 51]', 0, '{}', 0, '{}', NULL, '8.00', '10.00', '0.00', '0.00', '8.00', 0, 0, 0, NULL, '', '', 1, 0, 0, '[]', 0, '{}', '2025-12-20 10:22:48.422851', '2025-12-20 10:23:27.008912', 1, 37, 2),
(10, '5031b1f6ec7c4c5e96716783066b0b22', 4, 'completed', '2025-12-20 10:25:49.391376', '2025-12-20 10:26:13.163483', '2025-12-20 10:26:13.214736', 0, NULL, 0, 0, 4, 4, '[52, 53, 54, 55, 56]', 0, '{}', 0, '{}', NULL, '4.00', '5.00', '0.00', '0.00', '4.00', 0, 0, 0, NULL, '', '', 1, 0, 0, '[]', 0, '{}', '2025-12-20 10:25:49.392598', '2025-12-20 10:26:13.214736', 1, 35, 2),
(11, 'd522b46187d6438dbf62815333978767', 4, 'in_progress', '2025-12-20 10:26:21.956340', NULL, '2025-12-20 10:26:21.964760', 0, NULL, 0, 0, 0, 0, '[57, 58, 59, 60, 61]', 0, '{}', 0, '{}', NULL, '0.00', '5.00', '0.00', '0.00', '0.00', 0, 0, 0, NULL, '', '', 1, 0, 0, '[]', 0, '{}', '2025-12-20 10:26:21.958748', '2025-12-20 10:26:21.964760', 1, 36, 2);

-- --------------------------------------------------------

--
-- Table structure for table `app_olympiad`
--

CREATE TABLE `app_olympiad` (
  `id` bigint NOT NULL,
  `name` varchar(300) NOT NULL,
  `description` longtext NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `registration_start` datetime(6) NOT NULL,
  `registration_end` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `max_subjects_per_student` int UNSIGNED NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ;

--
-- Dumping data for table `app_olympiad`
--

INSERT INTO `app_olympiad` (`id`, `name`, `description`, `start_date`, `end_date`, `registration_start`, `registration_end`, `is_active`, `max_subjects_per_student`, `created_at`, `updated_at`) VALUES
(6, 'Весенняя онлайн олимпиада', 'Многопредметная олимпиада, этап онлайн', '2025-12-19 00:00:00.000000', '2026-03-25 00:00:00.000000', '2025-12-12 00:00:00.000000', '2026-03-05 00:00:00.000000', 1, 3, '2025-12-19 15:11:44.000000', '2025-12-20 09:27:03.691594'),
(7, 'Летняя STEM олимпиада', 'Математика, физика и информатика', '2026-06-15 00:00:00.000000', '2026-06-30 00:00:00.000000', '2026-05-01 00:00:00.000000', '2026-06-10 00:00:00.000000', 1, 2, '2025-12-19 15:11:44.000000', '2025-12-19 15:11:44.000000'),
(8, 'Зимняя интеллектуальная олимпиада', 'Гуманитарные и естественные науки', '2025-12-10 00:00:00.000000', '2025-12-20 00:00:00.000000', '2025-11-01 00:00:00.000000', '2025-12-05 00:00:00.000000', 0, 4, '2025-12-19 15:11:44.000000', '2025-12-19 15:11:44.000000'),
(9, 'Осенняя олимпиада 2024', 'Прошедшая олимпиада для школьников', '2024-10-05 00:00:00.000000', '2024-10-20 00:00:00.000000', '2024-09-01 00:00:00.000000', '2024-09-30 00:00:00.000000', 0, 3, '2025-12-19 15:11:44.000000', '2025-12-19 15:11:44.000000'),
(10, 'Международная олимпиада 2026', 'Крупная международная онлайн олимпиада', '2026-09-01 00:00:00.000000', '2026-09-20 00:00:00.000000', '2026-07-01 00:00:00.000000', '2026-08-25 00:00:00.000000', 1, 5, '2025-12-19 15:11:44.000000', '2025-12-19 15:11:44.000000');

-- --------------------------------------------------------

--
-- Table structure for table `app_olympiadsubject`
--

CREATE TABLE `app_olympiadsubject` (
  `id` bigint NOT NULL,
  `duration_minutes` int UNSIGNED NOT NULL,
  `max_score` int UNSIGNED NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `olympiad_id` bigint NOT NULL,
  `subject_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_olympiadsubject`
--

INSERT INTO `app_olympiadsubject` (`id`, `duration_minutes`, `max_score`, `is_active`, `olympiad_id`, `subject_id`) VALUES
(21, 120, 150, 1, 7, 1),
(22, 120, 150, 1, 7, 2),
(23, 150, 200, 1, 7, 3),
(24, 90, 100, 1, 8, 6),
(25, 90, 100, 1, 8, 7),
(26, 90, 100, 1, 8, 8),
(27, 90, 100, 1, 8, 10),
(28, 90, 100, 0, 9, 1),
(29, 90, 100, 0, 9, 5),
(30, 90, 100, 0, 9, 4),
(31, 120, 200, 1, 10, 1),
(32, 120, 200, 1, 10, 2),
(33, 150, 250, 1, 10, 3),
(34, 90, 100, 1, 10, 10),
(35, 60, 100, 1, 6, 3),
(36, 60, 100, 1, 6, 1),
(37, 60, 100, 1, 6, 2);

-- --------------------------------------------------------

--
-- Table structure for table `app_question`
--

CREATE TABLE `app_question` (
  `id` bigint NOT NULL,
  `text` longtext NOT NULL,
  `description` longtext NOT NULL,
  `scoring_method` varchar(20) NOT NULL,
  `base_points` decimal(10,2) NOT NULL,
  `max_points` decimal(10,2) NOT NULL,
  `min_points` decimal(10,2) NOT NULL,
  `difficulty_level` varchar(20) NOT NULL,
  `estimated_time_seconds` int UNSIGNED NOT NULL,
  `required_answers_count` int UNSIGNED NOT NULL,
  `allow_partial_selection` tinyint(1) NOT NULL,
  `shuffle_answers` tinyint(1) NOT NULL,
  `penalty_for_wrong` decimal(5,2) NOT NULL,
  `hint_available` tinyint(1) NOT NULL,
  `hint_text` longtext NOT NULL,
  `hint_cost_points` decimal(5,2) NOT NULL,
  `answer_combination_rules` json NOT NULL,
  `order` int UNSIGNED NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `olympiad_subject_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_question`
--

INSERT INTO `app_question` (`id`, `text`, `description`, `scoring_method`, `base_points`, `max_points`, `min_points`, `difficulty_level`, `estimated_time_seconds`, `required_answers_count`, `allow_partial_selection`, `shuffle_answers`, `penalty_for_wrong`, `hint_available`, `hint_text`, `hint_cost_points`, `answer_combination_rules`, `order`, `is_active`, `created_at`, `updated_at`, `olympiad_subject_id`) VALUES
(52, 'Какова временная сложность бинарного поиска?', 'Алгоритмы поиска', 'weighted_sum', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.30', 1, 'Массив должен быть отсортирован', '0.20', '{}', 1, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 35),
(53, 'Какие структуры данных являются линейными?', 'Структуры данных', 'proportional', '1.00', '1.00', '0.00', 'intermediate', 90, 2, 1, 1, '0.30', 1, 'Последовательный доступ', '0.30', '{}', 2, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 35),
(54, 'Что такое стек (stack)?', 'Абстрактные структуры данных', 'threshold', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.20', 1, 'LIFO принцип', '0.20', '{}', 3, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 35),
(55, 'Что такое очередь (queue)?', 'Абстрактные структуры данных', 'threshold', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.20', 1, 'FIFO принцип', '0.20', '{}', 4, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 35),
(56, 'Что такое хэш-таблица?', 'Структуры данных', 'weighted_sum', '1.00', '1.00', '0.00', 'intermediate', 90, 1, 0, 1, '0.30', 1, 'Использует ключи для быстрого доступа', '0.30', '{}', 5, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 35),
(57, 'Чему равна производная функции x³?', 'Производные', 'threshold', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.20', 1, 'Правило степеней', '0.20', '{}', 1, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 36),
(58, 'Какие числа являются простыми?', 'Теория чисел', 'proportional', '1.00', '1.00', '0.00', 'basic', 90, 2, 1, 1, '0.30', 1, 'Делятся только на 1 и себя', '0.30', '{}', 2, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 36),
(59, 'Чему равна площадь круга?', 'Геометрия', 'threshold', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.20', 1, 'Используйте формулу πr²', '0.20', '{}', 3, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 36),
(60, 'Чему равна производная sin(x)?', 'Производные', 'threshold', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.20', 1, 'Правило дифференцирования синуса', '0.20', '{}', 4, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 36),
(61, 'Чему равна производная e^x?', 'Производные', 'threshold', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.20', 1, 'Производная экспоненты', '0.20', '{}', 5, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 36),
(62, 'Какова формула силы?', 'Второй закон Ньютона', 'weighted_sum', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.20', 1, 'Масса и ускорение', '0.20', '{}', 1, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 37),
(63, 'Что такое ускорение?', 'Кинематика', 'weighted_sum', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.20', 1, 'Изменение скорости', '0.20', '{}', 2, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 37),
(64, 'Что такое закон сохранения энергии?', 'Механика', 'threshold', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.20', 1, 'Энергия не создаётся и не исчезает', '0.20', '{}', 3, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 37),
(65, 'Что такое масса тела?', 'Механика', 'threshold', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.20', 1, 'Масса не меняется', '0.20', '{}', 4, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 37),
(66, 'Что такое скорость?', 'Кинематика', 'threshold', '1.00', '1.00', '0.00', 'basic', 60, 1, 0, 1, '0.20', 1, 'Расстояние за единицу времени', '0.20', '{}', 5, 1, '2025-12-20 14:25:44.000000', '2025-12-20 14:25:44.000000', 37);

-- --------------------------------------------------------

--
-- Table structure for table `app_question_depends_on_questions`
--

CREATE TABLE `app_question_depends_on_questions` (
  `id` bigint NOT NULL,
  `from_question_id` bigint NOT NULL,
  `to_question_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_result`
--

CREATE TABLE `app_result` (
  `id` bigint NOT NULL,
  `total_score` decimal(10,2) NOT NULL,
  `max_possible_score` decimal(10,2) NOT NULL,
  `percentage` decimal(5,2) NOT NULL,
  `rank` int UNSIGNED DEFAULT NULL,
  `completed_at` datetime(6) NOT NULL,
  `olympiad_id` bigint NOT NULL,
  `student_id` bigint NOT NULL
) ;

--
-- Dumping data for table `app_result`
--

INSERT INTO `app_result` (`id`, `total_score`, `max_possible_score`, `percentage`, `rank`, `completed_at`, `olympiad_id`, `student_id`) VALUES
(1, '22.50', '39.00', '57.69', NULL, '2025-12-20 09:49:16.920930', 6, 1);

-- --------------------------------------------------------

--
-- Table structure for table `app_studentanswer`
--

CREATE TABLE `app_studentanswer` (
  `id` bigint NOT NULL,
  `text_answer` longtext NOT NULL,
  `is_correct` tinyint(1) NOT NULL,
  `points_earned` decimal(10,2) NOT NULL,
  `answered_at` datetime(6) NOT NULL,
  `exam_session_id` bigint NOT NULL,
  `question_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `app_studentanswer`
--

INSERT INTO `app_studentanswer` (`id`, `text_answer`, `is_correct`, `points_earned`, `answered_at`, `exam_session_id`, `question_id`) VALUES
(35, '', 1, '1.00', '2025-12-20 10:25:52.952362', 10, 52),
(36, '', 0, '0.00', '2025-12-20 10:26:03.891004', 10, 53),
(37, '', 1, '1.00', '2025-12-20 10:26:07.443841', 10, 54),
(38, '', 1, '1.00', '2025-12-20 10:26:11.011557', 10, 55),
(39, '', 1, '1.00', '2025-12-20 10:26:13.132965', 10, 56);

-- --------------------------------------------------------

--
-- Table structure for table `app_studentanswer_selected_answers`
--

CREATE TABLE `app_studentanswer_selected_answers` (
  `id` bigint NOT NULL,
  `studentanswer_id` bigint NOT NULL,
  `answer_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `app_studentanswer_selected_answers`
--

INSERT INTO `app_studentanswer_selected_answers` (`id`, `studentanswer_id`, `answer_id`) VALUES
(42, 35, 140),
(43, 36, 143),
(44, 37, 147),
(45, 38, 149),
(46, 39, 151);

-- --------------------------------------------------------

--
-- Table structure for table `app_studentregistration`
--

CREATE TABLE `app_studentregistration` (
  `id` bigint NOT NULL,
  `registered_at` datetime(6) NOT NULL,
  `olympiad_id` bigint NOT NULL,
  `student_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `app_studentregistration`
--

INSERT INTO `app_studentregistration` (`id`, `registered_at`, `olympiad_id`, `student_id`) VALUES
(2, '2025-12-19 13:58:14.304732', 6, 1);

-- --------------------------------------------------------

--
-- Table structure for table `app_studentregistration_subjects`
--

CREATE TABLE `app_studentregistration_subjects` (
  `id` bigint NOT NULL,
  `studentregistration_id` bigint NOT NULL,
  `subject_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `app_studentregistration_subjects`
--

INSERT INTO `app_studentregistration_subjects` (`id`, `studentregistration_id`, `subject_id`) VALUES
(4, 2, 1),
(5, 2, 2),
(6, 2, 3);

-- --------------------------------------------------------

--
-- Table structure for table `app_subject`
--

CREATE TABLE `app_subject` (
  `id` bigint NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `app_subject`
--

INSERT INTO `app_subject` (`id`, `name`, `description`, `is_active`, `created_at`) VALUES
(1, 'Математика', 'Задачи по алгебре, геометрии и логике', 1, '2025-12-19 15:09:04.000000'),
(2, 'Физика', 'Теоретические и практические задачи по физике', 1, '2025-12-19 15:09:04.000000'),
(3, 'Информатика', 'Алгоритмы, программирование и структуры данных', 1, '2025-12-19 15:09:04.000000'),
(4, 'Химия', 'Общая, органическая и неорганическая химия', 1, '2025-12-19 15:09:04.000000'),
(5, 'Биология', 'Зоология, ботаника и генетика', 1, '2025-12-19 15:09:04.000000'),
(6, 'История', 'Всемирная и национальная история', 1, '2025-12-19 15:09:04.000000'),
(7, 'География', 'Физическая и экономическая география', 1, '2025-12-19 15:09:04.000000'),
(8, 'Русский язык', 'Грамматика, орфография и пунктуация', 1, '2025-12-19 15:09:04.000000'),
(9, 'Литература', 'Анализ художественных произведений', 1, '2025-12-19 15:09:04.000000'),
(10, 'Английский язык', 'Грамматика, чтение и аудирование', 1, '2025-12-19 15:09:04.000000'),
(11, 'Немецкий язык', 'Лексика и грамматика немецкого языка', 1, '2025-12-19 15:09:04.000000'),
(12, 'Французский язык', 'Основы французского языка', 1, '2025-12-19 15:09:04.000000'),
(13, 'Экономика', 'Микро- и макроэкономика', 1, '2025-12-19 15:09:04.000000'),
(14, 'Обществознание', 'Социальные и политические процессы', 1, '2025-12-19 15:09:04.000000'),
(15, 'Право', 'Основы гражданского и конституционного права', 1, '2025-12-19 15:09:04.000000'),
(16, 'Астрономия', 'Строение Вселенной и небесные тела', 1, '2025-12-19 15:09:04.000000'),
(17, 'Экология', 'Окружающая среда и устойчивое развитие', 1, '2025-12-19 15:09:04.000000'),
(18, 'Робототехника', 'Основы проектирования и программирования роботов', 1, '2025-12-19 15:09:04.000000'),
(19, 'Логика', 'Логическое мышление и рассуждения', 1, '2025-12-19 15:09:04.000000'),
(20, 'Финансовая грамотность', 'Управление личными финансами', 1, '2025-12-19 15:09:04.000000');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Олимпиада', 6, 'add_olympiad'),
(22, 'Can change Олимпиада', 6, 'change_olympiad'),
(23, 'Can delete Олимпиада', 6, 'delete_olympiad'),
(24, 'Can view Олимпиада', 6, 'view_olympiad'),
(25, 'Can add Предмет', 7, 'add_subject'),
(26, 'Can change Предмет', 7, 'change_subject'),
(27, 'Can delete Предмет', 7, 'delete_subject'),
(28, 'Can view Предмет', 7, 'view_subject'),
(29, 'Can add Пользователь', 8, 'add_customuser'),
(30, 'Can change Пользователь', 8, 'change_customuser'),
(31, 'Can delete Пользователь', 8, 'delete_customuser'),
(32, 'Can view Пользователь', 8, 'view_customuser'),
(33, 'Can add Предмет олимпиады', 9, 'add_olympiadsubject'),
(34, 'Can change Предмет олимпиады', 9, 'change_olympiadsubject'),
(35, 'Can delete Предмет олимпиады', 9, 'delete_olympiadsubject'),
(36, 'Can view Предмет олимпиады', 9, 'view_olympiadsubject'),
(37, 'Can add Сессия экзамена', 10, 'add_examsession'),
(38, 'Can change Сессия экзамена', 10, 'change_examsession'),
(39, 'Can delete Сессия экзамена', 10, 'delete_examsession'),
(40, 'Can view Сессия экзамена', 10, 'view_examsession'),
(41, 'Can add Вопрос', 11, 'add_question'),
(42, 'Can change Вопрос', 11, 'change_question'),
(43, 'Can delete Вопрос', 11, 'delete_question'),
(44, 'Can view Вопрос', 11, 'view_question'),
(45, 'Can add Ответ', 12, 'add_answer'),
(46, 'Can change Ответ', 12, 'change_answer'),
(47, 'Can delete Ответ', 12, 'delete_answer'),
(48, 'Can view Ответ', 12, 'view_answer'),
(49, 'Can add Результат', 13, 'add_result'),
(50, 'Can change Результат', 13, 'change_result'),
(51, 'Can delete Результат', 13, 'delete_result'),
(52, 'Can view Результат', 13, 'view_result'),
(53, 'Can add Ответ студента', 14, 'add_studentanswer'),
(54, 'Can change Ответ студента', 14, 'change_studentanswer'),
(55, 'Can delete Ответ студента', 14, 'delete_studentanswer'),
(56, 'Can view Ответ студента', 14, 'view_studentanswer'),
(57, 'Can add Регистрация студента', 15, 'add_studentregistration'),
(58, 'Can change Регистрация студента', 15, 'change_studentregistration'),
(59, 'Can delete Регистрация студента', 15, 'delete_studentregistration'),
(60, 'Can view Регистрация студента', 15, 'view_studentregistration'),
(61, 'Can add Форма обратной связи', 16, 'add_contactform'),
(62, 'Can change Форма обратной связи', 16, 'change_contactform'),
(63, 'Can delete Форма обратной связи', 16, 'delete_contactform'),
(64, 'Can view Форма обратной связи', 16, 'view_contactform');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL
) ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(12, 'app', 'answer'),
(16, 'app', 'contactform'),
(8, 'app', 'customuser'),
(10, 'app', 'examsession'),
(6, 'app', 'olympiad'),
(9, 'app', 'olympiadsubject'),
(11, 'app', 'question'),
(13, 'app', 'result'),
(14, 'app', 'studentanswer'),
(15, 'app', 'studentregistration'),
(7, 'app', 'subject'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-12-17 12:19:28.966599'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-12-17 12:19:29.129177'),
(3, 'auth', '0001_initial', '2025-12-17 12:19:29.480494'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-12-17 12:19:29.566094'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-12-17 12:19:29.585667'),
(6, 'auth', '0004_alter_user_username_opts', '2025-12-17 12:19:29.594577'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-12-17 12:19:29.603946'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-12-17 12:19:29.606938'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-12-17 12:19:29.614259'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-12-17 12:19:29.621032'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-12-17 12:19:29.626217'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-12-17 12:19:29.706074'),
(13, 'auth', '0011_update_proxy_permissions', '2025-12-17 12:19:29.714210'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-12-17 12:19:29.720427'),
(15, 'app', '0001_initial', '2025-12-17 12:19:33.156116'),
(16, 'admin', '0001_initial', '2025-12-17 12:19:33.371509'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-12-17 12:19:33.386040'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-12-17 12:19:33.400264'),
(19, 'sessions', '0001_initial', '2025-12-17 12:19:33.450140'),
(20, 'app', '0002_contactform', '2025-12-19 10:06:22.480345'),
(21, 'app', '0003_remove_studentregistration_approved_at_and_more', '2025-12-19 14:00:59.025105');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('itubjs4mgv4hunspxigwtteesu29joxj', '.eJxVjEEOwiAQRe_C2pACUhiX7j0DGZhBqgaS0q6MdzckXej2v_f-WwTctxL2zmtYSFyEFqffLWJ6ch2AHljvTaZWt3WJcijyoF3eGvHrerh_BwV7GTVkjSmazEigHFiXpuSNNtYaAvBOIyicLM7ek1NIKp7RziZxBoicxecL72E4SA:1vWwAF:h6QwmlDsIg8aJfwauBe2aABwDEu3LNs3zxQDb27YQ7o', '2026-01-03 12:34:27.572485');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `app_answer`
--
ALTER TABLE `app_answer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_answer_questio_dd6542_idx` (`question_id`,`correctness_weight`);

--
-- Indexes for table `app_answer_conflicts_with_answers`
--
ALTER TABLE `app_answer_conflicts_with_answers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_answer_conflicts_wit_from_answer_id_to_answer_eee11247_uniq` (`from_answer_id`,`to_answer_id`),
  ADD KEY `app_answer_conflicts_to_answer_id_fa80d429_fk_app_answe` (`to_answer_id`);

--
-- Indexes for table `app_answer_requires_other_answers`
--
ALTER TABLE `app_answer_requires_other_answers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_answer_requires_othe_from_answer_id_to_answer_456b0f8e_uniq` (`from_answer_id`,`to_answer_id`),
  ADD KEY `app_answer_requires__to_answer_id_a0a8f37c_fk_app_answe` (`to_answer_id`);

--
-- Indexes for table `app_contactform`
--
ALTER TABLE `app_contactform`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_customuser`
--
ALTER TABLE `app_customuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `student_id` (`student_id`);

--
-- Indexes for table `app_customuser_groups`
--
ALTER TABLE `app_customuser_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_customuser_groups_customuser_id_group_id_a5a0ca22_uniq` (`customuser_id`,`group_id`),
  ADD KEY `app_customuser_groups_group_id_47e49ebd_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `app_customuser_user_permissions`
--
ALTER TABLE `app_customuser_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_customuser_user_perm_customuser_id_permission_22e31019_uniq` (`customuser_id`,`permission_id`),
  ADD KEY `app_customuser_user__permission_id_c5920c75_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `app_examsession`
--
ALTER TABLE `app_examsession`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `session_token` (`session_token`),
  ADD UNIQUE KEY `app_examsession_student_id_olympiad_subj_bf7ccd1a_uniq` (`student_id`,`olympiad_subject_id`,`registration_id`,`attempt_number`),
  ADD KEY `app_examsession_registration_id_3befcaa5_fk_app_stude` (`registration_id`),
  ADD KEY `app_examses_session_304591_idx` (`session_token`),
  ADD KEY `app_examses_student_08be39_idx` (`student_id`,`olympiad_subject_id`),
  ADD KEY `app_examses_status_972842_idx` (`status`,`started_at`),
  ADD KEY `app_examsession_olympiad_subject_id_a3cc4f14_fk_app_olymp` (`olympiad_subject_id`);

--
-- Indexes for table `app_olympiad`
--
ALTER TABLE `app_olympiad`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_olympiadsubject`
--
ALTER TABLE `app_olympiadsubject`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_olympiadsubject_olympiad_id_subject_id_8c15cd94_uniq` (`olympiad_id`,`subject_id`),
  ADD KEY `app_olympiadsubject_subject_id_5ba71ea8_fk_app_subject_id` (`subject_id`);

--
-- Indexes for table `app_question`
--
ALTER TABLE `app_question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_questio_olympia_6ae360_idx` (`olympiad_subject_id`,`difficulty_level`),
  ADD KEY `app_questio_order_e32175_idx` (`order`);

--
-- Indexes for table `app_question_depends_on_questions`
--
ALTER TABLE `app_question_depends_on_questions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_question_depends_on__from_question_id_to_ques_52e2534d_uniq` (`from_question_id`,`to_question_id`),
  ADD KEY `app_question_depends_to_question_id_4a4a43ad_fk_app_quest` (`to_question_id`);

--
-- Indexes for table `app_result`
--
ALTER TABLE `app_result`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_result_student_id_olympiad_id_a2f79894_uniq` (`student_id`,`olympiad_id`),
  ADD KEY `app_result_olympiad_id_93f42abe_fk_app_olympiad_id` (`olympiad_id`);

--
-- Indexes for table `app_studentanswer`
--
ALTER TABLE `app_studentanswer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_studentanswer_exam_session_id_question_id_2d9914c0_uniq` (`exam_session_id`,`question_id`),
  ADD KEY `app_studentanswer_question_id_8a2702fe_fk_app_question_id` (`question_id`);

--
-- Indexes for table `app_studentanswer_selected_answers`
--
ALTER TABLE `app_studentanswer_selected_answers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_studentanswer_select_studentanswer_id_answer__586fb59d_uniq` (`studentanswer_id`,`answer_id`),
  ADD KEY `app_studentanswer_se_answer_id_2fe66321_fk_app_answe` (`answer_id`);

--
-- Indexes for table `app_studentregistration`
--
ALTER TABLE `app_studentregistration`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_studentregistration_student_id_olympiad_id_68258443_uniq` (`student_id`,`olympiad_id`),
  ADD KEY `app_studentregistration_olympiad_id_532b5e53_fk_app_olympiad_id` (`olympiad_id`);

--
-- Indexes for table `app_studentregistration_subjects`
--
ALTER TABLE `app_studentregistration_subjects`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_studentregistration__studentregistration_id_s_82e8288b_uniq` (`studentregistration_id`,`subject_id`),
  ADD KEY `app_studentregistrat_subject_id_ca2c4f9a_fk_app_subje` (`subject_id`);

--
-- Indexes for table `app_subject`
--
ALTER TABLE `app_subject`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_app_customuser_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `app_answer`
--
ALTER TABLE `app_answer`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_answer_conflicts_with_answers`
--
ALTER TABLE `app_answer_conflicts_with_answers`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_answer_requires_other_answers`
--
ALTER TABLE `app_answer_requires_other_answers`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_contactform`
--
ALTER TABLE `app_contactform`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `app_customuser`
--
ALTER TABLE `app_customuser`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `app_customuser_groups`
--
ALTER TABLE `app_customuser_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_customuser_user_permissions`
--
ALTER TABLE `app_customuser_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_examsession`
--
ALTER TABLE `app_examsession`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_olympiad`
--
ALTER TABLE `app_olympiad`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_olympiadsubject`
--
ALTER TABLE `app_olympiadsubject`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_question`
--
ALTER TABLE `app_question`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_question_depends_on_questions`
--
ALTER TABLE `app_question_depends_on_questions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_result`
--
ALTER TABLE `app_result`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_studentanswer`
--
ALTER TABLE `app_studentanswer`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `app_studentanswer_selected_answers`
--
ALTER TABLE `app_studentanswer_selected_answers`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `app_studentregistration`
--
ALTER TABLE `app_studentregistration`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `app_studentregistration_subjects`
--
ALTER TABLE `app_studentregistration_subjects`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `app_subject`
--
ALTER TABLE `app_subject`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `app_answer`
--
ALTER TABLE `app_answer`
  ADD CONSTRAINT `app_answer_question_id_4b805cab_fk_app_question_id` FOREIGN KEY (`question_id`) REFERENCES `app_question` (`id`);

--
-- Constraints for table `app_answer_conflicts_with_answers`
--
ALTER TABLE `app_answer_conflicts_with_answers`
  ADD CONSTRAINT `app_answer_conflicts_from_answer_id_43c646de_fk_app_answe` FOREIGN KEY (`from_answer_id`) REFERENCES `app_answer` (`id`),
  ADD CONSTRAINT `app_answer_conflicts_to_answer_id_fa80d429_fk_app_answe` FOREIGN KEY (`to_answer_id`) REFERENCES `app_answer` (`id`);

--
-- Constraints for table `app_answer_requires_other_answers`
--
ALTER TABLE `app_answer_requires_other_answers`
  ADD CONSTRAINT `app_answer_requires__from_answer_id_5862803e_fk_app_answe` FOREIGN KEY (`from_answer_id`) REFERENCES `app_answer` (`id`),
  ADD CONSTRAINT `app_answer_requires__to_answer_id_a0a8f37c_fk_app_answe` FOREIGN KEY (`to_answer_id`) REFERENCES `app_answer` (`id`);

--
-- Constraints for table `app_customuser_groups`
--
ALTER TABLE `app_customuser_groups`
  ADD CONSTRAINT `app_customuser_group_customuser_id_164d073f_fk_app_custo` FOREIGN KEY (`customuser_id`) REFERENCES `app_customuser` (`id`),
  ADD CONSTRAINT `app_customuser_groups_group_id_47e49ebd_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `app_customuser_user_permissions`
--
ALTER TABLE `app_customuser_user_permissions`
  ADD CONSTRAINT `app_customuser_user__customuser_id_4bcbaafb_fk_app_custo` FOREIGN KEY (`customuser_id`) REFERENCES `app_customuser` (`id`),
  ADD CONSTRAINT `app_customuser_user__permission_id_c5920c75_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `app_examsession`
--
ALTER TABLE `app_examsession`
  ADD CONSTRAINT `app_examsession_olympiad_subject_id_a3cc4f14_fk_app_olymp` FOREIGN KEY (`olympiad_subject_id`) REFERENCES `app_olympiadsubject` (`id`),
  ADD CONSTRAINT `app_examsession_registration_id_3befcaa5_fk_app_stude` FOREIGN KEY (`registration_id`) REFERENCES `app_studentregistration` (`id`),
  ADD CONSTRAINT `app_examsession_student_id_290e21fd_fk_app_customuser_id` FOREIGN KEY (`student_id`) REFERENCES `app_customuser` (`id`);

--
-- Constraints for table `app_olympiadsubject`
--
ALTER TABLE `app_olympiadsubject`
  ADD CONSTRAINT `app_olympiadsubject_olympiad_id_32a4eafb_fk_app_olympiad_id` FOREIGN KEY (`olympiad_id`) REFERENCES `app_olympiad` (`id`),
  ADD CONSTRAINT `app_olympiadsubject_subject_id_5ba71ea8_fk_app_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `app_subject` (`id`);

--
-- Constraints for table `app_question`
--
ALTER TABLE `app_question`
  ADD CONSTRAINT `app_question_olympiad_subject_id_69b707af_fk_app_olymp` FOREIGN KEY (`olympiad_subject_id`) REFERENCES `app_olympiadsubject` (`id`);

--
-- Constraints for table `app_question_depends_on_questions`
--
ALTER TABLE `app_question_depends_on_questions`
  ADD CONSTRAINT `app_question_depends_from_question_id_41654348_fk_app_quest` FOREIGN KEY (`from_question_id`) REFERENCES `app_question` (`id`),
  ADD CONSTRAINT `app_question_depends_to_question_id_4a4a43ad_fk_app_quest` FOREIGN KEY (`to_question_id`) REFERENCES `app_question` (`id`);

--
-- Constraints for table `app_result`
--
ALTER TABLE `app_result`
  ADD CONSTRAINT `app_result_olympiad_id_93f42abe_fk_app_olympiad_id` FOREIGN KEY (`olympiad_id`) REFERENCES `app_olympiad` (`id`),
  ADD CONSTRAINT `app_result_student_id_164a685f_fk_app_customuser_id` FOREIGN KEY (`student_id`) REFERENCES `app_customuser` (`id`);

--
-- Constraints for table `app_studentanswer`
--
ALTER TABLE `app_studentanswer`
  ADD CONSTRAINT `app_studentanswer_exam_session_id_fa5b6a9d_fk_app_examsession_id` FOREIGN KEY (`exam_session_id`) REFERENCES `app_examsession` (`id`),
  ADD CONSTRAINT `app_studentanswer_question_id_8a2702fe_fk_app_question_id` FOREIGN KEY (`question_id`) REFERENCES `app_question` (`id`);

--
-- Constraints for table `app_studentanswer_selected_answers`
--
ALTER TABLE `app_studentanswer_selected_answers`
  ADD CONSTRAINT `app_studentanswer_se_answer_id_2fe66321_fk_app_answe` FOREIGN KEY (`answer_id`) REFERENCES `app_answer` (`id`),
  ADD CONSTRAINT `app_studentanswer_se_studentanswer_id_a7a26fac_fk_app_stude` FOREIGN KEY (`studentanswer_id`) REFERENCES `app_studentanswer` (`id`);

--
-- Constraints for table `app_studentregistration`
--
ALTER TABLE `app_studentregistration`
  ADD CONSTRAINT `app_studentregistration_olympiad_id_532b5e53_fk_app_olympiad_id` FOREIGN KEY (`olympiad_id`) REFERENCES `app_olympiad` (`id`),
  ADD CONSTRAINT `app_studentregistration_student_id_a69b28bf_fk_app_customuser_id` FOREIGN KEY (`student_id`) REFERENCES `app_customuser` (`id`);

--
-- Constraints for table `app_studentregistration_subjects`
--
ALTER TABLE `app_studentregistration_subjects`
  ADD CONSTRAINT `app_studentregistrat_studentregistration__6e75ed54_fk_app_stude` FOREIGN KEY (`studentregistration_id`) REFERENCES `app_studentregistration` (`id`),
  ADD CONSTRAINT `app_studentregistrat_subject_id_ca2c4f9a_fk_app_subje` FOREIGN KEY (`subject_id`) REFERENCES `app_subject` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_app_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `app_customuser` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
